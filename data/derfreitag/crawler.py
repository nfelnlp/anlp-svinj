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

if __name__ == "__main__":
    counter = 1
    d_str = '/home/himbiss/news-please-repo/data/2018/01/24/freitag.de'
    for f_path in os.listdir(d_str):
        if f_path.endswith('.json'):
            with open(os.path.join(d_str, f_path)) as f:
                d = json.load(f)
                try:
                    text = bp_extract(d['url'])
                    path = 'data/'+str(counter)+'.txt'
                    with open(path, 'w+') as u:
                        with open('derfreitag.csv', 'a+') as csvfile:
                            print(d['url'])
                            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            sent_tokenize_list = sent_tokenize(text, language='german')
                            for sent in sent_tokenize_list:
                                u.write(str(sent)+'\n')
                            ts = time.time()
                            ts_format = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                            writer.writerow([path, d['url'], ts_format])
                            counter += 1
                except socket.timeout:
                    print('Caught socket timeout!')
