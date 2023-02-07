## Lineage Specificity Analysis

### Methods 
see paper for detailed methods

**Input**: Predicted secretome of a species, using SignalP

#### Obtaining Lineage Specific Proteins for a single species: 
1. construct a BLASTp query to query the species against a combined fasta file of all translated open reading frames (ORFs) of all other oomycete species (Supplemental Table 2). example `blastp` query:

```bash
blastp -db $OOMYCETE_DATABASE -query $GENOME -outfmt "6 std qcovs" -out sp_$GENOME_vs_all.tab -num_threads 4
```

2. Save output in tabular file. i.e. `sp_B_lac_vs_All.tab` would indicate a file of the tabular output from querying `B. lactucae` secreted proteins against the secretomes of all other Oomycetes you have in your database.

3. Utilize [getLSGs.R](https://github.com/mjnur/oomycete-effector-prediction/blob/master/lineage_specificity_analysis/getLSGs.R) script to output Lineage specific IDs, which uses these thresholds to identify lineage specific sequences:  
    - e-value cutoff of `<10e-7`  
    - percent identity of `>30%`  
    - query coverage of `>30%`  
