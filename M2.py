import pickle
import math
import nltk


file = open("index", "rb")
index = pickle.load(file)
file.close()
while True:
    queury = input("Search:")
    tokens = nltk.word_tokenize(queury)
    urls = []
    ps = nltk.stem.PorterStemmer()
    for token in tokens:
        t = ps.stem(token)
        urls.append(set(index[t].keys()))
    url_int = set.intersection(*urls) #<-- finds intersection of all list in URLs
    url_int_sorted = sorted(url_int, key = lambda url:sum([index[ps.stem(token)][url] for token in tokens]), reverse=True)
    print("Results")
    print("-------")
    for url in url_int_sorted[0:5]:
        print(url)
