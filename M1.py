import os
import json
import nltk
import pickle
from bs4 import BeautifulSoup
from scraper import is_valid

directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]

for i in range(len(directs)):
    directs[i] = "DEV/" + directs[i]

index = {}

ps = nltk.stem.PorterStemmer()

for d in directs:
    directory = os.fsencode(d)
    for file in os.listdir(directory):
        fname = os.fsdecode(file)
        f = open(d+"/"+fname, "r")
        data = json.load(f)
        f.close()
        url = data['url']
        if is_valid(url):
            soup = BeautifulSoup(data['content'], 'html.parser').get_text(' ', strip=True)
            tokens = nltk.word_tokenize(soup)
            for token in tokens:
                token = ps.stem(token)
                if token in index.keys():
                    if url in index[token].keys():
                        index[token][url] += 1
                    else:
                        index[token][url] = 1
                else:
                    index[token] = {url:1}
            else:
                print("skipping", url)
            print(fname, "AKA", url, " is Indexed")
    print(d, " is done")
file = open("index", "wb")
pickle.dump(index, file)
file.close()
# print(index)

# TODO: Make tokenizer than works only for alphanumeric (NLTK includes symbols and contractions)