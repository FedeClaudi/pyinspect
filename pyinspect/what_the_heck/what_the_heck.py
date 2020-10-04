from pyinspect.what_the_heck import error_cache
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from googlesearch import search


from pyinspect._colors import mocassin, salmon, lilla, lightblue

SO_url = "http://stackoverflow.com"
console = Console(highlight=False)
ls = f"bold underline {lightblue}"


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


def _get_link_so_top_answer(query):
    # get search string
    params = f"q=python {query}&sort=relevance"
    search_url = SO_url + "/search?" + params

    # query SO
    res = requests.get(search_url)
    if not res.ok:
        return None, search_url

    # get link to top anser
    bs = BeautifulSoup(res.content, "lxml")
    link = bs.find("a", attrs={"class": "question-hyperlink"})

    if link is None:
        return None, search_url
    else:
        return link.get("href")


def get_stackoverflow(query):
    # get link to top question
    questionlink = _get_link_so_top_answer(query)

    if questionlink is None:
        console.print(
            f"[{salmon}]Failed to find anything on stack overflow, sorry."
        )
        return

    console.print(
        f"[{mocassin}]Link to top [{lilla}]Stack Overflow[/{lilla}] question for your error: ",
        f"       [{ls}]" + SO_url + questionlink + "/",
        "",
        f"[{mocassin}]To find more related answers on [{lilla}]Stack Overflow[/{lilla}], visit: ",
        f"       [{ls}]" + SO_url + questionlink + "/",
        sep="\n",
    )


def get_google(query):
    console.print(
        f"[{mocassin}]Links to the top 3 results on [{lilla}]google.com[/{lilla}] for your error:"
    )
    for j in search("python " + query, tld="co.in", num=3, stop=3, pause=0.5):
        console.print(f"       [{ls}]" + j, "")


def get_answers():
    query = load_cached()
    console.print(
        f"[{mocassin}]Searching online for solutions to your error: [{salmon}]{query}"
    )

    get_google(query)
    console.print("")
    get_stackoverflow(query)
