import nltk 
from nltk.tokenize import RegexpTokenizer
import pandas as pd
	

# Calculate total length of the article ( words )	
def count(article):
	# Prefilter for the words
	tokenizer = RegexpTokenizer(r'\w+')
	
	#Only words list
	word_list = tokenizer.tokenize(article)
	
	words_len = len(word_list)
	return words_len 

def add_feature(df):
	art_length =[]
		# Retrieve the text data from the dataframe
	articles = df["text"].tolist()
	
	
	# sending each article at a time for count
	for filename in articles:
		list1 = (count(filename))
		art_length.append(list1)
	df["art_len"] = pd.Series(art_length)
	
	return df

