from ..core import Manager

class LanguagesManager(Manager):
    def __init__(self, editor) -> None:
        super().__init__(editor)

    def set(self, lexer:object) -> object:
        if callable(lexer):
            lang = lexer(self.editor)
        else:
            lang = lexer
        self._features.append(lang)
        return lang