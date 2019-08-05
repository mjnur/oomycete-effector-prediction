## oomycete-effector-prediction

### Predicting oomycete effector genes using lineage-specificity and machine learning classifiers

Please see our [2019 UC Davis URC poster](https://drive.google.com/file/d/1n7ccBZi6c5K6h600u0lF9xnMRiMtKWVa/view?usp=sharing) for a high-level description of this research.


how to get predicted effectors from an oomycete, secreted fasta file:

1) make sure python3.6 is downloaded 
2) make sure all packages are downloaded
3) git clone this repository, cd into scripts directory
4) run this on command line:

```python
python3.6 predict_effectors.py YOUR_INPUT_FASTA_PATH
```

- output:
  - csv of IDs|class_prediction|meaning|probability_of_prediction
  - fasta file of predicted effectors
