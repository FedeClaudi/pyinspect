import sys
import rich
from rich.traceback import Traceback
from rich.console import Console
from rich.prompt import Confirm
from rich.theme import Theme
import difflib

from pyinspect._exceptions import inspect_traceback, _extract_traceback_stack
from pyinspect.answers import cache_error, get_answers
from pyinspect.utils import _class_name


class ErrorManager:
    def __init__(
        self,
        type_,
        value,
        traceback,
        keep_frames,
        all_locals,
        relevant_only,
        hide_locals,
    ):
        self.traceback_console = Console(
            file=sys.stderr, theme=Theme(rich.default_styles.DEFAULT_STYLES)
        )
        self.type_ = type_
        self.value = value
        self.traceback = traceback

        self.keep_frames = keep_frames
        self.all_locals = all_locals
        self.relevant_only = relevant_only
        self.hide_locals = hide_locals

    def render_attribute_error(self):
        """
        Looks for attributes of the class that
        triggered the AttributeError that are close
        to the one given
        """
        # process stack
        stack = _extract_traceback_stack(self.traceback)

        # Get class that triggered the error
        last = stack[-1]
        _cls_name = (
            self.value.args[0].split(" ")[0].replace("'", "").split(".")[-1]
        )
        _attr_name = self.value.args[0].split(" ")[-1].replace("'", "")

        _cls = None
        locs = [(_class_name(v), v) for k, v in last.f_locals.items()]
        for k, v in locs:
            if k == _cls_name:
                _cls = v

        if _cls is None:
            self.render_error()
            return

        # Get class attributes
        attrs = dir(_cls)

        # Get closest attributes
        closest = difflib.get_close_matches(_attr_name, attrs, cutoff=0)

        # edit self.value
        self.value.args = (
            f"{self.value.args[0]}. Perhaps you meant to say: {closest}",
        )
        self.render_error()

    def render_error(self):
        if not self.hide_locals:
            # print showing locals panels
            self.traceback_console.print(
                *inspect_traceback(
                    self.traceback,
                    keep_frames=self.keep_frames,
                    all_locals=self.all_locals,
                    relevant_only=self.relevant_only,
                ),
                "",
                Traceback.from_exception(
                    self.type_, self.value, self.traceback
                ),
                sep="\n" * 2,
            )
        else:
            # print without locals panels
            self.traceback_console.print(
                Traceback.from_exception(
                    self.type_, self.value, self.traceback
                ),
                sep="\n" * 2,
            )


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

    def excepthook(
        type_,
        value,
        traceback,
    ):
        # cache error message
        if not len(value.args):
            value.args = ["No message"]
        cache_error(f"{type_.__name__}: {value.args[0]}", value.__doc__)

        # show error traceback
        emanager = ErrorManager(
            type_,
            value,
            traceback,
            keep_frames,
            all_locals,
            relevant_only,
            hide_locals,
        )

        if isinstance(value, AttributeError):
            emanager.render_attribute_error()
        else:
            emanager.render_error()

        # Ask user if they want to google the error
        if enable_prompt:
            if Confirm().ask(
                "\n[white]Do you want me to google solutions to this error?  "
            ):
                get_answers(hide_panel=True)

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook
