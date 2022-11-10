import os
import json
import nltk
import pickle
from bs4 import BeautifulSoup
from scraper import is_valid

directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]
directs = os.listdir("DEV")

for i in range(len(directs)):
    directs[i] = "DEV/" + directs[i]

index = {}
page_count = {} # Key is a token, value is a set of urls

ps = nltk.stem.PorterStemmer()

for d in directs:
    directory = os.fsencode(d)
    counter = 0
    files = os.listdir(directory)
    for file in files:
        fname = os.fsdecode(file)
        f = open(d+"/"+fname, "r")
        data = json.load(f)
        f.close()
        url = data['url']
        try:
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
            counter += 1
            # print("\r" + str(counter) + " " + fname + " AKA " + url + " is indexed".ljust(100)[:100], end="")
            print("\r" + "{:<50}".format(d) + " | ", end="")
            out_of_10 = counter*10//len(files)
            for i in range(out_of_10):
                print("# ", end="")
            for i in range(10-out_of_10):
                print("  ", end="")
            print("| " + str(counter) + "/" + str(len(files)), end="")
        except Exception as e:
            print("EXCEPTION THROWN: Tried", url, "got", e)
    print()

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