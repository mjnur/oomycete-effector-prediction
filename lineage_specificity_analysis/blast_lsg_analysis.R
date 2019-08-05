# either choose data of all WYs, or data from sigP 4.1/5.0 secreted WYs
# the Bremia WYs were blasted against the 13 other genomes using blastp
# default e-value cutoff, but in R I only plot hits with e-value < 0.01
setwd("/Users/munir/Desktop/20190328_ml_research/LSG_extraction_20190330")
oo <- read.table("v8_secreted_WYs_vs_all.tab",sep="\t",stringsAsFactors =F)
#oo <- read.table("20190329_LSG_results.tab",sep="\t",stringsAsFactors =F)

names(oo) <- c("qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore","qcovs")

prefixes <- as.character(read.csv(pipe("cut -f1 -d' ' filename_to_prefix.txt"), header=F)$V1)
genome_names <- as.character(read.csv("genome_names.txt", header=F)$V1)

genomes <- list()
uniq_genomes <- list()

for (i in 1:length(prefixes)) {
  new_frame <- oo[grep(prefixes[i], oo$sseqid),]
  
  # sort by bitscore, arrange by query sequence in bremia (for viewing purposes)
  sorted_by_bitscore <- new_frame[ order(new_frame[,'qseqid'], new_frame[,'bitscore'], decreasing=T), ]
  
  # only keep highest bitscore for every qseqid
  # i think this should keep the highest quality of alignment,
  #   since bitscore incorporates qcovs 
  best_hit <- sorted_by_bitscore[ !duplicated(sorted_by_bitscore$qseqid), ]
  
  # add species name so we know where these hits came from
  best_hit$species <- genome_names[i]

  # append the best hit for each WY in bremia. so in total, only as many hits as #WY sequences
  genomes[[i]] <- best_hit
}

# genomes[[]] is a list of dataframes, so bind them all into one dataframe
# we have created a column for species above in the for loop, so we know what where hits came from
all_oomycetes <- do.call("rbind", genomes)

# select hits where the e-value is at least smaller than 0.01 to get rid of garbage hits
#selected_data <- subset(all_oomycetes, evalue<0.0000001 & qcovs>30 & pident>40)
selected_data <- subset(all_oomycetes, evalue<0.01)

# make boxplot for our selected data above, plots pident (sequence identity)
library("ggplot2")
ggplot(selected_data, aes(factor(species, levels=rev(unique(species))), log(bitscore)),trim=FALSE) +
  geom_boxplot(aes(fill=factor(species, levels=(unique(species))))) + 
  theme(legend.position = "none") + # removes legend
  coord_flip() + 
  xlab("Species") + 
  ggtitle("blastp data (Bremia secretome v8 ORFs query)")
  theme(axis.title.x = element_text(color="black", size=14),
        axis.title.y = element_text(color="black", size=14))

# save as PDF 6 x 8 inches

  # make boxplot to show evalue vs pident for best hits (bitscore
  my_sorted_by_bitscore <- all_oomycetes[ order(all_oomycetes[,'qseqid'], all_oomycetes[,'bitscore'], decreasing=T), ]
  my_best_hits <- my_sorted_by_bitscore[ !duplicated(my_sorted_by_bitscore$qseqid), ]
  conserved_hits <- subset(my_best_hits, evalue<0.0000001 & qcovs>30 & pident>40)

  library("ggplot2")
  pie <- ggplot(conserved_hits, aes(x = "", fill = factor(species))) + 
    geom_bar(width = 1) +
    theme(axis.line = element_blank(), 
          plot.title = element_text(hjust=0.5)) + 
    labs(fill="species", 
         x=NULL, 
         y=NULL, 
         title="species of best hit in Conserved Genes (non-LSGs)")
  pie + coord_polar(theta = "y", start=0)
    
  # save as PDF 6 x 8 inches



# 
# # sort by bitscore, arrange by query sequence in bremia (for viewing purposes)
# 
# # only keep highest bitscore for every qseqid
# # i think this should keep the highest quality of alignment,
# #   since bitscore incorporates qcovs 
  
  
#HOW TO GET LSGs:
sorted_by_bitscore <- all_oomycetes[ order(all_oomycetes[,'qseqid'], all_oomycetes[,'bitscore'], decreasing=T), ]
best_hit <- sorted_by_bitscore[ !duplicated(sorted_by_bitscore$qseqid), ]
nonLSGs<- subset(best_hit, evalue<0.0000001 & qcovs>30 & pident>40)
  
  
write.table(nonLSGs['qseqid'], file="nonLSGs_20190404.txt", row.names = F, col.names = F, quote = F)






