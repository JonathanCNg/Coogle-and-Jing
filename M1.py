import os
import json
import nltk
import pickle
import math
from bs4 import BeautifulSoup
from scraper import is_valid
from collections import OrderedDict

# Jon: Feel free to comment in whichever one you want. They're just different collections of domains, some smaller so that w can test easily.
# directs = os.listdir("DEV")
# directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]
directs = ["www_informatics_uci_edu"]

for i in range(len(directs)):
    directs[i] = "DEV/" + directs[i]

index = {}
total_pages = 0
word_count = {}
ps = nltk.stem.PorterStemmer()

print("\n" + "{:<50}".format("URL") + "PROGRESS")

for d in directs:
    directory = os.fsencode(d)
    counter = 0
    files = os.listdir(directory)
    total_pages += len(files)
    checksums = {}
    for file in files:
        fname = os.fsdecode(file)
        f = open(d+"/"+fname, "r")
        data = json.load(f)
        f.close()
        url = data['url']
        try:
            # TODO: Figure out whether we're supposed to use is_valid and whether our is_valid is too aggressive
            if is_valid(url):
                is_dup = False
                # TODO: What happens when we use BeautifulSoup on non-HTML? 🤔
                soup = BeautifulSoup(data['content'], 'html.parser').get_text(' ', strip=True)
                # TODO: Make tokenizer than works only for alphanumeric (NLTK includes symbols and contractions)
                tokens = nltk.word_tokenize(soup)
                checksum = sum(ord(char) for char in "".join(tokens)) #checks for dupes
                if checksum in checksums.keys():
                    is_dup = True
                if is_dup == False:
                    checksums[checksum] = url
                    word_count[url] = len(tokens)

                    for token in tokens:
                        token = ps.stem(token)

                        if token in index.keys():
                            if url in index[token].keys():
                                index[token][url] += 1
                            else:
                                index[token][url] = 1
                        else:
                            index[token] = {url:1}
                
            counter += 1
            print("\r" + "{:<50}".format(d) + "| ", end="")
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
for token in index:
    idf = math.log(total_pages/len(index[token]))
    for url in index[token]:
        index[token][url] = index[token][url]/word_count[url]*idf
# alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# for l in alpha:
#     i = 0

file = open("index", "wb")
pickle.dump(index, file)
file.close()
# with open("delete_me.json", "w") as f: # Jon: I commented this out because the output is so large, we cannot even view it. Feel free to uncomment for small test batches.
#     json.dump(index, f)
with open("output.txt", "w") as f:
    f.write("# of Indexed Documents: " + str(total_pages) + "\n")
    f.write("# of Unique Tokens: " + str(len(index)) + "\n")
    f.write("Size of Index on Disk: " + str(os.path.getsize("index")//1000) + " KB")

with open("output.txt", "r") as f:
    print("\n ~ STATS ~ ")
    for line in f:
        print(line, end="")
    print()

# print(index) # Jon: I commented this out because the output is too large



