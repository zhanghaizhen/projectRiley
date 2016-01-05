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


def force_gender(first_name, gender, males, females):
    '''
    males and females are sets of known male and female names
    '''
    if first_name in females:
        return 'female'
    if first_name in males:
        return 'male'
    return gender


def gender_predict(classifier, first_name):
    # get the features of the set to be classified
    #print (first_name)
    name_features = gender_features(first_name)
    gender = classifier.classify(name_features)
    return gender


def get_gender_sets():
    my_fem_file = '/Users/lekha/galvanize/capstone/projectRiley/data/genderpredict/my_female.txt'
    my_male_file = '/Users/lekha/galvanize/capstone/projectRiley/data/genderpredict/my_male.txt'
    common_file =  '/Users/lekha/galvanize/capstone/projectRiley/data/genderpredict/common_names'

    common_names = []
    with open(common_file, 'r') as f:
        for line in f:
            rows = line.split(',')
            g = rows[1]
            if g == 'c':
                common_names.append(rows[0].strip())

    with open(my_fem_file, 'r') as f:
        females = f.readlines()
    females = [f.strip() for f in females]

    with open(my_male_file, 'r') as f:
        males = f.readlines()
    males = [m.strip() for m in males]

    return set(males), set(females), set(common_names)

def gender_type(first_name, males, females, commons):
    if first_name in males:
        return 'male'
    elif first_name in females:
        return 'female'
    elif first_name in commons:
        return 'common'
    else:
        return 'predicted'


def load_model(input_file):
    with open(input_file, 'r') as f:
        classifier = pickle.load(f)
    return classifier

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    males, females, commons = get_gender_sets()
    df = pd.read_csv(input_file, sep="|")

    pickle_file = '/Users/lekha/galvanize/capstone/projectRiley/models/gender.pkl'
    classifier = load_model(pickle_file)

    df['first_name'].fillna(value='realnan', inplace=True)

    df['gender'] = df['first_name'].apply(lambda x: gender_predict(classifier, x))

    # Add more Features
    ## gender_type: returns male, female,
    df['gender_type'] = df['first_name'].apply(lambda x:gender_type(x, males, females, commons))

    df['gender_forced'] = df.apply(lambda x: force_gender(x['first_name'], x['gender'], males, females), axis=1)

    # For each row, return the total count of first_names that are the same and create a column
    counts = df.groupby('first_name').size()
    counts.name = 'name_counts'
    df = df.set_index('first_name').join(counts).reset_index()

    # Print the final DF out to a text file
    df.to_csv(output_file, sep="|", index=False)


if __name__=='__main__':
    error_msg = "Usage:python predict_gender_w_name.py <input_file> <output_file>\n"
    if len(sys.argv) != 3:
        print (error_msg)
        exit()

    main()
