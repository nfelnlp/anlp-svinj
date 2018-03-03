import re
import operator
import pandas as pd
from nltk.corpus import stopwords

def ngrams(articles,n):
	stops=set(stopwords.words('german'))
	ngrams=[]
	for article in articles:
		tokens=re.split('\W',article)#.lower())
		uni=[x for x in tokens if not x in [""," ","\n"]]
		start=0
		end=n
		while end <= len(uni):
			ngram=uni[start:end]
# if intersection of stopwords and ngram words is not empty, ignore ngram, otherwise, add to list of ngrams
			if stops & set(ngram) == set():
				ngrams.append(tuple(ngram))
				print(ngram)
			start+=1
			end+=1			
	ngramdict={}	
	for ngram in ngrams: 
		if ngram in ngramdict:	#count ngrams
			ngramdict[ngram]+=1
		else:
			ngramdict[ngram]=1
	ngramdict_sorted=sorted(ngramdict.items(),key=operator.itemgetter(1))	#sort dictionary by value

	return ngramdict_sorted


def add_feature(df,uni_no,bi_no):
	list_of_vectors=[]
	df_train=df[df["split"]=="train"]
	articles_train=df_train["text"].tolist()
	unigrams_train=ngrams(articles_train,1)[-uni_no:]
	bigrams_train=ngrams(articles_train,2)[-bi_no:]
	most_common_ngrams=[x for x,y in unigrams_train]+[x for x,y in bigrams_train]
	articles=df["text"].tolist()
	c=1
	for article in articles:
#		print(c)
		c+=1
		unigrams=ngrams(list([article]),1)
		bigrams=ngrams(list([article]),2)
		vector_article=unigrams+bigrams
		vector_ngrams=[x for x,y in unigrams+bigrams]
		vectordict={}
		for ngram in most_common_ngrams:	#if ngram is most common ngrams, get count and add to dictionary
			if ngram in vector_ngrams:
				for tup in vector_article:
					if ngram==tup[0]:
						vectordict[ngram]=tup[1]
			else:
				vectordict[ngram]=0
		vector=list(vectordict.values())
		indices=[]
		for element in vector:
			if not element==0:
				indices.append(vector.index(element))
		list_of_vectors.append(vector)
	ngram_df=pd.DataFrame(list_of_vectors)
	df=pd.concat([df,ngram_df],axis=1)

	return df

