## EffectorO

If you have any questions or trouble running this, please email authors at **mjnur@ucdavis.edu** or **kjwood@ucdavis.edu**

### Predicting oomycete effector genes using lineage-specificity and machine learning classifiers

Please see our [2019 UC Davis URC poster](https://drive.google.com/file/d/1n7ccBZi6c5K6h600u0lF9xnMRiMtKWVa/view?usp=sharing) for a high-level description of this research.


### How to get predicted effectors from an oomycete fasta file (works best on secreted proteins):

#### (using pre-trained Random Forest oomycete effector classifcation model):

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
