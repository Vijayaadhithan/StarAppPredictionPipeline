import numpy as np
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import datetime
import joblib # to dump the trained model to a .pkl file

data = pd.read_csv('repo_features.csv')

print(data.head())
print(len(data.index))
print("types: ",data.dtypes)

y = data['stars']
X = data.drop(columns=["stars"])

models = {} #Dictionary of models

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Linear Regression - model_1 - y_pred_1
model_1 = LinearRegression()
model_1.fit(X_train, y_train)
y_pred_1 = model_1.predict(X_test)
models["model_1"] = model_1

#Random Forests - model_2 - y_pred_2
model_2=RandomForestClassifier()
model_2.fit(X_train, y_train)
y_pred_2 = model_2.predict(X_test)
models["model_2"]=model_2

#Decision Tree - model_3 - y_pred_3
model_3 = tree.DecisionTreeClassifier()
model_3.fit(X_train,y_train)
y_pred_3 = model_3.predict(X_test)
models["model_3"] = model_3

# Neural Network - model_4 y_pred_4
model_4 = MLPClassifier()
model_4.fit(X_train, y_train)
y_pred_4 = model_4.predict(X_test)
models["model_4"] = model_4

#R squared

r2_scores = {}

# Linear Regression scores
lin_reg_score = model_1.score(X_test, y_pred_1)
print("R-squared score 1 for Linear Regression:", lin_reg_score)

lin_reg_score_2 = r2_score(y_test, y_pred_1)
print("R-squared score 2 for Linear Regression: ", lin_reg_score_2)

r2_scores["model_1"] = lin_reg_score_2

# Random Forest scores
rand_for_score = model_1.score(X_test, y_pred_2)
print("R-squared score 1 for Random Forests:", rand_for_score)

rand_for_score_2 = r2_score(y_test, y_pred_2)
print("R-squared score 2 for Random Forests: ", rand_for_score_2)

r2_scores["model_2"] = rand_for_score_2

#Decision Tree scores
tree_score = model_1.score(X_test, y_pred_3)
print("R-squared score 1 for Decision Tree:", tree_score)

tree_score_2 = r2_score(y_test, y_pred_3)
print("R-squared score 2 for Decision Tree: ", tree_score_2)

r2_scores["model_3"] = tree_score_2

# Neural Network scores
neural_score = model_4.score(X_test, y_pred_4)
neural_score_2 = model_4.score(y_test, y_pred_4)
print("R-squared  score 1 for Neural Network:", neural_score)
print("R-squared  score 2 for Neural Network:", neural_score_2)
r2_scores["model_3"] = neural_score_2

#Picking the "best" model
best_model = models[max(r2_scores, key=r2_scores.get())]

#Dumping the model to a pkl file
joblib.dump(best_model, 'best_model.pkl')


