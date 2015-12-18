# Extract Name, Summary, Education
#from __future__ import unicode_literals
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from collections import defaultdict
import os
import sys
import pdb
import re
import string


kGhostUrl = "https://static.licdn.com/scds/common/u/images/themes/katy/ghosts/person/ghost_person_50x50_v1.png"
def extractPicture(soup):
    photo_dict = defaultdict(lambda: None)
    if soup.find(name='div', class_='profile-picture'):
        photo = soup.find(
            name='div',
            class_='profile-picture').img.attrs['src']
        if photo == kGhostUrl:
            photo_dict['pic_yes'] = False
            return
        photo_dict['type'] = 'photo'
        photo_dict['photo'] = photo
        photo_dict['pic_yes'] = True
        return [photo_dict]


def extractSummary(soup):
    summaries_dict = {}
    summary = soup.find(name='div', class_='summary')
    if summary:
        summary_f = ''
        for string in summary.stripped_strings:
            summary_f = summary_f + string
            summaries_dict["summary"] = summary_f
    else:
        summaries_dict["summary"] = "Missing"
    summaries_dict["summary"] = cleanSummaries(summaries_dict["summary"])
    return summaries_dict


def extractName(soup):
    names = {}
    full_name = soup.find(name='span', class_='full-name')
    # print "full name:{0}".format(full_name)
    # print "full_name_string:{0}".format(full_name.string)
    # print ('OUTPUT 1: Enik\xc3\xb6 Larisa Kocsis').decode('utf-8')
    # print full_name.string.decode('utf-8')
    if full_name:
        #temp = ''
        for string in full_name.stripped_strings:
            #print string
            #temp = temp + string
            # Punting on Unicode for now; Need to come back to fixing this
            if "\\x" in string:
                names["full_name"] = "Unicode"
            else:
                names["full_name"] = string
    else:
        names["full_name"] = "Missing"
    return names


def parseHtml(html):
    with open(html) as f:
        s = str(f.readlines())
        #new_s = UnicodeDammit.detwingle(s)
        #new_s = new_s.decode('utf-8', 'ignore')
        soup = BeautifulSoup(s, 'html.parser', from_encoding='utf-8')
        #print soup.original_encoding
        #print soup.prettify('utf-8')
        names = extractName(soup)
        summary = extractSummary(soup)
    return names, summary

def cleanSummaries(summary):
    '''
    Returns text stripped of tabs, newlines, funky characters
    '''
    # convert to lower case and remove tabs and newlines
    summary = summary.lower()
    summary = summary.replace('\\t', ' ')
    summary = summary.replace('\\n', ' ')

    # Strip everything except letters, numbers and spaces
    pattern = re.compile('([^\s\w]|_)+')
    summary = pattern.sub('', summary)

    return summary

def cleanNames(fname):

    fname = fname.lower()

    # Strip Prof. Dr.
    fname = fname.replace('prof.', "")
    fname = fname.replace('dr.',"")

    # Only keep letters, numbers and
    pattern = re.compile('([^\s\w]|_)+')
    fname = pattern.sub('', fname)

    # TO DO: Replace real bad ones explicitly

    # If first name is an initial, set first name to be "INI-ONLY". will go into first_name generator

    return fname


def listFiles(path):
    '''
    returns a list of names (with full path) of all files in folder path
    '''
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(os.path.join(path, name))
    return files


def main():
    input_path = sys.argv[1]
    out_file = sys.argv[2]
    files = listFiles(input_path)

    for html_file in files:
        [names, summary] = parseHtml(html_file)

        # output a line that includes all the extracted data for a profile
        with open(out_file, "a") as fp:
            for k, v in names.iteritems():
                v = v.encode('utf-8')
                fp.write(v)
                fp.write("||")
            for k1,v1 in summary.iteritems():
                v1 = v1.encode('utf-8')
                fp.write(v1)
                fp.write("||")
            fp.write(html_file)
            fp.write("\n")


# MAIN FILE

if __name__ == '__main__':
    error_message = "Usage: python extractData.py <input_path> <output_file>\n"
    if len(sys.argv) != 3:
        print error_message
        exit()
    main()
