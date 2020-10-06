from rich.table import Table
from rich.panel import Panel

from pyinspect.utils import timestamp
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
from pyinspect._rich import console


class BasePanel:
    color = verylightgray
    accent = white
    dim = gray
    _type = "Message"

    def _make_title(self, title):
        line = "─" * len(title)
        return title + "\n" + line

    def _info(self):
        return f"   {self._type} at {timestamp(just_time=True)}"

    def print(self, title, msg=None):
        """
            It prints the panel!

            :param title: str, panel title.
            :param msg: str, panel message.
        """

        tb = Table(box=None, show_lines=None, show_edge=None)
        tb.add_column()

        # add title
        tb.add_row(f"[bold {self.accent}]{self._make_title(title)}")
        tb.add_row("")  # spacer

        if msg is not None:
            tb.add_row(f"[{self.color}]{msg}")

        console.print(
            Panel.fit(
                tb, width=50, border_style=self.dim, padding=(0, 2, 1, 2)
            ),
            f"[dim {self.color}]{self._info()}",
            sep="\n",
        )


class Warning(BasePanel):
    color = lightorange
    accent = orange
    dim = dimorange
    _type = "Warning"


class Ok(BasePanel):
    color = lightgreen2
    accent = green
    dim = dimgreen
    _type = "Okay"


class Error(BasePanel):
    color = lightred
    accent = red
    dim = dimred
    _type = "Error"


def message(title, msg=None):
    BasePanel().print(title, msg=msg)


def ok(title, msg=None):
    Ok().print(title, msg=msg)


def warn(title, msg=None):
    Warning().print(title, msg=msg)


def error(title, msg=None):
    Error().print(title, msg=msg)
