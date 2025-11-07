library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)

dir.create("output", showWarnings = FALSE)

annotated_grn <- read.delim("/beegfs/prj/LINDA_LLM/RegulaTome/test_tf_annotations/annotated_tf_relations_dedup_new.txt")
annotated_grn <- annotated_grn[which(annotated_grn$set == "Test"), ]

## =========================
## Curated GRN (ground truth)
## =========================
curated_grn <- matrix(data = , nrow = 1000000, ncol = 2)
cnt <- 1
for(ii in 1:nrow(annotated_grn)){
  curr <- strsplit(x = annotated_grn$tf_relations[ii], split = "; ", fixed = TRUE)[[1]]
  for(jj in 1:length(curr)){
    curated_grn[cnt, 1] <- strsplit(x = curr[jj], split = "=", fixed = TRUE)[[1]][1]
    curated_grn[cnt, 2] <- strsplit(x = curr[jj], split = "=", fixed = TRUE)[[1]][2]
    cnt <- cnt + 1
  }
}
colnames(curated_grn) <- c("source", "target")
curated_grn <- as.data.frame(unique(curated_grn))
curated_grn <- curated_grn[complete.cases(curated_grn), ]
curated_grn$source <- tolower(curated_grn$source)
curated_grn$target <- tolower(curated_grn$target)
curated_grn <- unique(curated_grn)

## =========================
## LLM output file list
## =========================
llm_files <- c(
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/negpos_ex/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/dynex_k5/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/lookup/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/neg_ex/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/pos_ex/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/tot_n3_vote/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/nerrel/oneshot/docs/ensemble_n5_t0.8/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/negpos_ex/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/dynex_k5/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/lookup/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/neg_ex/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/pos_ex/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/tot_n3_vote/spacy_nes_given/triples.jsonl",
  "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/nerrel/oneshot/docs/ensemble_n5_t0.8/spacy_nes_given/triples.jsonl"
)

names(llm_files) <- c("Llama70b_Vanilla","Llama70b_AllExamples","Llama70b_DynExamples","Llama70b_StringLookup",
                      "Llama70b_NegExamples","Llama70b_PosExamples", "Llama70b_TotN3", "Llama70b_EnsemblN5",
                      "Llama8b_Vanilla","Llama8b_AllExamples","Llama8b_DynExamples","Llama8b_StringLookup",
                      "Llama8b_NegExamples","Llama8b_PosExamples", "Llama8b_TotN3", "Llama8b_EnsemblN5")

llm_files <- llm_files[which(file.exists(llm_files))]

## Treat curated GRNs as directed
curated_grn_ordered <- matrix(NA, nrow = nrow(curated_grn), ncol = 2)
for(ii in 1:nrow(curated_grn)){
  curated_grn_ordered[ii, ] <- c(curated_grn$source[ii], curated_grn$target[ii])
}
colnames(curated_grn_ordered) <- c("source","target")
curated_grn_ordered <- as.data.frame(curated_grn_ordered) |> unique()
curated_grn <- curated_grn_ordered

## =========================
## Synonym mappings
## =========================
## Read the synonyms of entities from the RegulaTome Test ground truth and create 
## lists of synonyms for each source and target entity in the Test set.
json_data <- fromJSON("/beegfs/prj/LINDA_LLM/outputs/synonyms/tf/llama31/synonyms.json")
df <- enframe(json_data, name = "Main", value = "Elements") %>%
  unnest(Elements)
df$Main <- tolower(df$Main)
df$Elements <- tolower(df$Elements)
curated_grn_synonyms_source <- list()
curated_grn_synonyms_target <- list()
for(ii in 1:nrow(curated_grn)){
  
  ind <- which(df$Main == curated_grn$source[ii])
  if(length(ind) > 0){
    curated_grn_synonyms_source[[length(curated_grn_synonyms_source)+1]] <- unique(c(curated_grn$source[ii], df$Elements[ind]))
  } else {
    curated_grn_synonyms_source[[length(curated_grn_synonyms_source)+1]] <- curated_grn$source[ii]
  }
  
  ind <- which(df$Main == curated_grn$target[ii])
  if(length(ind) > 0){
    curated_grn_synonyms_target[[length(curated_grn_synonyms_target)+1]] <- unique(c(curated_grn$target[ii], df$Elements[ind]))
  } else {
    curated_grn_synonyms_target[[length(curated_grn_synonyms_target)+1]] <- curated_grn$target[ii]
  }
  
}

mapping_files <- c("/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama31/direct/stepwise/docs/synonyms.json",
                   "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33/direct/stepwise/docs/synonyms.json",
                   "/beegfs/prj/LINDA_LLM/outputs/triples/regulatome/tf/llama33regutf/direct/stepwise/docs/synonyms.json")

mapping_files <- mapping_files[which(file.exists(mapping_files))]
mapping_table <- matrix(data = , nrow = 1, ncol = 2)
for(ii in 1:length(mapping_files)){
  
  library(jsonlite)
  library(tidyverse)
  
  json_data <- fromJSON(mapping_files[ii])
  json_data <- Filter(function(x) !(is.list(x) && length(x) == 0), json_data)
  
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

## =========================
## Parse LLM outputs & compare
## =========================
grn_genes_list <- list()
grn_genes_list_original <- list()
correct_predictions_list <- list()
incorrect_predictions_list <- list()
missing_predictions_list <- list()
plot_df_list <- list()

for(ll in 1:length(llm_files)){
  path <- llm_files[ll]
  lines <- readLines(path, warn = FALSE)
  objs <- lapply(lines[nzchar(lines)], function(z) fromJSON(z))
  dat  <- bind_rows(objs)
  dat_flat <- jsonlite::flatten(dat)
  data <- dat_flat$responses
  v <- 1:length(data)
  data <- data[which(!is.na(v) & v %% 2 == 0)]
  mm <- matrix(NA, nrow = 1, ncol = 2)
  
  if(length(data) > 0 && length(data[[1]]) == 3){
    for(jj in 1:length(data)){
      curr <- data[[jj]]
      if(class(curr) == "array"){
        curr <- as.data.frame(curr)
        ## NOTE: ctrl_ind was undefined in the original branch; we skip this fragile path.
        ## Fallback to next branch if possible.
      } else {
        if(length(curr) > 0 && nrow(curr) > 0){
          tobind <- cbind(curr[,1], curr[,3])
          mm <- unique(rbind(mm, tobind))
        }
      }
    }
  } else {
    for(jj in 1:length(data)){
      curr <- data[[jj]]
      if(class(curr) == "array"){
        curr <- as.data.frame(curr)
        tobind <- cbind(curr$head, curr$tail)
        mm <- unique(rbind(mm, tobind))
      } else {
        if(length(curr) > 0 && nrow(curr) > 0){
          tobind <- cbind(curr[,1], curr[,3])
          mm <- unique(rbind(mm, tobind))
        }
      }
    }
  }
  
  if(nrow(mm) > 1){
    mm <- unique(mm[2:nrow(mm), ])
    grn <- as.data.frame(mm); colnames(grn) <- c("source","target")
    ## undirected
    mm2 <- matrix(NA, nrow = nrow(grn), ncol = 2)
    for(zz in 1:nrow(grn)) mm2[zz, ] <- c(grn$source[zz], grn$target[zz])
    grn <- as.data.frame(unique(mm2)); colnames(grn) <- c("source","target")
    grn$source <- tolower(grn$source); grn$target <- tolower(grn$target)
    grn <- unique(grn)
    
    grn_mapped <- matrix(NA, nrow = 1, ncol = 2)
    tmp_grn1 <- grn; tmp_grn2 <- grn
    
    ## Fix-1: Remove trailing '(' fragments
    tmp_grn1$source <- sapply(strsplit(x = tmp_grn1$source, split = "(", fixed = TRUE), "[", 1)
    tmp_grn1$target <- sapply(strsplit(x = tmp_grn1$target, split = "(", fixed = TRUE), "[", 1)
    
    ## Fix-4: naive singularization if ALL CAPS ending with s (use upper/lower invariant)
    matches <- grep("^[a-z0-9]+s$", tmp_grn2$source, value = TRUE)
    if(length(matches) > 0){
      idxidx <- which(tmp_grn2$source %in% matches)
      tmp_grn2$source[idxidx] <- sub("s$", "", tmp_grn2$source[idxidx])
    }
    matches <- grep("^[a-z0-9]+s$", tmp_grn2$target, value = TRUE)
    if(length(matches) > 0){
      idxidx <- which(tmp_grn2$target %in% matches)
      tmp_grn2$target[idxidx] <- sub("s$", "", tmp_grn2$target[idxidx])
    }
    
    for(ii in 1:nrow(grn)){
      source_ids <- unique(c(
        grn$source[ii],
        mapping_table$synonyms[which(mapping_table$main_id == grn$source[ii])],
        tmp_grn1$source[ii], tmp_grn2$source[ii],
        strsplit(x = grn$source[ii], split = "[^A-Za-z0-9]+")[[1]]
      ))
      target_ids <- unique(c(
        grn$target[ii],
        mapping_table$synonyms[which(mapping_table$main_id == grn$target[ii])],
        tmp_grn2$target[ii], tmp_grn2$target[ii],
        strsplit(x = grn$target[ii], split = "[^A-Za-z0-9]+")[[1]]
      ))
      
      matching_indices_source <- c(
        which(sapply(curated_grn_synonyms_source, function(x) any(x %in% source_ids))),
        which(sapply(curated_grn_synonyms_source, function(x) any(x %in% target_ids)))
      )
      matching_indices_target <- c(
        which(sapply(curated_grn_synonyms_target, function(x) any(x %in% target_ids))),
        which(sapply(curated_grn_synonyms_target, function(x) any(x %in% source_ids)))
      )
      
      matching_indices <- intersect(matching_indices_source, matching_indices_target)
      if(length(matching_indices) > 0){
        tobind <- cbind(curated_grn$source[matching_indices], curated_grn$target[matching_indices])
        grn_mapped <- rbind(grn_mapped, tobind)
      } else {
        tobind <- t(as.matrix(c(grn$source[ii], grn$target[ii])))
        grn_mapped <- rbind(grn_mapped, tobind)
      }
    }
    
    grn_mapped <- unique(grn_mapped[2:nrow(grn_mapped), ])
    colnames(grn_mapped) <- c("source","target")
    grn <- unique(as.data.frame(grn_mapped))
    
    grn_genes_list_original[[length(grn_genes_list_original)+1]] <- grn
    
    correct_predictions <- which(tolower(paste0(grn$source, "=", grn$target)) %in%
                                   tolower(paste0(curated_grn[,1], "=", curated_grn[,2])))
    correct_predictions <- paste0(grn$source[correct_predictions], "=", grn$target[correct_predictions])
    correct_predictions_list[[length(correct_predictions_list)+1]] <- correct_predictions
    
    incorrect_predictions <- setdiff(
      tolower(paste0(grn$source, "=", grn$target)),
      tolower(paste0(curated_grn[,1], "=", curated_grn[,2]))
    )
    incorrect_predictions_list[[length(incorrect_predictions_list)+1]] <- incorrect_predictions
    
    missing_predictions <- setdiff(
      tolower(paste0(curated_grn[,1], "=", curated_grn[,2])),
      tolower(paste0(grn$source, "=", grn$target))
    )
    missing_predictions_list[[length(missing_predictions_list)+1]] <- missing_predictions
    
    other_predictions <- setdiff(paste0(grn$source, "=", grn$target), correct_predictions)
    
    grn_genes_list[[length(grn_genes_list)+1]] <- paste0(grn[,1], "=", grn[,2])
    plot_df_list[[length(plot_df_list)+1]] <- c(0, 0, length(other_predictions), length(correct_predictions))
  } else {
    grn_genes_list[[length(grn_genes_list)+1]] <- "NA=NA"
    plot_df_list[[length(plot_df_list)+1]] <- rep(0, 4)
  }
}

names(grn_genes_list) <- names(llm_files)
names(correct_predictions_list) <- names(llm_files)
names(incorrect_predictions_list) <- names(llm_files)
names(missing_predictions_list) <- names(llm_files)
names(grn_genes_list_original) <- names(llm_files)

## =========================
## Plot 1: counts per model
## =========================
names(plot_df_list) <- names(llm_files)
df <- matrix(data = "", nrow = length(plot_df_list)*2, ncol = 3)
cnt <- 1
colnames(df) <- c("Cnt","Model","Type")
for(ii in 1:length(plot_df_list)){
  df[cnt,] <- c(plot_df_list[[ii]][3], names(llm_files)[ii], "inaccurate_predictions"); cnt <- cnt + 1
  df[cnt,] <- c(plot_df_list[[ii]][4], names(llm_files)[ii], "correct_predictions"); cnt <- cnt + 1
}
df <- as.data.frame(df); df$Cnt <- as.numeric(df$Cnt)
df$Type <- factor(df$Type, levels = c("correct_predictions","inaccurate_predictions"))
df_all <- df

df <- df_all
df$Model <- factor(df$Model)
colors <- c("inaccurate_predictions" = "#D3D3D3", "correct_predictions" = "#33FF57")

pdf(file = "output/model_predictions_grn_spacy.pdf", width = 20, height = 10)
ggplot(df, aes(x = Model, y = Cnt, fill = Type)) +
  geom_bar(stat = "identity", position = "stack") +
  scale_fill_manual(values = colors) +
  labs(title = "Stacked Plot of Prediction Types - Stepwise - No NER's",
       x = "Model Type", y = "Count", fill = "Prediction Type") +
  theme_minimal(base_size = 15) +
  theme(plot.title = element_text(hjust = 0.5, face = "bold", color = "#333333"),
        axis.text.x = element_text(angle = 90, hjust = 1),
        legend.position = "right",
        panel.grid.major = element_line(size = 0.1, color = "gray80"),
        panel.grid.minor = element_blank(),
        axis.title = element_text(face = "bold", color = "#555555"),
        strip.text = element_text(face = "bold", size = 12)) +
  guides(fill = guide_legend(reverse = TRUE))
dev.off()

## =========================
## Precision–Recall with bootstrap CI & CV
## =========================
library(reshape2)

safe_div <- function(a,b) ifelse(b == 0, NA_real_, a / b)

calculate_metrics <- function(manual_list, model_list) {
  TP <- length(intersect(manual_list, model_list))
  FP <- length(setdiff(model_list, manual_list))
  FN <- length(setdiff(manual_list, model_list))
  precision <- safe_div(TP, TP + FP)
  recall    <- safe_div(TP, TP + FN)
  f1_score  <- ifelse(is.na(precision) | is.na(recall) | (precision + recall) == 0,
                      NA_real_, 2 * (precision * recall) / (precision + recall))
  data.frame(TP, FP, FN, precision, recall, f1_score)
}

## Bootstrap over the universe of relations (manual ∪ model), resampling with replacement
bootstrap_metrics <- function(manual_list, model_list, B = 100, conf = 0.95, seed = 1234){
  set.seed(seed)
  universe <- unique(c(manual_list, model_list))
  n <- length(universe)
  if(n == 0) {
    return(list(
      samples = data.frame(precision = NA_real_, recall = NA_real_, f1_score = NA_real_)[FALSE,],
      stats   = data.frame(metric = c("precision","recall","f1_score"),
                           mean = NA_real_, sd = NA_real_, cv = NA_real_, 
                           lower = NA_real_, upper = NA_real_)
    ))
  }
  res <- matrix(NA_real_, nrow = B, ncol = 3); colnames(res) <- c("precision","recall","f1_score")
  for(b in 1:B){
    S <- sample(universe, size = n, replace = TRUE)
    man_sub <- intersect(manual_list, S)
    mod_sub <- intersect(model_list,  S)
    m <- calculate_metrics(man_sub, mod_sub)
    res[b,] <- as.numeric(m[, c("precision","recall","f1_score")])
  }
  res_df <- as.data.frame(res)
  alpha <- (1 - conf)/2
  stats <- data.frame(
    metric = c("precision","recall","f1_score"),
    mean   = sapply(res_df, function(x) mean(x, na.rm = TRUE)),
    sd     = sapply(res_df, function(x) sd(x,   na.rm = TRUE)),
    lower  = sapply(res_df, function(x) quantile(x, probs = alpha,     na.rm = TRUE, names = FALSE)),
    upper  = sapply(res_df, function(x) quantile(x, probs = 1 - alpha, na.rm = TRUE, names = FALSE))
  )
  stats$cv <- stats$sd / stats$mean
  list(samples = res_df, stats = stats)
}

## Main (full) metrics per model
metrics_df <- NULL
boot_stats_list <- list()

for(ii in 1:length(grn_genes_list)){
  manual_relations <- unique(tolower(paste0(curated_grn$source, "=", curated_grn$target)))
  model_relations  <- unique(tolower(grn_genes_list[[ii]]))
  
  full <- calculate_metrics(manual_relations, model_relations)
  metrics_df <- if(is.null(metrics_df)) full else rbind(metrics_df, full)
  
  ## Bootstrap stats for this model
  boot_res <- bootstrap_metrics(manual_relations, model_relations, B = 100, conf = 0.95, seed = 100 + ii)
  tmp <- boot_res$stats
  tmp$Type <- names(llm_files)[ii]
  boot_stats_list[[length(boot_stats_list)+1]] <- tmp
}

metrics_df$Type <- names(llm_files)
metrics_long <- reshape2::melt(metrics_df, id.vars = "Type",
                               measure.vars = c("precision","recall","f1_score"),
                               variable.name = "Metric", value.name = "Score")

## Step/Model split
metrics_long$Step  <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 2)
metrics_long$Model <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1)

## Collect CI & CV and merge
boot_stats <- do.call(rbind, boot_stats_list)
colnames(boot_stats)[colnames(boot_stats) == "metric"] <- "Metric"
boot_stats$Metric <- factor(boot_stats$Metric, levels = c("precision","recall","f1_score"))

metrics_ci <- metrics_long %>%
  left_join(boot_stats %>% dplyr::select(Type, Metric, lower, upper, cv), by = c("Type","Metric"))

## Save a tidy table with main metrics + CI + CV
write.csv(metrics_ci %>%
            dplyr::select(Type, Model, Step, Metric, Score, lower, upper, cv),
          file = "output/metrics_with_ci_grn_spacy.csv", row.names = FALSE)

## =========================
## Plot 2: PR/F1 with CI (error bars) + CV in labels
## =========================

pad <- 0.03
metrics_ci <- metrics_ci %>%
  dplyr::mutate(
    label_pos = ifelse(
      !is.na(upper),
      upper + pad,           # right of the highest CI value
      Score + pad            # fallback when CI not available
    ),
    label_txt = ifelse(
      is.na(cv),
      sprintf("%.2f", Score),
      sprintf("%.2f (CV %.1f%%)", Score, 100 * cv)
    )
  )

pdf(file = "output/precision_recall_grn_spacy.pdf", width = 20, height = 12)

ggplot(metrics_ci, aes(x = Step, y = Score, fill = Metric, group = interaction(Model, Metric))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  # 95% bootstrap CIs
  geom_errorbar(aes(ymin = lower, ymax = upper),
                position = position_dodge(width = 0.8),
                width = 0.25, linewidth = 0.4) +
  # Labels to the RIGHT of the CI, slightly smaller, left-justified
  geom_text(aes(y = label_pos, label = label_txt),
            position = position_dodge(width = 0.8),
            hjust = 0,           # left-justify so text extends to the right
            size = 6) +          # a bit smaller than before
  facet_wrap(~Model, ncol = 2) +
  labs(title = "Precision, Recall, and F1-Score by Step and Model (95% CI; labels show CV)",
       y = "Score",
       x = "Examples Type") +
  theme_minimal() +
  scale_fill_manual(values = c("precision" = "#1E90FF", "recall" = "#FFA500", "f1_score" = "#808080")) +
  # Add extra room on the right so labels don't get clipped after coord_flip
  scale_y_continuous(expand = expansion(mult = c(0.02, 0.30))) +
  theme(
    axis.text.x = element_text(),
    panel.grid.major.x = element_blank(),
    strip.text = element_text(size = 14),
    axis.text.y  = element_text(size = 14),      # tick labels on the y axis
    axis.title.y = element_text(size = 16, face = "bold")  # axis title
  ) +
  coord_flip(clip = "off")

dev.off()

## =========================
## Fischer's Test Heatmaps
## =========================

library(dplyr)
library(tidyr)
library(ggplot2)
library(patchwork)   # for arranging plots
library(scales)

stopifnot(all(c("TP","FP","FN","Type") %in% colnames(metrics_df)))

metrics_counts <- metrics_df %>%
  dplyr::select(Type, TP, FP, FN) %>%
  distinct()

Types <- metrics_counts$Type
nT    <- length(Types)

# Helper to build a symmetric matrix of p-values for a given 2xK contingency definition
pairwise_fisher <- function(def_fun) {
  pmat <- matrix(NA_real_, nT, nT, dimnames = list(Types, Types))
  for (i in seq_len(nT)) {
    for (j in seq_len(nT)) {
      if (i == j) { pmat[i, j] <- NA_real_; next }
      a <- metrics_counts[i, ]
      b <- metrics_counts[j, ]
      tab <- def_fun(a, b)
      # Fisher's exact test works for 2x2 and 2xK; use simulate.p.value=FALSE by default
      p <- tryCatch(stats::fisher.test(tab)$p.value, error = function(e) NA_real_)
      pmat[i, j] <- p
    }
  }
  # Multiple testing correction across all off-diagonal comparisons
  pv <- as.vector(pmat)
  idx <- which(is.finite(pv))
  pv_adj <- rep(NA_real_, length(pv))
  pv_adj[idx] <- p.adjust(pv[idx], method = "BH")
  matrix(pv_adj, nT, nT, dimnames = list(Types, Types))
}

# Definitions of the contingency tables per metric
# Precision: TP vs FP
def_precision <- function(a, b) {
  matrix(c(a$TP, a$FP,
           b$TP, b$FP), nrow = 2, byrow = TRUE,
         dimnames = list(c(a$Type, b$Type), c("TP","FP")))
}
# Recall: TP vs FN
def_recall <- function(a, b) {
  matrix(c(a$TP, a$FN,
           b$TP, b$FN), nrow = 2, byrow = TRUE,
         dimnames = list(c(a$Type, b$Type), c("TP","FN")))
}
# Overall (proxy for F1): TP vs FP vs FN (2x3 Fisher)
# This tests whether the distribution over {TP, FP, FN} differs between Types.
def_overall <- function(a, b) {
  matrix(c(a$TP, a$FP, a$FN,
           b$TP, b$FP, b$FN), nrow = 2, byrow = TRUE,
         dimnames = list(c(a$Type, b$Type), c("TP","FP","FN")))
}

# Compute adjusted p-value matrices
p_precision <- pairwise_fisher(def_precision)
p_recall    <- pairwise_fisher(def_recall)
p_overall   <- pairwise_fisher(def_overall)

# Long-format helper for plotting
prep_long <- function(pmat) {
  as.data.frame(pmat) |>
    tibble::rownames_to_column("Var1") |>
    pivot_longer(-Var1, names_to = "Var2", values_to = "p_adj") |>
    mutate(neglog10_p = ifelse(is.finite(p_adj), -log10(p_adj), NA_real_),
           stars = dplyr::case_when(
             is.na(p_adj)            ~ "",
             p_adj < 0.001           ~ "***",
             p_adj < 0.01            ~ "**",
             p_adj < 0.05            ~ "*",
             TRUE                     ~ ""
           ),
           Var1 = factor(Var1, levels = Types),
           Var2 = factor(Var2, levels = Types))
}

df_prec <- prep_long(p_precision)
df_rec  <- prep_long(p_recall)
df_f1p  <- prep_long(p_overall)  # "overall" proxy (2x3 Fisher on TP/FP/FN)

# Reusable heatmap plotter
plot_heat <- function(df, title) {
  ggplot(df, aes(x = Var2, y = Var1, fill = neglog10_p)) +
    geom_tile(color = "white", linewidth = 0.2, na.rm = FALSE) +
    geom_text(aes(label = stars), size = 4.5, na.rm = TRUE) +
    scale_fill_viridis_c(option = "C", na.value = "grey90",
                         name = expression(-log[10]~"(adj p)")) +
    coord_fixed() +
    labs(title = title, x = NULL, y = NULL) +
    theme_minimal(base_size = 13) +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      panel.grid = element_blank(),
      plot.title = element_text(face = "bold", hjust = 0.5)
    )
}

plt_prec <- plot_heat(df_prec, "Precision")
plt_rec  <- plot_heat(df_rec,  "Recall")
plt_f1p  <- plot_heat(df_f1p,  "F1-Score")

# Arrange in one figure and save
final_plot <- plt_prec + plt_rec + plt_f1p + plot_layout(ncol = 2)

ggsave("output/significance_heatmaps_grn_spacy.pdf", final_plot, width = 20, height = 20)
ggsave("output/significance_heatmaps_grn_spacy.png", final_plot, width = 20, height = 20, dpi = 300)

