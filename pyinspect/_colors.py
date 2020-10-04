gray = "#C0C0C0"
lilla = "#C8A2C8"

lightgray = "#b4b5b3"
lightgreen = "#b7ed8e"
lightblue = "#a2f6fc"

yellow = "#FFFACD"
salmon = "#FA8072"
mocassin = "#FFE4B5"


# syntax style

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

# adaptation of: https://github.com/pygments/pygments/blob/5bd2a84bc1db0120828606c900a14276414fecdc/pygments/styles/monokai.py


class MonokaiStyle(Style):
    """
    This style mimics the Monokai color scheme.
    """

    background_color = "#232222"
    highlight_color = "#49483e"

    styles = {
        # No corresponding class for the following:
        Text: "#ffffff",
        Whitespace: "",
        Error: "#960050 bg:#1e0010",
        Other: "",
        Comment: "#46a30b",
        Comment.Multiline: "",
        Comment.Preproc: "",
        Comment.Single: "",
        Comment.Special: "",
        Keyword: "#66d9ef",
        Keyword.Constant: "",
        Keyword.Declaration: "",
        Keyword.Namespace: "#f92672",
        Keyword.Pseudo: "",
        Keyword.Reserved: "",
        Keyword.Type: "",
        Operator: "#f92672",
        Operator.Word: "",
        Punctuation: "#f8f8f2",
        Name: "#f8f8f2",
        Name.Attribute: "#a6e22e",
        Name.Builtin: "",
        Name.Builtin.Pseudo: "",
        Name.Class: "#a6e22e",
        Name.Constant: "#66d9ef",
        Name.Decorator: "#a6e22e",
        Name.Entity: "",
        Name.Exception: "#a6e22e",
        Name.Function: "#a6e22e",
        Name.Property: "",
        Name.Label: "",
        Name.Namespace: "",
        Name.Other: "#a6e22e",
        Name.Tag: "#f92672",
        Name.Variable: "",
        Name.Variable.Class: "",
        Name.Variable.Global: "",
        Name.Variable.Instance: "",
        Number: "#ae81ff",
        Number.Float: "",
        Number.Hex: "",
        Number.Integer: "",
        Number.Integer.Long: "",
        Number.Oct: "",
        Literal: "#ae81ff",
        Literal.Date: "#e6db74",
        String: "#CFCFCF",
        String.Backtick: "",
        String.Char: "",
        String.Doc: "",
        String.Double: "",
        String.Escape: "#ae81ff",
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
