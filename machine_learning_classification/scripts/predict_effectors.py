import numpy as np
import FEAT as FEAT
import sys, warnings
import pandas as pd
import numpy as np
import pickle
from Bio import SeqIO

## take in: 
##    1) secreted proteins fasta file
##    2) (optional) model file path (will default to best Random Forest)

## RUN LIKE THIS:
##    python3.6 predict_effectors.py {INPUT_FASTA_PATH}

## output:
##    1) csv of IDs|class_prediction|meaning|probability_of_prediction
##    2) fasta file of predicted effectors

FASTA_FILE = sys.argv[1]

if len(sys.argv) < 3:
    MODEL_FILE = "../trained_models/RF_88_best.sav"
else:
    MODEL_FILE = sys.argv[2]
    
if not sys.warnoptions:
    warnings.simplefilter("ignore")
    
trained_model = pickle.load(open(MODEL_FILE, 'rb'))
seqs_to_predict = SeqIO.parse(open(FASTA_FILE),'fasta')
prediction_map = {'0': "predicted_non-effector", '1': "predicted_effector"}

    
def main():
    # preprocessing
    seq_ids = []
    full_sequences = []
    str_sequences = []

    # generate features, retrieve fasta IDs
    for protein in seqs_to_predict:
        seq_ids.append(protein.id)
        full_sequences.append(protein.seq)
        str_sequences.append(str(protein.seq))



    seq_features = np.array([get_average_features(seq) for seq in full_sequences])

    print("Sequences to run secreted oomycete-trained Random Forest \
effector classifier on: ", len(seq_features))
    
    print("\n**NOTES**: \n\n \
            Positive training dataset: ~100 experimentally validated oomycete avirulence effectors \n \
            Negative training dataset: ~100 secreted orthologous oomycete genes \n\n\
**END OF NOTES**\n")
          

    # get predicted output
    predictions = trained_model.predict(seq_features)
    probabilities = trained_model.predict_proba(seq_features)
    meanings = np.array([prediction_map[pred] for pred in predictions])


    resultDF = pd.DataFrame({"proteinID": seq_ids,
                             "sequence": str_sequences,
                             "prediction": predictions, 
                             "probability": probabilities[:,1], 
                             "meaning": meanings})
    
    # round probabilities
    resultDF['probability'] = np.round(resultDF['probability'], 2)

    print("\nCounts of predicted classes: ")
    print(resultDF['meaning'].value_counts())
    
    # write table and predicted effectors to CSV
    resultDF.to_csv("effector_classification_table.csv")
    
    # write effectors
    outfile = open("predicted_effectors.fasta", 'w')
    effectors = resultDF[resultDF['meaning'] == "predicted_effector"]

    ids_to_write = effectors["proteinID"] + ' ' \
                    + effectors["meaning"] + ' ' \
                    + "probability=" \
                    + effectors["probability"].astype(str)
    
    ids_to_write = ids_to_write.tolist()
    effector_seqs = effectors['sequence'].tolist()
    
    for idx, cur_id in enumerate(ids_to_write):
        if idx != 0: outfile.write("\n")
        outfile.write(">" + cur_id + " \n")
        outfile.write(effector_seqs[idx])
        
    print("\nOutput fasta of predicted effectors available in: \n \
            predicted_effectors.fasta\n")
    print("Detailed CSV with fasta IDs | sequences | predictions | probabilities in: \n \
            effector_classification_table.csv\n")
        
def get_average_features(sequence, df=0, protID=0):
    '''
    Method: Fills feature columns in df with net averages
    Input: 
        - df: dataframe
        - protID: sequence identifier
        - sequence: amino acid string
    '''
    res = []
    gravy = hydrophobicity = exposed = disorder = bulkiness = interface = 0.0
    
    ## get NET cumulative sums
    #print("calculating for", sequence)
    length = min(len(sequence), 900)
    
    for ind,aa in enumerate(sequence):
        if ind == length: 
            break
            
        if aa.upper() in FEAT.INTERFACE_DIC:
            gravy += FEAT.GRAVY_DIC[aa.upper()]
            hydrophobicity += FEAT.HYDRO_DIC[aa.upper()]
            exposed += FEAT.EXPOSED_DIC[aa.upper()]
            disorder += FEAT.DISORDER_DIC[aa.upper()]
            bulkiness += FEAT.BULKY_DIC[aa.upper()]
            interface += FEAT.INTERFACE_DIC[aa.upper()]

    ## store averages in df_
    res.append(gravy / length)
    res.append(hydrophobicity / length)
    res.append(exposed / length)
    res.append(disorder / length)
    res.append(bulkiness / length)
    res.append(interface / length)
    
    return res

if __name__ == "__main__":
    main()
