import sys
import csv
import re
import time
import datetime
from urllib.error import HTTPError
from urllib.error import URLError
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
    
    
def article_extract(url):
    sub_path = url.split("/")[-2]
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        links = [('https://phinau.de/jf-archiv/' + sub_path + "/" + a.get('href', ''), text_to_authors(a.text)) for a in soup.find_all('a')]
        return links[2:]


def months_extract(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        links = [('https://phinau.de/jf-archiv/' +  a.get('href', ''), text_to_date(a.text)) for a in soup.find_all('a')]
        return links[1:]

def text_to_authors(text):
    last_row = text.split('\n')[-1]
    findings = re.findall(r".*von(.*)", last_row)
    if len(findings) < 1:
        return "None"
    return "['" + findings[0] + "']"

def text_to_date(text):
    findings = re.findall(r".*(\d\d)\.\s?([a-zA-Z|ä|ö|ü|Ä|Ö|Ü]*)\s(\d\d\d\d)", text)
    if len(findings) < 1:
        return "1970-01-01"
    day, month, year = findings[0]
    month_to_digit = {"januar": "01",
                      "februar": "02",
                      "märz": "03",
                      "april": "04",
                      "mai": "05",
                      "juni": "06",
                      "juli": "07",
                      "august": "08",
                      "september": "09",
                      "septemer": "09", # they made a spelling mistake ;) 
                      "oktober": "10",
                      "november": "11",
                      "dezember": "12"}
    month = month_to_digit[month.lower()]
    return year + "-" + month + "-" + day
    



    
if __name__ == "__main__":
    counter = 1
    #years_urls = years_extract('https://jungefreiheit.de/service/archiv/')
    years_urls = ["https://phinau.de/jf-archiv/archiv.htm",
                  "https://phinau.de/jf-archiv/archiv98.htm",
                  "https://phinau.de/jf-archiv/archiv99.htm",
                  "https://phinau.de/jf-archiv/archiv00.htm",
                  "https://phinau.de/jf-archiv/archiv01.htm",
                  "https://phinau.de/jf-archiv/archiv02.htm",
                  "https://phinau.de/jf-archiv/archiv03.htm",
                  "https://phinau.de/jf-archiv/archiv04.htm",
                  "https://phinau.de/jf-archiv/archiv05.htm",
                  "https://phinau.de/jf-archiv/archiv06.htm",
                  "https://phinau.de/jf-archiv/archiv07.htm",
                  "https://phinau.de/jf-archiv/archiv08.htm",
                  "https://phinau.de/jf-archiv/archiv09.htm",
                  "https://phinau.de/jf-archiv/archiv10.htm",
                  "https://phinau.de/jf-archiv/archiv11.htm",
                  "https://phinau.de/jf-archiv/archiv12.htm",
                  "https://phinau.de/jf-archiv/archiv13.htm",
                  "https://phinau.de/jf-archiv/archiv14.htm",
                  "https://phinau.de/jf-archiv/archiv15.htm",
                  "https://phinau.de/jf-archiv/archiv16.htm",
                  "https://phinau.de/jf-archiv/archiv17.htm",
                  "https://phinau.de/jf-archiv/archiv18.htm",
                  ]
    for url in years_urls:
        months_urls = months_extract(url)
        try:
            for murl, date in months_urls:
                print(murl, date)
                article_urls = article_extract(murl)
                for aurl, author in article_urls:
                    text = bp_extract(aurl)
                    path = 'data/'+str(counter)+'.txt'
                    with open('jungefreiheit.csv', 'a+') as csvfile:
                        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        with open(path, 'w+') as f:
                            sent_tokenize_list = sent_tokenize(text, language='german')
                            for sent in sent_tokenize_list:
                                f.write(str(sent)+'\n')
                            writer.writerow([path, aurl, date, "None", "None"])
                            counter += 1
        except HTTPError:
            print('HTTP Error 404')
        except URLError:
            print('URL Error')
        except:
            print('unknown Error')

