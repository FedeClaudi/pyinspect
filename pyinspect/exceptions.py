import sys
import inspect
import rich
from rich.scope import render_scope
from rich.traceback import Traceback
from rich import print
from rich.console import Console
from rich.style import Style
from rich.theme import Theme
import numpy as np

from pyinspect.utils import timestamp

# Override some of rich's default parameters
rich.default_styles.DEFAULT_STYLES["scope.border"] = Style(color="green")


def inspect_traceback(tb, skip_frame=1):
    """
        Get the whole traceback stack with 
        locals at each frame and expand the local
        with additional info that may be useful.
    """
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
    stack.reverse()
    stack = stack[skip_frame:]

    # improve traceback info
    cleaned_stack = []
    for frame in stack:
        cleaned_frame = {}
        for k, v in frame.f_locals.items():
            if isinstance(v, np.ndarray):
                obj = [
                    v,
                    "Shape:",
                    v.shape,
                    "max:",
                    v.max(),
                    "min:",
                    v.min(),
                    "has nan:",
                    np.any(np.isnan(v)),
                ]
            elif isinstance(v, (list, tuple, str)):
                obj = [v, f"Length: ", len(v)]
            else:
                obj = [v]

            obj += [v.__class__]
            cleaned_frame[k] = obj
        cleaned_stack.append(cleaned_frame)

    locals_panels = []
    for n, frame in enumerate(cleaned_stack):
        locals_panels.append(
            render_scope(frame, title=f"[i]locals frame {n + skip_frame}")
        )

    return locals_panels


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
    return render_scope(locals_map, title="[i]locals")


def print_exception(message=None, traceback=None, **kwargs):
    """
        It prints a nicely formatted traceback for an exception, 
        including the variables in the local scope.

        :param message: str, optional. A message to add to the start of the traceback.
                If none is passed a default message is used
    """
    # Get message
    if message is None:
        message = f":x:  [bold]Error -- [/bold][grey]{timestamp()} -- :x:\n"

    # Get traceback if not passed
    traceback = Traceback(**kwargs)

    # print
    print(message, traceback, "\n", get_locals(), sep="\n")


def install():
    """
        Install an improved rich traceback handler (it includes a view of the local variables).
        Once installed, any tracebacks will be printed with syntax highlighting and rich formatting.
    """
    traceback_console = Console(
        file=sys.stderr, theme=Theme(rich.default_styles.DEFAULT_STYLES)
    )

    def excepthook(
        type_, value, traceback,
    ):
        traceback_console.print(
            Traceback.from_exception(type_, value, traceback,),
            *inspect_traceback(traceback),
            sep="\n",
        )

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook
