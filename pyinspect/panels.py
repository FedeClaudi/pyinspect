from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.markdown import Markdown
from rich.jupyter import JupyterMixin

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


class BasePanel(JupyterMixin):
    """
    A simple panel to send messages which consist
    of a title and a message body.
    """

    color = verylightgray  # message body color
    accent = white  # title color
    dim = gray  # panel border color
    _type = "Message"  # To print some info under the panel
    width = 50  # panel width

    def __init__(self, title, msg=None):
        """
        :param title: str, panel title.
        :param msg: str, panel message.
        """
        self.title = title
        self.msg = msg

    def _make_title(self, title):
        """
        Add an underline to the title string
        """
        if title is None:
            return ""

        line = "─" * len(title)
        return title + "\n" + line

    def _info(self):
        """
        Return some info: panel type and timestamp
        """
        if self._type is not None:
            return f"   {self._type} at {timestamp(just_time=True)}"
        else:
            return f"   {timestamp(just_time=True)}"

    def __rich_console__(self, *args):
        """
        Yields the panel elements for printing in rich console
        """
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

    _color = verylightgray  # default color
    _accent = white  # default color
    _dim = gray  # default color

    _syntax_theme = Monokai  # default syntax theme

    _type = None  # panel type, printed in info

    width = 88  # panel width

    def __init__(
        self,
        title=None,
        color=None,
        accent=None,
        dim=None,
        show_info=False,
        table_kwargs={},
    ):
        """
        Initializes a rich Table which is used to organize content in the panel and
        sets a few parameters for rendering

        :param title: str, panel title
        :param color: str text color
        :param accent: str title color
        :param dim: str panel edge color
        :param show_info: bool, if True an 'info' text is shown below the report
        :param table_kwargs: dict, keyword arguments to pass to internal table at creation
        """
        BasePanel.__init__(self, title)

        # Get colors and other params
        self.color = self._color if color is None else color
        self.accent = self._accent if accent is None else accent
        self.dim = self._dim if dim is None else dim

        self.show_info = show_info

        # Initialize table
        self.tb = Table(
            box=None, show_lines=None, show_edge=None, **table_kwargs
        )
        self.tb.add_column()

        # add title
        if title is not None:
            self.tb.add_row(f"[bold {self.accent}]{self._make_title(title)}")
            self.tb.add_row("")  # spacer

    def _add_text(self, obj, **kwargs):
        """
        Add a text entry to the table
        """
        self.tb.add_row(Text.from_markup(obj, **kwargs))

    def _add_code(self, obj, language="python", theme=None, **kwargs):
        """
        Add a Syntax entry to the table
        """
        if theme is None:
            theme = self._syntax_theme
        self.tb.add_row(
            Syntax(obj, lexer_name=language, theme=theme, **kwargs)
        )

    def _add_code_file(self, obj, language="python", theme=None, **kwargs):
        """
        Add a Syntax entry to the table by parsing a file with the code
        """
        if theme is None:
            theme = self._syntax_theme

        self.tb.add_row(Syntax.from_path(obj, theme=theme, **kwargs))

    def _add_markdown(self, obj, **kwargs):
        """
        Add a markdown text entry to the table
        """
        self.tb.add_row(Markdown(obj, **kwargs))

    def _add_rich(self, obj, **kwargs):
        """
        add a rich object (e.g. a table or another panel)
        """
        self.tb.add_row(obj, **kwargs)

    def add(self, obj, *style, **kwargs):
        """
        Add various forms of content to the internal table
        """
        if not style:
            style = "text"
        else:
            style = style[0]

        if style == "text":
            self._add_text(obj, **kwargs)
        elif style == "code":
            self._add_code(obj, **kwargs)
        elif style == "code file":
            self._add_code_file(obj, **kwargs)
        elif style == "markdown":
            self._add_markdown(obj, **kwargs)
        elif style == "rich":
            self._add_rich(obj, **kwargs)
        else:
            raise ValueError(f"Report add type not recognized: {style}")

    def spacer(self, n=1):
        """
        Add an empty row ( or n rows) to internal table
        """
        for _ in range(n):
            self.add("")

    def line(self, style="#ffffff"):
        """
        Add a row of '-' to create a line in the report
        """
        self.tb.add_row(f"[{style}]─" * (self.width - 8))

    def __rich_console__(self, *args):
        """
        Yields the panel elements for printing in rich console
        """
        yield Panel.fit(
            self.tb,
            width=self.width,
            border_style=self.dim,
            padding=(0, 2, 1, 2),
        )

        if self.show_info:
            yield f"[dim {self.color}]{self._info()}"


class NestedPanel(Report):
    """
    A useful class to create Report-like panels that
    fit nicely when nested within other Report objects
    """

    def __init__(self, *args, **kwargs):
        Report.__init__(self, *args, **kwargs)
        self.tb.expand = True

    def __rich_console__(self, *args):
        yield Panel(
            self.tb,
            expand=True,
            border_style=self.dim,
            padding=(0, 2, 1, 2),
        )


class Warning(BasePanel):
    """
    Warning panel
    """

    color = lightorange
    accent = orange
    dim = dimorange
    _type = "Warning"


class Ok(BasePanel):
    """
    Ok panel
    """

    color = lightgreen2
    accent = green
    dim = dimgreen
    _type = "Okay"


class Error(BasePanel):
    """
    Error panel
    """

    color = lightred
    accent = red
    dim = dimred
    _type = "Error"


def message(title, msg=None):
    """ Print a message pabel """
    BasePanel(title, msg=msg).print()


def ok(title, msg=None):
    """ Print a Ok pabel """
    Ok(title, msg=msg).print()


def warn(title, msg=None):
    """ Print a Warning pabel """
    Warning(title, msg=msg).print()


def error(title, msg=None):
    """ Print a Error pabel """
    Error(title, msg=msg).print()
