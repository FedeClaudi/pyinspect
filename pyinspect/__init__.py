# nopycln: file
from pyinspect.exceptions import install_traceback
from pyinspect.show import showme, what
from pyinspect.find import search
from pyinspect.answers import get_answers, ask
from pyinspect.panels import ok, warn, error, message, Report
from pyinspect._rich import console

from pyinspect._colors import (
    salmon,
    lightsalmon,
    orange,
    mocassin,
    lightblue,
    lightorange,
)


__author__ = "Federico Claudi"
__license__ = "MIT"
__maintainer__ = "Federico Claudi"
__email__ = "federicoclaudi@protonmail.com"
__status__ = "dev"
__website__ = "https://github.com/FedeClaudi/pyinspect"
__version__ = "0.0.7rc"


def pi():
    """
        Prints a Report with an overview of `pyinspect`.

    """
    rep = Report(f"Pynspect", dim=orange, accent=orange)
    rep._type = "Pyinspect info"
    rep.width = 100

    rep.add(
        f"[b {lightorange}]The python package for lazy programmers",
        justify="center",
    )

    rep.add(
        f"""
[{salmon}]Don't remember a function's name?[/{salmon}] Use `pyinspect` to look for it. 
[{salmon}]Don't remember what a function does?[/{salmon}] Use `pyinspect` to print its source code directly to your terminal. 
[{salmon}]Can't figure out why you keep getting an error?[/{salmon}] Use `pyinspect`'s fancy tracebacks to figure it out
[{salmon}]Still can't figure it out, but too lazy to google it?[/{salmon}] Use `pyinspect` to print Stack Overflow's top answer for your error message directly to your terminal!
    """
    )

    rep.line()
    rep.add("""### Info""", "markdown", style=orange)
    rep.add(
        f"[b {lightblue}]Author[/b {lightblue}]: {__author__}", justify="right"
    )
    rep.add(
        f"[b {lightblue}]License[/b {lightblue}]: {__license__}",
        justify="right",
    )
    rep.add(
        f"[b {lightblue}]Version[/b {lightblue}]: {__version__}",
        justify="right",
    )
    rep.add(
        f"[b {lightblue}]Website[/b {lightblue}]: {__website__}",
        justify="right",
    )

    rep.spacer()
    rep.line()
    rep.add("""### Installation""", "markdown", style=orange)
    rep.add("pip install pyinspect", "code", language="shell")
    rep.spacer(3)

    rep.add("""### Features""", "markdown", style=orange)
    rep.add("With")
    rep.add("import pyinspect as pi", "code")

    features = {
        "Look up local variables": "pi.what()",
        "Search functions by name": "pi.search(package, function_name)",
        "Print source code to console": "pi.showme(function)",
        "Enhanced tracebacks": "pi.install_traceback()",
        "Render [i]Stack Overflow[/i] answers in the terminal": 'pi.ask("How to python?")',
    }

    for txt, code in features.items():
        rep.spacer()
        rep.add(f"[{lightorange}]" + txt)
        rep.add(code, "code")

    rep.spacer()
    rep.add(f"[{lightorange}]... and a bunch of others!")

    rep.spacer(2)
    rep.add(f"[{lightsalmon}]Get in touch at:[/{lightsalmon}] {__website__}")

    console.print(rep)
