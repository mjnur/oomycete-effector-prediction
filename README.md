## EffectorO

If you have any questions or trouble running this, please email authors at **mjnur@ucdavis.edu** or **kjwood@ucdavis.edu**

### Predicting oomycete effector genes using lineage-specificity and machine learning classifiers

Please see our [EffectorO bioRxiv preprint](https://www.biorxiv.org/content/10.1101/2021.03.19.436227v1) for more details! And see our [EffectorO-ML web server](https://effectoro.herokuapp.com) that is available.

### Data used
- For secretomes, EffectorO-ML hits, EffectorO-LSP hits, WY domain-containing proteins and RXLR-EER domain-containing proteins from the 28 genomes Oomycete genomes, see the **EffectorO_genome_Results** directory.
- For the original ORF files used, see this google drive link: https://drive.google.com/drive/folders/1iFH0nOd__SOluOQa4eRSVNCE0kEhQLu-?usp=sharing

### How to get machine-learning predicted effectors from an oomycete fasta file (works best on secreted proteins):

#### Using the EffectorO-ML web server:
1) Navigate to https://effectoro.herokuapp.com
2) Upload the FASTA file of our choice, of predicted amino acid sequences
3) See your results in the data table! Can sort each column by clicking the arrows, and can search for sequences by the ID

#### Using the EffectorO-ML command-line tool:

1) make sure python3 is downloaded
  ```bash
  python3 --version
  ```
2) git clone this repository, then make sure all packages are downloaded
  ```bash
  python3 -m pip install --user -r requirements.txt
  ```
3) cd into scripts directory to run ML prediction pipeline
  ```python
   cd machine_learning_classification/scripts
  ```
4) run this on command line:

```python
python3 predict_effectors.py YOUR_INPUT_FASTA_PATH
```

- output:
  - csv of IDs|class_prediction|meaning|probability_of_prediction
  - fasta file of predicted effectors
