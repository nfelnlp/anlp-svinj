import sys
from urllib import request
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor


def make_soup(url):
    with request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.find_all('p'))


def bp_extract(url):
    extr = Extractor(extractor='ArticleExtractor', url=url)
    text = extr.getText()
    print(text)


if __name__ == "__main__":
    bp_extract(sys.argv[1])
