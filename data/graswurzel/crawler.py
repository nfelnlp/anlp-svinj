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
import charade
from nltk.tokenize import sent_tokenize
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def make_soup(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.find_all('font'))


headers = {'User-Agent': 'Mozilla/5.0'}

def bp_extract(url):
    request = urllib2.Request(url, headers=headers)
    connection = urllib2.urlopen(request)
    data = connection.read()
    encoding = connection.headers['content-type'].lower().split('charset=')[-1]
    encoding = charade.detect(data)['encoding']
 
    extr = Extractor(extractor='ArticleExtractor', url=url)
    return extr.getText().encode(encoding).decode('iso-8859-15')

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

def paragraph_match(p):
    regex = re.compile(r"\/\d+\/.*")
    anchors = p.find_all('a')
    return len(anchors) == 1 and regex.match(anchors[0].get('href', ''))
        

def extract_url_and_date(p):
    anchors = p.find_all('a')
    url = 'http://graswurzel.net' + anchors[0].get('href', '')

    spans = p.find_all('span')
    if len(spans) > 0:
        date_str = p.find_all('span')[0].text
        return (url, text_to_date(date_str))
    else:
        return (url, "1970-01-01")
    
def months_extract(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        links = [extract_url_and_date(p) for p in soup.find_all('p') if paragraph_match(p)]
        return links[1:]

def text_to_authors(text):
    last_row = text.split('\n')[-1]
    findings = re.findall(r".*von(.*)", last_row)
    if len(findings) < 1:
        return "None"
    return "['" + findings[0] + "']"

def text_to_date(text):
    findings = re.findall(r".*[\s]+([A-Za-z].*)[\s]+(\d\d\d\d)", text)
    if len(findings) < 1:
        return "1970-01-01"
    month, year = findings[0]
    month_to_digit = {"januar": "01",
                      "februar": "02",
                      "märz": "03",
                      "april": "04",
                      "mai": "05",
                      "juni": "06",
                      "juli": "07",
                      "august": "08",
                      "september": "09",
                      "oktober": "10",
                      "november": "11",
                      "dezember": "12",
                      "sommer": "07",
                      "winter": "11",
                      "herbst": "09",
                      "frühling": "02"}
    try:
        month = month_to_digit[month.lower().strip()]
        return year + "-" + month + "-01"
    except:
        return "1970-01-01"
    



    
if __name__ == "__main__":
    counter = 1
    years_urls = [("http://www.graswurzel.net/archiv/anarchismus.shtml", "Anarchismus"),
                  ("http://www.graswurzel.net/archiv/anti-akw.shtml", "Anti-AKW"), 
                  ("http://www.graswurzel.net/archiv/antifa.shtml", "Antifaschismus"), 
                  ("http://www.graswurzel.net/archiv/anti-gentech.shtml", "Anti-Gentech"), 
                  ("http://www.graswurzel.net/archiv/antimilitarismus.shtml", "Antimilitarismus"), 
                  ("http://www.graswurzel.net/archiv/antiparlamentarismus.shtml", "Antiparlamentarismus"), 
                  ("http://www.graswurzel.net/archiv/antisexismus.shtml", "Antisexismus/Feminismus"), 
                  ("http://www.graswurzel.net/archiv/buecher.shtml", "Bücher"), 
                  ("http://www.graswurzel.net/archiv/concert.shtml", "Concert for anarchy"), 
                  ("http://www.graswurzel.net/archiv/gewaltfreiheit.shtml", "Gewaltfreiheit"), 
                  ("http://www.graswurzel.net/archiv/gwr.shtml", "Graswurzelrevolution"), 
                  ("http://www.graswurzel.net/archiv/kunst_kultur.shtml", "Kunst & Kultur"), 
                  ("http://www.graswurzel.net/archiv/paedagogik.shtml", "Libertäre Pädagogik"), 
                  ("http://www.graswurzel.net/archiv/oekologie.shtml", "Ökologie"), 
                  ("http://www.graswurzel.net/archiv/oekonomie.shtml", "Öknomie"), 
                  ("http://www.graswurzel.net/archiv/transnationales.shtml", "Transnationales")]
    for url , category in years_urls:
        months_urls = months_extract(url)
        try:
            for aurl, date in months_urls:
                print(aurl, date)
                # cannot extract author
                author = "None"
                text = bp_extract(aurl)[:-2]
                path = 'data/'+str(counter)+'.txt'
                with open('graswurzel.csv', 'a+') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    with open(path, 'w+') as f:
                        sent_tokenize_list = sent_tokenize(text, language='german')
                        for sent in sent_tokenize_list[3:]:
                            f.write(str(sent)+'\n')
                        writer.writerow([path, aurl, date, "None", "None"])
                        counter += 1
        except HTTPError as e:
            print('HTTP Error:', e)
        except URLError as e:
            print('URL Error:', e)
        except Exception as e:
            print('unknown Error:', e)

