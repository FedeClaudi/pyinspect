from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.markdown import Markdown

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
    Monokai,
)
from pyinspect._rich import console


class BasePanel:
    """
    A simple panel to send messages
    """

    color = verylightgray
    accent = white
    dim = gray
    _type = "Message"
    width = 50

    def __init__(self, title, msg=None):
        """
        :param title: str, panel title.
        :param msg: str, panel message.
        """
        self.title = title
        self.msg = msg

    def _make_title(self, title):
        if title is None:
            return ""

        line = "─" * len(title)
        return title + "\n" + line

    def _info(self):
        if self._type is not None:
            return f"   {self._type} at {timestamp(just_time=True)}"
        else:
            return f"   {timestamp(just_time=True)}"

    def __rich_console__(self, *args):
        tb = Table(box=None, show_lines=None, show_edge=None)
        tb.add_column()

        # add title
        tb.add_row(f"[bold {self.accent}]{self._make_title(self.title)}")
        tb.add_row("")  # spacer

        if self.msg is not None:
            tb.add_row(f"[{self.color}]{self.msg}")

        yield Panel.fit(
            tb, width=self.width, border_style=self.dim, padding=(0, 2, 1, 2)
        )
        yield f"[dim {self.color}]{self._info()}"

    def print(self):
        """
        It prints the panel!
        """
        console.print(self)


class Report(BasePanel):
    """
    Report combines rich's tables and panels to
    create a detailed styled report to which
    various kinds of data can be added programmatically.
    """

    _color = verylightgray
    _accent = white
    _dim = gray
    _syntax_theme = Monokai
    _type = None
    width = 88

    def __init__(self, title=None, color=None, accent=None, dim=None):
        BasePanel.__init__(self, title)

        self.color = self._color if color is None else color
        self.accent = self._accent if accent is None else accent
        self.dim = self._dim if dim is None else dim

        # Initialize table
        self.tb = Table(box=None, show_lines=None, show_edge=None)
        self.tb.add_column()

        # add title
        if title is not None:
            self.tb.add_row(f"[bold {self.accent}]{self._make_title(title)}")
            self.tb.add_row("")  # spacer

    def _add_text(self, obj, **kwargs):
        self.tb.add_row(Text.from_markup(obj, **kwargs))

    def _add_code(self, obj, language="python", theme=None, **kwargs):
        if theme is None:
            theme = self._syntax_theme
        self.tb.add_row(Syntax(obj, lexer_name=language, theme=theme))

    def _add_markdown(self, obj, **kwargs):
        self.tb.add_row(Markdown(obj, **kwargs))

    def add(self, obj, *style, **kwargs):
        if not style:
            style = "text"
        else:
            style = style[0]

        if style == "text":
            self._add_text(obj, **kwargs)
        elif style == "code":
            self._add_code(obj, **kwargs)
        elif style == "markdown":
            self._add_markdown(obj, **kwargs)
        elif style == "obj":
            self.tb.add_row(obj)
        else:
            raise ValueError(f"Report add style not recognized: {style}")

    def spacer(self, n=1):
        for _ in range(n):
            self.add("")

    def line(self):
        self.tb.add_row("─" * (self.width - 8))

    def __rich_console__(self, *args):
        """
        To make it work with rich's print
        """
        yield Panel.fit(
            self.tb,
            width=self.width,
            border_style=self.dim,
            padding=(0, 2, 1, 2),
        )
        yield f"[dim {self.color}]{self._info()}"


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
    BasePanel(title, msg=msg).print()


def ok(title, msg=None):
    Ok(title, msg=msg).print()


def warn(title, msg=None):
    Warning(title, msg=msg).print()


def error(title, msg=None):
    Error(title, msg=msg).print()
