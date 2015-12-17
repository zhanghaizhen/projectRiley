# Extract Name, Summary, Education

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from collections import defaultdict
import os
import sys
import pdb
import re

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
    return summaries_dict


def extractName(soup):
    names = {}
    full_name = soup.find(name='span', class_='full-name')
    if full_name:
        temp = ''
        for string in full_name.stripped_strings:
            temp = temp + string
            names["full_name"] = temp
    else:
        names["full_name"] = "Missing"
    return names


def parseHtml(html):
    with open(html) as f:
        s = str(f.readlines())
        new_s = UnicodeDammit.detwingle(s)
        new_s = new_s.decode("utf-8")
        soup = BeautifulSoup(new_s, 'html.parser')
        names = extractName(soup)
        summary = extractSummary(soup)
    return names, summary


def listFiles(path):
    '''
    returns a list of names (with extension, without full path) of all files in folder path
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

        with open(out_file, "a") as fp:
            for k, v in names.iteritems():
                fp.write(k)
                fp.write("|")
                fp.write(v)
                fp.write("||")
            for k1,v1 in summary.iteritems():
                v1 = v1.encode("utf-8")
                fp.write(k1)
                fp.write("|")
                fp.write(v1)
                fp.write("\n")


# MAIN FILE

if __name__ == '__main__':
    main()
