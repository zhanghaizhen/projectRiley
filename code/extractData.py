# Extract Name, Summary, Education
#from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
import pandas as pd
import numpy as np
from collections import defaultdict
import re
from HTMLParser import HTMLParser
import cPickle as pickle
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from datetime import datetime
import os
import sys
import pdb
import string


def formatDate(data, key):
    # for k, v in data.iteritems():
    #     print k, v
    #print "DATA key\n"
    #print data[key]
    if key not in data:
        return
    words = len(data[key].split())

    format = "%B %Y" if words == 2 else "%Y"
    try:
        data[key] = datetime.strptime(data[key], format).date()
    except ValueError:
        print ("Couldn't parse datetime '%s'", data[key])
        del data[key]

    return


def handle_dates(elements, encoded_dict):
    if not elements:
        return
    encoded_dict['start'] = elements[0].string
    if len(elements) > 1:
        encoded_dict['end'] = elements[1].string
    formatDate(encoded_dict, "start")
    formatDate(encoded_dict, "end")


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


def extractSummary2(soup):
    summaries_dict = {}

    # find summary for the older files
    #summary = soup.find(name='div', class_='summary')
    summary = soup.find(class_='profile-section', id='summary')
    if summary:
        temp_summ = []
        summary_text = ''
        for string in summary.stripped_strings:
            temp_summ.append(string)
        for string in temp_summ:
            string = string.lower()
            if not string.startswith('summary'):
                summary_text += ' ' + string
        summaries_dict["summary"] = summary_text
    else:
        summaries_dict["summary"] = "Missing"
    summaries_dict["summary"] = cleanSummaries(summaries_dict["summary"])
    return summaries_dict


def extractSummary1(soup):
    '''
    Extract Summary for the First Data Set - Huskies
    use extractSummary2 for the newer Datasets
    '''
    summaries_dict = {}
    summary = soup.find(name='div', class_='summary')
    if summary:
        summary_text = ''
        for string in summary.stripped_strings:
            summary_text += ' ' + string
        summaries_dict["summary"] = summary_text
    else:
        summaries_dict["summary"] = "Missing"
    summaries_dict["summary"] = cleanSummaries(summaries_dict["summary"])
    return summaries_dict


def extractName2(soup):
    names = {}
    full_name = soup.find(class_='fn', id='name')
    if full_name:
        names["full_name"] = full_name.string
    else:
        names["full_name"] = "missing"
    names["full_name"] = cleanNames(names["full_name"])
    return names


def extractName1(soup):
    '''
    extract Name for the first Data Set - Huskies.
    Use extractName2 for the newer Data Set
    '''
    names = {}
    full_name = soup.find(name='span', class_='full-name')
    if full_name:
        names["full_name"] = full_name.string
    else:
        names["full_name"] = "missing"
    names["full_name"] = cleanNames(names["full_name"])
    return names


def extractTitle1(soup):
    title = {}
    #title_str = soup.find_all('div', class_='editable-item', id='headline')
    title_str = soup.find('p', class_='title')
    if title_str:
        if isBlank(title_str.string):
            title["title"] = "missing"
        #for line in title_str:
        #title["title"] = line.find('p', class_='title').string
        else:
            title["title"] = title_str.string
    else:
        title["title"] = "missing"
    return title

# for x in soup.find_all('div', class_='editable-item', id='location'):
#     location = x.find('span', class_='locality').string
#     industry = x.find('dd', class_='industry').string
# print (title, location, industry)


def extractTitle2(soup):
    '''
    Extract Title for the newer data sets
    '''
    title = {}
    title_str = soup.find('p', class_='headline title')
    if title_str:
        title["title"] = title_str.string
    else:
        title["title"] = "missing"
    return title


def extractLocation1(soup):
    location = {}
    loc_string = soup.find_all('div', class_='editable-item', id='location')
    if loc_string:
        for line in loc_string:
            location["loc"] = line.find('span', class_='locality').string
    else:
        location["loc"] = "missing"
    return location


def extractLocation2(soup):
    location = {}
    loc_string = soup.find_all('span', class_='locality')
    if loc_string:
        for line in loc_string:
            location["loc"] = line.string
    else:
        location["loc"] = "missing"
    return location


def extractIndustry1(soup):
    industry = {}
    ind_string = soup.find_all('div', class_='editable-item', id='location')
    if ind_string:
        for line in ind_string:
            ind = line.find('dd', class_='industry')
            if ind:
                industry["industry"] = ind.string
            else:
                industry["industry"] = "missing"
    else:
        industry["industry"] = "missing"
    return industry


def extractIndustry2(soup):
    industry = {}
    ind_string = soup.find_all('dd', class_= 'descriptor')
    if ind_string:
        if len(ind_string) < 2:
            industry["industry"] = "missing"
            return industry
        else:
            industry["industry"] = ind_string[1].string
    else:
        industry["industry"] = "missing"
    return industry


def extractSkills(soup):
    skills = []
    #skill_dict = defaultdict(list)
    for skill in soup.find_all('a', class_='endorse-item-name-text'):
    #    skill_dict = defaultdict(list)
        #skill_dict["type"] = "skill"
        #skill_dict["skill"].append(skill.string)
        skills.append(skill.string)
    return skills


def extractEducations(soup):
    educations = []
    #education_dict = defaultdict(lambda: None)
    for edu in soup.find_all(name='div', class_='education'):
        education_dict = defaultdict(lambda: None)
        if edu.find('span', class_='major'):
            education_dict['major'] = edu.find('span', class_='major').text

        if edu.find(class_='org'):
            if edu.find(class_='org').a:
                education_dict['org'] = edu.find( class_='org').a.string
            else:
                education_dict['org'] = edu.find( class_='org').string

        if edu.find('span', class_='degree'):
            education_dict['degree'] = edu.find( 'span', class_='degree').string

        handle_dates( edu.find( class_='education-date').find_all('time'), education_dict)
        educations.append(education_dict)
    return educations


def extractOccupations(soup):
    #occupations = []
    #pos_dict = defaultdict(lambda: None)
    positions = soup.find_all(name="div", class_="past-position")
    positions += soup.find_all(name="div", class_="current-position")
    for pos in positions:
        pos_dict = defaultdict(lambda: None)
        if pos.div.header.h4:
            if pos.div.header.h4.a:
                pos_dict['title'] = pos.div.header.h4.a.string
            else:
                pos_dict['title'] = pos.div.header.h4.string

        org_link = pos.div.header.find(name='a', attrs={'dir': 'auto'})
        if org_link:
            pos_dict['org'] = org_link.string
            org_url = org_link.attrs['href']
            org_url = org_url[:org_url.find('?')]
            pos_dict['org_url'] = org_url
        elif pos.div.header.find(name='span', attrs={'dir': 'auto'}):
            pos_dict['org'] = pos.div.header.find( name='span', attrs={ 'dir': 'auto'}).string

        print (pos.find_all('time'))
        handle_dates(pos.find_all('time'), pos_dict)

        #occupations.append(pos_dict)
    return pos_dict


def parseHtml1(html):
    with open(html) as f:
        soup = BeautifulSoup(f, 'html.parser')
        names = extractName1(soup)
        summary = extractSummary1(soup)
        title = extractTitle1(soup)
        industry = extractIndustry1(soup)
        location = extractLocation1(soup)

    return names, summary, title, industry, location

def parseHtml2(html):
    with open(html) as f:
        soup = BeautifulSoup(f, 'html.parser')
        names = extractName2(soup)
        summary = extractSummary2(soup)
        title = extractTitle2(soup)
        industry = extractIndustry2(soup)
        location = extractLocation2(soup)

    return names, summary, title, industry, location


def cleanSummaries(summary):
    '''
    Returns text stripped of tabs, newlines, funky characters - this will remove anything that is not regular ascii.
    TO DO: need to put back the rest of the world
    '''
    # convert to lower case and remove tabs and newlines
    summary = summary.lower()
    summary = summary.replace('\\t', ' ')
    summary = summary.replace('\\n', ' ')
    summary = summary.replace('/', ' ')

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
        print (fname)
        fname = fname.replace('prof.', "")
        fname = fname.replace('dr.',"")
        fname = fname.replace('dr',"")

        # Only keep letters, numbers and
        pattern = re.compile('([^\s\w]|_)+')
        fname = pattern.sub('', fname)

    return fname

def isBlank(mystr):
    if mystr and mystr.strip():
        #mystr is not None AND mystr is not empty or blank
        return False
    #mystr is None OR mystr is empty or blank
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
    file_type = sys.argv[3]
    files = listFiles(input_path)

    for html_file in files:
        if (file_type == '1'):
            #print ("old")
            [names, summary, title, industry, location] = parseHtml1(html_file)
        else:
            [names, summary, title, industry, location] = parseHtml2(html_file)

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
            for k2,v2 in title.iteritems():
                v2 = v2.encode('utf-8')
                fp.write(v2)
                fp.write("||")
            for k3,v3 in industry.iteritems():
                v3= v3.encode('utf-8')
                fp.write(v3)
                fp.write("||")
            for k4,v4 in location.iteritems():
                v4= v4.encode('utf-8')
                fp.write(v4)
                fp.write("||")
            fp.write(html_file)
            fp.write("\n")


# MAIN FILE

if __name__ == '__main__':
    error_message = "Usage: python extractData.py <input_path> <output_file> <file_type (1=old) or (2=new)>\n"
    if len(sys.argv) != 4:
        print (error_message)
        exit()
    main()
