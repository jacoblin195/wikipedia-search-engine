import urllib
import urllib.request
import urllib.robotparser
import logging
import re
import time
import bs4
import nltk
from collections import Counter
import math
import pickle
import sys

from urllib.parse import urlparse


ignoringPostfix = ['#', '.js', '.css', '.php', '.png']

inverse_dict = {}

# Value: Tuple
# 0: Id corresponds to file name of html files
# 1: Document length
# 2: Title
# Key: url
doc_dict = {}


def endSearch():
    print("endsearch")

    f = open("inverse_dict.pkl", "wb")
    pickle.dump(inverse_dict, f)
    f.close()

    f2 = open("doc_dic.pkl", "wb")
    pickle.dump(doc_dict, f2)
    f2.close()


def part_1_procedure(contents,curr,id):
    soup = bs4.BeautifulSoup(contents, "lxml")
    text = soup.find_all(text=True)
    aSingleString = ""
    for t in text:
        if t != "\n":
            aSingleString += t.lower() + " "

    tokenized = nltk.word_tokenize(aSingleString)

    stemmer = nltk.stem.PorterStemmer()
    words = list(map(stemmer.stem, tokenized))
    for index,word in enumerate(words):

        if inverse_dict.get(word) is None:
            inverse_dict[word] = dict()
        wordFrequencyInDoc = inverse_dict[word]

        if wordFrequencyInDoc.get(curr) is None:
            wordFrequencyInDoc[curr] = 0
        wordFrequencyInDoc[curr] = 1
    try:
        title = soup.find("title",).text
    except:
        title = "Title Not Found"
    print(title)
    doc_dict[curr] = (id, len(words), title)
    return

def crawler_helper(frontier, explored, limit, counter, directory, searchtype):

    time.sleep(.1)

    counter += 1

    if counter > limit:
        print("done " + str(counter))
        endSearch()
        # sys.exit()
        return

    if searchtype == 'bfs':
        curr = frontier.pop(0)
    else:
        curr = frontier.pop(len(frontier)-1)

    explored.append(curr)

    p = urlparse(curr)
    hostname = p.hostname
    scheme = p.scheme

    try:

        if hostname is not None:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(scheme + "://" + hostname + '/robots.txt')
            rp.read()
            if not rp.can_fetch('IUB-I427-yichlin', curr):
                counter -= 1
                return crawler_helper(frontier, explored, limit, counter, directory, searchtype)
    except:

        counter-=1
        return crawler_helper(frontier, explored, limit, counter, directory, searchtype)

    try:
        req = urllib.request.Request(curr, headers={'User-Agent': 'IUB-I427-yichlin'})
        web_page = urllib.request.urlopen(req)
        contents = web_page.read().decode(errors="replace")
        logging.info(curr+" opens successfully!")
    except:
        counter -= 1
        print("\n"+curr+" fails to open!" + "\n")
        return crawler_helper(frontier, explored, limit, counter, directory, searchtype)

    part_1_procedure(contents,curr,counter)


    localList = re.findall('href[ ]*=[ ]*[\'|"](.+?)[\'|"]', contents)

    i = 0
    n = len(localList)
    while i < n:
        ignore = False
        if localList[i].startswith("#"):
            ignore = True
        if not ignore:
            for postfix in ignoringPostfix:
                if localList[i].endswith(postfix):
                    ignore = True
                    break
        if ignore:
            del localList[i]
            n -= 1
        else:
            i += 1

    # Add omitted URL heads for absolute and relative urls
    for index, localListUrl in enumerate(localList):
        if localListUrl[:2] == "//":
            localList[index] = "http:" + localListUrl
        elif localListUrl[:1] == "/":
            localList[index] = urllib.parse.urljoin(curr,localListUrl)

    # Remove duplicates
    localList = list(set(localList))

    localList = [url for url in localList if url not in explored]
    frontier.extend(localList)

    return crawler_helper(frontier, explored, limit, counter, directory, searchtype)


def crawler(url, limit, directory, searchtype):

    frontier = [url]
    explored = []
    counter = 0
    crawler_helper(frontier, explored, limit, counter, directory, searchtype)

#
# def main():
    # print command line arguments
#     crawler(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4].lower())


crawler("https://en.wikipedia.org/wiki/Lady_Cocoa", 20,"","bfs")





