# Extract Name, Summary, Education
#from __future__ import unicode_literals
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from collections import defaultdict
from datetime import datetime
import os
import sys
import pdb
import re
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


def extractSummary(soup):
    summaries_dict = {}
    #summary = soup.find(name='div', class_='summary')
    summary = soup.find(class_='profile-section', id='summary')
    if summary:
        summary_f = ''
        for string in summary.get_text():
            summary_f = summary_f + string
            summaries_dict["summary"] = summary_f
    else:
        summaries_dict["summary"] = "Missing"
    summaries_dict["summary"] = cleanSummaries(summaries_dict["summary"])
    return summaries_dict


def extractName(soup):
    names = {}
    #full_name = soup.find(name='span', class_='full-name')
    # using different tags for the new DATA
    full_name = soup.find(class_='fn', id='name')
    #print full_name

    #print ":".join("{:02x}".format(ord(c)) for c in full_name)
    #print ":".join("{:02x}".format(ord(c)) for c in 'Enik\xc3\xb6 Larisa Kocsis')

    if full_name:
        names["full_name"] = full_name.string
    else:
        names["full_name"] = "missing"
    names["full_name"] = cleanNames(names["full_name"])
    return names


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

        print pos.find_all('time')
        handle_dates(pos.find_all('time'), pos_dict)

        #occupations.append(pos_dict)
    return pos_dict


def parseHtml(html):
    with open(html) as f:
        soup = BeautifulSoup(f, 'html.parser')
        names = extractName(soup)
        summary = extractSummary(soup)
        # skills = extractSkills(soup)
        # occupations = extractOccupations(soup)
        # educations = extractEducations(soup)
        #
        # print "Educations\n"
        # for x in educations:
        #     for k, v in x.iteritems():
        #         print k, v
        #
        # print "Skills\n"
        # print skills
        # # for s in skills:
        # #     print s
        #
        # print "Occupations\n"
        # for k, v in occupations.iteritems():
        #     print k, v

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
        fname = fname.replace('dr',"")

        # Only keep letters, numbers and
        pattern = re.compile('([^\s\w]|_)+')
        fname = pattern.sub('', fname)

        # TO DO: Replace real bad ones explicitly

        # If first name is an initial, set first name to be "INI-ONLY". will go into first_name generator

        # names with only non-ascii characters are causing issues.

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
