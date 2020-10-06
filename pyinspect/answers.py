from googlesearch import search
import click
from pathlib import Path
from rich.text import Text
from rich.panel import Panel

from pyinspect._colors import salmon, lightgray, white, lightsalmon
from pyinspect.utils import warn_on_no_connection
from pyinspect.panels import warn
from pyinspect._answers import (
    _get_link_so_top_answer,
    _parse_so_top_answer,
    ls,
)
from pyinspect._rich import console

# Make a base folder for pyinspect
base_dir = Path.home() / ".pyinspect"
base_dir.mkdir(exist_ok=True)

error_cache = base_dir / "error_cache.txt"

# Get other vars


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


def get_stackoverflow(query):
    """ 
        Prints the results of interrogating SO
        with a search query (str).
    """
    # get link to top question
    questionlink, search_url = _get_link_so_top_answer(query)

    if questionlink is None:
        warn(
            "Failed to find anything on stack overflow, sorry.",
            "While parsing the URL with the top SO answer, could not detect any answer. Nothing to report",
        )
        return

    _parse_so_top_answer(questionlink)

    out = Text.from_markup(
        f"""
[{white}]Link to top [{lightsalmon}]Stack Overflow[/{lightsalmon}] question for the error: 
        [{ls}]{questionlink}[/{ls}]

[{white}]To find more related answers on [{lightsalmon}]Stack Overflow[/{lightsalmon}], visit: 
        [{ls}]{search_url}[/{ls}]
"""
    )

    console.print(out)


def get_google(query):
    """
        Prints links to the top hits on google given a search query (str).
    """
    out = [
        f"[{white}]Links to the top 3 results on [{lightsalmon}]google.com[/{lightsalmon}] for the error:\n"
    ]

    for n, j in enumerate(
        search("python " + query, tld="co.in", num=3, stop=3, pause=0.15)
    ):
        out.append(f"        [{ls}]{j}[/{ls}]\n")

        if n == 0:
            best = j

    console.print(*out, "\n")
    return best


@warn_on_no_connection
def get_answers(hide_panel=False):
    """
        Looks for solution to the last error encountered (as cached).
        Prints the error message, it's meaning and links
        to possible answers on google and stack overflow.
        It also parses the question and first answer from the top hit from
        google if that's a link to a SO page.

        :param hide_panel: bool, False. If true the panel with
            the error message is hidden
    """
    try:
        query, msg = load_cached()
    except ValueError:
        warn(
            "Failed to load cached error.",
            "This could be because no error had been cached, or it could be a bug",
        )

    # show a panel with a recap of the error message
    if not hide_panel:
        out = f"""
    [bold {white}]Searching online for solutions to:

            [bold {white}]>[/bold {white}] [bold {salmon}]{query}",
            [bold {white}]>[/bold {white}]
            [bold {white}]>[/bold {white}]    [{salmon}]{query.split(":")[0]}:[/{salmon}][{lightgray}] {msg}',
            """

        panel = Panel.fit(
            Text.from_markup(out), padding=(1, 2), border_style=salmon,
        )
        console.print(panel)
    else:
        console.print("\n")

    # ask google and stack overflow
    best_answer = get_google(query)
    # get_stackoverflow(query)

    if "stackoverflow" in best_answer:
        _parse_so_top_answer(best_answer)


@click.command()
def cli_get_answers():
    get_answers()
