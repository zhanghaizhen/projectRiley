from __future__ import division
from __future__ import print_function
import pandas as pd
import numpy as np
from collections import defaultdict
import re
import sys
import os

def locf(x):
    x = x.lower()
    pattern = re.compile('([^\s\w]|_)+')
    x = pattern.sub('', x)
    x = x.replace('area', ' ')
    x = x.replace('greater', ' ')
    x = x.replace('city', ' ')
    x = x.replace('stati', ' ')
    x = x.replace('uniti', ' ')
    x = x.replace('usa', ' ')
    x = x.replace('islands', ' ')
    x = x.replace('estados',' ')
    x = x.replace('unidos', ' ')
    loc_fields = x.split()
    return loc_fields


def get_location(df):
    df['location'] = df['location'].apply(lambda x: x.lower())

    abbrev_f = '/Users/lekha/galvanize/capstone/projectRiley/data/us_state_abbrev'
    replace_f = '/Users/lekha/galvanize/capstone/projectRiley/data/replace_state_strings'

    replace_states = {}
    with open(abbrev_f, 'r') as f:
        for line in f:
            fields = line.strip().lower().split(',')
            replace_states[fields[0].strip()] = fields[1].strip()

    with open(replace_f, 'r') as f:
        for line in f:
            fields = line.lower().split(',')
            replace_states[fields[0].strip()] = fields[1].strip()

    df['loc_fields'] = df['location'].apply(lambda x: locf(x))
    df['state'] = df['loc_fields'].apply(lambda x: get_state(x, replace_states))
    return df


def get_state(loc_fields, replace_dict):
    if 'carolina' in loc_fields:
        state = loc_fields[-2] + loc_fields[-1]
    elif 'dakota' in loc_fields:
        state = loc_fields[-2] + loc_fields[-1]
    else:
        state = loc_fields[-1]
    state = clean_state(state, replace_dict)
    return state.upper()


def clean_state(state, replace_dict):
    state = state.lower()
    result = replace_dict.get(state, 'other')
    return result.upper()


def main():
    '''
    1. Add Location Related columns to the dataset and create a new File to feed into the next step.
    2. Input: CSV file that is the output of predict_gender
    3. Output: CSV file that can be read into a DF
    '''
    infile = sys.argv[1]
    outfile = sys.argv[2]
    df = pd.read_csv(infile, sep="|")

    # Get rid of rows with nans if they number less than 5
    null_inds = df[df.isnull().any(axis=1)].index
    if len(null_inds) < 5:
        df = df.drop(df.index[[null_inds]])

    df = get_location(df)

    df.to_csv(outfile, sep='|', index=False)


if __name__ =='__main__':
    error_msg = "Usage: python add_location_cols.py <input csv file> <output_file>\n"
    if len(sys.argv) != 3:
        print (error_msg)
        exit()
    main()
