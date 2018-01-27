import csv
import re
import dateparser
from urllib import request
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
from nltk.tokenize import sent_tokenize


def get_metadata(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        meta_raw = soup.find("p", class_="entry_date").get_text()
        date_raw, author_raw = meta_raw.split('|')
        date_ger = re.match('.*\d{4}', date_raw).group(0)
        date = dateparser.parse(date_ger).date()
        # print(date)

        author = (author_raw.split(':'))[1].strip()
        # print(author)

        ctg_raw = soup.find("small", style="display:block").get_text()
        ctg_list = (ctg_raw.split(":"))[1].strip()
        categories = [c.strip() for c in ctg_list.split(",")]
        # print(categories)

    return date, author, categories


def traverse(outlet_url, num=3000):
    it = 42092
    retrieved = 0
    while retrieved < num:
        art_url = "{}?p={}".format(outlet_url, it)
        try:
            extr = Extractor(extractor='ArticleExtractor', url=art_url)
            text = extr.getText()
            write_to_files(text, art_url)
            print("Extracted {}: {}".format(it, art_url))
            retrieved += 1

        except Exception as e:
            print(e)
        it -= 1


def write_to_files(text, url):
    with open('nachdenkseiten.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        art_id = (url.split('='))[1]
        publ_date, author, categories = get_metadata(url)
        filename = 'articles/{}.txt'.format(art_id)

        with open(filename, 'w') as art:
            sent_tokenized = sent_tokenize(text, language='german')
            for sent in sent_tokenized:
                art.write(str(sent) + '\n')
            writer.writerow([filename, url, publ_date, author, categories])


if __name__ == "__main__":
    traverse('http://www.nachdenkseiten.de/')
