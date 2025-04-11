library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)

dir.create("output")

dir.create("output/curated_papers")

## Read the manually curated list of interactions
papers_relations <- read_delim("../src/curated_manuscripts/papers_relations.txt", 
                               delim = "\t", escape_double = FALSE, 
                               trim_ws = TRUE)

## Read table of manually curated entities synonyms and transform to lower case
entities_synonyms <- read_delim("../src/curated_manuscripts/entities_synonyms.txt", 
                                delim = "\t", escape_double = FALSE, 
                                trim_ws = TRUE)
entities_synonyms$Main <- tolower(entities_synonyms$Main)
entities_synonyms$Synonym <- tolower(entities_synonyms$Synonym)

## Process and standardize the names
curated_ppi <- matrix(data = , nrow = nrow(papers_relations), ncol = 2)
for(ii in 1:nrow(papers_relations)){
  curated_ppi[ii, ] <- sort(c(tolower(papers_relations$Protein1[ii]), tolower(papers_relations$Protein2[ii])))
}
colnames(curated_ppi) <- c("source", "target")
curated_ppi <- as.data.frame(curated_ppi)

## Read the LLM files
llm_files <- paste0("../llm_files/manuscript_eval_ppi/", list.files(path = "../llm_files/manuscript_eval_ppi/"))

names(llm_files) <- c("Llama70bV3_Dynamic_FineTuned_NoExamples",
                      "Llama70bV3_Dynamic_Standard_NoExamples",
                      "Llama70bV3_Lookup_FineTuned_NoExamples",
                      "Llama70bV3_Lookup_Standard_NoExamples",
                      "Llama70bV3_Stepwise_FineTuned_AllExamples",
                      "Llama70bV3_Stepwise_FineTuned_FPExamples",
                      "Llama70bV3_Stepwise_FineTuned_NoExamples",
                      "Llama70bV3_Stepwise_FineTuned_TPExamples",
                      "Llama70bV3_Stepwise_Standard_AllExamples",
                      "Llama70bV3_Stepwise_Standard_FPExamples",
                      "Llama70bV3_Stepwise_Standard_NoExamples",
                      "Llama70bV3_Stepwise_Standard_TPExamples",
                      "Llama8bV1_Dynamic_FineTuned_NoExamples",
                      "Llama8bV1_Dynamic_Standard_NoExamples",
                      "Llama8bV1_Lookup_FineTuned_NoExamples",
                      "Llama8bV1_Lookup_Standard_NoExamples",
                      "Llama8bV1_Stepwise_FineTuned_AllExamples",
                      "Llama8bV1_Stepwise_FineTuned_FPExamples",
                      "Llama8bV1_Stepwise_FineTuned_NoExamples",
                      "Llama8bV1_Stepwise_FineTuned_TPExamples",
                      "Llama8bV1_Stepwise_Standard_AllExamples",
                      "Llama8bV1_Stepwise_Standard_FPExamples",
                      "Llama8bV1_Stepwise_Standard_NoExamples",
                      "Llama8bV1_Stepwise_Standard_TPExamples")

eval_steps <- 1:3
ppi_genes_list <- list()
plot_df_list <- list()
nn <- c()
for(ctrl_ind in eval_steps){
  
  for(ll in 1:length(llm_files)){
    
    data <- fromJSON(llm_files[ll])
    data <- data$triples
    mm <- matrix(data = , nrow = 1, ncol = 2)
    if(length(data[[1]]) == 3){
      for(jj in 1:length(data)){
        
        curr <- data[[jj]]
        if(class(curr) == "array"){
          
          curr <- as.data.frame(curr)
          ind_all <- 1:ncol(curr)
          ind_int <- which(curr[ctrl_ind, ] == "INTERACTS_WITH")
          ind_ss <- 1:(ind_int[1]-1)
          ind_tt <- (ind_int[length(ind_int)]+1):ncol(curr)
          
          if((length(ind_ss) > 0) && (length(ind_tt) > 0) && (length(ind_ss)==length(ind_tt))){
            
            tobind <- matrix(data = , nrow = length(ind_ss), ncol = 2)
            tobind[, 1] <- as.vector(unlist(curr[ctrl_ind, ind_ss]))
            tobind[, 2] <- as.vector(unlist(curr[ctrl_ind, ind_tt]))
            mm <- unique(rbind(mm, tobind))
            
          }
          
        } else {
          
          if(length(curr[[ctrl_ind]]) > 0){
            
            if(nrow(curr[[ctrl_ind]]) > 0){
              
              tobind <- matrix(data = , nrow = nrow(curr[[ctrl_ind]]), ncol = 2)
              tobind[, 1] <- curr[[ctrl_ind]][, 1]
              tobind[, 2] <- curr[[ctrl_ind]][, 3]
              mm <- unique(rbind(mm, tobind))
              
            }
            
          }
          
        }
        
      }
    } else {
      for(jj in 1:length(data)){
        
        curr <- data[[jj]]
        if(class(curr) == "array"){
          
          curr <- as.data.frame(curr)
          ind_all <- 1:ncol(curr)
          ind_int <- which(curr[ctrl_ind+1, ] == "INTERACTS_WITH")
          ind_ss <- 1:(ind_int[1]-1)
          ind_tt <- (ind_int[length(ind_int)]+1):ncol(curr)
          
          if((length(ind_ss) > 0) && (length(ind_tt) > 0) && (length(ind_ss)==length(ind_tt))){
            
            tobind <- matrix(data = , nrow = length(ind_ss), ncol = 2)
            tobind[, 1] <- as.vector(unlist(curr[ctrl_ind+1, ind_ss]))
            tobind[, 2] <- as.vector(unlist(curr[ctrl_ind+1, ind_tt]))
            mm <- unique(rbind(mm, tobind))
            
          }
          
        } else {
          
          if(length(curr[[ctrl_ind+1]]) > 0){
            
            if(nrow(curr[[ctrl_ind+1]]) > 0){
              
              tobind <- matrix(data = , nrow = nrow(curr[[ctrl_ind+1]]), ncol = 2)
              tobind[, 1] <- curr[[ctrl_ind+1]][, 1]
              tobind[, 2] <- curr[[ctrl_ind+1]][, 3]
              mm <- unique(rbind(mm, tobind))
              
            }
            
          }
          
        }
        
      }
    }
    
    if(nrow(mm) > 2){
      
      mm <- unique(mm[2:nrow(mm), ])
      
      ind1 <- which(tolower(mm[, 1]) %in% entities_synonyms$Synonym)
      if(length(ind1) > 0){
        for(zz in 1:length(ind1)){
          idx <- which(entities_synonyms$Synonym == tolower(mm[ind1[zz], 1]))
          mm[ind1[zz], 1] <- entities_synonyms$Main[idx]
        }
      }
      ind2 <- which(tolower(mm[, 2]) %in% entities_synonyms$Synonym)
      if(length(ind2) > 0){
        for(zz in 1:length(ind2)){
          idx <- which(entities_synonyms$Synonym == tolower(mm[ind2[zz], 2]))
          mm[ind2[zz], 2] <- entities_synonyms$Main[idx]
        }
      }
      
      ppi <- matrix(data = , nrow = nrow(mm), ncol = 2)
      for(ii in 1:nrow(mm)){
        ppi[ii, ] <- c(sort(tolower(c(mm[ii, 1], mm[ii, 2]))))
      }
      colnames(ppi) <- c("source", "target")
      ppi <- as.data.frame(ppi)
      ppi <- unique(ppi)
      
      class_i_halucinations <- NULL
      class_ii_halucinations <- NULL
      
      correct_predictions <- which(tolower(paste0(ppi$source, "=", ppi$target)) %in%
                                     tolower(paste0(curated_ppi$source, "=", curated_ppi$target)))
      correct_predictions <- paste0(ppi$source[correct_predictions], 
                                    "=", 
                                    ppi$target[correct_predictions])
      
      other_predictions <- setdiff(x = paste0(ppi$source, "=", ppi$target), y = c(class_i_halucinations, 
                                                                                  class_ii_halucinations, 
                                                                                  correct_predictions))
      
      ppi_genes_list[[length(ppi_genes_list)+1]] <- paste0(ppi[, 1], "=", ppi[, 2])
      plot_df_list[[length(plot_df_list)+1]] <- c(length(setdiff(x = class_i_halucinations, y = "=")), 
                                                  length(setdiff(x = class_ii_halucinations, y = "=")), 
                                                  length(setdiff(x = other_predictions, y = "=")), 
                                                  length(setdiff(x = correct_predictions, y = "=")))
      
      nn <- c(nn, paste0(names(llm_files)[ll], "_Step", ctrl_ind))
      
      
    } else {
      
      ppi_genes_list[[length(ppi_genes_list)+1]] <- "NA=NA"
      plot_df_list[[length(plot_df_list)+1]] <- c(0, 0, 0, 0)
      
      nn <- c(nn, paste0(names(llm_files)[ll], "_Step", ctrl_ind))
      
    }
    
  }
  
}
names(plot_df_list) <- nn
names(ppi_genes_list) <- nn




#### Plot predictions
df <- matrix(data = , nrow = length(plot_df_list)*2, ncol = 4)
cnt <- 1
colnames(df) <- c("Cnt", "Step", "Model", "Type")
for(ii in 1:length(plot_df_list)){
  
  df[cnt, 1] <- plot_df_list[[ii]][3]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][5]
  df[cnt, 3] <- paste0(strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1],
                       "_",
                       strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3],
                       "_",
                       strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][4])
  df[cnt, 4] <- "inaccurate_predictions"
  
  cnt <- cnt + 1
  
  df[cnt, 1] <- plot_df_list[[ii]][4]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][5]
  df[cnt, 3] <- paste0(strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1],
                       "_",
                       strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3],
                       "_",
                       strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][4])
  df[cnt, 4] <- "correct_predictions"
  
  cnt <- cnt + 1
  
}
df <- as.data.frame(df)
df$Cnt <- as.numeric(df$Cnt)


df$Type <- factor(df$Type, 
                  levels = c("correct_predictions", 
                             "inaccurate_predictions"))

colors <- c("inaccurate_predictions" = "#D3D3D3",
            "correct_predictions" = "#33FF57")

df$Model <- factor(x = df$Model)


pdf(file = "output/curated_papers/model_predictions_ppi.pdf", width = 20, height = 10)
ggplot(df, aes(x = Model, y = Cnt, fill = Type)) +
  geom_bar(stat = "identity", position = "stack") +
  scale_fill_manual(values = colors) +
  labs(
    title = "Stacked Plot of Prediction Types Grouped by Style",
    x = "Model Type",
    y = "Count",
    fill = "Prediction Type"
  ) +
  theme_minimal(base_size = 15) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", color = "#333333"),
    axis.text.x = element_text(angle = 90, hjust = 1),
    legend.position = "right",
    panel.grid.major = element_line(size = 0.1, color = "gray80"),
    panel.grid.minor = element_blank(),
    axis.title = element_text(face = "bold", color = "#555555"),
    strip.text = element_text(face = "bold", size = 12) # Style facet labels
  ) +
  guides(fill = guide_legend(reverse = TRUE)) +
  facet_wrap(~Step, scales = "free_x", nrow = 1) # Create facets for each style
dev.off()

write.table(x = df, file = "output/curated_papers/model_predictions_ppi.txt", quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)




#### Precision-Recall
library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(reshape2)
library(reshape)

calculate_metrics <- function(manual_list, model_list) {
  TP <- length(intersect(manual_list, model_list))  # True Positives
  FP <- length(setdiff(model_list, manual_list))    # False Positives
  FN <- length(setdiff(manual_list, model_list))    # False Negatives
  precision <- TP / (TP + FP)
  recall <- TP / (TP + FN)
  f1_score <- 2 * (precision * recall) / (precision + recall)
  return(data.frame(TP, FP, FN, precision, recall, f1_score))
}

for(ii in 1:length(ppi_genes_list)){
  
  manual_relations <- unique(tolower(paste0(curated_ppi$source, "=", curated_ppi$target)))
  model_relations <- unique(tolower(ppi_genes_list[[ii]]))
  
  if(ii == 1){
    
    metrics_df <- calculate_metrics(manual_list = manual_relations, model_list = model_relations)
    
  } else {
    
    metrics_df <- rbind(metrics_df, calculate_metrics(manual_list = manual_relations, model_list = model_relations))
    
  }
  
}

metrics_df$Type <- nn

metrics_long <- melt(metrics_df, id.vars = "Type", 
                     measure.vars = c("precision", "recall", "f1_score"), 
                     variable.name = "Metric", value.name = "Score")

colnames(metrics_long)[colnames(metrics_long) == "value"] <- "Score"

metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 5)
metrics_long$Model <- paste0(sapply(strsplit(x = nn, split = "_", fixed = TRUE), "[", 1),
                             "_",
                             sapply(strsplit(x = nn, split = "_", fixed = TRUE), "[", 3),
                             "_",
                             sapply(strsplit(x = nn, split = "_", fixed = TRUE), "[", 4))

metrics_long$Model <- factor(x = metrics_long$Model)
metrics_long$Score[which(is.na(metrics_long$Score))] <- 0
metrics_long$variable <- as.character(metrics_long$variable)


## Llama8b Stepwise Standard
tmp <- metrics_long[which(grepl(pattern = "Llama8bV1_Stepwise_Standard", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_stepwise_llama8b_standard.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()


## Llama8b Stepwise FineTuned
tmp <- metrics_long[which(grepl(pattern = "Llama8bV1_Stepwise_FineTuned", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_stepwise_llama8b_stepwise_finetuned.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()

## Llama70b Stepwise Standard
tmp <- metrics_long[which(grepl(pattern = "Llama70bV3_Stepwise_Standard", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_stepwise_llama70b_standard.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()


## Llama70b Stepwise FineTuned
tmp <- metrics_long[which(grepl(pattern = "Llama70bV3_Stepwise_FineTuned", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_stepwise_llama70b_finetuned.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()




## Llama8b Dynamic Standard
tmp <- metrics_long[which(grepl(pattern = "Llama8bV1_Dynamic_Standard", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_dynamic_llama8b_standard.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()

## Llama70b Dynamic Standard
tmp <- metrics_long[which(grepl(pattern = "Llama70bV3_Dynamic_Standard", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_dynamic_llama70b_standard.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()


## Llama70b Dynamic FineTuned
tmp <- metrics_long[which(grepl(pattern = "Llama70bV3_Dynamic_FineTuned", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_dynamic_llama70b_finetuned.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()



## Llama8b Lookup Standard
tmp <- metrics_long[which(grepl(pattern = "Llama8bV1_Lookup_Standard", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_lookup_llama8b_standard.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()


## Llama8b Lookup FineTuned
tmp <- metrics_long[which(grepl(pattern = "Llama8bV1_Lookup_FineTuned", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_lookup_llama8b_stepwise_finetuned.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()

## Llama70b Lookup Standard
tmp <- metrics_long[which(grepl(pattern = "Llama70bV3_Lookup_Standard", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_lookup_llama70b_standard.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()


## Llama70b Lookup FineTuned
tmp <- metrics_long[which(grepl(pattern = "Llama70bV3_Lookup_FineTuned", x = metrics_long$Type, fixed = TRUE)), ]
tmp$variable <- factor(tmp$variable, levels = c("precision", "recall", "f1_score"))
pdf(file = "output/curated_papers/precision_recall_lookup_llama70b_finetuned.pdf", width = 12, height = 10)
ggplot(tmp, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 3) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 1) +  # Facet by Model to create separate panels for each
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()


write.table(x = metrics_long, file = "output/curated_papers/precision_recall_ppi.txt", quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)
