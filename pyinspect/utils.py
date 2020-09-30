import inspect
from rich.scope import render_scope
from rich.traceback import Traceback
from rich import print
from rich.syntax import Syntax

import time

def timestamp():
    return time.strftime("%y%m%d_%H%M%S")


def print_exception(message = None, **kwargs):
    # print message
    if message is None:
        message = f':x:  [bold]Error -- [/bold][grey]{timestamp()} -- :x:\n'

    # Get traceback
    traceback = Traceback(**kwargs)

    # Get locals
    caller = inspect.stack()[1]

    locals_map = {
        key: value
        for key, value in caller.frame.f_locals.items()
        if not key.startswith("__")
    }
    locals = (render_scope(locals_map, title="[i]locals"))

    print(message, traceback, '\n', locals, sep='\n')


def print_function(func):
    module = inspect.getfile(inspect.getmodule(func))

    print(f'\n[bold] function [yellow]{func.__name__}[/yellow] from {module}\n')
    try:
        print(Syntax(inspect.getsource(func), lexer_name='python'))
    except Exception:
        print_exception()