import sys
import rich
from rich.traceback import Traceback
from rich.console import Console
from rich.prompt import Confirm
from rich.theme import Theme

from pyinspect._exceptions import inspect_traceback
from pyinspect.answers import cache_error, get_answers


def install_traceback(
    keep_frames=2,
    hide_locals=False,
    all_locals=False,
    relevant_only=False,
    enable_prompt=False,
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
        :param enable_prompt: bool, False. If true a prompt comes up after the tracebcak asking
            if the user wants to google solutions to the error.
    """
    traceback_console = Console(
        file=sys.stderr, theme=Theme(rich.default_styles.DEFAULT_STYLES)
    )

    def excepthook(
        type_, value, traceback,
    ):
        # cache error message
        cache_error(f"{type_.__name__}: {value.args[0]}", value.__doc__)

        # show error traceback
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

        # Ask user if they want to google the error
        if enable_prompt:
            if Confirm().ask(
                "\n[white]Do you want me to google solutions to this error?  "
            ):
                get_answers(hide_panel=True)

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook
