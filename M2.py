import pickle
import math
import nltk
from flask import Flask, request, render_template # https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/
import time # https://www.codespeedy.com/how-to-create-a-stopwatch-in-python/

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  ms = sec / 1000
#   return "Time Lapsed = {0} sec".format(sec)
  return "Time Lapsed = {0} ms".format(ms)
file = open("index", "rb")
index = pickle.load(file)
file.close()

# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        query = request.form.get("query")
        
        if query != "":
            start_time = time.time()

            # getting input with name = lname in HTML form
            tokens = nltk.word_tokenize(query)
            urls = []
            ps = nltk.stem.PorterStemmer()
            for token in tokens:
                t = ps.stem(token)
                urls.append(set(index[t].keys()))
            url_int = set.intersection(*urls) #<-- finds intersection of all list in URLs
            url_int_sorted = sorted(url_int, key = lambda url:sum([index[ps.stem(token)][url] for token in tokens]), reverse=True)
            
            output = ""
            for i, url in enumerate(url_int_sorted[0:5]):
                output += "<p> #" + str(i+1) + " | <a href=\"" + url + "\" target=\"_blank\">"+ url + "</a></p>"
            
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
