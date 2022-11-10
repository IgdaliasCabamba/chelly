from .sh import SyntaxHighlighter

class Language(SyntaxHighlighter):
    def __init__(self, editor, color_scheme=None):
        super().__init__(editor, color_scheme)