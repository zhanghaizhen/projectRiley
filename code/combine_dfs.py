import pandas as pd

# Files that contain extracted names, summaries, title, industry, location and html
#file_list = ['/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_holyoke.txt',
# '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_utaustin.txt',
# '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_vassar.txt',
# '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_wellesley.txt',
# '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_caltech.txt',
# '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_gatech.txt',
#  '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_huskies.txt']

file_list = ['/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_holyoke.txt', '/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_utaustin.txt', '/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_vassar.txt', '/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_wellesley.txt', '/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_caltech.txt', '/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_gatech.txt', '/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_huskies.txt']

#outfile = '/Users/lekha/galvanize/capstone/projectRiley/data/withfirstname/withfirstname_all.txt'

outfile = '/Users/lekha/galvanize/capstone/projectRiley/data/withgender/withgender_all.txt'

def combine_dfs(infile_list):
    cnt = 0
    for f in infile_list:
        cnt += 1
        if cnt == 1:
            df = pd.read_csv(f, sep="|")
        else:
            df = pd.concat([df, pd.read_csv(f, sep="|")], axis=0)
    print ("Concatenated {0} files into a single data frame").format(cnt)

    return df

def main():
    df = combine_dfs(file_list)
    df.to_csv(outfile, sep="|", index=False)

if __name__=='__main__':
    main()
