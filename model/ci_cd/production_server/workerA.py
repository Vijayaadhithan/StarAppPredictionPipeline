from celery import Celery
from joblib import load

import numpy as np
from numpy import loadtxt
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import time

time_file = './time_final.joblib'
models_and_top10_git_repo = './best_model_and_top10_github_tepos.txt'
best_model = './best_model.joblib'
data_file = './modified_data.csv'
best_model_name = './best_model_name.txt'

time_start = time.time()


def load_model():
    with open(models_and_top10_git_repo, 'r') as file:
        result = file.read()
    return result

#def load_time():
#    time = load(time_file)
#    return time

def load_data():
    data = pd.read_csv('modified_data.csv')
    filtered_data = data.dropna()
    X = filtered_data.drop('stars', axis=1)
    y = filtered_data['stars']
    return X, y

def load_best_model():
    model = load(best_model)
    return model

def load_best_model_name():
    with open(best_model_name, 'r') as file:
        result = file.read()
    return result

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task()
def add_nums(a, b):
   return a + b

@celery.task
def get_model():
    model = load_model()
    return model

@celery.task
def get_accuracy_best_model():
    X, y = load_data()
    model = load_best_model()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    return score


@celery.task
def get_best_model_name():
    name = load_best_model_name()
    return name

time_final = time.time() - time_start

@celery.task
def get_time():
    time = time_final
    return time
