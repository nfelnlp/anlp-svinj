from boilerpipe.extract import Extractor
import re


def remove_support_request(text):
    ret_text = ""
    paywall = False
    for line in text.split("\n"):
        if not paywall:
            match = re.match(r"Unterstütze\sdas\snd\smit\seinem\smonatlichen\sBeitrag", line)
            if match:
                paywall = True

        if not paywall:
            match = re.match(r"(Foto:.*|Schlagwörter\szu\sdiesem\sArtikel.*|Lesedauer:|[0-9]{2}\.[0-9]{2}\.[0-9]{4})", line)
            if not match:
                ret_text += line + "\n"
            
        if paywall:
            match = re.match("r(Turnus|Vielleicht\sspäter)", line)
            if match:
                paywall = False

    return ret_text[:-1]

def actual_paywall(text):
    ret_text = ""
    for line in text.split("\n"):
        match = re.search(r"(Warum\sendet\sdieser\sText\sdenn\sjetzt\sschon?|ndPlus)", line)
        if match:
            return ret_text[:-1]
        else:
            ret_text += line + "\n"
    return ret_text

def extract_metadata(url):
    extractor = Extractor(extractor='KeepEverythingExtractor', url=url)
    text = extractor.getText().split("\n")
    author = None
    date = None
    keywords = []
    find_keywords = False
    for line in text:
        #author
        match = re.match("Von\s(\w+\s\w+)(,\s[\s\w]*$|$)", line)
        if match:
            author = match.group(1)
            continue

        #date
        match = re.match("([0-9]{2}\.[0-9]{2}\.[0-9]{4})$", line)
        if match:
            date = match.group(1)
            continue

        #keywords
        if find_keywords:
            match = re.match("Hat\sIhnen\sdieser\sArtikel\sgefallen.*", line)
            if match:
                find_keywords = False
                continue
            else:
                keywords.append(line) 
            
        match = re.match("Schlagwörter zu diesem Artikel:", line)
        if match:
            find_keywords = True
        
    return author, date, keywords


def extract_text(url):
    extractor = Extractor(extractor='ArticleExtractor', url=url)
    return actual_paywall(remove_support_request(extractor.getText()))


def extract_article(url):
    metadata = extract_metadata(url)
    text = extract_text(url)
    return text, metadata

