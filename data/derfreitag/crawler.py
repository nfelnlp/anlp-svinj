import sys
import csv
import os
import time
import json
import socket
import datetime
from urllib.error import HTTPError
from urllib import request
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
from nltk.tokenize import sent_tokenize
from newsplease import NewsPlease

def bp_extract(url):
    extr = Extractor(extractor='ArticleExtractor', url=url)
    return extr.getText()

def prepare_authors(authors):
    string = "['" + authors[0] + "'"
    for author in authors[1:]:
        string += ",'" + author + "'"
    string += "]"
    return string

if __name__ == "__main__":
    counter = 1
    d_str = '/home/himbiss/news-please-repo/data/2018/01/24/freitag.de'
    for f_path in os.listdir(d_str):
        if f_path.endswith('.json'):
            with open(os.path.join(d_str, f_path)) as f:
                d = json.load(f)
                if d['date_publish']:
                    try:
                        text = bp_extract(d['url'])
                        path = 'data/'+str(counter)+'.txt'
                        with open(path, 'w+') as u:
                            with open('derfreitag.csv', 'a+') as csvfile:
                                print(d['url'])
                                publish_date = d['date_publish'].split()[0]
                                authors = prepare_authors(d['authors'])
                                categories = 'None'

                                writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                sent_tokenize_list = sent_tokenize(text, language='german')
                                for sent in sent_tokenize_list:
                                    u.write(str(sent)+'\n')

                                writer.writerow([path, d['url'], publish_date, authors, categories])
                                counter += 1
                    except socket.timeout:
                        print('Caught socket timeout!')
