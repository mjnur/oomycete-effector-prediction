import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# get the data
url = "https://gist.githubusercontent.com/seankross/a412dfbd88b3db70b74b/raw/5f23f993cd87c283ce766e7ac6b329ee7cc2e1d1/mtcars.csv"
df = pd.read_csv(url) # read mt cars data
df['am'] = df['am'].apply(str) # convert 'am' into a string

# generate a table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div([
    html.H2('EffectortO: Predicting Oomycete Effector Genes using Machine Learning Classifiers'),
    html.P('This is a demonstration of how to use dash/plotly to deploy an interactive web app!'),
    dcc.Graph(
        id = "plot1",
        figure = {
            'data':[
                go.Scatter(
                    x = df[df['am'] == i]['mpg'],
                    y = df[df['am'] == i]['wt'],
                    text = df[df['am'] == i]['model'],
                    mode = 'markers',
                    opacity=0.7,
                    marker={
                        'size': 15
                    },
                    name = i,
                    showlegend=True

                ) for i in df.am.unique()
            ],
            'layout': go.Layout(
                title = "MT Cars Dataset",
                xaxis = {'title':'mpg'},
                yaxis = {'title':'wt'},
            )
        }
    ),
    html.Hr(),
    html.P("The underlying data is displayed below (first 10 rows):"),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)
