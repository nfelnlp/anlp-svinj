import sys
import csv
import time
import datetime
from urllib.error import HTTPError
from urllib import request
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
from nltk.tokenize import sent_tokenize


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
    years_urls = years_extract('https://phinau.de/jf-archiv/archiv.htm')
    for url in years_urls:
        months_urls = months_extract(url)
        try:
            for murl in months_urls:
                text = bp_extract(murl)
                path = 'data/'+str(counter)+'.txt'
                print(murl)
                with open('jungefreiheit.csv', 'a+') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    with open(path, 'w+') as f:
                        sent_tokenize_list = sent_tokenize(text, language='german')
                        for sent in sent_tokenize_list:
                            f.write(str(sent)+'\n')
                        ts = time.time()
                        ts_format = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([path, murl, ts_format])
                        counter += 1
        except HTTPError:
            print('HTTP Error 404')

