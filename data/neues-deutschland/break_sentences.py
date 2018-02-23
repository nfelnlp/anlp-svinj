from nltk.tokenize import sent_tokenize
import os

append_break = lambda x : x + "\n"

for art_file in os.listdir('./nd_texts'):
    with open(os.path.join("./nd_texts", art_file), "r") as article:
        text = "".join(list(map(append_break, sent_tokenize(article.read()))))
    with open(os.path.join("./nd_texts", art_file), "w") as article:
        article.write(text)
    
