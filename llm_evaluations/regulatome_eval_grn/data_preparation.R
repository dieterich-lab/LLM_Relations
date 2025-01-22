library(readr)
library(jsonlite)
library(XML)
library(stringr)

dir.create("src")
dir.create("src/corpus")
dir.create("src/relations")
dir.create("src/entities")
dir.create("src/entities_mapped")
dir.create("src/entities_relations")
dir.create("src/corpus_mapped")

## Retreiving and standardizing Ensembl gene names
gene_names <- read_csv("obj/gene_names.csv")
gene_names$external_gene_name <- tolower(gsub(pattern = " ", replacement = "", x = gene_names$external_gene_name))
gene_names$external_synonym <- tolower(gsub(pattern = " ", replacement = "", x = gene_names$external_synonym))
gene_names$description <- tolower(gsub(pattern = " ", replacement = "", x = gene_names$description))

#### The RegulaTome courpus can be downloaded from Zenodo: https://zenodo.org/records/10808330
#### It is in the obj/ directory that you should first store the RegulaTome corpus for this script to run.
#### The corpus consists of the annotation + scientific text .txt files divided in
#### 'test', 'train' and 'devel' categories. All three groups of data have been processed
#### and used to extract relations as well as entities.


## Take care of test
ff <- list.files(path = "obj/test/")
ff_txt <- ff[which(grepl(pattern = ".txt", x = ff, fixed = TRUE))]
ff_ann <- ff[which(grepl(pattern = ".ann", x = ff, fixed = TRUE))]
ids <- sapply(strsplit(x = ff_ann, split = ".", fixed = TRUE), "[", 1)

annotated_relations_1 <- matrix(data = , nrow = 1, ncol = 3)
for(ii in 1:length(ids)){
  
  print(paste0("Step ---- ", ii, "/", length(ids)))
  
  curr_annot <- read.delim(file = paste0("obj/test/", ff_ann[ii]), header = FALSE)
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
    
    annotated_relations_1 <- rbind(annotated_relations_1, mm)
    
    system(paste0("cp -a obj/test/", 
                  ff_txt[ii],
                  " src/corpus"))
    
    entities <- unique(curr_annot$V3[which(curr_annot$V1 %in% paste0("T", 1:10000))])
    
    write.table(x = as.matrix(entities), file = paste0("src/entities/", ids[ii], ".txt"), 
                quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
    
    entities_mapped <- c()
    for(kk in 1:length(entities)){
      ind <- which(gene_names$external_gene_name == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
      ind <- which(gene_names$external_synonym == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
      ind <- which(gene_names$description == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
    }
    
    if(length(entities_mapped) > 0){
      write.table(x = as.matrix(entities_mapped), file = paste0("src/entities_mapped/", ids[ii], ".txt"), 
                  quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
      
      system(paste0("cp -a obj/test/", 
                    ff_txt[ii],
                    " src/corpus_mapped"))
      
    }
    
    entities_relations <- unique(c(mm[, 1], mm[, 2]))
    
    write.table(x = as.matrix(entities_relations), file = paste0("src/entities_relations/", ids[ii], ".txt"), 
                quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
    
  }
  
}


## Take care of train
ff <- list.files(path = "obj/train/")
ff_txt <- ff[which(grepl(pattern = ".txt", x = ff, fixed = TRUE))]
ff_ann <- ff[which(grepl(pattern = ".ann", x = ff, fixed = TRUE))]
ids <- sapply(strsplit(x = ff_ann, split = ".", fixed = TRUE), "[", 1)

annotated_relations_2 <- matrix(data = , nrow = 1, ncol = 3)
for(ii in 1:length(ids)){
  
  print(paste0("Step ---- ", ii, "/", length(ids)))
  
  curr_annot <- read.delim(file = paste0("obj/train/", ff_ann[ii]), header = FALSE)
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
    
    annotated_relations_2 <- rbind(annotated_relations_2, mm)
    
    system(paste0("cp -a obj/train/", 
                  ff_txt[ii],
                  " src/corpus"))
    
    entities <- unique(curr_annot$V3[which(curr_annot$V1 %in% paste0("T", 1:10000))])
    
    write.table(x = as.matrix(entities), file = paste0("src/entities/", ids[ii], ".txt"), 
                quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
    
    entities_mapped <- c()
    for(kk in 1:length(entities)){
      ind <- which(gene_names$external_gene_name == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
      ind <- which(gene_names$external_synonym == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
      ind <- which(gene_names$description == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
    }
    
    if(length(entities_mapped) > 0){
      write.table(x = as.matrix(entities_mapped), file = paste0("src/entities_mapped/", ids[ii], ".txt"), 
                  quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
      
      system(paste0("cp -a obj/train/", 
                    ff_txt[ii],
                    " src/corpus_mapped"))
      
    }
    
    entities_relations <- unique(c(mm[, 1], mm[, 2]))
    
    write.table(x = as.matrix(entities_relations), file = paste0("src/entities_relations/", ids[ii], ".txt"), 
                quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
    
  }
  
}



## Take care of devel
ff <- list.files(path = "obj/devel/")
ff_txt <- ff[which(grepl(pattern = ".txt", x = ff, fixed = TRUE))]
ff_ann <- ff[which(grepl(pattern = ".ann", x = ff, fixed = TRUE))]
ids <- sapply(strsplit(x = ff_ann, split = ".", fixed = TRUE), "[", 1)

annotated_relations_3 <- matrix(data = , nrow = 1, ncol = 3)
for(ii in 1:length(ids)){
  
  print(paste0("Step ---- ", ii, "/", length(ids)))
  
  curr_annot <- read.delim(file = paste0("obj/devel/", ff_ann[ii]), header = FALSE)
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
    
    annotated_relations_3 <- rbind(annotated_relations_3, mm)
    
    system(paste0("cp -a obj/devel/", 
                  ff_txt[ii],
                  " src/corpus"))
    
    entities <- unique(curr_annot$V3[which(curr_annot$V1 %in% paste0("T", 1:10000))])
    
    write.table(x = as.matrix(entities), file = paste0("src/entities/", ids[ii], ".txt"), 
                quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
    
    entities_mapped <- c()
    for(kk in 1:length(entities)){
      ind <- which(gene_names$external_gene_name == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
      ind <- which(gene_names$external_synonym == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
      ind <- which(gene_names$description == tolower(gsub(pattern = " ", replacement = "", x = entities[kk], fixed = TRUE)))
      if(length(ind) > 0){
        entities_mapped <- c(entities_mapped, entities[kk])
      }
    }
    
    if(length(entities_mapped) > 0){
      write.table(x = as.matrix(entities_mapped), file = paste0("src/entities_mapped/", ids[ii], ".txt"), 
                  quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
      
      system(paste0("cp -a obj/devel/", 
                    ff_txt[ii],
                    " src/corpus_mapped"))
      
    }
    
    entities_relations <- unique(c(mm[, 1], mm[, 2]))
    
    write.table(x = as.matrix(entities_relations), file = paste0("src/entities_relations/", ids[ii], ".txt"), 
                quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
    
  }
  
}

annotated_relations <- unique(rbind(annotated_relations_1, annotated_relations_2, annotated_relations_3))

annotated_relations <- unique(annotated_relations[2:nrow(annotated_relations), ])
colnames(annotated_relations) <- c("source", "target", "type")
write.table(x = annotated_relations, file = "src/all_annotated_relations.txt", 
            quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)

relation_types <- unique(annotated_relations[, 3])

ppi_relations <- c("Complex_formation", relation_types[which(grepl(pattern = "catalysis", x = tolower(relation_types), fixed = TRUE))])

tf_relations <- c("Regulation_of_translation", "Negative_regulation", "Regulation",
                  "Regulation_of_gene_expression", "Positive_regulation",
                  "Regulation_of_transcription", "Regulation_of_degradation")

annotated_ppi <- annotated_relations[which(annotated_relations[, 3] %in% ppi_relations), ]
annotated_tf <- annotated_relations[which(annotated_relations[, 3] %in% tf_relations), ]

write.table(x = annotated_ppi, file = "src/ppi_annotated_relations.txt", 
            quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)

write.table(x = annotated_tf, file = "src/tf_annotated_relations.txt", 
            quote = FALSE, sep = "\t", row.names = FALSE, col.names = TRUE)



#### read all entities
ff <- list.files(path = "src/entities/")
entities_list <- list()
for(ii in 1:length(ff)){
  
  entities <- read.delim(file = paste0("src/entities/", ff[ii]), header = FALSE)
  entities_list[[length(entities_list)+1]] <- unique(c(tolower(entities$V1)))
  
}
all_entities <- unique(c(unlist(entities_list)))
write.table(x = as.matrix(all_entities), file = "src/all_annotated_entities.txt", quote = FALSE, 
            sep = "\t", row.names = FALSE, col.names = FALSE)



#### read ppi relation entities
ff <- list.files(path = "src/entities_relations_ppi/")
entities_list <- list()
for(ii in 1:length(ff)){
  
  entities <- read.delim(file = paste0("src/entities_relations_ppi/", ff[ii]), header = FALSE)
  entities_list[[length(entities_list)+1]] <- unique(c(tolower(entities$V1)))
  
}
all_entities <- unique(c(unlist(entities_list)))
write.table(x = as.matrix(all_entities), file = "src/ppi_annotated_entities.txt", quote = FALSE, 
            sep = "\t", row.names = FALSE, col.names = FALSE)


#### read ppi relation entities
ff <- list.files(path = "src/entities_relations_tf/")
entities_list <- list()
for(ii in 1:length(ff)){
  
  entities <- read.delim(file = paste0("src/entities_relations_tf/", ff[ii]), header = FALSE)
  entities_list[[length(entities_list)+1]] <- unique(c(tolower(entities$V1)))
  
}
all_entities <- unique(c(unlist(entities_list)))
write.table(x = as.matrix(all_entities), file = "src/tf_annotated_entities.txt", quote = FALSE, 
            sep = "\t", row.names = FALSE, col.names = FALSE)
