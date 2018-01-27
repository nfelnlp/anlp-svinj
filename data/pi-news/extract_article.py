import re
from newsplease import NewsPlease
import urllib


def keyword_from_link(link):
    keyword_regex = r">([^<]+)<"
    match = re.search(keyword_regex, link)
    if match:
        return match.group(1)
    else:
        raise Exception


def extract_keywords(url):
    response = urllib.request.urlopen(url)
    content = response.read().decode("utf-8", errors="replace")
    line_regex = r"<span>SCHLAGWORTE</span>"
    for n, line in enumerate(content.split("\n")):
        match = re.search(line_regex, line)
        if match:
            break
    link_regex = r"<a\s.*?/a>"
    link_list = re.findall(link_regex, line)
    keywords = list(map(keyword_from_link, link_list))

    return keywords

def extract_author(text):
    ret_text = ""
    lines = text.split("\n")
    author = None
    
    for n, line in enumerate(lines):
        author_regex = r"Von\s(\w+\s\w+)\s\|\s(.*)"
        match = re.match(author_regex, line)
        if match:
            author = match.group(1)
            rest_line = match.group(2)
            ret_text += rest_line + "\n"
            break
        else:
            ret_text += line + "\n"

    for line in lines[(n+1):]:
        ret_text += line + "\n"

    return author, ret_text




def extract_article(url):
    article = NewsPlease.from_url(url)
    date = article.date_publish
    author, text = extract_author(article.text)
    keywords = extract_keywords(url)

    metadata = author, date, keywords

    return text, metadata


