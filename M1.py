import os
import json
import nltk
import pickle
from bs4 import BeautifulSoup
from scraper import is_valid

directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]
directs = ["www-db_ics_uci_edu"]

for i in range(len(directs)):
    directs[i] = "DEV/" + directs[i]

index = {}
page_count = {} # Key is a token, value is a set of urls

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

                if token not in page_count:
                    page_count[token] = {url}
                else:
                    page_count[token].add(url)

                if token in index.keys():
                    if url in index[token].keys():
                        index[token][url] += 1
                    else:
                        index[token][url] = 1
                else:
                    index[token] = {url:1}
            print(fname, "AKA", url, "is indexed")
        else:
            print("skipping", url)
    print(d, "is done")



for token in index:
    idf = 1/len(page_count[token])
    for url in index[token]:
        index[token][url] = index[token][url]*idf

file = open("index", "wb")
# pickle.dump(index, file)
with open("delete_me.json", "w") as f:
    json.dump(index, f)

file.close()
# print(index)

# TODO: Make tokenizer than works only for alphanumeric (NLTK includes symbols and contractions)
# TODO: Figure out whether we're supposed to use is_valid and whether our is_valid is too aggressive
# TODO: What happens when we use BeautifulSoup on non-HTML? 🤔