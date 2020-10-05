from pyinspect.what_the_heck import error_cache
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from googlesearch import search


from pyinspect._colors import mocassin, salmon, lilla, lightblue, lightgray

SO_url = "http://stackoverflow.com"
console = Console(highlight=False)
ls = f"bold underline {lightgray}"


def cache_error(msg, doc):
    """
        Saves a string with an error message to file
        so that it can later be used to google the
        error
    """
    with open(str(error_cache), "w") as f:
        f.writelines(msg + "-x-" + doc)


def load_cached():
    """
        Loads a cached error message
    """
    with open(str(error_cache), "r") as f:
        txt = f.read()
    return txt.split("-x-")


def _highlight_link(query, url):
    """
        Highlights the part of a link corresponding to a search query

        :param query: str, search query
        :param url: str, link.
    """
    if query not in url:
        q = query.lower()
        q = q.replace(":", "").replace(" ", "-")
    else:
        q = query

    try:
        before, after = url.split(q)
        return before + f"[{lightblue}]{q}[/{lightblue}]" + after
    except ValueError:
        return url


def _get_link_so_top_answer(query):
    """
        Searches SO for answers given a query and sorts by relevance.
        returns the link to the best answer and to the list of all answers.

        :param query: str, search query
    """
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
        return link.get("href"), search_url


def get_stackoverflow(query):
    """ 
        Prints the results of interrogating SO
        with a search query (str).
    """
    # get link to top question
    questionlink, search_url = _get_link_so_top_answer(query)

    if questionlink is None:
        console.print(
            f"[{salmon}]Failed to find anything on stack overflow, sorry."
        )
        return

    console.print(
        f"[{mocassin}]Link to top [{lilla}]Stack Overflow[/{lilla}] question for your error: ",
        f"       [{ls}]" + _highlight_link(query, SO_url + questionlink) + "/",
        "",
        f"[{mocassin}]To find more related answers on [{lilla}]Stack Overflow[/{lilla}], visit: ",
        f"       [{ls}]" + _highlight_link(query, search_url) + "/",
        sep="\n",
    )


def get_google(query):
    """
        Prints links to the top hits on google given a search query (str).
    """
    console.print(
        f"[{mocassin}]Links to the top 3 results on [{lilla}]google.com[/{lilla}] for your error:"
    )
    for j in search("python " + query, tld="co.in", num=3, stop=3, pause=0.5):
        console.print(f"       [{ls}]" + _highlight_link(query, j), "")


def get_answers():
    """
        Looks for solution to the last error encountered.
        Prints the error message, it's meaning and links
        to possible answers on google and stack overflow.
    """

    query, msg = load_cached()
    console.print(
        f"[bold {mocassin}]Searching online for solutions to your error:",
        f"      [bold {salmon}]{query}",
        f'          [{lightgray}] [bold {salmon}]{query.split(":")[0]}: [/bold {salmon}]{msg}',
        "",
        sep="\n",
    )

    get_google(query)
    console.print("")
    get_stackoverflow(query)
