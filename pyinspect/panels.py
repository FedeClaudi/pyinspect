from rich import print
from rich.table import Table
from rich.panel import Panel


from pyinspect._colors import (
    verylightgray,
    white,
    gray,
    orange,
    dimorange,
    lightorange,
    green,
    dimgreen,
    lightgreen2,
    red,
    dimred,
    lightred,
)


class BasePanel:
    color = verylightgray
    accent = white
    dim = gray

    def print(self, title, msg=None):
        """
            It prints the panel!

            :param title: str, panel title.
            :param msg: str, panel message.
        """

        tb = Table(box=None, show_lines=None, show_edge=None)
        tb.add_column()

        # add title
        tb.add_row(f"[bold {self.accent}]{title}")
        tb.add_row("")  # spacer

        if msg is not None:
            tb.add_row(f"[{self.color}]{msg}")

        print(
            Panel.fit(
                tb, width=50, border_style=self.dim, padding=(0, 2, 1, 2)
            )
        )


class Warning(BasePanel):
    color = lightorange
    accent = orange
    dim = dimorange


class Ok(BasePanel):
    color = lightgreen2
    accent = green
    dim = dimgreen


class Error(BasePanel):
    color = lightred
    accent = red
    dim = dimred


def panel(title, msg=None):
    BasePanel().print(title, msg=msg)


def ok(title, msg=None):
    Ok().print(title, msg=msg)


def warn(title, msg=None):
    Warning().print(title, msg=msg)


def error(title, msg=None):
    Error().print(title, msg=msg)
