#!/usr/bin/env python3
#-*- coding:utf-8 -*-
	
import urllib.request
import re
from boilerpipe.extract import Extractor

def crawler(url,current_pos,counter):
	print(current_pos)
	link=urllib.request.urlopen(url)
	text=(link.read()).decode()	
	articles=re.findall(r'class="post-title"><a href=\"(.*?)\">',text)
	for match in articles:
		art_link=urllib.request.urlopen(match)
		art_text=(art_link.read()).decode()
		author=re.search(r'rel="author">(.*?)</a>',art_text).group(1)
		date=re.search(r'property="article:published_time" content="([-0-9]+)T',art_text).group(1)
		category=re.search(r'property="article:section" content="(.*?)" />',art_text).group(1)
		headline=re.search(r'itemprop="name headline">\s*([\w\W]+?)</h1>',art_text).group(1)
		print(headline)
		extr=Extractor(extractor='KeepEverythingExtractor',url=match)
		article=extr.getText()
		try:
			just_article=re.search(r'\geteilt([\s\S]+)\nAnzeige',article).group(1)
			fobj=open("compact"+str(counter)+".txt", "w")
			fobj.write(headline+"\n"+just_article)
			fobj.close()
			csv=open("compact.csv","a")
			csv.write("data/compact"+str(counter)+".txt"+","+match+","+date+","+author+","+category+"\n")
			csv.close()
			counter+=1		
		except AttributeError:
			pass
	while current_pos < 497:
		if not current_pos == 84:
			current_pos+=1
		else:
			current_pos+=2
		crawler('https://www.compact-online.de/thema/beitragsthemen/page/'+str(current_pos),current_pos,counter=counter)

crawler('https://www.compact-online.de/thema/beitragsthemen/',1,1)


