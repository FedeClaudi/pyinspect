from pygments.style import Style
from pygments.token import (
    Keyword,
    Name,
    Comment,
    String,
    Error,
    Text,
    Number,
    Operator,
    Generic,
    Whitespace,
    Punctuation,
    Other,
    Literal,
)

red = "#fc330f"
lightred = "#fcc0b6"
dimred = "#a32f1a"

orange = "#f59e42"
lightorange = "#facb98"
dimorange = "#b56510"

green = "#27cf49"
dimgreen = "#28803a"
lightgreen2 = "#c9f7b0"

gray = "#C0C0C0"
lilla = "#E46DEC"
yellow = "#FFFACD"
salmon = "#FA8072"
mocassin = "#FFE4B5"
white = "#ffffff"

lightgray = "#b4b5b3"
lightgreen = "#b7ed8e"
lightblue = "#a2f6fc"
lightblue2 = "#73C9FE"
lightsalmon = "#FEB2A9"
lightyellow = "#FFF2B2"
lightlilla = "#F798FB"
lightgreen = "#9CEC74"

verylightgray = "#EAEAEA"

darkgray = "#A9A9A9"

# syntax style
# adaptation of: https://github.com/pygments/pygments/blob/5bd2a84bc1db0120828606c900a14276414fecdc/pygments/styles/monokai.py

_style = {
    # No corresponding class for the following:
    Text: "#cccccc",
    Whitespace: "",
    Error: "#960050 bg:#1e0010",
    Other: "",
    Comment: lightgreen,
    Comment.Multiline: "",
    Comment.Preproc: "",
    Comment.Single: "",
    Comment.Special: "",
    Keyword: lightblue2,
    Keyword.Constant: "",
    Keyword.Declaration: "",
    Keyword.Namespace: "#f92672",
    Keyword.Pseudo: "",
    Keyword.Reserved: "",
    Keyword.Type: "",
    Operator: lightlilla,
    Operator.Word: "",
    Punctuation: verylightgray,
    Name: verylightgray,
    Name.Attribute: "#a6e22e",
    Name.Builtin: lightlilla,
    Name.Builtin.Pseudo: "",
    Name.Class: salmon,
    Name.Constant: mocassin,
    Name.Decorator: yellow,
    Name.Entity: "",
    Name.Exception: "#a6e22e",
    Name.Function: lightgreen,
    Name.Property: "",
    Name.Label: "",
    Name.Namespace: "",
    Name.Other: mocassin,
    Name.Tag: "#f92672",
    Name.Variable: "",
    Name.Variable.Class: "",
    Name.Variable.Global: "",
    Name.Variable.Instance: "",
    Number: "#b5cea8",
    Number.Float: "",
    Number.Hex: "",
    Number.Integer: "",
    Number.Integer.Long: "",
    Number.Oct: "",
    Literal: "#b5cea8",
    Literal.Date: "#e6db74",
    String: lightyellow,
    String.Backtick: "",
    String.Char: "",
    String.Doc: "",
    String.Double: "",
    String.Escape: mocassin,
    String.Heredoc: "",
    String.Interpol: "",
    String.Other: "",
    String.Regex: "",
    String.Single: "",
    String.Symbol: "",
    Generic: "",
    Generic.Deleted: "#f92672",
    Generic.Emph: "italic",
    Generic.Error: "",
    Generic.Heading: "",
    Generic.Inserted: "#a6e22e",
    Generic.Output: "#66d9ef",
    Generic.Prompt: "bold #f92672",
    Generic.Strong: "bold",
    Generic.Subheading: "#75715e",
    Generic.Traceback: "",
}

_dim_style = _style.copy()
_dim_style[String] = "#ffffff"
_dim_style[Name.Class] = lightsalmon


class Monokai(Style):
    """
    This style mimics the Monokai color scheme.
    """

    background_color = "#232222"
    highlight_color = "#49483e"

    styles = _style


class DimMonokai(Style):
    """
    This style mimics the Monokai color scheme.
    """

    background_color = "#232222"
    highlight_color = "#49483e"

    styles = _dim_style
