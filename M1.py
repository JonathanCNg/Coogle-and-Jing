import os
import json
import nltk
import pickle
import math
from bs4 import BeautifulSoup
from scraper import is_valid

# directs = os.listdir("DEV")
# directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]
directs = ["www-db_ics_uci_edu"]

for i in range(len(directs)):
    directs[i] = "DEV/" + directs[i]

index = {}
page_count = {} # Key is a token, value is a set of urls
total_pages = 0
word_count = {}
ps = nltk.stem.PorterStemmer()

for d in directs:
    directory = os.fsencode(d)
    counter = 0
    files = os.listdir(directory)
    total_pages += len(files)
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
                word_count[url] = len(tokens)

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

# TODO: uncomment this after MS1 ("for MS1, add only the term frequency" )
# for token in index:
#     idf = math.log(total_pages/len(page_count[token]))
#     for url in index[token]:
#         index[token][url] = index[token][url]/word_count[url]*idf

file = open("index", "wb")
pickle.dump(index, file)
file.close()
# with open("delete_me.json", "w") as f:
#     json.dump(index, f)
with open("output.txt", "w") as f:
    f.write("# of Indexed Documents: " + str(len(page_count)) + "\n")
    f.write("# of Unique Tokens: " + str(len(index)) + "\n")
    f.write("Size of Index on Disk: " + str(os.path.getsize("index")//1000) + " KB")

with open("output.txt", "r") as f:
    print("\n ~ STATS ~ ")
    for line in f:
        print(line, end="")

# print(index)

# TODO: Make tokenizer than works only for alphanumeric (NLTK includes symbols and contractions)
# TODO: Figure out whether we're supposed to use is_valid and whether our is_valid is too aggressive
# TODO: What happens when we use BeautifulSoup on non-HTML? 🤔