## R script to obtain lsg sequences (ids)

## takes in:
##    1) blast tabular output file
##        - in this case, secreted B.lactucae genes vs. other oomycetes blastp results
##
##    2) fasta protein sequence of desired genome
##
## returns:
##    both LSG and noonLSG text files of sequence ids
##
## ------------------------------------------------------------------------------------------------


# download seqinr package if don't already have it
if(!require(seqinr)){
  install.packages("seqinr")
  library(seqinr)
}

setwd("/Users/munir/Desktop/oomycete-effector-prediction/lineage_specificity_analysis")

# blast tabular output
blast_results <- read.table("bremia_vs_all_blast_results_20190330.tab", sep="\t", stringsAsFactors=F)

# rename columns
names(blast_results) <- c("qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore","qcovs")


## looking at lineage specificity:

# sort each query sequence (in B.lactucae secretome) by bit score (blast quality metric)
sorted_by_bitscore <- blast_results[ order(blast_results['qseqid'], blast_results['bitscore'], decreasing=T), ]

# obtain best blast hit for each query sequence in B.lactucae secretome
best_hit <- sorted_by_bitscore[ !duplicated(sorted_by_bitscore$qseqid), ]

# add in additional constraints, so low quality hits aren't kept
# currently using these cutoffs (based on papers, but are very flexible):
#     e-value: 1e-7
#     & qcovs (query sequence coverage percentage): > 30%
#     & pident (percent identity match): > 40%
nonLSGs <- subset(best_hit, evalue<0.0000001 & qcovs>30 & pident>40)
  

# read in full secretome, get LSG and nonLSG sequences:
b_lac <- read.fasta("secreted_B_lac.protein.fasta")

# get fasta ids of nonLSGs 
nonLSG_ids <- nonLSGs['qseqid']

# now get the fasta sequences for both groups
'%ni%' <- Negate('%in%')
nonLSG_seqs <- b_lac[c(which(nonLSG_ids$qseqid %in% names(b_lac)))]
LSG_seqs <- b_lac[c(which(names(b_lac) %ni% nonLSG_ids$qseqid))]

# write files
write.table(nonLSGs['qseqid'], file="20190404_nonLSGs.txt", row.names = F, col.names = F, quote = F)

write.fasta(LSG_seqs, names=names(LSG_seqs), file.out="fasta/20190731_2675_blac_LSG_sequences.fasta")
write.fasta(nonLSG_seqs, names=names(nonLSG_seqs), file.out="fasta/20190731_nonLSG_sequences.fasta")