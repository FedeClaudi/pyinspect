from rich import print
from rich.syntax import Syntax
import inspect
import time
import functools


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


def get_class_that_defined_method(meth):
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (
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
    if inspect.isfunction(meth):
        cls = getattr(
            inspect.getmodule(meth),
            meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
            None,
        )
        if isinstance(cls, type):
            return cls
    return getattr(
        meth, "__objclass__", None
    )  # handle special descriptor objects


def print_function(func):
    """
        Given a pointer to a python function, it prints the code of the function. 

        :param func: pointer to a python function
    """
    if not (inspect.isfunction(func) or inspect.isbuiltin(func)):
        raise ValueError("print_function expects a function as argument")

    # Print source class
    class_obj = get_class_that_defined_method(func)

    output = []
    if class_obj is not None:
        output.append(
            f"\n[bold green] Method [yellow]{func.__name__}[/yellow] from class [magenta]{class_obj.__name__}[/magenta]"
        )

        output.append(
            Syntax(
                inspect.getsource(class_obj),
                lexer_name="python",
                line_range=(0, 5),
                line_numbers=True,
            )
        )
        output.append("\nmethod code:")
    else:
        output.append(
            f"\n[bold]Function [yellow]{func.__name__}[/yellow] from [blue]{func.__module__}[/blue]\n"
        )

    print(
        *output,
        Syntax(
            inspect.getsource(func), lexer_name="python", line_numbers=True
        ),
    )
