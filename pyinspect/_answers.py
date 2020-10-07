from rich.columns import Columns
from bs4 import BeautifulSoup
import requests

from pyinspect.panels import warn, Report
from pyinspect._rich import console
from pyinspect._colors import (
    lightblue,
    lightlilla,
    lightsalmon,
    lightgray,
    mocassin,
)

SO_url = "http://stackoverflow.com"
ls = f"bold {lightgray}"  # link style


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
        return SO_url + link.get("href"), search_url


def _style_so_element(obj, name=None, color="white"):
    """
    # Given a bs4 obj with the html elements of a question or
    answer from a SO page, this function returns a nicely
    formatted Panel

    :param obj: bs4 element
    :param name: str, optional. Panel title
    :param color: optional. Panel endge color
    """
    body = obj.find("div", attrs={"class": "s-prose js-post-body"})

    rep = Report(name, color=color, accent=color, dim=color)

    for child in body.children:
        if child.name is None:
            continue

        if "pre" in child.name:
            rep.add(child.text, "code")
            rep.add("")
        elif "p" in child.name:
            rep.add("[bold]" + child.text)
            rep.add("")

    return rep


def _parse_so_top_answer(url):
    """
    Parses a link to a SO question
    to return the formatted text of the question and top answer
    """
    # get content
    res = requests.get(url)
    if not res.ok:
        return None

    # get question and answer
    console.print("[white]Parsing SO answer...")
    bs = BeautifulSoup(res.content, features="html.parser")

    question = bs.find("div", attrs={"class": "question"})
    answer = bs.find("div", attrs={"class": "answer"})

    if answer is None or question is None:
        warn(
            "Failed to parse SO answer",
            f"We tried to parse the SO question but failed...",
        )
        return

    # Print as nicely formatted panels
    panels = []
    for name, obj, color in zip(
        ["Question", "Answer"], [question, answer], [lightsalmon, lightblue]
    ):
        panels.append(_style_so_element(obj, name, color))

    if panels:
        console.print(
            f"[{mocassin}]\n\nAnswer to the top [i]Stack Overflow[/i] answer for your question.",
            Columns(
                panels,
                equal=True,
                width=88,
            ),
            sep="\n",
        )
    else:
        warn(
            "Failed to find answer on the SO page",
            "While parsing the URL with the top SO answer, could not detect any answer. Nothing to report",
        )
