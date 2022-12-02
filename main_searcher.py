import json
import pickle
import shelve
import math
import nltk
from flask import Flask, request, render_template # https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/
import time # https://www.codespeedy.com/how-to-create-a-stopwatch-in-python/

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return ("Time Lapsed = {0:.3f} secs".format(sec))

# Flask constructor
app = Flask(__name__)  
 

file = shelve.open("shelf_file")

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    start_time = time.time()
    if request.method == "POST":
        # getting input with name = fname in HTML form
        query = request.form.get("query")
        
        if query != "":
            ps = nltk.stem.PorterStemmer()

            # getting input with name = lname in HTML form
            query_tokens = list(set(sorted(nltk.word_tokenize(query))))

            # Separate tokens into single char and multi char
            single_char_tokens = []
            multi_char_tokens = []
            for token in query_tokens:
                stemmed_token = ps.stem(token)
                if len(stemmed_token) == 1:
                    single_char_tokens.append(stemmed_token)
                elif len(stemmed_token) >= 2:
                    multi_char_tokens.append(stemmed_token)

            # Declare important variables!
            urls = {}
            index = {}

            # Add points for single char tokens
            if len(single_char_tokens) > 0:
                with open("index2/index_singles", "rb") as f:
                    index = pickle.load(f)
                for q_token in single_char_tokens:
                    if q_token in index:
                        for url in index[q_token].keys():
                            urls[url] = float(urls.get(url, 0)) + float(index[q_token][url])

            # For multi char tokens...
            index_a = None
            for q_token in multi_char_tokens: 
                
                # Opens the right index!
                if q_token[0:2] != index_a:
                    index_a = q_token[0:2]
                    with open("index2/index_" + index_a, "rb") as f:
                        index = pickle.load(f) 
                
                # Add them points 😎
                if q_token in index:
                    for url in index[q_token].keys():
                        urls[url] = float(urls.get(url, 0)) + float(index[q_token][url])

            # Sort by points!
            urls_sorted = sorted(urls.items(), key=lambda item: item[1], reverse=True)
            
            output = ""
            for i, url in enumerate(urls_sorted[0:min(5,len(urls_sorted))]):
                output += "<p> #" + str(i+1) + " | <a href=\"" + url[0] + "\" target=\"_blank\">"+ url[0] + "</a></p>"
            
            time_html = "<p>" + time_convert(time.time() - start_time) + "</p>"

            return render_template("form.html") + time_html + output

        # return "Your name is "+first_name + last_name
    return render_template("form.html")
 
if __name__=='__main__':
    app.run()

# while True:
#     query = input("Search:")
#     tokens = nltk.word_tokenize(query)
#     urls = []
#     ps = nltk.stem.PorterStemmer()
#     for token in tokens:
#         t = ps.stem(token)
#         urls.append(set(index[t].keys()))
#     url_int = set.intersection(*urls) #<-- finds intersection of all list in URLs
#     url_int_sorted = sorted(url_int, key = lambda url:sum([index[ps.stem(token)][url] for token in tokens]), reverse=True)
#     print("Results")
#     print("-------")
#     for url in url_int_sorted[0:5]:
#         print(url)
