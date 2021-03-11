import pandas as pd

df = pd.read_csv('balanced_review.csv')

df.columns.tolist()

df['overall'].value_counts()

df.isnull().any(axis = 0)

df.isnull().any(axis = 1)

df[df.isnull().any(axis = 1)]

df.dropna(inplace = True)

df['overall'] != 3

df = df[df['overall'] != 3]


df['overall'].value_counts()

import numpy as np
df['Positivity'] = np.where(df['overall'] > 3, 1, 0 )

df['Positivity'].value_counts()


#features - reviewText col
#labels - Positivity

df['reviewText'].head()


#Bag of Words model

from sklearn.model_selection import train_test_split


features_train, features_test, labels_train, labels_test = train_test_split(df['reviewText'], df['Positivity'], random_state = 42 ) 

"""
list1 = [1,2,3,4,5,6,7,8,9,10]

train, test = train_test_split(list1, random_state = 42)

"""

from sklearn.feature_extraction.text import CountVectorizer


vect = CountVectorizer().fit(features_train)


len(vect.get_feature_names())

features_train_vectorized = vect.transform(features_train)

#features_train_vectorized.toarray()

from sklearn.linear_model import LogisticRegression

model=LogisticRegression(max_iter=1100)

model.fit(features_train_vectorized,labels_train)

predictions=model.predict(vect.transform(features_test))


from sklearn.metrics import roc_auc_score
print(roc_auc_score(labels_test, predictions))
















