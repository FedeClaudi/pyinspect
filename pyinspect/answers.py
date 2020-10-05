import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from googlesearch import search
import click


from pyinspect._colors import (
    salmon,
    lightblue,
    lightgray,
    lightlilla,
    white,
    lightsalmon,
)

from pathlib import Path


# Make a base folder for pyinspect
base_dir = Path.home() / ".pyinspect"
base_dir.mkdir(exist_ok=True)

error_cache = base_dir / "error_cache.txt"

# Get other vars
SO_url = "http://stackoverflow.com"
console = Console(highlight=False)
ls = f"bold {lightgray}"


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


def _highlight_link(query, url, website=""):
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

    for string, color in zip((website, q), (lightlilla, lightblue)):
        try:
            before, after = url.split(string)
            url = before + f"[{color}]{string}[/{color}]" + after
        except ValueError:
            return url
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
    bs = BeautifulSoup(res.content, features="html.parser")
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

    out = Text.from_markup(
        f"""
[{white}]Link to top [{lightsalmon}]Stack Overflow[/{lightsalmon}] question for the error: 
        [{ls}]{questionlink}[/{ls}]

[{white}]To find more related answers on [{lightsalmon}]Stack Overflow[/{lightsalmon}], visit: 
        [{ls}]"{search_url}[/{ls}]
"""
    )

    console.print(out)


def get_google(query):
    """
        Prints links to the top hits on google given a search query (str).
    """
    out = f"""
[{white}]Links to the top 3 results on [{lightsalmon}]google.com[/{lightsalmon}] for the error:
"""

    for j in search("python " + query, tld="co.in", num=3, stop=3, pause=0.15):
        out += f"""
        [{ls}]{j}[/{ls}]
        """

    console.print(out)


def get_answers(hide_panel=False):
    """
        Looks for solution to the last error encountered.
        Prints the error message, it's meaning and links
        to possible answers on google and stack overflow.

        :param hide_panel: bool, False. If true the panel with
            the error message is hidden
    """

    query, msg = load_cached()

    # show a panel with a recap of the error message
    if not hide_panel:
        out = f"""
    [bold {white}]Searching online for solutions to:

            [bold {white}]>[/bold {white}] [bold {salmon}]{query}",
            [bold {white}]>[/bold {white}]
            [bold {white}]>[/bold {white}]    [{salmon}]{query.split(":")[0]}:[/{salmon}][{lightgray}] {msg}',
            """

        panel = Panel.fit(
            Text.from_markup(out),
            padding=(1, 2),
            border_style=salmon,
            width=88,
        )
        console.print(panel)
    else:
        console.print("\n")
    # ask google and stack overflow
    get_google(query)
    get_stackoverflow(query)


@click.command()
def cli_get_answers():
    get_answers()
