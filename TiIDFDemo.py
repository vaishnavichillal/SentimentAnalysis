import pandas as pd

df = pd.read_csv('balanced_review.csv')



df.dropna(inplace = True)



df = df[df['overall'] != 3]



import numpy as np
df['Positivity'] = np.where(df['overall'] > 3, 1, 0 )


#features - reviewText col
#labels - Positivity


#Bag of Words model

from sklearn.model_selection import train_test_split


features_train, features_test, labels_train, labels_test = train_test_split(df['reviewText'], df['Positivity'], random_state = 42 ) 

"""
list1 = [1,2,3,4,5,6,7,8,9,10]

train, test = train_test_split(list1, random_state = 42)

"""

from sklearn.feature_extraction.text import CountVectorizer


# vect = CountVectorizer().fit(features_train)


# len(vect.get_feature_names())

# vect.get_feature_names()[15000:15010]

# features_train_vectorized = vect.transform(features_train)

# #features_train_vectorized.toarray()

# #prepare the model
# #KNN, SVM, Naive Bayes, Logistic Regression, Decision Tree, Random Forest, Xgboost

# #version 01
# from sklearn.linear_model import LogisticRegression

# model = LogisticRegression()
# model.fit(features_train_vectorized, labels_train)


# predictions = model.predict(vect.transform(features_test))


# from sklearn.metrics import roc_auc_score
# roc_auc_score(labels_test, predictions)




#TF-IDF - term frequency inverse document frequency
#version 02

features_train, features_test, labels_train, labels_test = train_test_split(df['reviewText'], df['Positivity'], random_state = 42 ) 


from sklearn.feature_extraction.text import TfidfVectorizer

vect = TfidfVectorizer(min_df = 5).fit(features_train)


features_train_vectorized = vect.transform(features_train)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1100)
model.fit(features_train_vectorized, labels_train)


pred = model.predict(vect.transform(features_test))







from sklearn.metrics import roc_auc_score
roc_auc_score(labels_test, pred)

# #to transfer the model to other server
import pickle


pkl_filename = "pickle_model.pkl"

with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)
pickle.dump(labels_train,open('train_data.pkl','wb'))
pickle.dump(features_train_vectorized,open('feature_vec.pkl','wb'))
pickle.dump(vect.vocabulary_,open('features.pkl','wb'))

"""
file =  open('pickle_model.pkl', 'wb')

pickle.dump(model, file)

file.close()



"""
#sylver machine has to run below code

"""
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)
    


pred = pickle_model.predict(vect.transform(features_test))

roc_auc_score(labels_test, pred)
"""
