from .python_highlighter import Highlighter

class PythonLexer(Highlighter):
    def __init__(self, editor) -> None:
        super().__init__(editor)