import mimetypes

from pygments.lexers import get_lexer_for_filename, get_lexer_for_mimetype
from pygments.lexers.agile import PythonLexer
from pygments.lexers.special import TextLexer
from pygments.styles import get_style_by_name, get_all_styles
from pygments.token import Whitespace, Comment, Token
from pygments.util import ClassNotFound

from ..core import (SyntaxHighlighter, ColorScheme, TextBlockUserData)

class PygmentsSH(SyntaxHighlighter):
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
    #: Mode description
    DESCRIPTION = "Apply syntax highlighting to the editor using pygments"

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

    def __init__(self, document, lexer=None, color_scheme=None):
        super().__init__(document, color_scheme=color_scheme)
        
        self._pygments_style = self.color_scheme.name
        self._style = None
        self._lexer = lexer if lexer else PythonLexer()

        self._init_style()
        self._prev_block = None

    def _init_style(self):
        """ Init pygments style """
        self._update_style()        

    def set_mime_type(self, mime_type):
        """
        Update the highlighter lexer based on a mime type.
        :param mime_type: mime type of the new lexer to setup.
        """

        if not mime_type:
            # Fall back to TextLexer
            self._lexer = TextLexer()
            return False
        try:
            self.set_lexer_from_mime_type(mime_type)
        except ClassNotFound:
            self._lexer = TextLexer()
            return False
        except ImportError:
            # import error while loading some pygments plugins, the editor
            # should not crash
            self._lexer = TextLexer()
            return False
        else:
            return True

    def set_lexer_from_filename(self, filename):
        """
        Change the lexer based on the filename (actually only the extension is
        needed)
        :param filename: Filename or extension
        """
        self._lexer = None
        try:
            self._lexer = get_lexer_for_filename(filename)
        except (ClassNotFound, ImportError):
            try:
                m = mimetypes.guess_type(filename)
                self._lexer = get_lexer_for_mimetype(m[0])
            except (ClassNotFound, IndexError, ImportError):
                self._lexer = get_lexer_for_mimetype('text/plain')
        if self._lexer is None:
            self._lexer = TextLexer()

    def set_lexer_from_mime_type(self, mime, **options):
        """
        Sets the pygments lexer from mime type.
        :param mime: mime type
        :param options: optional addtional options.
        """

        try:
            self._lexer = get_lexer_for_mimetype(mime, **options)
        except (ClassNotFound, ImportError):
            self._lexer = get_lexer_for_mimetype('text/plain')

    def highlight_block(self, text, block):
        """
        Highlights the block using a pygments lexer.
        :param text: text of the block to highlith
        :param block: block to highlight
        """
        if self.editor and self._lexer:

            # Lex the text using Pygments
            index = 0
            if block.userData() is None:
                block.setUserData(TextBlockUserData())

            tokens = list(self._lexer.get_tokens(text))
            
            for token, text in tokens:
                length = len(text)
                format = self._get_format(token)
                if token in [Token.Literal.String, Token.Literal.String.Doc,
                             Token.Comment]:
                    format.setObjectType(format.UserObject)
                self.setFormat(index, length, format)
                index += length

            self._prev_block = block

    def _update_style(self):
        """ Sets the style to the specified Pygments style.
        """
        try:
            self._style = get_style_by_name(self._pygments_style)
        except ClassNotFound:            
            self._style = get_style_by_name('dracula')
            self._pygments_style = 'dracula'
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