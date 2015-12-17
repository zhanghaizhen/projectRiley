# Extract Name, Summary, Education

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from collections import defaultdict
import os
import pdb
import re


gCollapserRxp = re.compile("\s+")
def handle_data(data):
    handled = collapse(clean(data, punctuation=False), matcher=gCollapserRxp) if data else None
    return handled


def formatDate(data, key):
    if key not in data:
        return
    words = len(data[key].split())

    format = "%B %Y" if words == 2 else "%Y"
    try:
        data[key] = datetime.strptime(data[key], format).date()
    except ValueError:
        logging.warning("Couldn't parse datetime '%s'", data[key])
        del data[key]
    return


def handle_dates(elements, encoded_dict):
    if not elements:
        return
    encoded_dict['start'] = handle_data(elements[0].string)
    if len(elements) > 1:
        encoded_dict['end'] = handle_data(elements[1].string)
    formatDate(encoded_dict, "start")
    formatDate(encoded_dict, "end")


def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    summary = extractSummary(soup)
    photos = extractPicture(soup)
    skills = extractSkills(soup)
    return summary, photos, skills


def extractEducations(soup):
    educations = []
    for edu in soup.find_all(name='div', class_='education'):
        education_dict = defaultdict(lambda: None)
        education_dict['type'] = 'education'

        if edu.find('span', class_='major'):
            education_dict['major'] = handle_data(
                edu.find(
                    'span',
                    class_='major').text)

        if edu.find(class_='org'):
            if edu.find(class_='org').a:
                education_dict['org'] = handle_data(
                    edu.find(
                        class_='org').a.string)
            else:
                education_dict['org'] = handle_data(
                    edu.find(
                        class_='org').string)

        if edu.find('span', class_='degree'):
            education_dict['degree'] = handle_data(
                edu.find(
                    'span',
                    class_='degree').string)

        handle_dates(
            edu.find(
                class_='education-date').find_all('time'),
            education_dict)
        educations.append(education_dict)
    return educations


def extractSummary(soup):
    summaries_dict = {}
    summary = soup.find(name='div', class_='summary')
    if summary:
#        summaries_dict["summary"] = summary.string
        temp = ''
        for string in summary.stripped_strings:
            temp = temp + string
            summaries_dict["summary"] = temp
    else:
        summaries_dict["summary"] = "Missing"
    return summaries_dict

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


def extractSkills(soup):
    skills = []
    for skill in soup.find_all('a', class_='endorse-item-name-text'):
        skill_dict = defaultdict(lambda: None)
        skill_dict["type"] = "skill"
#        skill_dict["skill"] = handle_data(skill.string)
        skill_dict["skill"] = skill.string
        skills.append(skill_dict)
    return skills


def parseArgs(args):
    parser = getBasicParser(
        "Extract education and work history from Scrapy-crawled LinkedIn profile",
        directory=True)

    # NOTE: type=open/FileType doesn't scale beyond maxdescriptor
    parser.add_argument("path", nargs="+", help="file(s) to parse")
    args = parser.parse_args(args)

    args.outputEdu = open(os.path.join(args.output, "educations.txt"), "a")
    args.outputWork = open(os.path.join(args.output, "occupations.txt"), "a")
    args.outputPhotos = open(os.path.join(args.output, "profiles.txt"), "a")
    args.outputSkills = open(os.path.join(args.output, "skills.txt"), "a")
    args.outputSummary = open(os.path.join(args.output, "summaries.txt"), "a")
    return args

def printEducationRows(items, opath):
    for it in items:
        printRow(args.outputEdu, [url, it["degree"], it["major"],
                                  it["start"], it["end"], it["org"]])
    return


def printWorkRows(items, opath):
    for it in items:
        printRow(args.outputWork, [url, it["title"], it["start"],
                                   it["end"], it["org"], it["org_url"] or "",])
    return


def printPhotoRows(items, opath):
    for it in items:
        printRow(args.outputPhotos, [url, it["pic_yes"], it["full_name"]])
    return


def printSkillRows(items, opath):
    for it in items:
        printRow(args.outputSkills, [url, it["skill"]])
    return


def printSummaryRows(items, opath):
    outputFile = open(os.path.join(opath, "summaries.txt"), "a")
    for k, v in items.iteritems():
        print k, v
        outputFile.write("|")
        outputFile.write(k)
        outputFile.write("|")
        outputFile.write(v)
        outputFile.write("|")
    outputFile.write("\n")


## MAIN FILE

my_path = '/Users/lekha/galvanize/capstone/prelims/huskies/data/2015-05-26-Washington/'
all_files = [f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path, f))]
data = {}

#files = ['00006.html', '05111108.html', '120394.html', '1bettyevans.html']
#files = ['05111108.html']


files = all_files[1000:]

for html_file in files:
    with open(os.path.join(my_path, html_file)) as f:
        s = str(f.readlines())
        new_s = UnicodeDammit.detwingle(s)
        new_s = new_s.decode("utf-8")
        soup = BeautifulSoup(new_s, 'html.parser')
        summary = extractSummary(soup)
        names = extractName(soup)

        opath = '/Users/lekha/galvanize/capstone/prelims/huskies/data/2015-05-26-Washington/'
        ofile = os.path.join(opath, "output0.txt")
        #printSummaryRows(summary, opath)
#        printPhotoRows(photos, opath)
#        printSkillRows(skills, opath)

        # soup = BeautifulSoup(s, 'html.parser')
        # full_name = soup.find('span', {'class': 'full-name'})
        # summary = soup.find('div', {'class':'summary'})
        # if full_name:
        #     full_name = full_name.get_text()
        # else:
        #     full_name = "NA"
        # if summary:
        #     summary = summary.get_text()
        # else:
        #     summary = "NA"
        # data[full_name] = summary


        with open(ofile, "a") as fp:
            for k, v in names.iteritems():
                fp.write(k)
                fp.write("|")
                fp.write(v)
                fp.write("}")
            for k1,v1 in summary.iteritems():
                v1 = v1.encode("utf-8")
                fp.write(k1)
                fp.write("|")
                fp.write(v1)
                fp.write("\n")


# ''' MAIN FILE AB'''
# args = parseArgs(sys.argv[1:])
# initializeLogging(args)
#
# for path in args.path:
#     with open(path) as handle:
#         html = clean(handle.read())
#         if not html:
#             logging.warning("Coudn't read '%s'", path)
#             continue
#
#     try:
#         simplified = os.path.splitext(os.path.basename(path))[0]
#         education, work, photos, skills = parseHtml(simplified, html)
#
#         printNameRows(name, simplified)
#         printSummaryRows(summary, simplified)
#         printPhotoRows(photos, simplified)
#         printSkillRows(skills, simplified)
#
#     except Exception as excp:
#         logging.warning("Couldn't fully parse '%s' -> %s", path, excp, exc_info=True)
#         continue
