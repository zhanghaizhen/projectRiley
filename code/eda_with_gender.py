from __future__ import division
from __future__ import print_function
import pandas as pd
import numpy as np
from collections import defaultdict
import re
import sys
import os

def ind_groups(ind):
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
                   'information services': 2,
                   'semiconductors': 2,
                   'computer hardware': 2,
                   'logistics and supply chain': 2,
                   'automotive': 2,
                   'program development': 2,
                   'computer games': 2,
                   'computer network security': 2,
                   'nanotechnology': 2,
                   'animation': 2,
                   'nanotechnologies': 2 }

    result = ind_groups.get('ind', 3)
    return result


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


def return_titles(df, ind, N):
    result = []
    df1 = df[df['industry'] == ind]
    titles = df1.title.value_counts()[0:N]
    for i in xrange(N):
        result.append((titles.index[i], titles[i]))
    return result


def strip_punc(x):
    x = x.lower()
    pattern = re.compile('([^\s\w]|_)+')
    x = pattern.sub(' ', x)
    return x


def get_top_titles(industries, N, filename):
    # EDA to look at the titles for the top 50 industries
    titles = {}
    for ind in inds[0:100]:
        titles[ind] = return_titles(df, ind, N)

    # Write to a file to look at
    with open(outfile, 'a') as f:
        for k, v in titles.iteritems():
            f.write(k)
            f.write("\t")
            f.write(str(v))
            f.write("\n")


def get_industry(df):
    df['industry'] = df['industry'].apply(lambda x: strip_punc(x))
    N = 10
    industries = df.industry.value_counts()
    inds = industries.index.tolist()
    outfile = "/Users/lekha/galvanize/capstone/projectRiley/data/titles"
    titles_to_file(inds, N, outfile)

    df['ind_group'] = df['industry'].apply(lambda x:get_ind_group(x))

    return df


def main(filename):
    '''
    1. EDA code to homogenize the data based on industry to be then fed into the gender predictor by summary code
    2. Output: Top 20 industries and Top 20 titles and counts for each industry - for all, male, female
    3. The output should be piped to something that can be plotted on a stacked bar graph
    '''
    df = pd.read_csv(filename, sep="|")
    df = get_location(df)
    df = get_industry(df)


if __name__ = '__main__':
    error_msg = "Usage: python eda_with_gender.py <input csv file>\n"
    if len(sys.argv) != 1:
        print (error_msg)
        exit()

    filename = sys.argv[1]
    main(filename)
