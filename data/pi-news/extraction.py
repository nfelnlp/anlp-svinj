from extract_article import extract_article
from boilerpipe.extract import Extractor
import re
import os
import urllib


def extract_month(month_url, start_num=1, end_num=10000):
    num = start_num

    already_visited = []

    while True:
        print(num)
        
        url = month_url + "page/" + str(num)
        try:
            response = urllib.request.urlopen(url)
        except Exception:
            break
        html = response.read().decode("utf8", errors="replace")
        #remove links that aren't part of the archive
        regex = r"Monatliche\sArchive:"
        for n, line in enumerate(html.split("\n")):
            match = re.search(regex, line)
            if match:
                break

            
        without_top_links = ""
        for line in html.split("\n")[(n+1):]:
            without_top_links += line + "\n"
        regex = r"<span\sclass=\"pages\">"
        #only_archive = ""
        #for line in without_top_links.split("\n"):
        #    match = re.search(regex, line)
        #    if match:
        #        break
        #    only_archive += line + "\n"
        only_archive = without_top_links
        
        
        links = re.findall(r"<h3\sclass=\"entry-title\std-module-title\"><a\shref=\"(.*?)\"", without_top_links)
        
        for link in links:
            print(link)
            if not link.startswith(month_url) or link in already_visited:
                continue
            already_visited.append(link) #the extracted html might contain duplicates of urls
            try:
                text, metadata = extract_article(link)
                match = re.match(r"http://www.pi-news.net/\d{4}/\d{2}/(.*?)/", link)
                text_file_name = os.path.join("pi_texts", match.group(1))
                with open(text_file_name, "w") as textfile:
                    textfile.write(text)
                with open("metadata_pi.csv", "a") as metafile:
                    author, date, keywords = metadata
                    if date:
                        date_str = str(date.year) + "-" + str_two_places(date.month) + "-" + str_two_places(date.day)
                    else:
                        date_str = "None"
                    line = text_file_name +\
                        " " +\
                        link +\
                        " " +\
                        date_str +\
                        " " +\
                        "|" + str(author) + "|" +\
                        " " +\
                        str(None) +\
                        " " +\
                        "|radically right|" +\
                        " |"
                    for keyword in keywords:
                        line += keyword + " "
                    if keywords != []:
                        line = line[:-1]
                    line += "|\n"
                    metafile.write(line)
            except Exception as e:
                print(e)
                
        
        if links == [] or num == end_num:
            break

        num += 1


def str_two_places(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


#extract_month("http://www.pi-news.net/2018/01/")

#extract_month("http://www.pi-news.net/2017/12/", start_num=14)
#extract_month("http://www.pi-news.net/2017/11/")
#extract_month("http://www.pi-news.net/2017/10/")
#extract_month("http://www.pi-news.net/2017/09/", start_num=19)
#extract_month("http://www.pi-news.net/2017/08/")
#extract_month("http://www.pi-news.net/2017/07/")
#extract_month("http://www.pi-news.net/2017/06/")
extract_month("http://www.pi-news.net/2017/05/", start_num=14)
extract_month("http://www.pi-news.net/2017/04/")
extract_month("http://www.pi-news.net/2017/03/")
extract_month("http://www.pi-news.net/2017/02/")
extract_month("http://www.pi-news.net/2017/01/")


