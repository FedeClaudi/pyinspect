# nopycln: file
from pyinspect.exceptions import install_traceback
from pyinspect.show import showme, what
from pyinspect.find import search
from pyinspect.answers import get_answers, ask
from pyinspect.panels import ok, warn, error, message, Report, NestedPanel
from pyinspect._rich import console
from pyinspect.classes import Enhanced
from pyinspect.builtins import List, Tuple, Dict, pilist, pidict


from pyinspect._colors import (
    salmon,
    lightsalmon,
    orange,
    mocassin,
    lightblue,
    lightorange,
    gray,
)

from rich import pretty

pretty.install()

try:
    from github import Github
except Exception:
    Github = None


__author__ = "Federico Claudi"
__license__ = "MIT"
__maintainer__ = "Federico Claudi"
__email__ = "federicoclaudi@protonmail.com"
__status__ = "dev"
__website__ = "https://github.com/FedeClaudi/pyinspect"
__version__ = "0.0.7"


def whats_pi():
    """
    Prints a Report with an overview of `pyinspect`.

    """
    # ? Intro
    rep = Report(f"Pynspect", dim=orange, accent=orange)
    rep._type = "Pyinspect info"
    rep.width = 100

    rep.add(
        f"[b {lightorange}]The python package for lazy programmers",
        justify="center",
    )

    # Features summary
    rep.add(
        f"""
[{salmon}]Don't remember a function's name?[/{salmon}] Use `pyinspect` to look for it. 
[{salmon}]Don't remember what a function does?[/{salmon}] Use `pyinspect` to print its source code directly to your terminal. 
[{salmon}]Can't figure out why you keep getting an error?[/{salmon}] Use `pyinspect`'s fancy tracebacks to figure it out
[{salmon}]Still can't figure it out, but too lazy to google it?[/{salmon}] Use `pyinspect` to print Stack Overflow's top answer for your error message directly to your terminal!
    """
    )

    # Package / Repo info as a nested panel
    info = NestedPanel(color=mocassin, dim=mocassin)
    _info = dict(
        Author=__author__,
        License=__license__,
        Version=__version__,
        Website=__website__,
    )

    if Github is not None:
        n_stars = Github().get_repo("FedeClaudi/pyinspect").stargazers_count

        _info["Github stars"] = n_stars
    else:
        warn(
            "Could not fetch repo info",
            "Perhaps `PyGithub` is not installed?s",
        )

    for k, v in _info.items():
        info.add(f"[b {gray}]{k}[/b {gray}]: [{orange}]{v}", justify="right")
    rep.add(info, "rich")

    # Features examples
    rep.add("""## Features""", "markdown", style=lightsalmon)

    features = {
        "Look up local variables": "pinspect.what()",
        "Search functions by name": "pinspect.search(package, function_name)",
        "Print source code to console": "pinspect.showme(function)",
        "Enhanced tracebacks": "pinspect.install_traceback()",
        "Render [i]Stack Overflow[/i] answers in the terminal": 'pinspect.ask("How to python?")',
    }

    for txt, code in features.items():
        rep.spacer()
        rep.add(f"[{gray}]" + txt, justify="center")
        rep.add("   " + code, "code")

    rep.spacer()
    rep.add(f"[{lightorange}]... and a bunch of others!")

    rep.spacer(2)
    rep.add(f"[{lightsalmon}]Get in touch at:[/{lightsalmon}] {__website__}")

    console.print(rep)
