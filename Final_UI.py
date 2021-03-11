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
project_name = "Sentiment Analysis with Insights"
balanced_review=None
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def load_model():
    global pickle_model
    global vocab
    global scrappedReviews
    global balanced_review
    
    pred=[]
    conn=sql.connect("scrappedReviewsAll.db")
    
    scrappedReviews=pd.read_sql_query("select * from scrappedReviewsTable", conn)
    #scrappedReviews = pd.read_csv('scrappedReviews.csv')
    balanced_review=pd.read_csv('balanced_review.csv')
   
    balanced_review.dropna(inplace = True)
    balanced_review = balanced_review[balanced_review['overall'] != 3]
    balanced_review['Positivity']=np.where(balanced_review['overall'] > 3, 1, 0 )
    
    
    balanced_review['Labels']=np.where(balanced_review['Positivity']==0,'Negative','Positive')
    
    global pickle_model
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)
    
    file = open("features.pkl", 'rb') 
    vocab = pickle.load(file)
    
    for review in balanced_review['reviewText']:
        pred.append(check_review(review))
        
    
    balanced_review['Predictions']=pred
    
    
   
   
   
    
   
    
    
    
    

    

    
    #print(df_pie_data.head())
    # labels=[]
    # for row in df_pie_data['Positivity']:
    #     if row == 0 :   labels.append('Negative')
    #     else:
    #         labels.append('Positive')
        
    # df_pie_data['labels']=labels
    
    
  
    #df['y_hats'] = y_hats2
   
        
        
    
    #balanced_review['Predictions']=pickle_model.predict(balanced_review)
   # df_out = pd.merge(balanced_review,y_test[['preds']],how = 'left',left_index = True, right_index = True)
   
   # print(scrappedReviews.head())
   
    
    
    
    
    
        
def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    #print(len(loaded_vec))
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    
    
    return pickle_model.predict(reviewText)

def create_app_ui():
    global project_name
    #Positivity_counts=balanced_review.Positivity.value_counts()
    #fig=px.pie(balanced_review,values=Positivity_counts)
    
    
    #fig=balanced_review.overall.value_counts().plot(kind='pie', autopct='%1.0f%%', colors=["blue", "red"])
   # Predictions_values=balanced_review['Predictions'].value_counts()
    #airline_tweets.airline_sentiment.value_counts().plot(kind='pie', autopct='%1.0f%%', colors=["red", "yellow", "green"])
    fig=px.pie(balanced_review,values=balanced_review['Predictions'].value_counts(),names=balanced_review['Labels'].unique())
    
    main_layout = dbc.Container(
        
        
        dbc.Jumbotron(
                [
                    html.H1(id = 'heading', children = project_name, className = 'display-3 mb-4'),
                    dbc.Container([dcc.Graph(figure=fig)]),
                    html.Br(),
                    
                    dbc.Container([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i[:100] + "...", 'value': i} for i in scrappedReviews.reviews],
                    
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