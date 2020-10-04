from pyinspect.what_the_heck import error_cache

# import requests
# import re

# SO_url = "http://stackoverflow.com/search?"


def cache_error(msg):
    """
        Saves a string with an error message to file
        so that it can later be used to google the
        error
    """
    with open(str(error_cache), "w") as f:
        f.write(msg)


def load_cached():
    """
        Loads a cached error message
    """
    with open(str(error_cache), "r") as f:
        return f.read()


# TODO search google
"""
from google import google
num_page = 3
search_results = google.search("This is my query", num_page)
for result in search_results:
    print(result.description)
"""


# def get_stackoverflow():
#     query = load_cached()

#     params = f"q=python best practices&sort=relevance"

#     res = requests.get(SO_url + params)

#     if not res.ok:
#         print("Failed to find anything on stack overflow, sorry")
#         return

#     content = str(res.content)

#     #  tml = urllib2.urlopen("http://stackoverflow.com/search?%s" % params).read()
#     # TODO fix parsing of outcome to find links
#     # TODO open first link and get answer..
#     links = re.findall(
#         r'<h3><a class="question-hyperlink">([^<]*)</a></h3>', str(res.content)
#     )

#     a = 1
#     # links = [(urlparse.urljoin('http://stackoverflow.com/', url), title) for url,title in links]

#     return params
