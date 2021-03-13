# Importing the libraries
import pickle
import pandas as pd
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px
import numpy as np
import sqlite3 as sql
from dash.exceptions import PreventUpdate

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name = "Sentiment Analysis using AI based Text Analysis"
balanced_review=None

scrappedReviews_sql=None
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def load_model():
    global pickle_model
    global vocab
    
    global balanced_review
    global scrappedReviews_sql
    
    
    #load the train model pickle file and features vector file
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)
    
    file = open("features.pkl", 'rb') 
    vocab = pickle.load(file)
    
    pred=[]
    conn=sql.connect("scrappedReviewsAll.db")
    
    
    scrappedReviews_sql=pd.read_sql_query("select * from scrappedReviewsAll", conn)
    #scrappedReviews = pd.read_csv('scrappedReviews_All.csv')
    balanced_review=pd.read_csv('balanced_review.csv')
   
    balanced_review.dropna(inplace = True)
    balanced_review = balanced_review[balanced_review['overall'] != 3]
    balanced_review['Positivity']=np.where(balanced_review['overall'] > 3, 1, 0 )
    
    
    balanced_review['Labels']=np.where(balanced_review['Positivity']==0,'Negative','Positive')
    
   
        
        
    
   
   
    
    
    
    
    
        
def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    
    
    return pickle_model.predict(reviewText)

def create_app_ui():
    global project_name
    
    fig=px.pie(balanced_review,values=balanced_review['Positivity'].value_counts(),names=balanced_review['Labels'].unique())
    
    main_layout = dbc.Container(
        
        
        dbc.Jumbotron(
                [
                    html.H2(id = 'heading', children = project_name, className = 'display-3 mb-4'),
                    html.Br(),
                    
                    dbc.Container([html.H3('Positive V/s Negative values in Balanced Reviews'),dcc.Graph(figure=fig)]),
                    html.Br(),
                    
                    dbc.Container([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i[:100] + "...", 'value': i} for i in scrappedReviews_sql.Reviews],
                    
                    style = {'margin-bottom': '30px'}
                    
                    )
                       ],
                        style = {'padding-left': '50px', 'padding-right': '50px'}
                        ),
                   # dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '100px'}),
                    html.Div(id = 'result'),
                    #html.Div(id = 'result1')
                    
                
                
                      dbc.Row(
                          [
                    
                    dbc.Textarea(id = 'textarea', className="mb-3", placeholder="Enter the Review", value = 'My daughter loves these shoes', style = {'height': '150px'}),
                    
                    dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '100px'}),
                   
                    #html.Div(id = 'result1')
                    ],
                    style = {'padding-left': '50px', 'padding-right': '50px'}
                    ) ,
                    html.Div(id = 'result1')
                ],
                className = 'text-center'
        
        ),
        className = 'mt-4'
        )
        
        
       
        
    
    
    return main_layout

@app.callback(
    Output('result', 'children'),
    [
    Input('dropdown', 'value')
    ],
    [
    State('dropdown', 'value')
    ]
    )    
def update_dropdown(dropdown, value):
    
        
    result_list = check_review(dropdown)
        
    if (result_list[0] == 0 ):
        return dbc.Alert("Negative", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Positive", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")

@app.callback(
    Output('result1', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
      State('textarea', 'value')
    ]
    )
def update_textarea(n_clicks, textarea):
    result_list = check_review(textarea)
    if(n_clicks >0):
        
        if (result_list[0] == 0 ):
            return dbc.Alert("Negative", color="danger")
        elif (result_list[0] == 1 ):
            return dbc.Alert("Positive", color="success")
        else:
            return dbc.Alert("Unknown", color="dark")
    
def main():
    global app
    global project_name
    load_model()
    open_browser()
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
    app = None
    project_name = None
if __name__ == '__main__':
    main()