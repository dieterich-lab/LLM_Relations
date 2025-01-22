library(readr)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)

dir.create("output")


## Manually annotated relations for each paper
ppi_manual <- list()
ppi_manual[[length(ppi_manual)+1]] <- unique(strsplit(x = "BNIP-2=LATS1, LATS1=YAP, BNIP-2=RhoA", split = ", ", fixed = TRUE)[[1]])
ppi_manual[[length(ppi_manual)+1]] <- unique(strsplit(x = "TRIM11=DUSP1, DUSP=MAPK, DUSP=ERK, DUSP=JNK, TRIM11=JNK", split = ", ", fixed = TRUE)[[1]])
ppi_manual[[length(ppi_manual)+1]] <- unique(strsplit(x = "GATA4=NKX2-5, GATA4=FOG2, GATA4=TBX5, MAPK=GATA4, GATA4=MEF2C, GATA4=HAND2, GATA4=SRF", split = ", ", fixed = TRUE)[[1]])
ppi_manual[[length(ppi_manual)+1]] <- unique(strsplit(x = "PTEN=Akt, AKT=Erk1/2, ROS=PTEN, MKK1=Erk1/2, Mad=ROS", split = ", ", fixed = TRUE)[[1]])
ppi_manual[[length(ppi_manual)+1]] <- unique(strsplit(x = "PKGI=PDE5", split = ", ", fixed = TRUE)[[1]])
names(ppi_manual) <- paste0("Paper", 1:5)

papers_relations <- matrix(data = , nrow = 1, ncol = 3)
for(ii in 1:length(ppi_manual)){
  
  curr <- ppi_manual[[ii]]
  tobind <- matrix(data = , nrow = length(curr), ncol = 3)
  for(jj in 1:length(curr)){
    
    tobind[, 1] <- names(ppi_manual)[ii]
    tobind[, 2] <- sapply(strsplit(x = curr, split = "=", fixed = TRUE), "[", 1)
    tobind[, 3] <- sapply(strsplit(x = curr, split = "=", fixed = TRUE), "[", 2)
    
  }
  papers_relations <- unique(rbind(papers_relations, tobind))
  
}
papers_relations <- papers_relations[2:nrow(papers_relations), ]
colnames(papers_relations) <- c("Paper", "Protein1", "Protein2")
papers_relations[which(papers_relations[, 1] == "Paper1"), 1] <- "Wong etal"
papers_relations[which(papers_relations[, 1] == "Paper2"), 1] <- "He etal"
papers_relations[which(papers_relations[, 1] == "Paper3"), 1] <- "Valimaki etal"
papers_relations[which(papers_relations[, 1] == "Paper4"), 1] <- "Chen etal"
papers_relations[which(papers_relations[, 1] == "Paper5"), 1] <- "Park etal"
write.table(x = papers_relations, file = "output/papers_relations.txt", quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)

## We do some standardizing of named entities
map_table <- matrix(data = , nrow = 24, ncol = 2)
map_table[1, ] <- c("BNIP-2", "BINP2")
map_table[2, ] <- c("bnip-2", "BINP2")
map_table[3, ] <- c("DUSP", "DUSP1")
map_table[4, ] <- c("Akt", "AKT")
map_table[5, ] <- c("AKT1", "AKT")
map_table[6, ] <- c("AKT2", "AKT")
map_table[7, ] <- c("AKT3", "AKT")
map_table[8, ] <- c("akt1", "AKT")
map_table[9, ] <- c("akt2", "AKT")
map_table[10, ] <- c("akt3", "AKT")
map_table[11, ] <- c("Erk1/2", "ERK")
map_table[12, ] <- c("erk1/2", "ERK")
map_table[13, ] <- c("ERK1", "ERK")
map_table[14, ] <- c("ERK2", "AKT")
map_table[15, ] <- c("PKGI", "PKG")
map_table[16, ] <- c("JNK1/2", "JNK")
map_table[17, ] <- c("JNK1", "JNK")
map_table[18, ] <- c("JNK2", "JNK")
map_table[19, ] <- c("jnk1/2", "JNK")
map_table[20, ] <- c("jnk1", "JNK")
map_table[21, ] <- c("jnk2", "JNK")
map_table[22, ] <- c("cGMP", "CGMP")
map_table[23, ] <- c("sGC", "SGC")
map_table[24, ] <- c("PDE5", "PDE")
map_table <- map_table[complete.cases(map_table), ]

tmp <- list()
for(ii in 1:length(ppi_manual)){
  cc <- c()
  for(jj in 1:length(ppi_manual[[ii]])){
    ss <- strsplit(x = ppi_manual[[ii]][jj], split = "=", fixed = TRUE)[[1]][1]
    tt <- strsplit(x = ppi_manual[[ii]][jj], split = "=", fixed = TRUE)[[1]][2]
    if(ss %in% map_table[, 1]){
      ss <- map_table[which(map_table[, 1] == ss), 2]
    }
    if(tt %in% map_table[, 1]){
      tt <- map_table[which(map_table[, 1] == tt), 2]
    }
    cc <- c(cc, paste0(ss, "=", tt))
  }
  tmp[[length(tmp)+1]] <- cc
}
names(tmp) <- names(ppi_manual)
ppi_manual <- tmp

#### ChatGPT-v4o results across each step
# Prompt-1
ppi_chatgpt <- list()
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "BNIP-2=LATS1, LATS1=YAP, RhoA=Myosin II", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "DUSP1=JNK1/2, TRIM11=DUSP1", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "PTEN=Akt, Akt=Erk1/2", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "NO=PKG, sGC=PKG, PKG=Phospholamban, PKG=MitoKATP", split = ", ", fixed = TRUE)[[1]])
names(ppi_chatgpt) <- paste0("Paper", 1:5)
ppi_chatgpt1 <- ppi_chatgpt

tmp <- list()
for(ii in 1:length(ppi_chatgpt1)){
  cc <- c()
  ll <- length(ppi_chatgpt1[[ii]])
  if(ll > 0){
    for(jj in 1:length(ppi_chatgpt1[[ii]])){
      ss <- strsplit(x = ppi_chatgpt1[[ii]][jj], split = "=", fixed = TRUE)[[1]][1]
      tt <- strsplit(x = ppi_chatgpt1[[ii]][jj], split = "=", fixed = TRUE)[[1]][2]
      if(ss %in% map_table[, 1]){
        ss <- map_table[which(map_table[, 1] == ss), 2]
      }
      if(tt %in% map_table[, 1]){
        tt <- map_table[which(map_table[, 1] == tt), 2]
      }
      cc <- c(cc, paste0(ss, "=", tt))
    }
    tmp[[length(tmp)+1]] <- cc
  } else {
    tmp[[length(tmp)+1]] <- ""
  }
}
names(tmp) <- names(ppi_chatgpt1)
ppi_chatgpt1 <- tmp

# Prompt-2
ppi_chatgpt <- list()
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "BNIP-2=LATS1, LATS1=YAP, RhoA=Myosin II", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "DUSP1=JNK1/2, TRIM11=DUSP1", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "PTEN=Akt, Akt=Erk1/2", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "NO=PKG, PKG=Phospholamban, PKG=MitoKATP", split = ", ", fixed = TRUE)[[1]])
names(ppi_chatgpt) <- paste0("Paper", 1:5)
ppi_chatgpt2 <- ppi_chatgpt

tmp <- list()
for(ii in 1:length(ppi_chatgpt2)){
  cc <- c()
  ll <- length(ppi_chatgpt2[[ii]])
  if(ll > 0){
    for(jj in 1:length(ppi_chatgpt2[[ii]])){
      ss <- strsplit(x = ppi_chatgpt2[[ii]][jj], split = "=", fixed = TRUE)[[1]][1]
      tt <- strsplit(x = ppi_chatgpt2[[ii]][jj], split = "=", fixed = TRUE)[[1]][2]
      if(ss %in% map_table[, 1]){
        ss <- map_table[which(map_table[, 1] == ss), 2]
      }
      if(tt %in% map_table[, 1]){
        tt <- map_table[which(map_table[, 1] == tt), 2]
      }
      cc <- c(cc, paste0(ss, "=", tt))
    }
    tmp[[length(tmp)+1]] <- cc
  } else {
    tmp[[length(tmp)+1]] <- ""
  }
}
names(tmp) <- names(ppi_chatgpt2)
ppi_chatgpt2 <- tmp

# Prompt-3
ppi_chatgpt <- list()
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "BNIP-2=LATS1, LATS1=YAP, RhoA=Myosin II", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "DUSP1=JNK1/2, TRIM11=DUSP1", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = " ", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "PTEN=Akt, Akt=Erk1/2", split = ", ", fixed = TRUE)[[1]])
ppi_chatgpt[[length(ppi_chatgpt)+1]] <- unique(strsplit(x = "NO=PKG, PKG=Phospholamban, PKG=MitoKATP", split = ", ", fixed = TRUE)[[1]])
names(ppi_chatgpt) <- paste0("Paper", 1:5)
ppi_chatgpt3 <- ppi_chatgpt

tmp <- list()
for(ii in 1:length(ppi_chatgpt3)){
  cc <- c()
  ll <- length(ppi_chatgpt3[[ii]])
  if(ll > 0){
    for(jj in 1:length(ppi_chatgpt3[[ii]])){
      ss <- strsplit(x = ppi_chatgpt3[[ii]][jj], split = "=", fixed = TRUE)[[1]][1]
      tt <- strsplit(x = ppi_chatgpt3[[ii]][jj], split = "=", fixed = TRUE)[[1]][2]
      if(ss %in% map_table[, 1]){
        ss <- map_table[which(map_table[, 1] == ss), 2]
      }
      if(tt %in% map_table[, 1]){
        tt <- map_table[which(map_table[, 1] == tt), 2]
      }
      cc <- c(cc, paste0(ss, "=", tt))
    }
    tmp[[length(tmp)+1]] <- cc
  } else {
    tmp[[length(tmp)+1]] <- ""
  }
}
names(tmp) <- names(ppi_chatgpt3)
ppi_chatgpt3 <- tmp

## Curated PPI relations in a tabular format
curated_ppi <- cbind(sapply(strsplit(x = unique(unlist(ppi_manual)), split = "=", fixed = TRUE), "[", 1),
                     sapply(strsplit(x = unique(unlist(ppi_manual)), split = "=", fixed = TRUE), "[", 2))


llm_files <- c("../../llm_files/manuscript_eval_ppi/Llama70b.json",
               "../../llm_files/manuscript_eval_ppi/Llama405b.json")

names(llm_files) <- c("Llama70b_Between_Style1", "Llama405b_Between_Style1")

human_genes <- unique(tolower(c(curated_ppi[, 1], curated_ppi[, 2])))


#### Step 1
ctrl_ind <- 1
ppi_genes_list <- list()
plot_df_list <- list()
nn <- c()
for(ll in 1:2){
  
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
  
  ind <- which(mm[, 1] %in% map_table[, 1])
  if(length(ind) > 0){
    
    for(jj in 1:length(ind)){
      
      idx <- which(map_table[, 1] == mm[ind[jj], 1])
      mm[ind[jj], 1] <- map_table[idx, 2]
      
    }
    
  }
  
  ind <- which(mm[, 2] %in% map_table[, 1])
  if(length(ind) > 0){
    
    for(jj in 1:length(ind)){
      
      idx <- which(map_table[, 1] == mm[ind[jj], 2])
      mm[ind[jj], 2] <- map_table[idx, 2]
      
    }
    
  }
  
  idx2keep <- intersect(x = which(tolower(mm[, 1])%in%human_genes), 
                        y = which(tolower(mm[, 2])%in%human_genes))
  
  if(length(idx2keep) == 0){
    ppi <- t(as.matrix(c(NA, NA)))
  } else {
    ppi <- mm[idx2keep, ]
  }
  colnames(ppi) <- c("source", "target")
  ppi <- as.data.frame(ppi)
  
  idx2rem <- which(duplicated(paste0(tolower(ppi$source), "=", tolower(ppi$target))))
  
  if(length(idx2rem) > 0){ppi <- ppi[-idx2rem, ]}
  
  pp1 <- paste0(tolower(ppi$source), "=", tolower(ppi$target))
  pp2 <- paste0(tolower(ppi$target), "=", tolower(ppi$source))
  pp <- intersect(x = pp1, y = pp2)
  
  idx2rem <- which(pp2 %in% pp)
  
  if(length(idx2rem) > 0){ppi <- ppi[-idx2rem, ]}
  
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
  
  
}


#### Step 2
ctrl_ind <- 2
for(ll in 1:2){
  
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
  
  ind <- which(mm[, 1] %in% map_table[, 1])
  if(length(ind) > 0){
    
    for(jj in 1:length(ind)){
      
      idx <- which(map_table[, 1] == mm[ind[jj], 1])
      mm[ind[jj], 1] <- map_table[idx, 2]
      
    }
    
  }
  
  ind <- which(mm[, 2] %in% map_table[, 1])
  if(length(ind) > 0){
    
    for(jj in 1:length(ind)){
      
      idx <- which(map_table[, 1] == mm[ind[jj], 2])
      mm[ind[jj], 2] <- map_table[idx, 2]
      
    }
    
  }
  
  idx2keep <- intersect(x = which(tolower(mm[, 1])%in%human_genes), 
                        y = which(tolower(mm[, 2])%in%human_genes))
  
  if(length(idx2keep) == 0){
    ppi <- t(as.matrix(c(NA, NA)))
  } else {
    ppi <- mm[idx2keep, ]
  }
  colnames(ppi) <- c("source", "target")
  ppi <- as.data.frame(ppi)
  
  idx2rem <- which(duplicated(paste0(tolower(ppi$source), "=", tolower(ppi$target))))
  
  if(length(idx2rem) > 0){ppi <- ppi[-idx2rem, ]}
  
  pp1 <- paste0(tolower(ppi$source), "=", tolower(ppi$target))
  pp2 <- paste0(tolower(ppi$target), "=", tolower(ppi$source))
  pp <- intersect(x = pp1, y = pp2)
  
  idx2rem <- which(pp2 %in% pp)
  
  if(length(idx2rem) > 0){ppi <- ppi[-idx2rem, ]}
  
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
  
  
}


#### Step 3
ctrl_ind <- 3
for(ll in 1:2){
  
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
  
  ind <- which(mm[, 1] %in% map_table[, 1])
  if(length(ind) > 0){
    
    for(jj in 1:length(ind)){
      
      idx <- which(map_table[, 1] == mm[ind[jj], 1])
      mm[ind[jj], 1] <- map_table[idx, 2]
      
    }
    
  }
  
  ind <- which(mm[, 2] %in% map_table[, 1])
  if(length(ind) > 0){
    
    for(jj in 1:length(ind)){
      
      idx <- which(map_table[, 1] == mm[ind[jj], 2])
      mm[ind[jj], 2] <- map_table[idx, 2]
      
    }
    
  }
  
  idx2keep <- intersect(x = which(tolower(mm[, 1])%in%human_genes), 
                        y = which(tolower(mm[, 2])%in%human_genes))
  
  if(length(idx2keep) == 0){
    ppi <- t(as.matrix(c(NA, NA)))
  } else {
    ppi <- mm[idx2keep, ]
  }
  colnames(ppi) <- c("source", "target")
  ppi <- as.data.frame(ppi)
  
  idx2rem <- which(duplicated(paste0(tolower(ppi$source), "=", tolower(ppi$target))))
  
  if(length(idx2rem) > 0){ppi <- ppi[-idx2rem, ]}
  
  pp1 <- paste0(tolower(ppi$source), "=", tolower(ppi$target))
  pp2 <- paste0(tolower(ppi$target), "=", tolower(ppi$source))
  pp <- intersect(x = pp1, y = pp2)
  
  idx2rem <- which(pp2 %in% pp)
  
  if(length(idx2rem) > 0){ppi <- ppi[-idx2rem, ]}
  
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
  
  
}

## ChatGPT - Step 1
class_i_halucinations <- 0
class_ii_halucinations <- 0
correct_predictions <- length(intersect(x = unique(tolower(unlist(ppi_manual))), 
                                        y = unique(tolower(unlist(ppi_chatgpt1)))))
other_predictions <- length(setdiff(x = unique(tolower(unlist(ppi_chatgpt1))), 
                                    y = unique(tolower(unlist(ppi_manual)))))
plot_df_list[[length(plot_df_list)+1]] <- c(class_i_halucinations, class_ii_halucinations, other_predictions, correct_predictions)


## ChatGPT - Step 2
class_i_halucinations <- 0
class_ii_halucinations <- 0
correct_predictions <- length(intersect(x = unique(tolower(unlist(ppi_manual))), 
                                        y = unique(tolower(unlist(ppi_chatgpt2)))))
other_predictions <- length(setdiff(x = unique(tolower(unlist(ppi_chatgpt2))), 
                                    y = unique(tolower(unlist(ppi_manual)))))
plot_df_list[[length(plot_df_list)+1]] <- c(class_i_halucinations, class_ii_halucinations, other_predictions, correct_predictions)



## ChatGPT - Step 3
class_i_halucinations <- 0
class_ii_halucinations <- 0
correct_predictions <- length(intersect(x = unique(tolower(unlist(ppi_manual))), 
                                        y = unique(tolower(unlist(ppi_chatgpt3)))))
other_predictions <- length(setdiff(x = unique(tolower(unlist(ppi_chatgpt3))), 
                                    y = unique(tolower(unlist(ppi_manual)))))
plot_df_list[[length(plot_df_list)+1]] <- c(class_i_halucinations, class_ii_halucinations, other_predictions, correct_predictions)

names(plot_df_list) <- c(nn, paste0("ChatGPT_Style1_Step", 1:3))
names(plot_df_list) <- gsub(pattern = "_Between", replacement = "", x = names(plot_df_list), fixed = TRUE)

df <- matrix(data = , nrow = length(plot_df_list)*2, ncol = 4)
cnt <- 1
colnames(df) <- c("Cnt", "Step", "Model", "Type")
for(ii in 1:length(plot_df_list)){
  
  df[cnt, 1] <- plot_df_list[[ii]][3]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3]
  df[cnt, 3] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1]
  df[cnt, 4] <- "inaccurate_predictions"
  
  cnt <- cnt + 1
  
  df[cnt, 1] <- plot_df_list[[ii]][4]
  df[cnt, 2] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][3]
  df[cnt, 3] <- strsplit(x = names(plot_df_list)[ii], split = "_", fixed = TRUE)[[1]][1]
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

df$Model <- factor(x = df$Model, levels = c("ChatGPT", "Llama70b", "Llama405b"))


pdf(file = "output/model_predictions_ppi.pdf", width = 20, height = 10)
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

write.table(x = df, file = "output/model_predictions_ppi.txt", quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)



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
  
  manual_relations <- unique(tolower(unlist(ppi_manual)))
  model_relations <- unique(tolower(ppi_genes_list[[ii]]))
  
  if(ii == 1){
    
    metrics_df <- calculate_metrics(manual_list = manual_relations, model_list = model_relations)
    
  } else {
    
    metrics_df <- rbind(metrics_df, calculate_metrics(manual_list = manual_relations, model_list = model_relations))
    
  }
  
}

model_relations <- unique(tolower(unlist(ppi_chatgpt1)))
metrics_df <- rbind(metrics_df, calculate_metrics(manual_list = manual_relations, model_list = model_relations))
model_relations <- unique(tolower(unlist(ppi_chatgpt2)))
metrics_df <- rbind(metrics_df, calculate_metrics(manual_list = manual_relations, model_list = model_relations))
model_relations <- unique(tolower(unlist(ppi_chatgpt3)))
metrics_df <- rbind(metrics_df, calculate_metrics(manual_list = manual_relations, model_list = model_relations))

metrics_df$Type <- c(gsub(pattern = "_Between_", replacement = "_", x = nn, fixed = TRUE),
                     paste0("ChatGPT_Style1_Step", 1:3))

metrics_long <- melt(metrics_df, id.vars = "Type", 
                     measure.vars = c("precision", "recall", "f1_score"), 
                     variable.name = "Metric", value.name = "Score")

colnames(metrics_long)[colnames(metrics_long) == "value"] <- "Score"

metrics_long$Step <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 3)
metrics_long$Model <- sapply(strsplit(x = metrics_long$Type, split = "_", fixed = TRUE), "[", 1)

metrics_long$Model <- factor(x = metrics_long$Model, levels = c("ChatGPT", "Llama70b", "Llama405b"))

pdf(file = "output/precision_recall_ppi.pdf", width = 12, height = 10)
ggplot(metrics_long, aes(x = Step, y = Score, fill = variable, group = interaction(Model, variable))) +
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

write.table(x = metrics_long, file = "output/precision_recall_ppi.txt", quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)
