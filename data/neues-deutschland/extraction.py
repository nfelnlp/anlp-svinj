from extract_article import extract_article
from boilerpipe.extract import Extractor
import re
import os


def category_extract(category_url, category, start_num=0, end_num=100):
    num = start_num

    while True:
        print(num)
        
        url = category_url + "?s=" + str(num)
        extractor = Extractor(extractor='KeepEverythingExtractor', url=url)
        html = extractor.getHTML()
        links = re.findall(r"<A\shref=\"(/artikel/.*?)\">", html)
        for link in links:
            try:
                article_url = "https://www.neues-deutschland.de" + link
                text, metadata = extract_article(article_url)
                match = re.match(r"/artikel/(.*?)\.html", link)
                text_file_name = os.path.join("nd_texts", match.group(1))
                with open(text_file_name, "w") as textfile:
                    textfile.write(text)
                with open("metadata_nd.csv", "a") as metafile:
                    author, date, keywords = metadata
                    if date:
                        date = date.split(".")
                        date_str = date[2] + "-" + date[1] + "-" + date[0]
                    else:
                        date_str = "None"
                    line = text_file_name +\
                        " " +\
                        article_url +\
                        " " +\
                        date_str +\
                        " " +\
                        "|" + str(author) + "|" +\
                        " " +\
                        category +\
                        " " +\
                        "|radically left|" +\
                        " |"
                    for keyword in keywords:
                        line += keyword + " "
                    if keywords != []:
                        line = line[:-1]
                    line += "|\n"
                    metafile.write(line)
            except Exception as e:
                print(e)
                
        num += 25
        
        if links == [] or num == end_num:
            break



category_extract("https://www.neues-deutschland.de/rubrik/politik/", "politics", start_num=0, end_num=1000)
category_extract("https://www.neues-deutschland.de/rubrik/wirtschaft-umwelt/", "economy/environment", start_num=0, end_num=1000)
category_extract("https://www.neues-deutschland.de/rubrik/bewegung/", "leftist_movement", start_num=0, end_num=1000)
