from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.highlighter import ReprHighlighter
from rich.filesize import decimal as format_size
import pkgutil
import importlib
from pathlib import Path
import ast
import requests
import os

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

from pyinspect._colors import darkgray, orange, mocassin, lightorange
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


def stringify(obj, maxlen=31):
    buf = StringIO()
    _console = Console(file=buf, force_jupyter=False)
    _console.print(obj)

    out = buf.getvalue()
    if maxlen > 0:
        if len(out) > maxlen:
            out = out[:maxlen] + " ..."
    return out


def textify(obj, maxlen=31):
    return Text(stringify(obj, maxlen=maxlen))


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


# ---------------------------------------------------------------------------- #
#                                   FILE I/O                                   #
# ---------------------------------------------------------------------------- #


def dir_files(path, pattern="*"):
    """
    Returns all files in a directory
    """
    if not isinstance(path, Path):
        raise TypeError("path must be an instance of pathlib.Path")

    return [f for f in path.glob(pattern) if f.is_file()]


def subdirs(path, pattern="*"):
    """
    Returns all subdirectories in a directory
    """
    if not isinstance(path, Path):
        raise TypeError("path must be an instance of pathlib.Path")

    return [f for f in path.glob(pattern) if f.is_dir()]


def listdir(path, extension=None, sortby=None):
    """
    Prints a nicely formatted table with an overview of files
    in a given directory

    :param path: str or Path object. Path to directory being listed
    :param extension: str. If passed files with that extension are highlighted
    :param sortby: str, default None. How to sort items. If None items
            are sorted alphabetically, if 'ext' or 'extension' items are
            sorted by extension, if 'size' items are sorted by size

    returns a list of files
    """

    def sort_ext(item):
        return item.suffix

    def sort_size(item):
        return item.stat().st_size

    # Check paths
    p = Path(path)
    if not p.is_dir():
        raise ValueError(f"The path passed is not a directory: {path}")

    # Create table
    tb = Table(
        box=None,
        show_lines=None,
        show_edge=None,
        expand=False,
        header_style=f"bold {mocassin}",
    )
    tb.add_column(header="Name")
    tb.add_column(header="Size")

    # Sort items
    if sortby == "extension" or sortby == "ext":
        std = sorted(dir_files(p), key=sort_ext)
    elif sortby == "size":
        std = sorted(dir_files(p), key=sort_size, reverse=True)
    else:
        std = sorted(dir_files(p))

    for fl in std:
        complete_path = str(fl)
        parent = fl.parent.name
        fl = fl.name
        _fl = fl

        # Format file name
        fl = f"[{mocassin}]{fl}"

        if extension is not None and fl.endswith(extension):
            fl = f"[{orange}]{_fl}"
            _col = orange
            _dimcol = orange
        else:
            _col = lightorange
            _dimcol = darkgray

        # Get file size
        size = format_size(os.path.getsize(_fl)).split(" ")

        tb.add_row(
            f'[link=file://"{complete_path}"][dim]{parent}/[/]' + fl,
            f"[{_col}]" + size[0] + f"[/] [{_dimcol}]" + size[1],
        )

    console.print(
        f"Files in {path}\n", tb, sep="\n", highlight=ReprHighlighter()
    )

    return std
