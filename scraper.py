from multiprocessing.resource_sharer import stop
import re
import random
from urllib.parse import urlparse
import urllib.parse
from xmlrpc.client import Boolean
import validators
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import string
import pickle
import tldextract
from urllib.parse import parse_qs


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    # Debugging Messages
    
    try:
        # Get all the links!
        content = resp.raw_response.content.decode("utf-8")
        
        
        


        # Filter for good links (that stay within our domain) and defrag!
        links = re.findall(r"href=[\'\"]{1,1}.*?[\'\"]{1,1}", content)
        real_links = []
        for link in links:
            link = link[6:-1] # Removes href
            if validators.url(link):
                real_links.append(urllib.parse.urldefrag(link)[0])
                
        return real_links
    except Exception as e:
        print("ERROR 🔥 in scraper.py.extract_next_links", e, "for", url)
        return []




def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv|php|sql"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False

        if re.match(r".*/feed/?$", parsed.path.lower()):
            # print("Stop 🛑 the feed at", url)
            return False
        
        if re.match(r"/wp-json/", parsed.path.lower()[0:9]):
            # print("Get outta here, JSON! \U0001F624 ", url)
            return False
        
        parameters = parse_qs(parsed.query)
        if "action" in parameters and "download" in parameters["action"]:
            # print("🚫 Prevented a download at", url)
            return False
        if "ical" in parameters and "1" in parameters["ical"]:
            # print("🚫 Prevented ical download at", url)
            return False

        allowed_subdomains = set(["ics", "cs", "informatics", "stat", "today"])
        allowed_today_path = "/department/information_computer_sciences/"

        authority = parsed.netloc.split('.')
        authority.reverse()

        if len(authority) < 3:
            return False

        domain, suffix = authority[1], authority[0]
        subdomain = authority[2]
        path = parsed.path

        ### NEW SECTION START
        # http://stat.uci.edu 🤮
        # http://www.stat.uci.edu 😍
        # http://today.uci.edu/department/information_computer_sciences/ 😍
        # Every authority with only 3 parts shall not pass unless the subdomain is "today"
        if len(authority) == 3 and subdomain != "today":
            return False

        ### NEW SECTION END

        if domain == "uci" and suffix == "edu" and subdomain in allowed_subdomains:
            if subdomain == "today":
                return (path.find(allowed_today_path) == 0)
            return True
        


    except TypeError:
        print ("TypeError for ", parsed)
        raise
    except Exception as e:
        print("WEIRD ERROR ⚠️ in scraper.py.is_valid:",  e, "for", url)
        return False

