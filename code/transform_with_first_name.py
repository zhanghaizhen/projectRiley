from __future__ import division
from __future__ import print_function
import pandas as pd
import numpy as np
from collections import defaultdict
import cPickle as pickle
import os
import sys


def create_df(file_name):
    cols = defaultdict(list)
    num_rows = 0
    with open(file_name) as f:
        for line in f:
            num_rows += 1
            fields = line.strip().split('||')
            print (fields)
            print (fields[0], fields[5], fields[3])
            cols['full_name'].append(fields[0])
            cols['summary'].append(fields[1])
            cols['title'].append(fields[2])
            cols['industry'].append(fields[3])
            cols['location'].append(fields[4])
            cols['html'].append(fields[5])
    df = pd.DataFrame(data=cols, index = np.arange(num_rows))
    return df

# Add columns
def new_cols(df, source):
    df['counter'] = np.ones(len(df))
    df['source'] = source
    df['full_name_fields'] = df['full_name'].apply(lambda x: x.split())
    df['name_fields'] = df['full_name_fields'].apply(lambda x: len(x))
    # Add new column for first_name
    df['first_name'] = df['full_name'].apply(lambda x: x.split()[0])
    df = df[df['first_name'] != 'missing']
    df = df[df['first_name'] != 'unicode-only']
    df = df[df['first_name'].map(len) > 1]
    return df


# debugging nonetype strings. Keeping the code since I seem to need it often
def check_for_nonetypes(df):
    name_fields = df['full_name'].apply(lambda x: x.split())
    lens = []
    # create a list for number of strings in name
    for x in name_fields:
        lens.append(len(x))
    # convert lengths to np.array; easier to do numpy magic
    nplens = np.array(lens)
    zero_idx = np.where(nplens == 0)
    if len(zero_idx) > 0:
        print ("There are nonetype strings in the df; dropping the rows below\n")
        print (zero_idx)
        df.drop(df.index[zero_idx], inplace=True)
    else:
        print ("There are no nonetype strings. Yay!\n")
    return df

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    source = sys.argv[3]
    df = create_df(input_file)
    df = check_for_nonetypes(df)
    df = new_cols(df, source)
    #output_file = '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_vassar.txt'

    df.to_csv(output_file, sep="|", index=False)

if __name__=='__main__':
    error_message = 'Usage: python transform_with_first_name.py <input_file> <output_file> <file_source>'
    if (len(sys.argv) != 4):
        print (error_message)
        exit()
    main()
