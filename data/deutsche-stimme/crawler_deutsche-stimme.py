import csv
import re
from urllib import request
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
from nltk.tokenize import sent_tokenize


def get_metadata(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        date_raw = re.findall('\d{4}\/\d{2}\/\d{2}', url)
        date = re.sub('\/','-',str(date_raw[0]))
        print(date)

        author = None
        #print(author)

        categories = None
        #print(categories)

        title_raw = soup.find("title").get_text().strip()
        title = re.sub(' ','-',str(title_raw))[:30]

    return date, author, categories, title


def write_to_files(text, url, art_id):
    with open('deutsche-stimme.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        publ_date, author, categories, title_str = get_metadata(url)
        art_id = str(art_id).zfill(4)
        filename = 'articles/{}_{}.txt'.format(art_id, title_str)

        with open(filename, 'w') as art:
            sent_tokenized = sent_tokenize(text, language='german')
            for sent in sent_tokenized:
                art.write(str(sent) + '\n')
            writer.writerow([filename, url, publ_date, author, categories])


def traverse(outlet_url, num=4000):
    retrieved = 0
    page = 1
    while retrieved < num:

        if page < 2:
            page_url = outlet_url
        else:
            page_url = "{}page/{}".format(outlet_url, page)

        extractor = Extractor(extractor='KeepEverythingExtractor', url=page_url)
        html = extractor.getHTML()

        links = re.findall(r"<A\shref=\".*de\/(\d{4}\/\d{2}\/\d{2}\/.*)\"\s", html)

        for link in links:
            try:
                art_url = outlet_url + link
                extr = Extractor(extractor='ArticleExtractor', url=art_url)
                text = extr.getText()
                retrieved += 1
                write_to_files(text, art_url, retrieved)
                print("Extracted {}: {}".format(retrieved, art_url))

            except Exception as e:
                print(e)
        page += 1


if __name__ == "__main__":
    traverse('http://deutsche-stimme.de/')