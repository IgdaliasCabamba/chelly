from typing import Union

from pygments.style import Style
from pygments.token import Punctuation, Token
from qtpy.QtGui import QBrush, QColor, QFont, QTextCharFormat
from .. import drift_color


class ColorScheme(object):
    """
    Translates a pygments style into a dictionary of colors associated with a
    style key.
    See :attr:`pyqode.core.api.syntax_highligter.COLOR_SCHEM_KEYS` for the
    available keys.
    """

    highlighting_rules = []

    COLOR_SCHEME_KEYS = {
        "normal": Token.Text,
        "keyword": Token.Keyword,
        "namespace": Token.Keyword.Namespace,
        "type": Token.Keyword.Type,
        "keyword_reserved": Token.Keyword.Reserved,
        "keyword_constant": Token.Keyword.Constant,
        "keyword_declaration": Token.Keyword.Declaration,
        "keyword_namespace": Token.Keyword.Namespace,
        "keyword_pseudo": Token.Keyword.Pseudo,
        "keyword_reserved": Token.Keyword.Reserved,
        "keyword_type": Token.Keyword.Type,
        "name": Token.Name,
        "name_attribute": Token.Name.Attribute,
        "name_builtin_pseudo": Token.Name.Builtin.Pseudo,
        "name_entity": Token.Name.Entity,
        "name_exception": Token.Name.Exception,
        "name_function_magic": Token.Name.Function.Magic,
        "name_label": Token.Name.Label,
        "name_namespace": Token.Name.Namespace,
        "name_other": Token.Name.Other,
        "name_property": Token.Name.Property,
        "name_variable_class": Token.Name.Variable.Class,
        "name_variable_global": Token.Name.Variable.Global,
        "name_variable_instance": Token.Name.Variable.Instance,
        "name_variable_magic": Token.Name.Variable.Magic,
        "builtin": Token.Name.Builtin,
        "definition": Token.Name.Class,
        "comment": Token.Comment,
        "string": Token.Literal.String,
        "docstring": Token.Literal.String.Doc,
        "number": Token.Number,
        "instance": Token.Name.Variable,
        "whitespace": Token.Comment,
        "tag": Token.Name.Tag,
        "self": Token.Name.Builtin.Pseudo,
        "decorator": Token.Name.Decorator,
        "punctuation": Punctuation,
        "constant": Token.Name.Constant,
        "function": Token.Name.Function,
        "operator": Token.Operator,
        "operator_word": Token.Operator.Word,
    }

    @property
    def background(self) -> QColor:
        return self.formats["background"].background().color()

    @property
    def brushes(self) -> dict:
        return self._brushes

    def __init__(self, style: Style) -> None:
        self._style = style
        self._brushes = {}
        self.formats = {}

        self.load_formats_from_style(self._style)

    def load_formats_from_style(self, style: Style):
        self.formats["background"] = self.get_format_from_color(style.background_color)

        for key, token in self.COLOR_SCHEME_KEYS.items():
            if token and key:
                self.formats[key] = self.get_format_from_style(token, style)

    def get_format_from_color(self, color):
        fmt = QTextCharFormat()
        fmt.setBackground(self.get_brush(color))
        return fmt

    def get_format_from_style(self, token, style):
        """Returns a QTextCharFormat for token by reading a Pygments style."""
        result = QTextCharFormat()
        items = list(style.style_for_token(token).items())

        for key, value in items:
            if value is None and key == "color":
                # make sure to use a default visible color for the foreground
                # brush
                value = drift_color(self.background, 1000).name()

            if value:
                if key == "color":
                    result.setForeground(self.get_brush(value))
                elif key == "bgcolor":
                    result.setBackground(self.get_brush(value))
                elif key == "bold":
                    result.setFontWeight(QFont.Bold)
                elif key == "italic":
                    result.setFontItalic(value)
                elif key == "underline":
                    result.setUnderlineStyle(QTextCharFormat.SingleUnderline)
                elif key == "sans":
                    result.setFontStyleHint(QFont.SansSerif)
                elif key == "roman":
                    result.setFontStyleHint(QFont.Times)
                elif key == "mono":
                    result.setFontStyleHint(QFont.TypeWriter)
        if token in [Token.Literal.String, Token.Literal.String.Doc, Token.Comment]:
            # mark strings, comments and docstrings regions for further queries
            result.setObjectType(result.UserObject)
        return result

    def get_brush(self, color: str) -> QBrush:
        """Returns a brush for the color."""
        result = self._brushes.get(color)
        if result is None:
            qcolor = self.get_color(color)
            result = QBrush(qcolor)
            self._brushes[color] = result
        return result

    @staticmethod
    def get_color(color):
        """Returns a QColor built from a Pygments color string."""
        color = str(color).replace("#", "")
        qcolor = QColor()
        qcolor.setRgb(
            int(color[:2], base=16), int(color[2:4], base=16), int(color[4:6], base=16)
        )
        return qcolor


__all__ = ["ColorScheme"]
