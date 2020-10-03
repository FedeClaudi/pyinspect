from rich.table import Table
from rich.highlighter import ReprHighlighter
from rich.pretty import Pretty
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.syntax import Syntax
from rich.scope import render_scope as rich_render_scope

import inspect
from collections import namedtuple
import numpy as np

from pyinspect.utils import textify, read_single_line, _class_name
from pyinspect._colors import lightgray, yellow, lilla, salmon

PANEL_WIDTH = 125
local = namedtuple("local", "key, obj, type, info, eline")


def _print_object(obj):
    """
        Returns a coincise and pretty print
        of any object
    """
    highlighter = ReprHighlighter()

    if isinstance(obj, dict):  # deal with dicts
        newobj = {k: _class_name(v) for k, v in obj.items()}
        return Pretty(
            newobj,
            highlighter=highlighter,
            no_wrap=True,
            overflow=None,
            justify="left",
        )

    elif isinstance(obj, (list, tuple, str)):  # deal with lists and tuples
        return textify(obj)

    elif isinstance(obj, np.ndarray):  # deal with numpy arrays
        return textify(obj)
    else:  # deal with everything else
        return Pretty(
            obj, highlighter=highlighter, justify="left", overflow="ellipsis"
        )


def render_scope(synt, scope, *, title=None, relevant_only=False):
    """
        Creates a rich panel display a 'frame' in a traceback
        stack. It include a clickable link to the source filepath,
        an overview of the line causing the error and a table with
        local variables.
    """

    def sort_items(item):
        """Sort special variables first, then alphabetically."""
        key, _ = item
        return (not key.startswith("__"), key.lower())

    def get_variables_in_line(eline):
        """Given a string with a line of code, it founds variable names in it"""
        # Isolte words
        eline = eline.replace("\n", " ").replace("\t", " ")
        chrs = "(),.="
        for ch in chrs:
            eline = eline.replace(ch, " ")

        # get all single words
        names = eline.split(" ")
        return names

    # Make table
    items_table = Table(
        padding=(0, 1),
        expand=False,
        box=box.SIMPLE,
        header_style="bold magenta",
        width=PANEL_WIDTH,
    )
    items_table.add_column(
        justify="right",
        width=6,
        header=f"[{lightgray}]object",
        overflow="fold",
    )
    items_table.add_column(
        justify="left",
        width=25,
        header=f"[{lightgray}]value",
        overflow="ellipsis",
    )
    items_table.add_column(
        justify="left", width=15, header=f"[{lightgray}]type", overflow="fold"
    )
    items_table.add_column(
        justify="left", header=f"[{lightgray}]info", overflow="fold"
    )

    # sort items
    items = sorted(scope.items(), key=sort_items)

    added_items = False  # flag to check if table is filled in
    if items:
        # Split items to get variables in error line
        linevars = get_variables_in_line(items[0][1].eline)
        in_eline = [itm for itm in items if itm[0] in linevars]
        not_in_eline = [itm for itm in items if itm[0] not in linevars]

        # Populate table
        styles = ["bold", "dim"]
        items_groups = (
            [in_eline, not_in_eline] if not relevant_only else [in_eline]
        )
        for items, style in zip(items_groups, styles):
            for key, value in items:
                if key.startswith("__"):
                    continue

                key_text = Text.assemble(
                    (
                        key,
                        "scope.key.special"
                        if key.startswith("__")
                        else "scope.key",
                    ),
                    (" =", "scope.equals"),
                )

                # Add to table
                items_table.add_row(
                    key_text,
                    _print_object(value.obj),
                    value.type,
                    str(value.info),
                    style=style,
                )
                added_items = True

    # make a table with the syntax and the variables
    table = Table(box=None)
    table.add_row("[bold white]Error line:")
    table.add_row(synt)
    table.add_row("")

    if added_items:
        table.add_row("[bold white]Local variables")
        table.add_row(items_table)
    else:
        table.add_row("No local variables to show")

    return Panel(
        table,
        title=title,
        border_style="green",
        padding=(0, 1),
        expand=False,
        width=PANEL_WIDTH,
        title_align="left",
    )


def inspect_traceback(
    tb, keep_frames=2, all_locals=False, relevant_only=False
):
    """
        Get the whole traceback stack with 
        locals at each frame and expand the local
        with additional info that may be useful.

        :param tb: traceback object
        :param keep_frames: int. Keep only the last N frames for traceback
        :all_locals: bool, False. If True all locals (e.g. including imported modules) are shown.
            Otherwise only variables are shown
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
    stack.reverse()

    if len(stack) > keep_frames:
        if keep_frames > 1:
            stack = [stack[0]] + list(stack[-keep_frames:])
        else:
            stack = [stack[-1]]

    # Make a locals panel for each frame
    panels = []
    for f in stack:
        # get filepath
        fpath = f.f_code.co_filename

        # Get error line as text
        eline = read_single_line(fpath, f.f_lineno - 1)

        # get error line as Syntax
        synt = Syntax.from_path(
            fpath,
            line_numbers=True,
            line_range=[f.f_lineno, f.f_lineno],
            code_width=PANEL_WIDTH,
        )

        # make clickable filepath
        text = Text(fpath + f":{f.f_lineno}", style="bold white underline")
        text.stylize(f"link file://{fpath}")

        # Get locals
        locs = {}
        for k, v in f.f_locals.items():
            mod = v.__class__.__module__
            name = v.__class__.__name__
            _type = f"{mod}.{name}"

            # Check if object should be included
            if not all_locals:
                # Skip a bunch of stuff
                if (
                    inspect.isfunction(v)
                    or inspect.ismodule(v)
                    or inspect.isbuiltin(v)
                    or "function" in name
                    or "module" in name
                    or "type" in name
                ):
                    continue

            # Get some additional info
            if isinstance(v, np.ndarray):
                info = f"[#808080]Shape: {v.shape} max: {v.max()} min: {v.min()} has nan: {np.any(np.isnan(v))}"
            elif isinstance(v, (list, tuple, str)):
                info = f"[#808080]Length: {len(v)}"
            else:
                info = ""

            # get type color
            if "function" in _type:
                type_color = yellow
            elif "module" in _type:
                type_color = lilla
            elif "." in _type:
                type_color = salmon
            else:
                type_color = "white"

            # Store all info
            locs[k] = local(
                k,
                v,
                f"[{lightgray}]{_type}".replace(".", f".[{type_color}]"),
                info,
                eline,
            )

        # make panel
        title = f"[i #D3D3D3]file: [bold underline]{text}[/bold underline] line {f.f_lineno}"
        panels.append(
            render_scope(synt, locs, title=title, relevant_only=relevant_only)
        )
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
    return rich_render_scope(locals_map, title="[i]locals")
