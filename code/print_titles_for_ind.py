from __future__ import division
from __future__ import print_function
import pandas as pd
import numpy as np
import sys

def get_top_titles(df, ind, N):
    result = []
    df1 = df[df['industry'] == ind]
    num_titles = len(df1.title.value_counts())
    N = min(N, num_titles)
    titles = df1.title.value_counts()[0:N]
    for i in xrange(N):
        result.append((titles.index[i], titles[i]))
    return result


def main():
    '''
    1. Input: Text File which includes the industry and industry groups
    2. Output: Top 50 industries and Top 20 titles and counts for each industry - for all, male, female
    '''
    infile = sys.argv[1]
    outfile = sys.argv[2]
    df = pd.read_csv(infile, sep="|")

    IndN = 50
    TitleN = 20
    industries = df.industry.value_counts()
    inds = industries.index.tolist()
    IndN = min(len(inds), IndN)

    titles = {}
    for ind in inds[0:IndN]:
        titles[ind] = get_top_titles(df, ind, TitleN)

    # Write to the output title file
    with open(outfile, 'a') as f:
        for k, v in titles.iteritems():
            f.write(k)
            f.write("\t")
            f.write(str(v))
            f.write("\n")


if __name__ =='__main__':
    error_msg = "Usage: python print_titles_for_ind.py <input csv file> <output_title_file>\n"
    if len(sys.argv) != 3:
        print (error_msg)
        exit()

    main()
