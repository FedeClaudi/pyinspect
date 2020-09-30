import sys
import inspect
import rich
from rich.scope import render_scope
from rich.traceback import Traceback
from rich import print
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

from pyinspect.utils import timestamp

# Override some of rich's default parameters
rich.default_styles.DEFAULT_STYLES['scope.border'] =  Style(color="green")

def get_locals():
    """
        Returns a rich rendering of the variables in the local scope
    """
    caller = inspect.stack()[1]

    locals_map = {
        key: value
        for key, value in caller.frame.f_locals.items()
        if not key.startswith("__")
    }
    return (render_scope(locals_map, title="[i]locals"))


def print_exception(message = None, traceback, **kwargs):
    """
        It prints a nicely formatted traceback for an exception, 
        including the variables in the local scope.

        :param message: str, optional. A message to add to the start of the traceback.
                If none is passed a default message is used
    """
    # Get message
    if message is None:
        message = f':x:  [bold]Error -- [/bold][grey]{timestamp()} -- :x:\n'

    # Get traceback if not passed
    traceback = Traceback(**kwargs)

    # print
    print(message, traceback, '\n', get_locals(), sep='\n')


def install():
    """
        Install an improved rich traceback handler (it includes a view of the local variables).
        Once installed, any tracebacks will be printed with syntax highlighting and rich formatting.
    """
    traceback_console = Console(file=sys.stderr, theme=Theme(rich.default_styles.DEFAULT_STYLES))

    def excepthook(
        type_,
        value,
        traceback,
    ):
        traceback_console.print(
            Traceback.from_exception(
                type_,
                value,
                traceback,
            ),
            get_locals(),
            sep='\n',
        )

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook