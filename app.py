import dash
import dash_table
from dash_table.Format import Format
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import numpy as np
from skimage import io, filters, measure, color, img_as_ubyte
import PIL
import pandas as pd
import matplotlib as mpl
import pickle
from Bio import SeqIO
from machine_learning_classification.scripts import FEAT as FEAT
from sklearn.ensemble import RandomForestClassifier


import json
import datetime
import operator
import os

import base64
import io

# Set up the app
external_stylesheets = [dbc.themes.BOOTSTRAP, "assets/object_properties_style.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

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



# file upload function
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
            
        trained_model = pickle.load(open('machine_learning_classification/trained_models/RF_88_best.sav', 'rb'))
        seqs_to_predict = SeqIO.parse(io.StringIO(decoded.decode('utf-8')),'fasta')
        prediction_map = {'0': "predicted non-effector", '1': "predicted effector"}
        
        seq_ids = []
        full_sequences = []
        for protein in seqs_to_predict:
            seq_ids.append(protein.id)
            full_sequences.append(protein.seq)

        seq_features = np.array([get_average_features(seq) for seq in full_sequences])
        
        # get predicted output
        predictions = trained_model.predict(seq_features)
        probabilities = trained_model.predict_proba(seq_features)
        meanings = np.array([prediction_map[pred] for pred in predictions])
    
        df = pd.DataFrame({"proteinID": seq_ids,
                           "prediction": predictions, 
                           "probability": probabilities[:,1], 
                           "meaning": meanings
                          })
        
        # round probabilities
        df['probability'] = np.round(df['probability'], 2)

    except Exception as e:
        print(e)
        return None

    return df

@app.callback(Output('datatable','children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def get_new_datatable(contents, filename):
    table = parse_contents(contents, filename)
    table = table[['proteinID', 'prediction', 'probability', 'meaning']]
    formatted_table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in table.columns],            
            data=table.to_dict("records"),
            tooltip_header={
                'proteinID': 'Protein ID obtained from fasta file',
                'prediction': 'Binary classification value of non-effector (0) and effector(1), \
                                using a cutoff of 0.5',
                'probability': 'Random Forest predicted probability of being an effector',
                'meaning': 'Classification value in a readable format'
            },
            style_header={
                "textDecoration": "underline",
                "textDecorationStyle": "dotted",
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                "font-size": "16px"
            },
            tooltip_delay=0,
            page_size=18,
            export_format="csv",
            sort_action='native',
            tooltip_duration=None,
            style_table={"overflowY": "scroll"},
            fixed_rows={"headers": False, "data": 0},
            style_cell={"width": "85px", 
                        "font-size": "16px",
                        'fontFamily': 'Sans-Serif'
                       },
        )
    
    return html.Div([formatted_table])

# Buttons
button_howto = dbc.Button(
    "View Code on github",
    outline=False,
    color="primary",
    href="https://github.com/mjnur/oomycete-effector-prediction",
    id="gh-link",
    style={"text-transform": "none"},
)

# Define Header Layout
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            html.Img(
                                src=app.get_asset_url("genomecenter_logo.png"),
                                height="30px",
                            ),
                            href="https://bremia.ucdavis.edu",
                        )
                    ),
                    dbc.Col(dbc.NavbarBrand("EffectorO: Motif-Independent Oomycete Effector Prediction")),
                ],
                align="center",
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.NavbarToggler(id="navbar-toggler"),
                        dbc.Collapse(
                            dbc.Nav(
                                [dbc.NavItem(button_howto)],
                                className="ml-auto",
                                navbar=True,
                            ),
                            id="navbar-collapse",
                            navbar=True,
                        ),
                    ]
                ),
                align="center",
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
)

# Define Cards

image_card = dbc.Card(
    [
        dbc.CardHeader(html.H3("Input FASTA protein file for EffectorO-ML")),
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    # create upload button, with max file size of 10MB
                    dcc.Upload(html.Button('Select a fasta file', 
                                           style={"width": "100%",
                                                  'borderStyle': 'dashed',
                                                  'font-family': 'sans-serif',
                                                  'borderRadius': '5px',
                                                  'borderWidth': '2px',}), 
                               id="upload-data",
                               max_size=10000000,
                               style={"width": "100%"})

                ], width=12, style={"padding-left": 0}),
                html.Div([
                    dcc.Markdown('''**File requirements**:''', style={'padding-top': '10px'}),
                    dcc.Markdown('''
                      - FASTA-formatted file of amino acid sequences
                      - File size less than 10MB
                    ''')
                ]),
            ]),
        ),
    ], style={'height': '30vh'}
)

methodology_card = dbc.Card(
    [
        dbc.CardHeader(html.H3("Methodology")),
        dbc.CardBody(
            dbc.Row([
                html.Div([
                    dcc.Markdown('''See [bioRxiv pre-print](https://www.biorxiv.org) for detailed information'''),
                    dcc.Markdown('''This pipeline runs **EffectorO-ML**, a pre-trained 
                    machine-learning based Oomycete effector classifier, built from Random Forest models using
                    biochemical amino acid characteristics as features.''')


                ]),
            ]),
        ),
    ], style={'height': '30vh'}

)
table_card = dbc.Card(
    [
        dbc.CardHeader(html.H2("EffectorO-ML Prediction Table")),
        dbc.CardBody(
            dbc.Row(
                dbc.Col(
                    [
                        html.Div(id='datatable')
                    ]
                )
            )
        ),
    ]
)

app.layout = html.Div(
    [
        header,
        dbc.Container(
            [dbc.Row([dbc.Col(image_card, md=6), 
                      dbc.Col(methodology_card, md=6)
                      ], ),
            dbc.Row([dbc.Col(table_card)])],
            fluid=True,
        ),
    ]
)


# we use a callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
