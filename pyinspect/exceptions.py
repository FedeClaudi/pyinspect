import sys
import rich
from rich.traceback import Traceback
from rich import print
from rich.console import Console
from rich.theme import Theme

from pyinspect.utils import timestamp
from pyinspect._exceptions import inspect_traceback, get_locals


def print_exception(message=None, traceback=None, **kwargs):
    """
        It prints a nicely formatted traceback for an exception, 
        including the variables in the local scope.
        Example:
        try:
            do_something()
        except Exception:
            print_exception('oops')

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


def install_traceback(
    keep_frames=2, hide_locals=False, all_locals=False, relevant_only=False
):
    """
        Install an improved rich traceback handler (it includes a view of the local variables).
        Once installed, any tracebacks will be printed with syntax highlighting and rich formatting.

        :param keep_frames: int. Keep only the last N frames for traceback with the more relevant data
        :param hide_locals: bool, False. If True local variables are not printed
        :param all_locals: bool, False. If True all locals (e.g. including imported modules) are shown.
            Otherwise only variables are shown
        :param relevant_only: bool, False. If True only the variables in the error
            line are shown, otherwise all variables are shown. 
    """
    traceback_console = Console(
        file=sys.stderr, theme=Theme(rich.default_styles.DEFAULT_STYLES)
    )

    def excepthook(
        type_, value, traceback,
    ):
        if not hide_locals:
            traceback_console.print(
                *inspect_traceback(
                    traceback,
                    keep_frames=keep_frames,
                    all_locals=all_locals,
                    relevant_only=relevant_only,
                ),
                "",
                Traceback.from_exception(type_, value, traceback),
                sep="\n" * 3,
            )

        else:
            traceback_console.print(
                Traceback.from_exception(type_, value, traceback),
                sep="\n" * 3,
            )

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook
