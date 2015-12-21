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
    #print full_name

    #print ":".join("{:02x}".format(ord(c)) for c in full_name)
    #print ":".join("{:02x}".format(ord(c)) for c in 'Enik\xc3\xb6 Larisa Kocsis')

    if full_name:
        names["full_name"] = full_name.string
    else:
        names["full_name"] = "missing"
    names["full_name"] = cleanNames(names["full_name"])
    return names


def parseHtml(html):
    with open(html) as f:
        soup = BeautifulSoup(f, 'html.parser')
        #print soup.original_encoding
        names = extractName(soup)
        summary = extractSummary(soup)

    # with open(html) as f:
    #     s = str(f.readlines().decode('string-escape').decode("utf-8"))
    #     #new_s = UnicodeDammit.detwingle(s)
    #     #new_s = new_s.decode('latin-1', 'ignore')
    #     soup = BeautifulSoup(s)
    #
    #     print soup.original_encoding
    #     #print soup.prettify('utf-8')
    #     names = extractName(soup)
    #     summary = extractSummary(soup)
    return names, summary


def cleanSummaries(summary):
    '''
    Returns text stripped of tabs, newlines, funky characters - this will remove anything that is not regular ascii.
    TO DO: need to put back the rest of the world
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
    #import pdb; pdb.set_trace()

    if isBlank(fname):
        fname = "unicode-only"
    else:
        # Strip Prof. Dr.
        fname = fname.lower()
        print fname
        fname = fname.replace('prof.', "")
        fname = fname.replace('dr.',"")

        # Only keep letters, numbers and
        pattern = re.compile('([^\s\w]|_)+')
        fname = pattern.sub('', fname)

        # TO DO: Replace real bad ones explicitly

        # If first name is an initial, set first name to be "INI-ONLY". will go into first_name generator

        # names with only non-ascii characters are causing issues.

    return fname

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


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
