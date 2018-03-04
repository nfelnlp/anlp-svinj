import nltk 
from nltk.tokenize import RegexpTokenizer
import pandas as pd


	# calculates the average sentence length of article upto 2 decimal place	
def count(article):
	# Prefilter for the words
	tokenizer = RegexpTokenizer(r'\w+')
	# list of the only words in the article 
	word_list = tokenizer.tokenize(article)
	words_len = len(word_list)
	# list of all the sentences in the article
	sents_list = nltk.sent_tokenize(article)
	sent_len = words_len/len(sents_list)
	# rounding the decimal to 2 places
	f_sent_len = format(sent_len, '0.2f')
	return f_sent_len

def add_feature(df):
	#Retrieve the text data from the dataframe
	articles = df["text"].tolist()
	sent_length=[]
	#sending each article at a time for count
	for filename in articles:
		list1 = (count(filename))
		sent_length.append(list1)	
	df["sent_len"] = pd.Series(sent_length)
	return df

