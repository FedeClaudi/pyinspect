from rich import print
from rich.syntax import Syntax
from rich.console import Console
from rich.text import Text
from pprint import PrettyPrinter
import pkgutil
import importlib
from pathlib import Path

import inspect
from inspect import (
    getfile,
    getmodule,
    isfunction,
    ismethod,
    isclass,
    getsource,
    isbuiltin,
)
import time
import functools

from io import StringIO

from pyinspect._colors import mocassin


def showme(func):
    """
        Given a pointer to a python function, it prints the code of the function. 

        :param func: pointer to a python function
    """
    if isbuiltin(func):
        print(
            f'[black on {mocassin}]`showme` currently does not work with builtin functions like "{_name(func)}", sorry. '
        )
        return False
    if not (isfunction(func) or isclass(func) or ismethod(func)):
        print(
            f'[black on {mocassin}]`showme` only accepts functions and classes, not "{_class_name(func)}", sorry. '
        )
        return False

    # Print source class
    class_obj = get_class_that_defined_method(func)

    output = []
    if class_obj is not None:
        output.append(
            f"\n[bold green] Method [yellow]{_name(func)}[/yellow] from class [magenta]{_name(class_obj)}[/magenta]"
        )

        output.append(
            Syntax(
                getsource(class_obj),
                lexer_name="python",
                line_range=(0, 5),
                line_numbers=True,
            )
        )
        output.append("\nmethod code:")
    else:
        output.append(
            f"\n[bold]Function [yellow]{_name(func)}[/yellow] from [blue]{_module(func)}[/blue]\n"
        )

    print(
        *output,
        Syntax(getsource(func), lexer_name="python", line_numbers=True),
    )

    return True


# ---------------------------------------------------------------------------- #
#                                    OBJECTS                                   #
# ---------------------------------------------------------------------------- #


def _class(obj):
    return obj.__class__


def _name(obj):
    return obj.__name__


def _class_name(obj):
    return obj.__class__.__name__


def _module(obj):
    return obj.__module__


def get_submodules(module):
    """
        Attempts to find all submodules of a given module object
    """
    try:
        path = module.__path__
    except Exception:
        path = [getfile(module)]

    modules = {_name(module): module}
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=path, prefix=_name(module) + ".", onerror=lambda x: None,
    ):
        try:
            modules[modname] = importlib.import_module(modname)
        except (ImportError, OSError):
            pass
    return modules


def get_class_that_defined_method(meth):
    """
        Given a reference to some classes' method, 
        this function returns the class the method
        belongs to.

        :param meth: method object.
    """
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)

    if ismethod(meth) or (
        inspect.isbuiltin(meth)
        and getattr(meth, "__self__", None) is not None
        and getattr(meth.__self__, "__class__", None)
    ):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(
            meth, "__func__", meth
        )  # fallback to __qualname__ parsing

    if isfunction(meth):
        cls = getattr(
            getmodule(meth),
            meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
            None,
        )
        if isinstance(cls, type):
            return cls
    return getattr(
        meth, "__objclass__", None
    )  # handle special descriptor objects


# ---------------------------------------------------------------------------- #
#                                  SMALL STUFF                                 #
# ---------------------------------------------------------------------------- #
def read_single_line(fpath, lineno):
    """
        Read a single line from a given path
    """
    if not isinstance(lineno, int):
        raise ValueError(
            "When reading a single line from file, lineno should be a number"
        )

    if not Path(fpath).exists():
        raise FileExistsError(
            "When reading a single line from file: the file doesnt exist!"
        )

    with open(fpath, "r") as f:
        for i, line in enumerate(f):
            if i == lineno:
                return line


def textify(obj, maxlen=31):
    pretty = PrettyPrinter(compact=True)
    buf = StringIO()
    console = Console(file=buf, force_jupyter=False)
    console.print(pretty.pformat(obj))

    out = buf.getvalue()

    if len(out) > maxlen:
        out = out[:maxlen] + " ..."

    return Text(out)


def timestamp():
    """
        Returns a formatted timestamp
    """
    return time.strftime("%y%m%d_%H%M%S")


def clean_doc(doc, maxn=47):
    """
        Cleans a docstring and shortens it if necessary + appends and ellips

        :param doc: str, string with docstring
        :param maxn: int, docstrings longer than maxn will be truncated

        :returns: str
    """
    if doc is None:
        return ""
    else:
        doc = doc.strip()
        if len(doc) > maxn:
            return doc[:maxn] + "..."
        else:
            return doc
