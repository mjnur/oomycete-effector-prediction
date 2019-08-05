## oomycete-effector-prediction

### Predicting oomycete effector genes using lineage-specificity and machine learning classifiers

Please see our [2019 UC Davis URC poster](https://drive.google.com/file/d/1n7ccBZi6c5K6h600u0lF9xnMRiMtKWVa/view?usp=sharing) for a high-level description of this research.


how to get predicted effectors from an oomycete, secreted fasta file:
(using Random Forest classifier and 6 amino acid features):

1) make sure python3 is downloaded 
  ```bash
  python3 --version
  ```
2) make sure all packages are downloaded
  ```bash
  pip3 install --user -r requirements.txt
  ```
3) git clone this repository, cd into scripts directory
4) run this on command line:

```python
python3 predict_effectors.py YOUR_INPUT_FASTA_PATH
```

- output:
  - csv of IDs|class_prediction|meaning|probability_of_prediction
  - fasta file of predicted effectors
