import sys
import inspect
import rich
from rich.scope import render_scope
from rich.traceback import Traceback
from rich import print
from rich.console import Console
from rich.style import Style
from rich.theme import Theme
import traceback

from pyinspect.utils import timestamp

# Override some of rich's default parameters
rich.default_styles.DEFAULT_STYLES['scope.border'] =  Style(color="green")


def inspect_traceback(tb):
    # Get the whole traceback stack
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse(  )
    return stack

def get_locals():
    """
        Returns a rich rendering of the variables in the local scope
    """
    tb = sys.exc_info(  )[2]
  

    print(len(inspect.stack()))
    caller = inspect.stack()[1]

    locals_map = {
        key: value
        for key, value in caller.frame.f_locals.items()
        if not key.startswith("__")
    }
    return (render_scope(locals_map, title="[i]locals"))


def print_exception(message = None, traceback=None, **kwargs):
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
        stack = inspect_traceback(traceback)

        locals_panels = []
        for n, frame in enumerate(stack):
            locals_panels.append(render_scope(frame.f_locals, title=f"[i]locals frame {n}"))


        traceback_console.print(
            Traceback.from_exception(
                type_,
                value,
                traceback,
            ),
            *locals_panels,
            sep='\n',
        )

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook