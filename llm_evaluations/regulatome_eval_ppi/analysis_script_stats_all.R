#### Here we evaluate PPI RE's without prior filtering of ground truth and LLM outputs
#### for relations consisting of Ensembl entities ("external_gene_name", "external_synonym", 
#### and "wikigene_description" attributes).

library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)
library(parallel)

remove_special_characters <- function(input_string) {
  cleaned_string <- gsub("[[:punct:]]", "", input_string)
  return(cleaned_string)
}

find_match_indices <- function(string, char_vector) {
  indices <- which(sapply(char_vector, function(x) grepl(x, string, fixed = TRUE) || grepl(string, x, fixed = TRUE)))
  return(indices)
}

num_cores <- 10

parallel_process <- function(chunk_indices) {
  ppi_fixed_chunk <- matrix(data = NA, nrow = length(chunk_indices), ncol = 2)
  
  for (ii in seq_along(chunk_indices)) {
    idx <- chunk_indices[ii]
    
    ind <- intersect(x = which(curated_ppi$cleaned_source == ppi$source[idx]), 
                     y = which(curated_ppi$cleaned_target == ppi$target[idx]))
    
    if (length(ind) > 0) {
      ppi_fixed_chunk[ii, ] <- as.character(ppi[idx, ])
    } else {
      ind1 <- as.numeric(find_match_indices(string = ppi$source[idx], char_vector = curated_ppi$cleaned_source))
      ind2 <- as.numeric(find_match_indices(string = ppi$target[idx], char_vector = curated_ppi$cleaned_target))
      
      ind <- intersect(x = ind1, y = ind2)
      
      if (length(ind) > 0) {
        ppi_fixed_chunk[ii, ] <- as.character(curated_ppi[ind[1], 3:4])
      } else {
        ppi_fixed_chunk[ii, ] <- as.character(ppi[idx, ])
      }
    }
  }
  
  return(ppi_fixed_chunk)
}

all_annotated_entities <- read.delim(file = "src/all_annotated_entities.txt", header = FALSE)
true_annotated_entities <- read.delim(file = "src/ppi_annotated_entities.txt", header = FALSE)

ppi_annotated_relations <- read.delim("src/ppi_annotated_relations.txt")

curated_ppi <- matrix(data = , nrow = nrow(ppi_annotated_relations), ncol = 2)
for(ii in 1:nrow(ppi_annotated_relations)){
  curated_ppi[ii, ] <- sort(c(ppi_annotated_relations$source[ii], ppi_annotated_relations$target[ii]))
}
colnames(curated_ppi) <- c("source", "target")
curated_ppi <- as.data.frame(unique(curated_ppi))
curated_ppi$source <- tolower(curated_ppi$source)
curated_ppi$target <- tolower(curated_ppi$target)
curated_ppi <- unique(curated_ppi)
curated_ppi$cleaned_source <- sapply(curated_ppi$source, remove_special_characters)
curated_ppi$cleaned_target <- sapply(curated_ppi$target, remove_special_characters)
curated_ppi$cleaned_source <- gsub(pattern = " ", replacement = "", x = curated_ppi$cleaned_source)
curated_ppi$cleaned_target <- gsub(pattern = " ", replacement = "", x = curated_ppi$cleaned_target)
ind2rem <- c()
for(ii in 1:nrow(curated_ppi)){
  
  nn1 <- nchar(curated_ppi$cleaned_source[ii])
  nn2 <- nchar(curated_ppi$cleaned_target[ii])
  
  if((nn1 <= 1) || (nn2 <= 1)){
    
    ind2rem <- c(ind2rem, ii)
    
  }
  
}
curated_ppi <- curated_ppi[-ind2rem, ]

llm_files <- c("../../llm_files/regulatome_eval_ppi/Llama70b_TrueEntities.json",
               "../../llm_files/regulatome_eval_ppi/Llama70b_AllEntities.json",
               "../../llm_files/regulatome_eval_ppi/Llama70b_NoEntities.json",
               "../../llm_files/regulatome_eval_ppi/Llama405b_TrueEntities.json",
               "../../llm_files/regulatome_eval_ppi/Llama405b_AllEntities.json",
               "../../llm_files/regulatome_eval_ppi/Llama405b_NoEntities.json")
names(llm_files) <- c("Llama70b_TrueEntities", "Llama70b_AllEntities", "Llama70b_NoEntities", "Llama405b_TrueEntities", "Llama405b_AllEntities", "Llama405b_NoEntities")

ensembl <- useEnsembl(biomart = "genes", host = "nov2020.archive.ensembl.org")

ensembl_human <- useDataset("hsapiens_gene_ensembl", mart = ensembl)
attrListHs <- as.data.frame(listAttributes(ensembl_human))
attributes <- c("ensembl_gene_id", "external_gene_name", "external_synonym", "wikigene_description")
human_genes <- getBM(attributes = attributes, mart = ensembl_human)
human_genes$external_gene_name <- tolower(human_genes$external_gene_name)
human_genes$external_synonym <- tolower(human_genes$external_synonym)
human_genes$wikigene_description <- tolower(human_genes$wikigene_description)

all_annotated_entities$cleaned <- sapply(all_annotated_entities$V1, remove_special_characters)
all_annotated_entities$cleaned <- gsub(pattern = " ", replacement = "", x = all_annotated_entities$cleaned)

true_annotated_entities$cleaned <- sapply(true_annotated_entities$V1, remove_special_characters)
true_annotated_entities$cleaned <- gsub(pattern = " ", replacement = "", x = true_annotated_entities$cleaned)

#### Step 1
ctrl_ind <- 1
ppi_genes_list <- list()
ppi_genes_list_original <- list()
entities_check <- list()
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
  
  mm <- unique(mm[2:nrow(mm), ])
  
  ppi <- mm
  colnames(ppi) <- c("source", "target")
  ppi <- as.data.frame(ppi)
  
  mm <- matrix(data = , nrow = nrow(ppi), ncol = 2)
  for(zz in 1:nrow(ppi)){
    mm[zz, ] <- sort(c(ppi$source[zz], ppi$target[zz]))
  }
  ppi <- as.data.frame(unique(mm))
  colnames(ppi) <- c("source", "target")
  ppi$source <- tolower(ppi$source)
  ppi$target <- tolower(ppi$target)
  
  ppi <- unique(ppi)
  
  ppi_genes_list_original[[length(ppi_genes_list_original)+1]] <- ppi
  
  ppi$source <- sapply(ppi$source, remove_special_characters)
  ppi$target <- sapply(ppi$target, remove_special_characters)
  ppi$source <- gsub(pattern = " ", replacement = "", x = ppi$source, fixed = TRUE)
  ppi$target <- gsub(pattern = " ", replacement = "", x = ppi$target, fixed = TRUE)
  
  ind2rem <- c()
  for(ii in 1:nrow(ppi)){
    
    nn1 <- nchar(ppi$source[ii])
    nn2 <- nchar(ppi$target[ii])
    
    if((nn1 <= 1) || (nn2 <= 1)){
      
      ind2rem <- c(ind2rem, ii)
      
    }
    
  }
  if(length(ind2rem) > 0){ppi <- ppi[-ind2rem, ]}
  
  indices <- seq_len(nrow(ppi))
  chunks <- split(indices, cut(indices, num_cores, labels = FALSE))
  
  cl <- makeCluster(num_cores)
  clusterExport(cl, varlist = c("ppi", "curated_ppi", "find_match_indices"))
  results <- parLapply(cl, chunks, parallel_process)
  stopCluster(cl)
  
  ppi_fixed <- do.call(rbind, results)
  colnames(ppi_fixed) <- c("source", "target")
  ppi_fixed <- as.data.frame(unique(ppi_fixed))
  ppi <- ppi_fixed
  
  class_i_halucinations <- NULL
  class_ii_halucinations <- NULL
  
  correct_predictions <- which(tolower(paste0(ppi$source, "=", ppi$target)) %in%
                                 tolower(paste0(curated_ppi[, 3], "=", curated_ppi[, 4])))
  correct_predictions <- paste0(ppi$source[correct_predictions], 
                                "=", 
                                ppi$target[correct_predictions])
  
  other_predictions <- setdiff(x = paste0(ppi$source, "=", ppi$target), y = c(class_i_halucinations, 
                                                                              class_ii_halucinations, 
                                                                              correct_predictions))
  
  ###
  
  ppi_genes_list[[length(ppi_genes_list)+1]] <- paste0(ppi[, 1], "=", ppi[, 2])
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
  
  mm <- unique(mm[2:nrow(mm), ])
  
  ppi <- mm
  colnames(ppi) <- c("source", "target")
  ppi <- as.data.frame(ppi)
  
  mm <- matrix(data = , nrow = nrow(ppi), ncol = 2)
  for(zz in 1:nrow(ppi)){
    mm[zz, ] <- sort(c(ppi$source[zz], ppi$target[zz]))
  }
  ppi <- as.data.frame(unique(mm))
  colnames(ppi) <- c("source", "target")
  ppi$source <- tolower(ppi$source)
  ppi$target <- tolower(ppi$target)
  
  ppi <- unique(ppi)
  
  ppi_genes_list_original[[length(ppi_genes_list_original)+1]] <- ppi
  
  ppi$source <- sapply(ppi$source, remove_special_characters)
  ppi$target <- sapply(ppi$target, remove_special_characters)
  ppi$source <- gsub(pattern = " ", replacement = "", x = ppi$source, fixed = TRUE)
  ppi$target <- gsub(pattern = " ", replacement = "", x = ppi$target, fixed = TRUE)
  
  ind2rem <- c()
  for(ii in 1:nrow(ppi)){
    
    nn1 <- nchar(ppi$source[ii])
    nn2 <- nchar(ppi$target[ii])
    
    if((nn1 <= 1) || (nn2 <= 1)){
      
      ind2rem <- c(ind2rem, ii)
      
    }
    
  }
  if(length(ind2rem) > 0){ppi <- ppi[-ind2rem, ]}
  
  indices <- seq_len(nrow(ppi))
  chunks <- split(indices, cut(indices, num_cores, labels = FALSE))
  
  cl <- makeCluster(num_cores)
  clusterExport(cl, varlist = c("ppi", "curated_ppi", "find_match_indices"))
  results <- parLapply(cl, chunks, parallel_process)
  stopCluster(cl)
  
  ppi_fixed <- do.call(rbind, results)
  colnames(ppi_fixed) <- c("source", "target")
  ppi_fixed <- as.data.frame(unique(ppi_fixed))
  ppi <- ppi_fixed
  
  class_i_halucinations <- NULL
  class_ii_halucinations <- NULL
  
  correct_predictions <- which(tolower(paste0(ppi$source, "=", ppi$target)) %in%
                                 tolower(paste0(curated_ppi[, 3], "=", curated_ppi[, 4])))
  correct_predictions <- paste0(ppi$source[correct_predictions], 
                                "=", 
                                ppi$target[correct_predictions])
  
  other_predictions <- setdiff(x = paste0(ppi$source, "=", ppi$target), y = c(class_i_halucinations, 
                                                                              class_ii_halucinations, 
                                                                              correct_predictions))
  
  ###
  
  ppi_genes_list[[length(ppi_genes_list)+1]] <- paste0(ppi[, 1], "=", ppi[, 2])
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
  
  mm <- unique(mm[2:nrow(mm), ])
  
  ppi <- mm
  colnames(ppi) <- c("source", "target")
  ppi <- as.data.frame(ppi)
  
  mm <- matrix(data = , nrow = nrow(ppi), ncol = 2)
  for(zz in 1:nrow(ppi)){
    mm[zz, ] <- sort(c(ppi$source[zz], ppi$target[zz]))
  }
  ppi <- as.data.frame(unique(mm))
  colnames(ppi) <- c("source", "target")
  ppi$source <- tolower(ppi$source)
  ppi$target <- tolower(ppi$target)
  
  ppi <- unique(ppi)
  
  ppi_genes_list_original[[length(ppi_genes_list_original)+1]] <- ppi
  
  ppi$source <- sapply(ppi$source, remove_special_characters)
  ppi$target <- sapply(ppi$target, remove_special_characters)
  ppi$source <- gsub(pattern = " ", replacement = "", x = ppi$source, fixed = TRUE)
  ppi$target <- gsub(pattern = " ", replacement = "", x = ppi$target, fixed = TRUE)
  
  ind2rem <- c()
  for(ii in 1:nrow(ppi)){
    
    nn1 <- nchar(ppi$source[ii])
    nn2 <- nchar(ppi$target[ii])
    
    if((nn1 <= 1) || (nn2 <= 1)){
      
      ind2rem <- c(ind2rem, ii)
      
    }
    
  }
  if(length(ind2rem) > 0){ppi <- ppi[-ind2rem, ]}
  
  indices <- seq_len(nrow(ppi))
  chunks <- split(indices, cut(indices, num_cores, labels = FALSE))
  
  cl <- makeCluster(num_cores)
  clusterExport(cl, varlist = c("ppi", "curated_ppi", "find_match_indices"))
  results <- parLapply(cl, chunks, parallel_process)
  stopCluster(cl)
  
  ppi_fixed <- do.call(rbind, results)
  colnames(ppi_fixed) <- c("source", "target")
  ppi_fixed <- as.data.frame(unique(ppi_fixed))
  ppi <- ppi_fixed
  
  class_i_halucinations <- NULL
  class_ii_halucinations <- NULL
  
  correct_predictions <- which(tolower(paste0(ppi$source, "=", ppi$target)) %in%
                                 tolower(paste0(curated_ppi[, 3], "=", curated_ppi[, 4])))
  correct_predictions <- paste0(ppi$source[correct_predictions], 
                                "=", 
                                ppi$target[correct_predictions])
  
  other_predictions <- setdiff(x = paste0(ppi$source, "=", ppi$target), y = c(class_i_halucinations, 
                                                                              class_ii_halucinations, 
                                                                              correct_predictions))
  
  ###
  
  ppi_genes_list[[length(ppi_genes_list)+1]] <- paste0(ppi[, 1], "=", ppi[, 2])
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


pdf(file = "output/model_predictions_ppi_all.pdf", width = 20, height = 10)
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

write.table(x = df, file = "output/model_predictions_ppi_all.txt", quote = FALSE, sep = "\t", 
            row.names = FALSE, col.names = TRUE)


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
  
  manual_relations <- unique(tolower(paste0(curated_ppi$cleaned_source, "=", curated_ppi$cleaned_target)))
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

pdf(file = "output/precision_recall_ppi_all.pdf", width = 20, height = 14)
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
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
        panel.grid.major.x = element_blank(),
        strip.text = element_text(size = 14)) +  # Increase the size of Model labels
  coord_cartesian(clip = 'off')
dev.off()

write.table(x = metrics_long, file = "output/precision_recall_ppi_all.txt", quote = FALSE, sep = "\t", 
            row.names = FALSE, col.names = TRUE)


