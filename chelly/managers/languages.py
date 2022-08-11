from ..core import Manager

class LanguagesManager(Manager):
    def __init__(self, editor) -> None:
        super().__init__(editor)
        self._lexer = None
    
    @property
    def lexer(self):
        return self._lexer

    @lexer.setter
    def lexer(self, new_lexer:object) -> None:
        if callable(new_lexer):
            self._lexer = new_lexer(self.editor.document())
        else:
            self._lexer = new_lexer
        self.on_state_changed.emit(self._lexer)