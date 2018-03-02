import baseline as base
import re
import pandas as pd

def add_feature(df):
	quoted_ratios=[]
	articles=df["text"].tolist()
	for article in articles:
		text_length=len(article.split(" "))
		quoted=re.findall(r'("[\W\w]+?"|„[\W\w]+?“|»[\W\w]+?«|«[\W\w]+?»)',article)
		length_quoted=0
		for item in quoted:
#			print(item)
			length=len(item.split(" ")) 
			if length > 2:
				length_quoted+=length
		quoted_ratio=length_quoted/text_length
		quoted_ratios.append(quoted_ratio)
	
	df["quoted_speech"]=pd.Series(quoted_ratios)
	
	return df
