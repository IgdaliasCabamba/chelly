from ..core import Manager

class LanguagesManager(Manager):
    def __init__(self) -> None:
        super().__init__()

    def set(self, lexer:object) -> object:
        if callable(lexer):
            lang = lexer(self.editor)
        else:
            lang = lexer
        self._features.append(lang)
        return lang