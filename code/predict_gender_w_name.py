from __future__ import division
from __future__ import print_function
import nltk
import pandas as pd
import numpy as np
from collections import defaultdict
import cPickle as pickle
import os
import sys


def gender_features(word):
    '''
    Returns the following features given a word:
    - name
    - last letter
    - last 2 letters
    - boolean if last letter is vowel
    '''
    return {'name': word, 'last_letter': word[-1], 'last_2_letters': word[-2:], 'last_is_vowel': (word[-1] in 'aeiou')}


def force_names(gender):
    my_fem_file = '/Users/lekha/galvanize/capstone/projectRiley/data/genderpredict/my_female.txt'
    my_male_file = '/Users/lekha/galvanize/capstone/projectRiley/data/genderpredict/my_male.txt'

    with open(my_fem_file, 'r') as f:
        females = f.readlines()
    females = [f.strip() for f in females]

    with open(my_male_file, 'r') as f:
        males = f.readlines()
    males = [m.strip() for m in males]

    if name in females:
        return 'female'
    if name in males:
        return 'male'
    return gender


def gender_predict(classifier, first_name):
    # get the features of the set to be classified
    name_features = gender_features(first_name)
    gender = classifier.classify(name_features)
    gender = force_names(first_name, g)
    return gender


def main():
    # read in classifier model that is stored as a pickle file
    input_file = '/Users/lekha/galvanize/capstone/projectRiley/models/gender.pkl'
    with open(input_file, 'r') as f:
        classifier = pickle.load(f)
    gender = gender_predict(classifier, first_name)


if __name__=='__main__':
    main()
