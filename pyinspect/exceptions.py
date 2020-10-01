import sys
import inspect
import rich
from rich.traceback import Traceback
from rich import print, box
from rich.console import Console
from rich.style import Style
from rich.theme import Theme
from rich.table import Table
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text
from rich.syntax import Syntax
from collections import namedtuple

import numpy as np

from pyinspect.utils import timestamp

# Override some of rich's default parameters
rich.default_styles.DEFAULT_STYLES["scope.border"] = Style(color="green")


PANEL_WIDTH = 180
local = namedtuple("local", "key, obj, type, info")


def render_scope(synt, scope, *, title=None, sort_keys=True):
    def sort_items(item):
        """Sort special variables first, then alphabetically."""
        key, _ = item
        return (not key.startswith("__"), key.lower())

    # Make table
    items_table = Table(
        padding=(0, 1),
        expand=False,
        box=box.SIMPLE,
        header_style="bold magenta",
        width=PANEL_WIDTH,
    )
    items_table.add_column(justify="right", width=8, header="key")
    items_table.add_column(justify="left", width=30, header="value")
    items_table.add_column(justify="left", width=15, header="type")
    items_table.add_column(justify="left", header="info")

    # sort items
    items = (
        sorted(scope.items(), key=sort_items) if sort_keys else scope.items()
    )

    # Populate table
    for key, value in items:
        if key.startswith("__"):
            continue
        key_text = Text.assemble(
            (
                key,
                "scope.key.special" if key.startswith("__") else "scope.key",
            ),
            (" =", "scope.equals"),
        )

        items_table.add_row(
            key_text,
            Pretty(value.obj, highlighter=ReprHighlighter()),
            value.type,
            str(value.info),
        )

    # make a table with the syntax and the variables
    table = Table(box=None)
    table.add_row("[bold white]Error line:")
    table.add_row(synt)
    table.add_row("")
    table.add_row("[bold white]Local variables")
    table.add_row(items_table)

    return Panel(
        table,
        title=title,
        border_style="scope.border",
        padding=(0, 1),
        expand=False,
        width=PANEL_WIDTH,
        title_align="left",
    )


def inspect_traceback(tb, keep_frames=2):
    """
        Get the whole traceback stack with 
        locals at each frame and expand the local
        with additional info that may be useful.

        :param tb: traceback object
        :param keep_frames: int. Keep only the last N frames for traceback
    """
    # Get the whole traceback stack
    while True:
        if not tb.tb_next:
            break
        tb = tb.tb_next

    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    if len(stack) > keep_frames:
        stack = stack[-keep_frames:]

    panels = []
    for f in stack:
        # get filepath
        fpath = f.f_code.co_filename

        # get error line
        synt = Syntax.from_path(
            fpath,
            line_numbers=True,
            line_range=[f.f_lineno, f.f_lineno + 1],
            code_width=PANEL_WIDTH,
        )

        # make clickable filepath
        text = Text(fpath, style="bold white underline")
        text.stylize(f"link file://{fpath}")

        # Get locals
        locs = {}
        for k, v in f.f_locals.items():
            if isinstance(v, np.ndarray):
                info = f"[#808080]Shape: {v.shape} max: {v.max()} min: {v.min()} has nan: {np.any(np.isnan(v))}"
            elif isinstance(v, (list, tuple, str)):
                info = f"[#808080]Length: {len(v)}"
            else:
                info = ""

            # get type color
            _type = str(v.__class__)
            if "function" in _type:
                type_color = "#FFFACD"
            elif "module" in _type:
                type_color = "#C8A2C8"
            elif "." in _type:
                type_color = "#FA8072"
            else:
                type_color = "white"

            locs[k] = local(k, v, f"[{type_color}]{_type}", info)

        # make panel
        title = f"[i #D3D3D3]file: [bold underline]{text}[/bold underline] line {f.f_lineno}"
        panels.append(render_scope(synt, locs, title=title))

    return panels


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


def install_traceback(keep_frames=2, hide_locals=False):
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
        if not hide_locals:
            traceback_console.print(
                *inspect_traceback(traceback, keep_frames=keep_frames),
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
