from typing import Union

from pygments.styles import get_style_by_name
from pygments.style import Style, StyleMeta
from pygments.token import Punctuation, Token
from pygments.util import ClassNotFound
from PySide6.QtCore import QRegularExpression, Qt, Signal
from PySide6.QtGui import (QBrush, QColor, QCursor, QFont, QSyntaxHighlighter,
                           QTextBlockUserData, QTextCharFormat)
from PySide6.QtWidgets import QApplication
from ..core import drift_color

class Highlighter(QSyntaxHighlighter):

    class HighlightingRule():
        pattern = QRegularExpression()
        format = QTextCharFormat()

    class Format(QTextCharFormat):
        def __init__(self, *args, **kvargs):
            super().__init__(*args, **kvargs)

    class Expression(QRegularExpression):
        def __init__(self, *args, **kvargs):
            super().__init__(*args, **kvargs)

    @staticmethod
    def get_style(style: Union[str, StyleMeta, Style, dict]) -> Style:
        class CustomStyle(Style):
            pass

        if isinstance(style, Style) or isinstance(style, StyleMeta):
            return style

        elif isinstance(style, str):
            try:
                style = get_style_by_name(style)
                return style
            except ClassNotFound:
                return CustomStyle

        elif isinstance(style, dict):
            CustomStyle.styles = style
            return CustomStyle

        else:
            raise TypeError(
                f"style must be Union[str, Style, dict] not {type(style)}")

    @staticmethod
    def get_style_name(style: Style) -> str:
        return style.__name__

    highlighting_rules = []

    COLOR_SCHEME_KEYS = {
        # editor background
        "background": None,
        # highlight color (used for caret line)
        "highlight": None,
        # normal text
        "normal": Token.Text,
        # any keyword
        "keyword": Token.Keyword,
        # namespace keywords (from ... import ... as)
        "namespace": Token.Keyword.Namespace,
        # type keywords
        "type": Token.Keyword.Type,
        # reserved keyword
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
        # "": Token.,
        # any builtin name
        "builtin": Token.Name.Builtin,
        # any definition (class or function)
        "definition": Token.Name.Class,
        # any comment
        "comment": Token.Comment,
        # any string
        "string": Token.Literal.String,
        # any docstring (python docstring, c++ doxygen comment,...)
        "docstring": Token.Literal.String.Doc,
        # any number
        "number": Token.Number,
        # any instance variable
        "instance": Token.Name.Variable,
        # whitespace color
        "whitespace": Token.Comment,
        # any tag name (e.g. shinx doctags,...)
        'tag': Token.Name.Tag,
        # self paramter (or this in other languages)
        'self': Token.Name.Builtin.Pseudo,
        # python decorators
        'decorator': Token.Name.Decorator,
        # colors of punctuation characters
        'punctuation': Punctuation,
        # name or keyword constant
        'constant': Token.Name.Constant,
        # function definition
        'function': Token.Name.Function,
        # operator
        'operator': Token.Operator,
        # operator words (and, not)
        'operator_word': Token.Operator.Word
    }


class ColorScheme(object):
    """
    Translates a pygments style into a dictionary of colors associated with a
    style key.
    See :attr:`pyqode.core.api.syntax_highligter.COLOR_SCHEM_KEYS` for the
    available keys.
    """
    @property
    def name(self):
        return self._name

    @property
    def background(self):
        return self.formats['background'].background().color()

    @property
    def highlight(self):
        return self.formats['highlight'].background().color()

    @property
    def brushes(self) -> dict:
        return self._brushes

    def __init__(self, style: Union[str, dict]) -> None:
        """
        :param style: name of the pygments style to load
        """
        self._style = Highlighter.get_style(style)
        self._name = Highlighter.get_style_name(self._style)
        self._brushes = {}
        #: Dictionary of formats colors (keys are the same as for
        #: :attr:`pyqode.core.api.COLOR_SCHEME_KEYS`
        self.formats = {}

        self.load_formats_from_style(self._style)

    def load_formats_from_style(self, style):
        # background
        self.formats['background'] = self.get_format_from_color(
            style.background_color)
        # highlight
        self.formats['highlight'] = self.get_format_from_color(
            style.highlight_color)

        for key, token in Highlighter.COLOR_SCHEME_KEYS.items():
            if token and key:
                self.formats[key] = self.get_format_from_style(token, style)

    def get_format_from_color(self, color):
        fmt = Highlighter.Format()
        fmt.setBackground(self.get_brush(color))
        return fmt

    def get_format_from_style(self, token, style):
        """ Returns a QTextCharFormat for token by reading a Pygments style.
        """
        result = Highlighter.Format()
        items = list(style.style_for_token(token).items())

        for key, value in items:
            if value is None and key == 'color':
                # make sure to use a default visible color for the foreground
                # brush
                value = drift_color(self.background, 1000).name()
            if value:
                if key == 'color':
                    result.setForeground(self.get_brush(value))
                elif key == 'bgcolor':
                    result.setBackground(self.get_brush(value))
                elif key == 'bold':
                    result.setFontWeight(QFont.Bold)
                elif key == 'italic':
                    result.setFontItalic(value)
                elif key == 'underline':
                    result.setUnderlineStyle(
                        QTextCharFormat.SingleUnderline)
                elif key == 'sans':
                    result.setFontStyleHint(QFont.SansSerif)
                elif key == 'roman':
                    result.setFontStyleHint(QFont.Times)
                elif key == 'mono':
                    result.setFontStyleHint(QFont.TypeWriter)
        if token in [Token.Literal.String, Token.Literal.String.Doc,
                     Token.Comment]:
            # mark strings, comments and docstrings regions for further queries
            result.setObjectType(result.UserObject)
        return result

    def get_brush(self, color):
        """ Returns a brush for the color.
        """
        result = self._brushes.get(color)
        if result is None:
            qcolor = self.get_color(color)
            result = QBrush(qcolor)
            self._brushes[color] = result
        return result

    @staticmethod
    def get_color(color):
        """ Returns a QColor built from a Pygments color string. """
        color = str(color).replace("#", "")
        qcolor = QColor()
        qcolor.setRgb(int(color[:2], base=16),
                      int(color[2:4], base=16),
                      int(color[4:6], base=16))
        return qcolor

class SyntaxHighlighter(Highlighter):
    #: Signal emitted at the start of highlightBlock. Parameters are the
    #: highlighter instance and the current text block
    block_highlight_started = Signal(object, object)

    #: Signal emitted at the end of highlightBlock. Parameters are the
    #: highlighter instance and the current text block
    block_highlight_finished = Signal(object, object)

    @property
    def formats(self):
        """
        Returns the color shcme formats dict.
        """
        return self._color_scheme.formats

    @property
    def color_scheme(self):
        """
        Gets/Sets the color scheme of the syntax highlighter, this will trigger
        a rehighlight automatically.
        """
        return self._color_scheme

    @color_scheme.setter
    def color_scheme(self, color_scheme):
        if isinstance(color_scheme, str):
            color_scheme = ColorScheme(color_scheme)

        if color_scheme.name != self._color_scheme.name:
            self._color_scheme = color_scheme
            self.rehighlight()

    def __init__(self, editor, color_scheme=None):
        """
        :param parent: parent document (QTextDocument)
        :param color_scheme: color scheme to use.
        """
        super().__init__(editor.document())
        self.__editor = editor

        if not color_scheme:
            color_scheme = "default"

        self._color_scheme = ColorScheme(color_scheme)

    @property
    def editor(self):
        return self.__editor

    def highlightBlock(self, text):
        """
        Highlights a block of text. Please do not override, this method.
        Instead you should implement
        :func:`pyqode.core.api.SyntaxHighlighter.highlight_block`.
        :param text: text to highlight.
        """
        current_block = self.currentBlock()
        self.highlight_block(text, current_block)

    def highlight_block(self, text, block):
        """
        Abstract method. Override this to apply syntax highlighting.
        :param text: Line of text to highlight.
        :param block: current block
        """
        raise NotImplementedError()

    def rehighlight(self):
        """
        Rehighlight the entire document, may be slow.
        """
        QApplication.setOverrideCursor(
            QCursor(Qt.WaitCursor))
        try:
            super().rehighlight()
        except RuntimeError:
            # cloned widget, no need to rehighlight the same document twice ;)
            pass
        QApplication.restoreOverrideCursor()

class Language(SyntaxHighlighter):
    pass

class TextBlockUserData(QTextBlockUserData):
    """
    Custom text block user data, mainly used to store checker messages and
    markers.
    """
    def __init__(self) -> None:
        super().__init__()
        #: List of checker messages associated with the block.
        self.messages = []
        #: List of markers draw by a marker panel.
        self.markers = []