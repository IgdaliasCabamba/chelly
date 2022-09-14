"""
This module contains Syntax Highlighting mode and the QSyntaxHighlighter based
on pygments.
.. note: This code is taken and adapted from the pyqode project. (LOL)
"""
from ..core import (Language, ColorScheme, TextBlockUserData)
from .utils.pygments_utils import *

class JavaScriptSH(Language):
    """ Highlights code using the pygments parser.
    This mode enable syntax highlighting using the pygments library. This is a
    generic syntax highlighter, it is slower than a native highlighter and
    does not do any code folding detection. Use it as a fallback for languages
    that do not have a native highlighter available. Check the other pyqode
    namespace packages to see what other languages are available (at the time
    of writing, only python has specialised support).
    .. warning:: There are some issues with multi-line comments, they are not
                 properly highlighted until a full re-highlight is triggered.
                 The text is automatically re-highlighted on save.
    """
    @property
    def pygments_style(self):
        """
        Gets/Sets the pygments style
        """
        return self.color_scheme.name

    @pygments_style.setter
    def pygments_style(self, value):
        self._pygments_style = value
        self._update_style()
        # triggers a rehighlight
        self.color_scheme = ColorScheme(value)

    def __init__(self, editor, color_scheme=None):
        super().__init__(editor, color_scheme=color_scheme)
        self._pygments_style = self.color_scheme.name
        self._style = None
        self._lexer = JavascriptLexer()

        self._init_style()
        self._prev_block = None

    def _init_style(self):
        """ Init pygments style """
        self._update_style()

    def highlight_block(self, text, block):
        """
        Highlights the block using a pygments lexer.
        :param text: text of the block to highlith
        :param block: block to highlight
        """
        try:
            if self.editor and self._lexer:
                if block.blockNumber():
                    prev_data = self._prev_block.userData()
                    if prev_data:
                        if hasattr(prev_data, "syntax_stack"):
                            self._lexer._saved_state_stack = prev_data.syntax_stack
                        elif hasattr(self._lexer, '_saved_state_stack'):
                            del self._lexer._saved_state_stack

                # Lex the text using Pygments
                index = 0
                usd = block.userData()
                if usd is None:
                    usd = TextBlockUserData()
                    block.setUserData(usd)
                tokens = list(self._lexer.get_tokens(text))
                for token, text in tokens:
                    length = len(text)
                    fmt = self._get_format(token)
                    if token in [Token.Literal.String, Token.Literal.String.Doc,
                                Token.Comment]:
                        fmt.setObjectType(fmt.UserObject)
                    self.setFormat(index, length, fmt)
                    index += length

                if hasattr(self._lexer, '_saved_state_stack'):
                    setattr(usd, "syntax_stack", self._lexer._saved_state_stack)
                    # Clean up for the next go-round.
                    del self._lexer._saved_state_stack

            self._prev_block = block
        
        except:
            pass

    def _update_style(self):
        """ Sets the style to the specified Pygments style.
        """
        try:
            self._style = get_style_by_name(self._pygments_style)
        except ClassNotFound:
            
            self._style = get_style_by_name('default')
            self._pygments_style = 'default'
        self._clear_caches()

    def _update_style(self):
        """ Sets the style to the specified Pygments style.
        """
        try:
            self._style = get_style_by_name(self._pygments_style)
        except ClassNotFound:            
            self._style = get_style_by_name('material')
            self._pygments_style = 'material'
        self._clear_caches()

    def _clear_caches(self):
        """ Clear caches for brushes and formats.
        """
        self.color_scheme.brushes.clear()
        self.color_scheme.formats.clear()

    def _get_format(self, token):
        """ Returns a QTextCharFormat for token or None.
        """
        if token in self.color_scheme.formats:
            return self.color_scheme.formats[token]

        result = self.color_scheme.get_format_from_style(token, self._style)

        self.color_scheme.formats[token] = result
        return result
    
class JavaScriptLanguage(JavaScriptSH):
    ...