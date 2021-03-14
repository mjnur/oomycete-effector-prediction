#!/bin/bash

gene_ids=$1
gff=$2

while IFS= read -r ID 
do
	scaffold=`grep $ID $gff | awk '{print $1}' | uniq`
	locus_tag=`grep $ID $gff | awk -F 'locus_tag=' '{print $2}' | cut -f1 -d ';' | uniq`
	begin=`grep $locus_tag $gff | awk '$3 == "gene" {print $4}'`
	end=`grep $locus_tag $gff | awk '$3 == "gene" {print $5}'`

	#output BED format
	echo -e "$scaffold\t$begin\t$end\t$locus_tag"

done < $gene_ids
