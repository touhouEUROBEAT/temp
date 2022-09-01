import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sn
import pickle

# Import module to split the datasets
from sklearn.model_selection import train_test_split
# Import modules to evaluate the metrics
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, roc_curve, auc
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

import time

import random
from account.models import Student

# Global parameters
# root folder
t = time.time()
root_folder = '.'
data_folder_name = 'data'
glove_filename = '../../../temp/word_vec/glove.6B.50d.txt'

train_filename = 'train.csv'
# Variable for data directory
DATA_PATH = os.path.abspath(os.path.join(root_folder, data_folder_name))
glove_path = os.path.abspath(os.path.join(DATA_PATH, glove_filename))

# Both train and test set are in the root data directory
train_path = DATA_PATH
test_path = DATA_PATH

# Relevant columns
TEXT_COLUMN = 'text'
TARGET_COLUMN = 'target'

word2vec_output_file = glove_filename + '.word2vec'
# glove2word2vec(glove_path, word2vec_output_file)

# User attributes
# Change nerdy to foody once on cloud instance and have better access to bigger datasets
# Also, introduce UCSD score
ATTRIBUTE = ('introvert', 'athletic', 'nerdy', 'chad', 'academics')

print("start")
model = KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)
print("time takes to load model", time.time() - t)

t = time.time()


def calc_attrib(interests, attr=ATTRIBUTE):
    toReturn = {}

    for i in attr:
        for j in interests:
            if not i in toReturn.keys():
                try:
                    toReturn[i] = model.similarity(i, j).item()
                except:
                    toReturn[i] = 0
            else:
                try:
                    toReturn[i] += model.similarity(i, j).item()
                except:
                    toReturn[i] += 0
    return toReturn
