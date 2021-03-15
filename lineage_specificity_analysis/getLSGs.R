## R script to obtain lsg sequences (ids)

## takes in:
##    1) blast tabular output file path
##        - in this case, secreted B.lactucae genes vs. other oomycetes blastp results
##
##    2) fasta protein sequence of desired genome path
##
## prints:
##    LSG sequences
##
## ------------------------------------------------------------------------------------------------


# download seqinr package if don't already have it
if(!require(seqinr)){
  install.packages("seqinr")
  library(seqinr)
}

args<-commandArgs(TRUE)

# blast tabular outpu
cat(paste("species: ", args[2]),'\n')
blast_results <- read.table(args[1], sep="\t", stringsAsFactors=F)
# rename columns

names(blast_results) <- c("qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore","qcovs")

# if species is Peronospora, remove effusa/schachtii hits:
if (grepl("Per_", args[2])) {
	cat(paste(args[2], "contains Per_, removing rows ~"),'\n')

	# get inital num rows
	cat(paste("rows without removal: ", nrow(blast_results)),'\n')

	# remove effusa hits
	blast_results = blast_results[!grepl("Peff", blast_results$sseqid), ]
	cat(paste("rows - effusa: ", nrow(blast_results)),'\n')

	# remove schachtii hits
	blast_results = blast_results[!grepl("schachtii", blast_results$sseqid), ]
	cat(paste("rows - schachtii: ", nrow(blast_results)),'\n')
}

# if species is Peronosclerospora, remove Pmay/Pphil/Psac/Psor hits:
if (grepl("Perscl", args[2])) {
	cat(paste(args[2], "contains Perscl, removing rows ~"),'\n')

	# get inital num rows
	cat(paste("rows without removal: ", nrow(blast_results)),'\n')

	# remove Pmay hits
	blast_results = blast_results[!grepl("Pmay", blast_results$sseqid), ]
	cat(paste("rows - effusa: ", nrow(blast_results)),'\n')

	# remove Pphil hits
	blast_results = blast_results[!grepl("Pphil", blast_results$sseqid), ]
	cat(paste("rows - phil: ", nrow(blast_results)),'\n')

	# remove Psac hits
	blast_results = blast_results[!grepl("Psac", blast_results$sseqid), ]
	cat(paste("rows - sac: ", nrow(blast_results)),'\n')

	# remove Psor hits
	blast_results = blast_results[!grepl("Psor", blast_results$sseqid), ]
	cat(paste("rows - sor: ", nrow(blast_results)),'\n')
}

# read in full secretome, to get LSG and nonLSG sequences:
in_genome <- read.fasta(args[2])

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
#nonLSGs <- subset(best_hit, evalue<0.0000001 & qcovs>30 & pident>40)
nonLSGs <- subset(best_hit, evalue<0.0000001 & qcovs>30 & pident>30)
# get fasta ids of nonLSGs 
nonLSG_ids <- nonLSGs['qseqid']

# now get the fasta sequences for both groups
'%ni%' <- Negate('%in%')
nonLSG_seqs <- in_genome[c(which(nonLSG_ids$qseqid %in% names(in_genome)))]
LSG_seqs <- in_genome[c(which(names(in_genome) %ni% nonLSG_ids$qseqid))]

# write files
#write.table(nonLSGs['qseqid'], file="20190404_nonLSGs.txt", row.names = F, col.names = F, quote = F)
#write.fasta(LSG_seqs, names=names(LSG_seqs), nbchar=9999999,
            #file.out=args[3])
write(names(LSG_seqs), file=args[3])
