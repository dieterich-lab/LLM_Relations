library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)
library(parallel)

ppi_annotated_relations <- read.delim("src/ppi_annotated_relations.txt")
tf_annotated_relations <- read.delim("src/tf_annotated_relations.txt")


#### All these numbers are stats reported in the Supplementary Materials of the RegulaTome study: https://academic.oup.com/database/article/doi/10.1093/database/baae095/7756349
stats_vec <- c("Catalysis of deubiquitination   92.3%   12/13   80.0%   12/15   85.7%   79   15",
               "Complex formation   78.6%   965/1227   79.0%   965/1221   78.8%   6463   1221",
               "Catalysis of demethylation   69.6%   16/23   88.9%   16/18   78.0%   110   18",
               "Catalysis of ubiquitination   66.4%   77/116   81.9%   77/94   73.3%   474   94",
               "Catalysis of phosphorylation   76.5%   65/85   66.3%   65/98   71.0%   442   99",
               "Catalysis of dephosphorylation   68.1%   32/47   71.1%   32/45   69.6%   213   45",
               "Catalysis of methylation   70.0%   35/50   68.6%   35/51   69.3%   259   259   51",
               "Catalysis of neddylation   100.0%   1/1   50.0%   1/2   66.7%   20   2",
               "Negative regulation   64.8%   263/406   63.2%   263/416   64.0%   1920   417",
               "Positive regulation   61.7%   276/447   62.6%   276/441   62.2%   2130   443",
               "Regulation of degradation   51.4%   36/70   73.5%   36/49   60.5%   336   49",
               "Regulation of transcription   61.1%   102/167   59.6%   102/171   60.4%   899   172",
               "Catalysis of acetylation   60.7%   17/28   58.6%   17/29   59.6%   129   29",
               "Catalysis of palmitoylation   58.3%   7/12   58.3%   7/12   58.3%   66   12",
               "Regulation of gene expression   59.3%   48/81   49.5%   48/97   53.9%   521   97",
               "Catalysis of SUMOylation   58.3%   7/12   50.0%   7/14   53.8%   86   14",
               "Catalysis of deacetylation   45.5%   5/11   55.6%   5/9   50.0%   53   9",
               "Regulation   53.0%   223/421   46.1%   223/484   49.3%   2294   484",
               "Catalysis of ADP-ribosylation   50.0%   2/4   33.3%   2/6   40.0%   31   6",
               "Other catalysis of small molecule conjugation   50.0%   1/2   25.0%   1/4   33.3%   33   4",
               "Catalysis of small protein conjugation   50.0%   1/2   20.0%   1/5   28.6%   42   5",
               "Catalysis of posttranslational modification   37.5%   6/16   13.6%   6/44   20.0%   169   44",
               "Catalysis of glycosylation   20.0%   1/5   12.5%   1/8   15.4%   43   8",
               "Catalysis of deneddylation   0.0%   0/0   0.0%   0/6   0.0%   19   6",
               "Catalysis of other small molecule conjugation or removal   0.0%   0/0   0.0%   0/6   0.0%   9   6",
               "Catalysis of phosphoryl group conjugation or removal   0.0%   0/0   0.0%   0/1   0.0%   7   1",
               "Catalysis of small protein conjugation or removal   0.0%   0/0   0.0%   0/2   0.0%   5   2",
               "Other catalysis of small protein conjugation   0.0%   0/0   0.0%   0/1   0.0%   4   1",
               "Other catalysis of small protein removal   0.0%   0/0   0.0%   0/1   0.0%   3   1",
               "Regulation of translation   0.0%   0/0   0.0%   0/7   0.0%   22   7")


stats_vec_df <- matrix(data = , nrow = length(stats_vec), ncol = 8)
stats_vec_df[, 1] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 1)
stats_vec_df[, 2] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 2)
stats_vec_df[, 3] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 3)
stats_vec_df[, 4] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 4)
stats_vec_df[, 5] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 5)
stats_vec_df[, 6] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 6)
stats_vec_df[, 7] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 7)
stats_vec_df[, 8] <- sapply(strsplit(x = stats_vec, split = "   ", fixed = TRUE), "[", 8)
colnames(stats_vec_df) <- c("Relationship", "Precision", "TP/TP+FP", "Recall", "TP/TP+FN", "F-score", "Count", "Test")
stats_vec_df <- as.data.frame(stats_vec_df)
stats_vec_df$Precision <- gsub(pattern = "%", replacement = "", x = stats_vec_df$Precision, fixed = TRUE)
stats_vec_df$Recall <- gsub(pattern = "%", replacement = "", x = stats_vec_df$Recall, fixed = TRUE)
stats_vec_df$`F-score` <- gsub(pattern = "%", replacement = "", x = stats_vec_df$`F-score`, fixed = TRUE)
stats_vec_df$Precision <- as.numeric(stats_vec_df$Precision)/100
stats_vec_df$Recall <- as.numeric(stats_vec_df$Recall)/100
stats_vec_df$`F-score` <- as.numeric(stats_vec_df$`F-score`)/100
stats_vec_df$Count <- as.numeric(stats_vec_df$Count)
stats_vec_df$Test <- as.numeric(stats_vec_df$Test)
stats_vec_df$Relationship <- tolower(stats_vec_df$Relationship)

ppi_relations <- unique(ppi_annotated_relations$type)
ppi_relations <- tolower(gsub(pattern = "_", replacement = " ", x = ppi_relations, fixed = TRUE))

tf_relations <- unique(tf_annotated_relations$type)
tf_relations <- tolower(gsub(pattern = "_", replacement = " ", x = tf_relations, fixed = TRUE))

ppi <- stats_vec_df[which(stats_vec_df$Relationship %in% ppi_relations), ]
tf <- stats_vec_df[which(stats_vec_df$Relationship %in% tf_relations), ]


##
df <- matrix(data = , nrow = 2, ncol = 4)

# PPI
prec_eval <- 0
rec_eval <- 0
f1_eval <- 0
for(ii in 1:nrow(ppi)){
  
  prec_eval <- prec_eval + (ppi$Precision[ii]*ppi$Test[ii])/(sum(ppi$Test))
  rec_eval <- rec_eval + (ppi$Recall[ii]*ppi$Test[ii])/(sum(ppi$Test))
  f1_eval <- f1_eval + (ppi$`F-score`[ii]*ppi$Test[ii])/(sum(ppi$Test))
  
}
df[1, ] <- c("PPI", as.character(round(x = c(prec_eval, rec_eval, f1_eval), digits = 3)))


# TF-Genes
prec_eval <- 0
rec_eval <- 0
f1_eval <- 0
for(ii in 1:nrow(tf)){
  
  prec_eval <- prec_eval + (tf$Precision[ii]*tf$Test[ii])/(sum(tf$Test))
  rec_eval <- rec_eval + (tf$Recall[ii]*tf$Test[ii])/(sum(tf$Test))
  f1_eval <- f1_eval + (tf$`F-score`[ii]*tf$Test[ii])/(sum(tf$Test))
  
}
df[2, ] <- c("TF-Genes", as.character(round(x = c(prec_eval, rec_eval, f1_eval), digits = 3)))

colnames(df) <- c("Type", "Precision", "Recall", "F1_Score")
df <- as.data.frame(df)
df$Precision <- as.numeric(df$Precision)
df$Recall <- as.numeric(df$Recall)
df$F1_Score <- as.numeric(df$F1_Score)

library(ggplot2)
library(tidyr)

df_long <- df %>%
  pivot_longer(
    cols = c(Precision, Recall, F1_Score),
    names_to = "Metric",
    values_to = "Score"
  )

df_long$Metric <- factor(df_long$Metric, 
                         levels = c("Precision",
                                    "Recall",
                                    "F1_Score"))

pdf(file = "output/precision_recall_regulatome_stats.pdf", width = 14, height = 8)
ggplot(df_long, aes(x = Type, y = Score, fill = Metric, group = Metric)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)), 
            position = position_dodge(width = 0.8), 
            vjust = -0.3, 
            size = 6) +
  labs(title = "Precision, Recall, and F1-Score by Type",
       y = "Score",
       x = "Type") +
  theme_minimal() +
  scale_fill_manual(values = c("Precision" = "#1E90FF", "Recall" = "#FFA500", "F1_Score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()

write.table(x = df_long, file = "output/precision_recall_regulatome_stats.txt", quote = FALSE, 
            sep = "\t", row.names = FALSE, col.names = TRUE)




