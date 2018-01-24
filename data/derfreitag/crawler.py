import sys
import csv
import os
import time
import json
import datetime
from urllib.error import HTTPError
from urllib import request
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
from nltk.tokenize import sent_tokenize
from newsplease import NewsPlease


def make_soup(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.find_all('font'))


def bp_extract(url):
    extr = Extractor(extractor='ArticleExtractor', url=url)
    return extr.getText()

def years_extract(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        links = ['https://phinau.de/jf-archiv/' + a.get('href') for a in soup.find_all('a')]
        return links[1:]
    
    
def months_extract(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        links = ['https://phinau.de/jf-archiv/archiv/' +  a.get('href') for a in soup.find_all('a')]
        return links[1:]


    
if __name__ == "__main__":
    counter = 1
    d_str = '/home/himbiss/news-please-repo/data/2018/01/24/freitag.de'
    for f_path in os.listdir(d_str):
        if f_path.endswith('.json'):
            with open(os.path.join(d_str, f_path)) as f:
                d = json.load(f)
                text = d['text']
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
