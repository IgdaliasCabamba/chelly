from .python_highlighter import PythonHighlighter, SyntaxHighlighter

class PythonLexer(PythonHighlighter):
    def __init__(self, editor) -> None:
        super().__init__(editor)