import os
import json
import nltk
import pickle
import math
from bs4 import BeautifulSoup
from scraper import is_valid
from collections import OrderedDict
from shutil import rmtree
import time

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))


def dump_index(index):
    print("\tEmptying Index in Memory")
    keys = sorted(index.keys())
    al_index = {}
    for i, key in enumerate(keys):
        if key[0] in alpha:
            # Open disk index to memory!
            if len(al_index) == 0:
                f = open("index/index"+key[0], 'rb')
                al_index = pickle.load(f)
                f.close()
            
            # Append to disk index loaded to memory!
            if key not in al_index:
                al_index[key] = index[key]
            else:
                for k, v in index[key].items():
                    al_index[key][k] = v
            
            # Save changes to disk index!
            if (i+1) >= len(keys) or keys[i+1][0] != key[0]:
                f = open("index/index"+key[0], 'wb')
                pickle.dump(al_index, f)
                f.close()
                al_index = {}

start_time = time.time()
# Jon: Feel free to comment in whichever one you want. They're just different collections of domains, some smaller so that w can test easily.
directs = os.listdir("DEV")
# directs = ["www-db_ics_uci_edu", "www_informatics_uci_edu", "www_cs_uci_edu"]
# directs = ["www_cs_uci_edu"]
if os.path.exists("index"):
    rmtree("index")

for i in range(len(directs)):
    directs[i] = "DEV/" + directs[i]

os.makedirs("./index/")
alpha = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for a in alpha:
    f = open("index/index"+a, 'wb')
    edict = {}
    pickle.dump(edict, f)
    f.close()

index = {}
total_pages = 0
word_count = {}
ps = nltk.stem.PorterStemmer()

print("\n" + "{:<50}".format("URL") + "PROGRESS")


dump_countdown = 1000000   # Decrements by 1 each time a new url is added to a token, which is a good proxy for the size of the index
for d in directs:
    directory = os.fsencode(d)
    counter = 0
    files = os.listdir(directory)
    total_pages += len(files)
    checksums = {}
    for file in files:
        if dump_countdown <= 0:
            dump_index(index)
            index = {}
            dump_countdown = 1000000
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
                soup = BeautifulSoup(data['content'], 'html.parser')
                if soup.find(): # Checks if there's any html in the file lol
                    soup_text = soup.get_text(' ', strip=True)
                    # TODO: Make tokenizer than works only for alphanumeric (NLTK includes symbols and contractions)
                    tokens = nltk.word_tokenize(soup_text)
                    word_count[url] = len(tokens)
                    for token in tokens:
                        token = ps.stem(token)

                        if token not in index.keys():
                            index[token] = {}
                        
                        if url in index[token].keys():
                            index[token][url] += 1
                        else:
                            index[token][url] = 1
                            dump_countdown -= 1
                            
                    else:
                        index[token] = {url:1}

                    # For important words
                    important_tags = {'title':5, 'h1':4, 'h2':3, 'h3':2, 'b':1, 'strong':1}
                    for tag in important_tags:
                        important = soup.find_all(tag)
                        for item in important:
                            item_text = item.get_text(' ', strip=True)
                            item_tokens = nltk.word_tokenize(item_text)
                            for token in item_tokens:
                                token = ps.stem(token)
                                if token not in index:
                                    index[token] = {}
                                if url not in index[token]:
                                    index[token][url] = 0
                                index[token][url] += important_tags[tag]


            counter += 1
            print("\r" + "{:<50}".format(d) + "| ", end="")
            out_of_10 = counter*10//len(files)
            for i in range(out_of_10):
                print("# ", end="")
            for i in range(10-out_of_10):
                print("  ", end="")
            print("| " + str(counter) + "/" + str(len(files)), end="")
        except Exception as e:
            print("\nEXCEPTION THROWN: Tried", url, "got", type(e).__name__, ":", e.args)

        
    print()

dump_index(index)

time_convert(time.time() - start_time)

for a in alpha:
    match = True
    f = open("index/index"+a, "rb")
    index = pickle.load(f)
    f.close()
    for token in index.keys():
        if token[0] != a:
            match = False
        if type(index[token]) is dict:
            idf = math.log(total_pages/len(index[token]))
            for url in index[token]:
                if word_count[url] == 0:
                    index[token][url] = 0
                else:
                    index[token][url] = index[token][url]/word_count[url]*idf
    f = open("index/index"+a, "wb")
    pickle.dump(index, f)
    f.close()
    print("file has all", a, ":", match)
    if match == False:
        print(index.keys())
with open("output.txt", "w") as f:
    f.write("# of Indexed Documents: " + str(total_pages) + "\n")
    f.write("# of Unique Tokens: " + str(len(index)) + "\n")
    f.write("Size of Index on Disk: " + str(os.path.getsize("index")//1000) + " KB")

with open("output.txt", "r") as f:
    print("\n ~ STATS ~ ")
    for line in f:
        print(line, end="")
    print()

time_convert(time.time() - start_time)


