library(readr)
library(readxl)
library(dplyr)
library(ggplot2)
library(biomaRt)
library(jsonlite)
library(parallel)

ppi_relation_types <- "Complex Formation, Catalysis Of Posttranslational Modification, Catalysis Of Ubiquitination, Catalysis Of Methylation, Catalysis Of Deacetylation, Catalysis Of Phosphorylation, Catalysis Of Dephosphorylation, Catalysis Of Acetylation, Catalysis Of Glycosylation, Catalysis Of Acylation, Catalysis Of Deneddylation, Catalysis Of Small Protein Conjugation, Catalysis Of Sumoylation, Catalysis Of Other Small Molecule Conjugation Or Removal, Catalysis Of Demethylation, Other Catalysis Of Small Molecule Conjugation, Catalysis Of Adp-Ribosylation, Catalysis Of Palmitoylation, Catalysis Of Neddylation, Catalysis Of Phosphoryl Group Conjugation Or Removal, Catalysis Of Deubiquitination, Catalysis Of Small Protein Conjugation Or Removal, Other Catalysis Of Small Protein Conjugation, Other Catalysis Of Small Protein Removal, Catalysis Of Geranylgeranylation, Catalysis Of Farnesylation, Catalysis Of Lipidation, Catalysis Of Prenylation, Catalysis Of Small Protein Removal, Catalysis Of Deglycosylation, Catalysis Of Desumoylation, Catalysis Of Depalmitoylation, Catalysis Of Deacylation, Catalysis Of Small Molecule Removal, Other Catalysis Of Small Molecule Removal"
ppi_relation_types <- tolower(x = unique(unlist(x = strsplit(x = ppi_relation_types, split = ", ", fixed = TRUE))))

annotated_ppi_relations <- matrix(data = , nrow = 1, ncol = 2)

## Take care of test
ff <- list.files(path = "path/to/regulatome/zenodo/resource/obj/test/")
ff_txt <- ff[which(grepl(pattern = ".txt", x = ff, fixed = TRUE))]
ff_ann <- ff[which(grepl(pattern = ".ann", x = ff, fixed = TRUE))]
ids <- sapply(strsplit(x = ff_ann, split = ".", fixed = TRUE), "[", 1)

for(ii in 1:length(ids)){
  
  print(paste0("Step ---- ", ii, "/", length(ids)))
  
  curr_annot <- read.delim(file = paste0("path/to/regulatome/zenodo/resource/obj/test/", ff_ann[ii]), header = FALSE)
  relations <- curr_annot$V2[intersect(x = which(grepl(pattern = "Arg", x = curr_annot$V2, fixed = TRUE)), 
                                       y = which(grepl(pattern = "R", x = curr_annot$V1, fixed = TRUE)))]
  
  if(length(relations) > 0){
    
    mm <- matrix(data = , nrow = length(relations), ncol = 3)
    for(jj in 1:length(relations)){
      
      curr <- relations[jj]
      reac <- strsplit(x = curr, split = " ", fixed = TRUE)[[1]][1]
      ss <- strsplit(x = strsplit(x = curr, split = " ", fixed = TRUE)[[1]][2], split = ":", fixed = TRUE)[[1]][2]
      tt <- strsplit(x = strsplit(x = curr, split = " ", fixed = TRUE)[[1]][3], split = ":", fixed = TRUE)[[1]][2]
      
      mm[jj, ] <- c(curr_annot$V3[which(curr_annot$V1 == ss)],
                    curr_annot$V3[which(curr_annot$V1 == tt)],
                    reac)
      
    }
    
    ind <- which(tolower(gsub(pattern = "_", replacement = " ", x = mm[, 3], fixed = TRUE)) %in% ppi_relation_types)
    if(length(ind) > 0){
      
      mm <- mm[ind, ]
      if(length(ind) == 1){
        mm <- t(as.matrix(mm))
      }
      
      tobind <- matrix(data = , nrow = 1, ncol = 2)
      tobind[1, ] <- c(ids[ii], paste0(mm[, 1], "=", mm[, 2], collapse = "; "))
      annotated_ppi_relations <- unique(rbind(annotated_ppi_relations, tobind))
      
    }
    
  }
  
}



## Take care of train
ff <- list.files(path = "path/to/regulatome/zenodo/resource/obj/train/")
ff_txt <- ff[which(grepl(pattern = ".txt", x = ff, fixed = TRUE))]
ff_ann <- ff[which(grepl(pattern = ".ann", x = ff, fixed = TRUE))]
ids <- sapply(strsplit(x = ff_ann, split = ".", fixed = TRUE), "[", 1)

for(ii in 1:length(ids)){
  
  print(paste0("Step ---- ", ii, "/", length(ids)))
  
  curr_annot <- read.delim(file = paste0("path/to/regulatome/zenodo/resource/obj/train/", ff_ann[ii]), header = FALSE)
  relations <- curr_annot$V2[intersect(x = which(grepl(pattern = "Arg", x = curr_annot$V2, fixed = TRUE)), 
                                       y = which(grepl(pattern = "R", x = curr_annot$V1, fixed = TRUE)))]
  
  if(length(relations) > 0){
    
    mm <- matrix(data = , nrow = length(relations), ncol = 3)
    for(jj in 1:length(relations)){
      
      curr <- relations[jj]
      reac <- strsplit(x = curr, split = " ", fixed = TRUE)[[1]][1]
      ss <- strsplit(x = strsplit(x = curr, split = " ", fixed = TRUE)[[1]][2], split = ":", fixed = TRUE)[[1]][2]
      tt <- strsplit(x = strsplit(x = curr, split = " ", fixed = TRUE)[[1]][3], split = ":", fixed = TRUE)[[1]][2]
      
      mm[jj, ] <- c(curr_annot$V3[which(curr_annot$V1 == ss)],
                    curr_annot$V3[which(curr_annot$V1 == tt)],
                    reac)
      
    }
    
    ind <- which(tolower(gsub(pattern = "_", replacement = " ", x = mm[, 3], fixed = TRUE)) %in% ppi_relation_types)
    if(length(ind) > 0){
      
      mm <- mm[ind, ]
      if(length(ind) == 1){
        mm <- t(as.matrix(mm))
      }
      
      tobind <- matrix(data = , nrow = 1, ncol = 2)
      tobind[1, ] <- c(ids[ii], paste0(mm[, 1], "=", mm[, 2], collapse = "; "))
      annotated_ppi_relations <- unique(rbind(annotated_ppi_relations, tobind))
      
    }
    
  }
  
}



## Take care of devel
ff <- list.files(path = "path/to/regulatome/zenodo/resource/obj/devel/")
ff_txt <- ff[which(grepl(pattern = ".txt", x = ff, fixed = TRUE))]
ff_ann <- ff[which(grepl(pattern = ".ann", x = ff, fixed = TRUE))]
ids <- sapply(strsplit(x = ff_ann, split = ".", fixed = TRUE), "[", 1)

for(ii in 1:length(ids)){
  
  print(paste0("Step ---- ", ii, "/", length(ids)))
  
  curr_annot <- read.delim(file = paste0("path/to/regulatome/zenodo/resource/obj/devel/", ff_ann[ii]), header = FALSE)
  relations <- curr_annot$V2[intersect(x = which(grepl(pattern = "Arg", x = curr_annot$V2, fixed = TRUE)), 
                                       y = which(grepl(pattern = "R", x = curr_annot$V1, fixed = TRUE)))]
  
  if(length(relations) > 0){
    
    mm <- matrix(data = , nrow = length(relations), ncol = 3)
    for(jj in 1:length(relations)){
      
      curr <- relations[jj]
      reac <- strsplit(x = curr, split = " ", fixed = TRUE)[[1]][1]
      ss <- strsplit(x = strsplit(x = curr, split = " ", fixed = TRUE)[[1]][2], split = ":", fixed = TRUE)[[1]][2]
      tt <- strsplit(x = strsplit(x = curr, split = " ", fixed = TRUE)[[1]][3], split = ":", fixed = TRUE)[[1]][2]
      
      mm[jj, ] <- c(curr_annot$V3[which(curr_annot$V1 == ss)],
                    curr_annot$V3[which(curr_annot$V1 == tt)],
                    reac)
      
    }
    
    ind <- which(tolower(gsub(pattern = "_", replacement = " ", x = mm[, 3], fixed = TRUE)) %in% ppi_relation_types)
    if(length(ind) > 0){
      
      mm <- mm[ind, ]
      if(length(ind) == 1){
        mm <- t(as.matrix(mm))
      }
      
      tobind <- matrix(data = , nrow = 1, ncol = 2)
      tobind[1, ] <- c(ids[ii], paste0(mm[, 1], "=", mm[, 2], collapse = "; "))
      annotated_ppi_relations <- unique(rbind(annotated_ppi_relations, tobind))
      
    }
    
  }
  
}

annotated_ppi_relations <- annotated_ppi_relations[2:nrow(annotated_ppi_relations), ]
colnames(annotated_ppi_relations) <- c("reference", "ppi_relations")



write.table(x = annotated_ppi_relations, file = "../src/regulatome_corpus/annotated_ppi_relations.txt", quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)
