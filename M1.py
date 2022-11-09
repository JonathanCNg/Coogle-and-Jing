import os
import json
import nltk
from nltk.corpus import stopwords, words
nltk.download('stopwords')
nltk.download('words')
from unicodedata import category
import sys
import pickle

directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]
stop_words = set(stopwords.words('english'))
eng_words = set(words.words())
codepoints = range(sys.maxunicode + 1)
punctuation = {c for i in codepoints if category(c := chr(i)).startswith("P")}  #implemented with guidance from: https://stackoverflow.com/questions/60983836/complete-set-of-punctuation-marks-for-python-not-just-ascii


index = {}

for d in directs:
    directory = os.fsencode(d)
    for file in os.listdir(directory):
        fname = os.fsdecode(file)
        f = open(d+"/"+fname, "r")
        data = json.load(f)
        f.close()
        tokens = nltk.word_tokenize(data['content'])
        tokens_cleaned = [word.lower() for word in tokens if word.lower() not in stop_words and word.lower() not in punctuation and word.lower() in eng_words]
        for token in tokens_cleaned:
            if token in index.keys():
                if fname in index[token].keys():
                    index[token][fname] += 1
                else:
                    index[token][fname] = 1
            else:
                index[token] = {fname:1}
        print(fname, " is Indexed")
    print(d, " is done")
# file = open("index", "wb")
# pickle.dump(index, file)
# file.close()
print("Unique ")

