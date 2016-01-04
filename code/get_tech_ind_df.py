from __future__ import division
from __future__ import print_function
import pandas as pd
import numpy as np
from collections import defaultdict
import re
import sys
import os

def get_ind_group(ind):
    ind = ind.strip().lower()
    ind_groups = { 'missing': 0,
                   'higher education': 1,
                   'research': 1,
                   'computer software': 2,
                   'information technology and services': 2,
                   'internet': 2,
                   'design': 2,
                   'mechanical or industrial engineering': 2,
                   'aviation aerospace': 2,
                   'electrical electronic manufacturing': 2,
                   'civil engineering': 2,
                   'telecommunications': 2,
                   'graphic design': 2,
                   'semiconductors': 2,
                   'computer hardware': 2,
                   'logistics and supply chain': 2,
                   'computer games': 2,
                   'computer network security': 2,
                   'nanotechnology': 2,
                   'animation': 2,
                   'nanotechnologies': 2 }

    result = ind_groups.get(ind, 3)
    return result


def strip_punc(x):
    x = x.lower()
    pattern = re.compile('([^\s\w]|_)+')
    x = pattern.sub(' ', x)
    return x


def get_industry(df):
    df['industry'] = df['industry'].apply(lambda x: strip_punc(x))
    industries = df.industry.value_counts()
    inds = industries.index.tolist()
    df['ind_group'] = df['industry'].apply(lambda x:get_ind_group(x))
    return df


def main():
    '''
    1. INPUT: Data after location columns have been added
    2. Output: 2 files - one containing all rows with industry grouping added, another with just the rows that are grouped as "tech" from the list in this file
    '''
    infile = sys.argv[1]
    techfile = sys.argv[2]
    allout = sys.argv[3]
    df = pd.read_csv(infile, sep="|")
    df = get_industry(df)
    df.to_csv(allout, sep="|", index=False)
    techdf = df[df['ind_group'] == 2]
    techdf.to_csv(techfile, sep="|", index=False)


if __name__ == '__main__':
    error_msg = "Usage: python get_tech_ind.py <input csv file> <output_tech_file> <output_all_with_ind>\n"
    if len(sys.argv) != 4:
        print (error_msg)
        exit()

    main()
