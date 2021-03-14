#!/bin/bash

#SBATCH -c 1  ## number of cores
#SBATCH -B 1  ## Number of machines cores are located on (1 is optimal)
#SBATCH -J count ## Job name
#SBATCH -p production  ## partitional to submit to -- generally gc
#SBATCH --mem=1G # Memory pool required - Not currently implemented on cabernet
#SBATCH --time=1-0 # day-hours:min:sec   min:sec
#SBATCH --mail-type=END,FAIL # Tpe of email notification to recieve
#SBATCH --output=slurm-CGSF5_sort_and_index-%x.%j.out
#SBATCH --mail-user=mjnur@ucdavis.edu # email to which notifications will be sent

#bam_input="/share/rwmwork/fletcher/OutLinks/Kelsey/RNAmap/AllRNAseq.CG_SF5.Tcourse.bam"
#bam_input="/share/rwmwork/rjugil/RNAseq/2019/re-map/Combined-ref/STARout/merged-bams/sf5/CG_SF5-All.bam"


bed_input="bed/sp_GCA_004359215.1_BlacSF5_genomic_ORFs.bed"
sorted_bam_output="bam/sorted-CG_SF5-All.bam"
read_count_output="output/sp_GCA_004359215.1_BlacSF5_genomic_ORFs_readcounts.txt"

#sort
#echo "sorting, current time: $(date)"
#/share/rwmwork/fletcher/programs/samtools-1.3.1/samtools sort -@ 1 -m 1G  -o $sorted_bam_output $bam_input

#index
#echo "indexing, current time: $(date)"
#/share/rwmwork/fletcher/programs/samtools-1.3.1/samtools index $sorted_bam_output

#get readcounts
echo "get readcounts, current time: $(date)"
/share/rwmwork/fletcher/programs/bedtools2/bin/bedtools multicov -bams $sorted_bam_output -bed $bed_input > $read_count_output

echo "finished readcounts, current time: $(date)"
