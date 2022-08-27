from typing import Any
from ..core import Manager, Language
from ..core import Highlighter
from dataclasses import dataclass

class LanguagesManager(Manager):
    
    @dataclass(frozen=True)
    class LexerObject:
        language:Language
        style:Any

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.__lexer = None
        self._style = None
    
    def set_mime_type(self, mime_type):
        return self

    def set_lexer_from_filename(self, filename):
        return self

    def set_lexer_from_mime_type(self, mime, **options):
        return self
    
    def set_lexer_from_code(self, code:str):
        return self
    
    @property
    def lexer(self):
        return self.__lexer
    
    @property
    def style(self):
        return self._style
    
    @staticmethod
    def get_lexer_from_any(arg) -> LexerObject:
        if isinstance(arg, dict):
            language = arg.get("language", None)
            _style = arg.get("style", None)
            
            if _style is None:
                style = Highlighter.get_style("default")
            
            else:
                style = Highlighter.get_style(_style)
            
            return LanguagesManager.LexerObject(language, style)
        
        elif isinstance(arg, tuple) or isinstance(arg, list):
            return LanguagesManager.LexerObject(language=arg[0], style=arg[1])
        
        elif isinstance(arg, Language):
            style = Highlighter.get_style("default")
            return LanguagesManager.LexerObject(arg, style)

    @lexer.setter
    def lexer(self, arg:dict) -> None:
        lexer_object = self.get_lexer_from_any(arg)

        if callable(lexer_object.language):
            self.__lexer = lexer_object.language(self.editor, lexer_object.style)
        else:
            self.__lexer = lexer_object.language

        self._style = lexer_object.style
        self.on_state_changed.emit(self.__lexer)