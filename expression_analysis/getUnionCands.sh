#!/bin/bash

cat mlRF88IDs_secreted_genes/ml_sp_B_lac-SF5gene-models.protei.fasta  lsg_secreted_genes/lsgIDs_sp_B_lac-SF5gene-models.protein.fasta rxlr_eer_secreted_genes/rxlr_eer_cleaved_sp_B_lac-SF5gene-models.protein.fasta  wy_secreted_genes/wy_cleaved_sp_B_lac-SF5gene-models.protein.fasta  | sort | uniq | wc -l > LSG_u_ML_u_RXLREER_u_WY_SF5_genemodels.fasta
