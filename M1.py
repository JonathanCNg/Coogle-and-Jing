import os
import json
import nltk
import pickle
from bs4 import BeautifulSoup

directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]
directs = ["www_cs_uci_edu"]

for i in range(len(directs)):
    directs[i] = "DEV/" + directs[i]

print(directs)

index = {}

ps = nltk.stem.PorterStemmer()

for d in directs:
    directory = os.fsencode(d)
    for file in os.listdir(directory):
        fname = os.fsdecode(file)
        f = open(d+"/"+fname, "r")
        data = json.load(f)
        f.close()
        soup = BeautifulSoup(data['content'], 'html.parser').get_text(' ', strip=True)
        tokens = nltk.word_tokenize(soup)
        for token in tokens:
            token = ps.stem(token)
            if token in index.keys():
                if fname in index[token].keys():
                    index[token][fname] += 1
                else:
                    index[token][fname] = 1
            else:
                index[token] = {fname:1}
        print(fname, " is Indexed")
    print(d, " is done")
file = open("index", "wb")
pickle.dump(index, file)
file.close()
print(index)

