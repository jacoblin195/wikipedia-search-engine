#! /usr/bin/env python3
print('Content-type: text/html\n')

import pickle
import cgi
import nltk
from random import *
print("<!doctype html>")
print("<html>")
print("<head>")
print("<meta charset=\"UTF-8\">")
print("<title>Search Engine</title>")
print("</head>")

print("<body>")

print("<img src=\"logo.jpg\">")
print("<form action=\"retrieve.cgi\">")
print("<p style=\"margin: 0;\">Search</p>")
print("	<input type=\"text\" name=\"query\"><input type=\"submit\" value=\"search\">")
print("<input type=\"submit\" name=\"lucky\" value=\"Lucky\">")
print("</form>")

inverse_dict = pickle.load(open("inverse_dict.pkl", "rb"))
doc_dict = pickle.load(open("doc_dic.pkl", "rb"))

form = cgi.FieldStorage()

query = form.getfirst("query", "cocoa")

query = query.split()

stemmer = nltk.stem.PorterStemmer()

for idx,queryword in enumerate(query):
    query[idx] = queryword.lower()
    query[idx] = stemmer.stem(queryword)

number_of_docs = len(doc_dict.keys())


if "lucky" in form:

    randindex = randint(0, number_of_docs-1)
    docUrl = list(doc_dict.keys())[randindex]
    
    print("<p>"+doc_dict[docUrl][2]+"</p>\n")
    print("<p>"+docUrl+"</p>\n\n")
else:
    print("search")
    urlset = set()
    for queryword in query:
        word_urls = inverse_dict.get(queryword,{})
        for url in word_urls.keys():
            urlset.add(url)
    for docUrl in list(urlset):
        print("<p>" + doc_dict[docUrl][2] + "</p>\n")
        print("<p>" + docUrl + "</p>\n\n")

print("</body>")
print("</html>")

