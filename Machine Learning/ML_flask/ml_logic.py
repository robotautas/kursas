import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

"""
Čia yra praktiškai copy-paste iš paskaitos, 
iškomentuota dalis nebereikalinga, nes apmokytas modelis jau apmokytas.
sukuriame funkciją, kurią paskui importuosime iš šio failo į flasko logiką. 
"""


# iris = sns.load_dataset('iris')
# cols = iris.columns.tolist()
# X = iris[cols[:-1]]
# y = iris['species']
# X_train, X_test, y_train, y_test = \
# train_test_split(X, y, test_size=0.4, random_state=42)
# model = RandomForestClassifier(n_estimators = 10000).fit(X_train, y_train)
# print(model.score(X_test, y_test))

# with open ('iris_predictor.pickle', 'wb') as f:
#     pickle.dump(model, f)

pickled_model = open('iris_predictor.pickle', 'rb')
loaded_model = pickle.load(pickled_model)

def predict(sl, sw, pl, pw):
    prediction = loaded_model.predict([[sl, sw, pl, pw]])
    return prediction[0]

predict(5.5, 5.5, 5.5, 5.5)
