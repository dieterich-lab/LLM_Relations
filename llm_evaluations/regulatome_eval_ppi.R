library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)

dir.create("output/regulatome")

## Read the annotated RegulaTome PPIs and keep the class Test for evaluations
annotated_ppi <- read.delim("../src/regulatome_corpus/annotated_ppi_relations_by_class.txt")
annotated_ppi <- annotated_ppi[which(annotated_ppi$set == "Test"), ]

curated_ppi <- matrix(data = , nrow = 1000000, ncol = 2)
cnt <- 1
for(ii in 1:nrow(annotated_ppi)){
  curr <- strsplit(x = annotated_ppi$ppi_relations[ii], split = "; ", fixed = TRUE)[[1]]
  for(jj in 1:length(curr)){
    curated_ppi[cnt, 1] <- strsplit(x = curr[jj], split = "=", fixed = TRUE)[[1]][1]
    curated_ppi[cnt, 2] <- strsplit(x = curr[jj], split = "=", fixed = TRUE)[[1]][2]
    cnt <- cnt + 1
  }
}
colnames(curated_ppi) <- c("source", "target")
curated_ppi <- as.data.frame(unique(curated_ppi))
curated_ppi <- curated_ppi[complete.cases(curated_ppi), ]
curated_ppi$source <- tolower(curated_ppi$source)
curated_ppi$target <- tolower(curated_ppi$target)
curated_ppi <- unique(curated_ppi)

## Read the LLM files
llm_files <- paste0("../llm_files/regulatome_eval_ppi/", list.files(path = "../llm_files/regulatome_eval_ppi/"))

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
                      "Llama8bV1_Lookup_Standard_NoExamples",
                      "Llama8bV1_Stepwise_FineTuned_AllExamples",
                      "Llama8bV1_Stepwise_FineTuned_FPExamples",
                      "Llama8bV1_Stepwise_FineTuned_NoExamples",
                      "Llama8bV1_Stepwise_FineTuned_TPExamples",
                      "Llama8bV1_Stepwise_Standard_AllExamples",
                      "Llama8bV1_Stepwise_Standard_FPExamples",
                      "Llama8bV1_Stepwise_Standard_NoExamples",
                      "Llama8bV1_Stepwise_Standard_TPExamples")

curated_ppi_ordered <- matrix(data = , nrow = nrow(curated_ppi), ncol = 2)
for(ii in 1:nrow(curated_ppi)){
  curated_ppi_ordered[ii, ] <- sort(c(curated_ppi$source[ii], curated_ppi$target[ii]))
}
colnames(curated_ppi_ordered) <- c("source", "target")
curated_ppi_ordered <- as.data.frame(curated_ppi_ordered)
curated_ppi_ordered <- unique(curated_ppi_ordered)
curated_ppi <- curated_ppi_ordered


## Read the synonyms of entities from the RegulaTome Test ground truth and create 
## lists of synonyms for each source and target entity in the Test set.
json_data <- fromJSON("../llm_files/regulatome_synonyms/llama70bv3_test_entities.json")
df <- enframe(json_data, name = "Main", value = "Elements") %>%
  unnest(Elements)
df$Main <- tolower(df$Main)
df$Elements <- tolower(df$Elements)
curated_ppi_synonyms_source <- list()
curated_ppi_synonyms_target <- list()
for(ii in 1:nrow(curated_ppi)){
  
  ind <- which(df$Main == curated_ppi$source[ii])
  if(length(ind) > 0){
    curated_ppi_synonyms_source[[length(curated_ppi_synonyms_source)+1]] <- unique(c(curated_ppi$source[ii], df$Elements[ind]))
  } else {
    curated_ppi_synonyms_source[[length(curated_ppi_synonyms_source)+1]] <- curated_ppi$source[ii]
  }
  
  ind <- which(df$Main == curated_ppi$target[ii])
  if(length(ind) > 0){
    curated_ppi_synonyms_target[[length(curated_ppi_synonyms_target)+1]] <- unique(c(curated_ppi$target[ii], df$Elements[ind]))
  } else {
    curated_ppi_synonyms_target[[length(curated_ppi_synonyms_target)+1]] <- curated_ppi$target[ii]
  }
  
}


## Read the synonyms of entities extracted from RE LLM evaluations and create a mapping table
mapping_files <- c("../llm_files/regulatome_synonyms/llama70bv3_standard_re.json",
                   "../llm_files/regulatome_synonyms/llama70bv3_finetuned_re.json")

mapping_files <- mapping_files[which(file.exists(mapping_files))]
mapping_table <- matrix(data = , nrow = 1, ncol = 2)
for(ii in 1:length(mapping_files)){
  
  library(jsonlite)
  library(tidyverse)
  
  json_data <- fromJSON(mapping_files[ii])
  
  df <- enframe(json_data, name = "Main", value = "Elements") %>%
    unnest(Elements)
  
  tobind1 <- matrix(data = , nrow = nrow(df), ncol = 2)
  tobind1[, 1] <- df$Main
  tobind1[, 2] <- df$Elements
  
  tobind2 <- matrix(data = , nrow = length(unique(df$Main)), ncol = 2)
  tobind2[, 1] <- unique(df$Main)
  tobind2[, 2] <- unique(df$Main)
  
  mapping_table <- unique(rbind(mapping_table, tobind1, tobind2))
  
}
mapping_table <- as.data.frame(mapping_table)
colnames(mapping_table) <- c("main_id", "synonyms")
mapping_table <- mapping_table[complete.cases(mapping_table), ]
mapping_table$main_id <- tolower(mapping_table$main_id)
mapping_table$synonyms <- tolower(mapping_table$synonyms)
mapping_table <- unique(mapping_table)



######### Evaluations
eval_steps <- 1:3
ppi_genes_list <- list()
ppi_genes_list_original <- list()
entities_check <- list()
plot_df_list <- list()
nn <- c()
ind_llm_1 <- 1:length(llm_files)

for(ctrl_ind in eval_steps){
  
  for(ll in ind_llm_1){
    
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
    
    if(nrow(mm) > 1){
      
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
      
      ###
      tmp_ppi1 <- ppi
      tmp_ppi2 <- ppi
      
      # Fix-1: Brakets
      tmp_ppi1$source <- sapply(strsplit(x = tmp_ppi1$source, split = "(", fixed = TRUE), "[", 1)
      tmp_ppi1$target <- sapply(strsplit(x = tmp_ppi1$target, split = "(", fixed = TRUE), "[", 1)
      
      
      # Fix-4: Identify those cases which end with 's' in the end
      matches <- grep("^[A-Z]+s$", tmp_ppi2$source, value = TRUE)
      if(length(matches) > 0){
        idxidx <- which(tmp_ppi2$source %in% matches)
        tmp_ppi2$source[idxidx] <- sub("s$", "", tmp_ppi2$source[idxidx])
      }
      matches <- grep("^[A-Z]+s$", tmp_ppi2$target, value = TRUE)
      if(length(matches) > 0){
        idxidx <- which(tmp_ppi2$target %in% matches)
        tmp_ppi2$target[idxidx] <- sub("s$", "", tmp_ppi2$target[idxidx])
      }
      
      ppi_mapped <- matrix(data = , nrow = 1, ncol = 2)
      
      for(ii in 1:nrow(ppi)){
        
        source_ids <- unique(c(ppi$source[ii], mapping_table$synonyms[which(mapping_table$main_id == ppi$source[ii])], 
                               tmp_ppi1$source[ii], tmp_ppi2$source[ii], 
                               strsplit(x = ppi$source[ii], split = "[^A-Za-z0-9]+")[[1]]))
        target_ids <- unique(c(ppi$target[ii], mapping_table$synonyms[which(mapping_table$main_id == ppi$target[ii])],
                               tmp_ppi2$target[ii], tmp_ppi2$target[ii],
                               strsplit(x = ppi$target[ii], split = "[^A-Za-z0-9]+")[[1]]))
        
        
        ## Check for overlapping synonyms between the LLM extracted relations and the ground truth
        matching_indices_source <- c(which(sapply(curated_ppi_synonyms_source, function(x) {
          any(x %in% source_ids)
        })),
        which(sapply(curated_ppi_synonyms_source, function(x) {
          any(x %in% target_ids)
        })))
        
        matching_indices_target <- c(which(sapply(curated_ppi_synonyms_target, function(x) {
          any(x %in% target_ids)
        })),
        which(sapply(curated_ppi_synonyms_target, function(x) {
          any(x %in% source_ids)
        })))
        
        matching_indices <- intersect(x = matching_indices_source, matching_indices_target)
        if(length(matching_indices) > 0){
          tobind <- matrix(data = , nrow = length(matching_indices), ncol = 2)
          tobind[, 1] <- curated_ppi$source[matching_indices]
          tobind[, 2] <- curated_ppi$target[matching_indices]
          ppi_mapped <- rbind(ppi_mapped, tobind)
        } else {
          tobind <- t(as.matrix(sort(c(ppi$source[ii], ppi$target[ii]))))
          ppi_mapped <- rbind(ppi_mapped, tobind)
        }
        
      }
      ppi_mapped <- unique(ppi_mapped[2:nrow(ppi_mapped), ])
      colnames(ppi_mapped) <- c("source", "target")
      ppi_mapped <- as.data.frame(ppi_mapped)
      ppi <- unique(ppi_mapped)
      
      ###
      class_i_halucinations <- NULL
      class_ii_halucinations <- NULL
      
      correct_predictions <- which(tolower(paste0(ppi$source, "=", ppi$target)) %in%
                                     tolower(paste0(curated_ppi[, 1], "=", curated_ppi[, 2])))
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
      plot_df_list[[length(plot_df_list)+1]] <- rep(0, 4)
      
      nn <- c(nn, paste0(names(llm_files)[ll], "_Step", ctrl_ind))
      
    }
    
    
  }
  
}


########## Now do the plots
names(plot_df_list) <- nn


df <- matrix(data = "", nrow = length(plot_df_list)*2, ncol = 7)
cnt <- 1
colnames(df) <- c("Cnt", "Model", "Style", "NER", "Step", "Type", "Confidence")
for(ii in 1:length(plot_df_list)){
  
  df[cnt, 1] <- plot_df_list[[ii]][3]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1]
  df[cnt, 3] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3]
  df[cnt, 4] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][4]
  df[cnt, 5] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][5]
  df[cnt, 6] <- "inaccurate_predictions"
  if(grepl(pattern = "HighRel", x = names(plot_df_list)[ii], fixed = TRUE)){df[cnt, 7] <- "HighRel"}
  if(grepl(pattern = "AllRel", x = names(plot_df_list)[ii], fixed = TRUE)){df[cnt, 7] <- "AllRel"}
  
  cnt <- cnt + 1
  
  df[cnt, 1] <- plot_df_list[[ii]][4]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1]
  df[cnt, 3] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3]
  df[cnt, 4] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][4]
  df[cnt, 5] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][5]
  df[cnt, 6] <- "correct_predictions"
  if(grepl(pattern = "HighRel", x = names(plot_df_list)[ii], fixed = TRUE)){df[cnt, 7] <- "HighRel"}
  if(grepl(pattern = "AllRel", x = names(plot_df_list)[ii], fixed = TRUE)){df[cnt, 7] <- "AllRel"}
  
  cnt <- cnt + 1
  
}
df <- as.data.frame(df)
df$Cnt <- as.numeric(df$Cnt)


df$Type <- factor(df$Type, 
                  levels = c("correct_predictions", 
                             "inaccurate_predictions"))

df_all <- df


## Stepwise
df <- df_all

df$Model <- paste0(df$Model, "_", df$Style, "_", df$NER)
df$Model[which(df$Confidence!="")] <- paste0(df$Model[which(df$Confidence!="")], "_", df$Confidence[which(df$Confidence!="")])
df$Model <- factor(df$Model,
                   levels = intersect(x = gsub(pattern = "_Stepwise", replacement = "", x = names(llm_files)), y = unique(df$Model)))

colors <- c("inaccurate_predictions" = "#D3D3D3",
            "correct_predictions" = "#33FF57")


pdf(file = "output/regulatome/model_predictions_ppi_stepwise_finetuned_all_integrated.pdf", width = 20, height = 10)
ggplot(df, aes(x = Model, y = Cnt, fill = Type)) +
  geom_bar(stat = "identity", position = "stack") +
  scale_fill_manual(values = colors) +
  labs(
    title = "Stacked Plot of Prediction Types - Stepwise",
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

metrics_long_all <- metrics_long


## Llama8b Stepwise
metrics_long <- metrics_long_all[which(grepl(pattern = "Llama8bV1_Stepwise", x = metrics_long_all$Type, fixed = TRUE)), ]
metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 5)
metrics_long$Model <- paste0(sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 3),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 4))

metrics_long$Model <- factor(metrics_long$Model,
                             levels = intersect(x = gsub(pattern = "_Stepwise", replacement = "", x = names(llm_files)), y = unique(df$Model)))

pdf(file = "output/regulatome/precision_recall_ppi_stepwise_llama8bv1.pdf", width = 22, height = 18)
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


## Llama70b Stepwise
metrics_long <- metrics_long_all[which(grepl(pattern = "Llama70bV3_Stepwise", x = metrics_long_all$Type, fixed = TRUE)), ]
metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 5)
metrics_long$Model <- paste0(sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 3),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 4))

metrics_long$Model <- factor(metrics_long$Model,
                             levels = intersect(x = gsub(pattern = "_Stepwise", replacement = "", x = names(llm_files)), y = unique(df$Model)))

pdf(file = "output/regulatome/precision_recall_ppi_stepwise_llama70bv3.pdf", width = 22, height = 18)
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


## Llama70b Dynamic
metrics_long <- metrics_long_all[which(grepl(pattern = "Llama70bV3_Dynamic", x = metrics_long_all$Type, fixed = TRUE)), ]
metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 5)
metrics_long$Model <- paste0(sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 3),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 4))

metrics_long$Model <- factor(metrics_long$Model,
                             levels = intersect(x = gsub(pattern = "_Stepwise", replacement = "", x = names(llm_files)), y = unique(df$Model)))

pdf(file = "output/regulatome/precision_recall_ppi_dynamic_llama70bv3.pdf", width = 22, height = 18)
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


## Llama8b Lookup
metrics_long <- metrics_long_all[which(grepl(pattern = "Llama8bV1_Lookup", x = metrics_long_all$Type, fixed = TRUE)), ]
metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 5)
metrics_long$Model <- paste0(sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 3),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 4))

metrics_long$Model <- factor(metrics_long$Model,
                             levels = intersect(x = gsub(pattern = "_Stepwise", replacement = "", x = names(llm_files)), y = unique(df$Model)))

pdf(file = "output/regulatome/precision_recall_ppi_lookup_llama8bv1.pdf", width = 22, height = 18)
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


## Llama70b Lookup
metrics_long <- metrics_long_all[which(grepl(pattern = "Llama70bV3_Lookup", x = metrics_long_all$Type, fixed = TRUE)), ]
metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 5)
metrics_long$Model <- paste0(sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 3),
                             "_",
                             sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 4))

metrics_long$Model <- factor(metrics_long$Model,
                             levels = intersect(x = gsub(pattern = "_Stepwise", replacement = "", x = names(llm_files)), y = unique(df$Model)))

pdf(file = "output/regulatome/precision_recall_ppi_lookup_llama70bv3.pdf", width = 22, height = 18)
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



write.table(x = metrics_long, file = "output/regulatome/precision_recall_ppi.txt", quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)


