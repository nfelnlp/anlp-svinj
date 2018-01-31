import csv
import re
from urllib import request
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
from nltk.tokenize import sent_tokenize


def get_metadata(url):
    with request.urlopen(url) as response:
        html = response.read()
        html_text = html.decode("utf8")
        soup = BeautifulSoup(html, 'html.parser')
        date_raw = soup.find("span",class_="date").get_text()
        date_no_space = re.findall(r'\s*(.*?)\W',date_raw)
        date = date_no_space[2] + "-" + date_no_space[1] + "-" + date_no_space[0]
        #print(date)

        author = soup.find("link", rel="author").get('href')
                          
        #print(author)
        
        category_check = re.search(r"<body\sclass=\"artikel\s(.*?)\s",html_text)
        categories =  category_check.group(1)
       
        title = soup.find("meta", property="og:title").get("content")
        
        #print(title)

    return date, author, categories, title      


def traverse(outlet_url, num=5000):
    retrieved = 0
    page = 1
    while retrieved < num:
        current_url = "{}?page={}".format(outlet_url, page)
        #print(current_url)
        extractor = Extractor(extractor='KeepEverythingExtractor', url=current_url)
        html = extractor.getHTML()
        #print(html)
        link1 = re.findall(r"<A\shref=\"/artikel/(\d{4}/\d{2}/.*?)\"",html)
        #print(link1)
        links = set(link1)
        #print(links)
        for link in links:
            try:
                art_url = 'https://jungle.world/artikel/' +link
                #print(art_url)
                extr = Extractor(extractor='ArticleExtractor', url=art_url)
                text = extr.getText()
                #print(text)
                retrieved += 1
                write_to_files(text, art_url, retrieved)
                print("Extracted {}: {}".format(retrieved, art_url))
            except Exception as e:
                print(e)
        page += 1


def write_to_files(text, url, art_id,):
    with open('jungle.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        publ_date, author, categories, title_str = get_metadata(url)
        art_id = str(art_id).zfill(4)
        filename = 'articles/{}_{}.txt'.format(art_id, title_str)

        with open(filename, 'w') as art:
            sent_tokenized = sent_tokenize(text, language='german')
            for sent in sent_tokenized:
                art.write(str(sent) + '\n')
            writer.writerow([filename, url, publ_date, author, categories,[]])


if __name__ == "__main__":
    traverse('https://jungle.world/node')
    
    # https://jungle.world/node?page=1



			