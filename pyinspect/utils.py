from rich.console import Console
from rich.text import Text
from pprint import PrettyPrinter
import pkgutil
import importlib
from pathlib import Path
import ast
import requests


import inspect
from inspect import (
    getfile,
    getmodule,
    isfunction,
    ismethod,
    isclass,
    getsource,
    isbuiltin,
    getdoc,
)
import time
import functools

from io import StringIO


from pyinspect._rich import console

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
    _skip = [
        "numpy.f2py",
        "numpy.f2py.__main__",
        "numpy.testing.print_coercion_tables",
    ]
    try:
        path = module.__path__
    except Exception:
        path = [getfile(module)]

    modules = {_name(module): module}
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=path,
        prefix=_name(module) + ".",
        onerror=lambda x: None,
    ):

        # Some known packages cause issues
        if modname in _skip:
            continue

        try:
            modules[modname] = importlib.import_module(modname)
        except Exception:
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
    _console = Console(file=buf, force_jupyter=False)
    _console.print(pretty.pformat(obj))

    out = buf.getvalue()

    if len(out) > maxlen:
        out = out[:maxlen] + " ..."

    return Text(out)


def timestamp(just_time=False):
    """
    Returns a formatted timestamp
    """
    if not just_time:
        return time.strftime("%y%m%d_%H%M%S")
    else:
        return time.strftime("%H:%M:%S")


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


def get_end_of_doc_lineno(obj):
    """
    Given a class or a function it returns the number
    of the line at which the docstring ends
    """
    # check argument
    if not isclass(obj) and not (isfunction(obj) or isbuiltin(obj)):
        raise ValueError(
            f"get_end_of_doc_lineno expects a class or a function as input, not {_class_name(obj)}"
        )

    # Check docstring
    if getdoc(obj) is None:
        return None

    root = ast.parse(getsource(obj))
    for node in ast.walk(root):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):

            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Str)
            ):

                return node.body[0].value.lineno


# ---------------------------------------------------------------------------- #
#                                   WEB STUFF                                  #
# ---------------------------------------------------------------------------- #


def connected_to_internet(url="http://www.google.com/", timeout=5):
    """
    Check that there is an internet connection
    :param url: url to use for testing (Default value = 'http://www.google.com/')
    :param timeout:  timeout to wait for [in seconds] (Default value = 5)
    """

    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def warn_on_no_connection(func):
    """
    Decorator to avoid running a function when there's no internet
    """

    def inner(*args, **kwargs):
        if not connected_to_internet():
            console.print(
                "No internet connection found.",
                f"Can't proceed with the function: {_name(func)}.",
                sep="\n",
            )
        else:
            return func(*args, **kwargs)

    return inner
