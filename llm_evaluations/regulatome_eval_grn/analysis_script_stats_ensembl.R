#### Here we evaluate GRN RE's with prior filtering of ground truth and LLM outputs
#### for relations consisting of Ensembl entities ("external_gene_name", "external_synonym", 
#### and "wikigene_description" attributes).

library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)

all_annotated_entities <- read.delim(file = "src/all_annotated_entities.txt", header = FALSE)

tf_annotated_relations <- read.delim("src/tf_annotated_relations.txt")

curated_tf <- matrix(data = , nrow = nrow(tf_annotated_relations), ncol = 2)
for(ii in 1:nrow(tf_annotated_relations)){
  curated_tf[ii, ] <- c(tf_annotated_relations$source[ii], tf_annotated_relations$target[ii])
}
colnames(curated_tf) <- c("source", "target")
curated_tf <- as.data.frame(unique(curated_tf))
curated_tf$source <- tolower(curated_tf$source)
curated_tf$target <- tolower(curated_tf$target)
curated_tf <- unique(curated_tf)

llm_files <- c("../../llm_files/regulatome_eval_grn/Llama70b_TrueEntities.json",
               "../../llm_files/regulatome_eval_grn/Llama70b_AllEntities.json",
               "../../llm_files/regulatome_eval_grn/Llama70b_NoEntities.json",
               "../../llm_files/regulatome_eval_grn/Llama405b_TrueEntities.json",
               "../../llm_files/regulatome_eval_grn/Llama405b_AllEntities.json",
               "../../llm_files/regulatome_eval_grn/Llama405b_NoEntities.json")
names(llm_files) <- c("Llama70b_TrueEntities", "Llama70b_AllEntities", "Llama70b_NoEntities", "Llama405b_TrueEntities", "Llama405b_AllEntities", "Llama405b_NoEntities")

ensembl <- useEnsembl(biomart = "genes", host = "nov2020.archive.ensembl.org")

ensembl_human <- useDataset("hsapiens_gene_ensembl", mart = ensembl)
attrListHs <- as.data.frame(listAttributes(ensembl_human))
attributes <- c("ensembl_gene_id", "external_gene_name", "external_synonym", "wikigene_description")
human_genes <- getBM(attributes = attributes, mart = ensembl_human)
human_genes$external_gene_name <- tolower(human_genes$external_gene_name)
human_genes$external_synonym <- tolower(human_genes$external_synonym)
human_genes$wikigene_description <- tolower(human_genes$wikigene_description)

curated_tf_ensembl <- matrix(data = , nrow = 1, ncol = 2)
for(ii in 1:nrow(curated_tf)){
  
  ## Source
  ind <- which(human_genes$external_gene_name == curated_tf$source[ii])
  if(length(ind) > 0){
    
    ss <- curated_tf$source[ii]
    
  } else {
    
    ind <- which(human_genes$external_synonym == curated_tf$source[ii])
    if(length(ind) > 0){
      
      ss <- human_genes$external_gene_name[ind[1]]
      
    } else {
      
      ind <- which(human_genes$wikigene_description == curated_tf$source[ii])
      if(length(ind) > 0){
        
        ss <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        ss <- NULL
        
      }
      
    }
    
  }
  
  
  ## Target
  ind <- which(human_genes$external_gene_name == curated_tf$target[ii])
  if(length(ind) > 0){
    
    tt <- curated_tf$target[ii]
    
  } else {
    
    ind <- which(human_genes$external_synonym == curated_tf$target[ii])
    if(length(ind) > 0){
      
      tt <- human_genes$external_gene_name[ind[1]]
      
    } else {
      
      ind <- which(human_genes$wikigene_description == curated_tf$target[ii])
      if(length(ind) > 0){
        
        tt <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        tt <- NULL
        
      }
      
    }
    
  }
  
  if((length(ss) > 0) && (length(tt) > 0)){
    
    tobind <- matrix(data = , nrow = 1, ncol = 2)
    tobind[1, ] <- c(ss, tt)
    curated_tf_ensembl <- rbind(curated_tf_ensembl, tobind)
    
  }
  
}
curated_tf_ensembl <- unique(curated_tf_ensembl[2:nrow(curated_tf_ensembl), ])
colnames(curated_tf_ensembl) <- c("source", "target")
curated_tf_ensembl <- as.data.frame(curated_tf_ensembl)


#### Step 1
ctrl_ind <- 1
tf_genes_list <- list()
plot_df_list <- list()
nn <- c()
for(ll in 1:length(llm_files)){
  
  data <- fromJSON(llm_files[ll])
  mm <- matrix(data = , nrow = 1, ncol = 2)
  for(jj in 1:length(data)){
    
    curr <- data[[jj]]
    if(class(curr) == "array"){
      
      curr <- as.data.frame(curr)
      ind_all <- 1:ncol(curr)
      ind_int <- which(curr[ctrl_ind, ] %in% c("REGULATES", "REPRESS", "ACTIVATES"))
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
  
  mm <- unique(mm[2:nrow(mm), ])
  
  tf <- mm
  colnames(tf) <- c("source", "target")
  tf <- as.data.frame(tf)
  
  tf$source <- tolower(tf$source)
  tf$target <- tolower(tf$target)
  
  tf <- unique(tf)
  
  ###
  tf_ensembl <- matrix(data = , nrow = 1, ncol = 2)
  
  for(ii in 1:nrow(tf)){
    
    ## Source
    ind <- which(human_genes$external_gene_name == tf$source[ii])
    if(length(ind) > 0){
      
      ss <- tf$source[ii]
      
    } else {
      
      ind <- which(human_genes$external_synonym == tf$source[ii])
      if(length(ind) > 0){
        
        ss <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        ind <- which(human_genes$wikigene_description == tf$source[ii])
        if(length(ind) > 0){
          
          ss <- human_genes$external_gene_name[ind[1]]
          
        } else {
          
          ss <- NULL
          
        }
        
      }
      
    }
    
    
    ## Target
    ind <- which(human_genes$external_gene_name == tf$target[ii])
    if(length(ind) > 0){
      
      tt <- tf$target[ii]
      
    } else {
      
      ind <- which(human_genes$external_synonym == tf$target[ii])
      if(length(ind) > 0){
        
        tt <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        ind <- which(human_genes$wikigene_description == tf$target[ii])
        if(length(ind) > 0){
          
          tt <- human_genes$external_gene_name[ind[1]]
          
        } else {
          
          tt <- NULL
          
        }
        
      }
      
    }
    
    if((length(ss) > 0) && (length(tt) > 0)){
      
      tobind <- matrix(data = , nrow = 1, ncol = 2)
      tobind[1, ] <- c(ss, tt)
      tf_ensembl <- rbind(tf_ensembl, tobind)
      
    }
    
  }
  tf_ensembl <- unique(tf_ensembl[2:nrow(tf_ensembl), ])
  colnames(tf_ensembl) <- c("source", "target")
  tf_ensembl <- as.data.frame(tf_ensembl)
  tf <- tf_ensembl
  
  
  ###
  class_i_halucinations <- NULL
  class_ii_halucinations <- NULL
  
  correct_predictions <- which(tolower(paste0(tf$source, "=", tf$target)) %in%
                                 tolower(paste0(curated_tf_ensembl[, 1], "=", curated_tf_ensembl[, 2])))
  correct_predictions <- paste0(tf$source[correct_predictions], 
                                "=", 
                                tf$target[correct_predictions])
  
  other_predictions <- setdiff(x = paste0(tf$source, "=", tf$target), y = c(class_i_halucinations, 
                                                                              class_ii_halucinations, 
                                                                              correct_predictions))
  
  tf_genes_list[[length(tf_genes_list)+1]] <- paste0(tf[, 1], "=", tf[, 2])
  plot_df_list[[length(plot_df_list)+1]] <- c(length(setdiff(x = class_i_halucinations, y = "=")), 
                                              length(setdiff(x = class_ii_halucinations, y = "=")), 
                                              length(setdiff(x = other_predictions, y = "=")), 
                                              length(setdiff(x = correct_predictions, y = "=")))
  
  nn <- c(nn, paste0(names(llm_files)[ll], "_Step", ctrl_ind))
  
  
}



#### Step 2
ctrl_ind <- 2
for(ll in 1:length(llm_files)){
  
  data <- fromJSON(llm_files[ll])
  mm <- matrix(data = , nrow = 1, ncol = 2)
  for(jj in 1:length(data)){
    
    curr <- data[[jj]]
    if(class(curr) == "array"){
      
      curr <- as.data.frame(curr)
      ind_all <- 1:ncol(curr)
      ind_int <- which(curr[ctrl_ind, ] %in% c("REGULATES", "REPRESS", "ACTIVATES"))
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
  
  mm <- unique(mm[2:nrow(mm), ])
  
  tf <- mm
  colnames(tf) <- c("source", "target")
  tf <- as.data.frame(tf)
  
  tf$source <- tolower(tf$source)
  tf$target <- tolower(tf$target)
  
  tf <- unique(tf)
  
  ###
  tf_ensembl <- matrix(data = , nrow = 1, ncol = 2)
  
  for(ii in 1:nrow(tf)){
    
    ## Source
    ind <- which(human_genes$external_gene_name == tf$source[ii])
    if(length(ind) > 0){
      
      ss <- tf$source[ii]
      
    } else {
      
      ind <- which(human_genes$external_synonym == tf$source[ii])
      if(length(ind) > 0){
        
        ss <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        ind <- which(human_genes$wikigene_description == tf$source[ii])
        if(length(ind) > 0){
          
          ss <- human_genes$external_gene_name[ind[1]]
          
        } else {
          
          ss <- NULL
          
        }
        
      }
      
    }
    
    
    ## Target
    ind <- which(human_genes$external_gene_name == tf$target[ii])
    if(length(ind) > 0){
      
      tt <- tf$target[ii]
      
    } else {
      
      ind <- which(human_genes$external_synonym == tf$target[ii])
      if(length(ind) > 0){
        
        tt <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        ind <- which(human_genes$wikigene_description == tf$target[ii])
        if(length(ind) > 0){
          
          tt <- human_genes$external_gene_name[ind[1]]
          
        } else {
          
          tt <- NULL
          
        }
        
      }
      
    }
    
    if((length(ss) > 0) && (length(tt) > 0)){
      
      tobind <- matrix(data = , nrow = 1, ncol = 2)
      tobind[1, ] <- c(ss, tt)
      tf_ensembl <- rbind(tf_ensembl, tobind)
      
    }
    
  }
  tf_ensembl <- unique(tf_ensembl[2:nrow(tf_ensembl), ])
  colnames(tf_ensembl) <- c("source", "target")
  tf_ensembl <- as.data.frame(tf_ensembl)
  tf <- tf_ensembl
  
  
  ###
  class_i_halucinations <- NULL
  class_ii_halucinations <- NULL
  
  correct_predictions <- which(tolower(paste0(tf$source, "=", tf$target)) %in%
                                 tolower(paste0(curated_tf_ensembl[, 1], "=", curated_tf_ensembl[, 2])))
  correct_predictions <- paste0(tf$source[correct_predictions], 
                                "=", 
                                tf$target[correct_predictions])
  
  other_predictions <- setdiff(x = paste0(tf$source, "=", tf$target), y = c(class_i_halucinations, 
                                                                              class_ii_halucinations, 
                                                                              correct_predictions))
  
  tf_genes_list[[length(tf_genes_list)+1]] <- paste0(tf[, 1], "=", tf[, 2])
  plot_df_list[[length(plot_df_list)+1]] <- c(length(setdiff(x = class_i_halucinations, y = "=")), 
                                              length(setdiff(x = class_ii_halucinations, y = "=")), 
                                              length(setdiff(x = other_predictions, y = "=")), 
                                              length(setdiff(x = correct_predictions, y = "=")))
  
  nn <- c(nn, paste0(names(llm_files)[ll], "_Step", ctrl_ind))
  
  
}



#### Step 3
ctrl_ind <- 3
for(ll in 1:length(llm_files)){
  
  data <- fromJSON(llm_files[ll])
  mm <- matrix(data = , nrow = 1, ncol = 2)
  for(jj in 1:length(data)){
    
    curr <- data[[jj]]
    if(class(curr) == "array"){
      
      curr <- as.data.frame(curr)
      ind_all <- 1:ncol(curr)
      ind_int <- which(curr[ctrl_ind, ] %in% c("REGULATES", "REPRESS", "ACTIVATES"))
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
  
  mm <- unique(mm[2:nrow(mm), ])
  
  tf <- mm
  colnames(tf) <- c("source", "target")
  tf <- as.data.frame(tf)
  
  tf$source <- tolower(tf$source)
  tf$target <- tolower(tf$target)
  
  tf <- unique(tf)
  
  ###
  tf_ensembl <- matrix(data = , nrow = 1, ncol = 2)
  
  for(ii in 1:nrow(tf)){
    
    ## Source
    ind <- which(human_genes$external_gene_name == tf$source[ii])
    if(length(ind) > 0){
      
      ss <- tf$source[ii]
      
    } else {
      
      ind <- which(human_genes$external_synonym == tf$source[ii])
      if(length(ind) > 0){
        
        ss <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        ind <- which(human_genes$wikigene_description == tf$source[ii])
        if(length(ind) > 0){
          
          ss <- human_genes$external_gene_name[ind[1]]
          
        } else {
          
          ss <- NULL
          
        }
        
      }
      
    }
    
    
    ## Target
    ind <- which(human_genes$external_gene_name == tf$target[ii])
    if(length(ind) > 0){
      
      tt <- tf$target[ii]
      
    } else {
      
      ind <- which(human_genes$external_synonym == tf$target[ii])
      if(length(ind) > 0){
        
        tt <- human_genes$external_gene_name[ind[1]]
        
      } else {
        
        ind <- which(human_genes$wikigene_description == tf$target[ii])
        if(length(ind) > 0){
          
          tt <- human_genes$external_gene_name[ind[1]]
          
        } else {
          
          tt <- NULL
          
        }
        
      }
      
    }
    
    if((length(ss) > 0) && (length(tt) > 0)){
      
      tobind <- matrix(data = , nrow = 1, ncol = 2)
      tobind[1, ] <- c(ss, tt)
      tf_ensembl <- rbind(tf_ensembl, tobind)
      
    }
    
  }
  tf_ensembl <- unique(tf_ensembl[2:nrow(tf_ensembl), ])
  colnames(tf_ensembl) <- c("source", "target")
  tf_ensembl <- as.data.frame(tf_ensembl)
  tf <- tf_ensembl
  
  
  ###
  class_i_halucinations <- NULL
  class_ii_halucinations <- NULL
  
  correct_predictions <- which(tolower(paste0(tf$source, "=", tf$target)) %in%
                                 tolower(paste0(curated_tf_ensembl[, 1], "=", curated_tf_ensembl[, 2])))
  correct_predictions <- paste0(tf$source[correct_predictions], 
                                "=", 
                                tf$target[correct_predictions])
  
  other_predictions <- setdiff(x = paste0(tf$source, "=", tf$target), y = c(class_i_halucinations, 
                                                                              class_ii_halucinations, 
                                                                              correct_predictions))
  
  tf_genes_list[[length(tf_genes_list)+1]] <- paste0(tf[, 1], "=", tf[, 2])
  plot_df_list[[length(plot_df_list)+1]] <- c(length(setdiff(x = class_i_halucinations, y = "=")), 
                                              length(setdiff(x = class_ii_halucinations, y = "=")), 
                                              length(setdiff(x = other_predictions, y = "=")), 
                                              length(setdiff(x = correct_predictions, y = "=")))
  
  nn <- c(nn, paste0(names(llm_files)[ll], "_Step", ctrl_ind))
  
  
}



names(plot_df_list) <- nn


df <- matrix(data = , nrow = length(plot_df_list)*2, ncol = 4)
cnt <- 1
colnames(df) <- c("Cnt", "Step", "Model", "Type")
for(ii in 1:length(plot_df_list)){
  
  df[cnt, 1] <- plot_df_list[[ii]][3]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3]
  df[cnt, 3] <- paste0(strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1],
                       "_",
                       strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][2])
  df[cnt, 4] <- "inaccurate_predictions"
  
  cnt <- cnt + 1
  
  df[cnt, 1] <- plot_df_list[[ii]][4]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3]
  df[cnt, 3] <- paste0(strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1],
                       "_",
                       strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][2])
  df[cnt, 4] <- "correct_predictions"
  
  cnt <- cnt + 1
  
}
df <- as.data.frame(df)
df$Cnt <- as.numeric(df$Cnt)


df$Type <- factor(df$Type, 
                  levels = c("correct_predictions", 
                             "inaccurate_predictions"))

df$Model <- factor(df$Model,
                   levels = c("Llama70b_TrueEntities",
                              "Llama70b_AllEntities",
                              "Llama70b_NoEntities",
                              "Llama405b_TrueEntities",
                              "Llama405b_AllEntities",
                              "Llama405b_NoEntities"))

colors <- c("inaccurate_predictions" = "#D3D3D3",
            "correct_predictions" = "#33FF57")

write.table(x = df)


pdf(file = "output/model_predictions_grn_ensembl.pdf", width = 20, height = 10)
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

write.table(x = df, file = "output/model_predictions_grn_ensembl.txt", quote = FALSE, 
            sep = "\t", row.names = FALSE, col.names = TRUE)


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

for(ii in 1:length(tf_genes_list)){
  
  manual_relations <- unique(tolower(paste0(curated_tf_ensembl$source, "=", curated_tf_ensembl$target)))
  model_relations <- unique(tolower(tf_genes_list[[ii]]))
  
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

metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 3)
metrics_long$Model <- paste0(sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 2))

metrics_long$Model <- factor(metrics_long$Model,
                             levels = c("Llama70b_TrueEntities",
                                        "Llama405b_TrueEntities",
                                        "Llama70b_AllEntities",
                                        "Llama405b_AllEntities",
                                        "Llama70b_NoEntities",
                                        "Llama405b_NoEntities"))

pdf(file = "output/precision_recall_grn_ensembl.pdf", width = 20, height = 14)
ggplot(metrics_long, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(aes(label = round(Score, 2)),  # Add text labels with rounded scores
            position = position_dodge(width = 0.8),  # Position labels in the center of each bar
            vjust = -0.3,  # Adjust text position above the bar
            size = 6) +  # Adjust text size as needed
  facet_wrap(~Model, ncol = 2) +  # Arrange panels in a 2x2 grid
  labs(title = "Precision, Recall, and F1-Score by Step and Model",
       y = "Score",
       x = "Step") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.major.x = element_blank()) +
  coord_cartesian(clip = 'off')
dev.off()

write.table(x = metrics_long, file = "output/precision_recall_grn_ensembl.txt", quote = FALSE, 
            sep = "\t", row.names = FALSE, col.names = TRUE)



