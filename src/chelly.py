from PyQt6.QtWidgets import QTextEdit, QSplitter, QWidget, QVBoxLayout

from src.components.code_editor import ChellyEditor
from .components import CodeEditor, MinimapBox
from typing import Union
from .core import CONSTS
import pprint

class ImageViewer(QSplitter):
    pass

class EditorWidget(QSplitter):
    def __init__(self, parent, *args, **kvargs):
        super().__init__(parent)    
        self._editors = {
            "names":{},  # the names of the editors (their identification)
            "ids":{},    # ids to help to search for an editor
            "childs":{}, # the editors who has mirrors(childs)
            "mirrors":{} # the editors who are mirrors
        }
        self._components = {
            "minimaps":{}
        }

        self._kvargs = kvargs
        self._id_editor = 0
        self._build()
    
    def _build(self):
        """

        """
        self.new_editor("main")
        self.new_editor("mirror", mirror=True, mirror_of = "main")
        pprint.pprint(self._editors)
    
    def new_editor(self, name:str, mirror:bool = False, mirror_of:Union[str, int]=None) -> CodeEditor:
        """

        """
        editor = CodeEditor(self)
        minimap = MinimapBox(self)
        self._editors["names"][name] = editor
        self._editors["ids"][self._id_editor] = editor
        self._components["minimaps"][name] = minimap
        if mirror:
            if (
                mirror_of in self._editors["names"].keys()
                or
                mirror_of in self._editors["ids"].keys()
            ):  
                self.create_mirror(editor, name, mirror_of)
            
        self.addWidget(editor)
        self.addWidget(minimap)
        self.build_editor(editor)
        self._id_editor += 1
        return editor

    def create_mirror(self, editor:CodeEditor, name:str, mirror_of:Union[int, str])-> None:
            
            if isinstance(mirror_of, int):
                main = self._editors["ids"][mirror_of]
            elif isinstance(mirror_of, str):
                main = self._editors["names"][mirror_of]

            if mirror_of in self._editors["childs"].keys():
                self._editors["childs"][mirror_of].append(editor)
            else:
                self._editors["childs"][mirror_of] = [editor]
            self._editors["mirrors"][name] = main

            editor.chelly_editor.setDocument(main.chelly_editor.document())
    
    def build_editor(self, editor) -> None:
        print(self._kvargs)
        editor.editor.setPlainText(self._kvargs["text"])
    
    def get_editor(self, name:str, editor:bool=True) -> Union[CodeEditor, ChellyEditor]:
        if name in self._editors["names"].keys():
            if editor:
                return self._editors["names"][name].editor
            return self._editors["names"][name]


class Chelly(QWidget):
    def __init__(self, parent, file:str = None, text:str = None):
        super().__init__(parent)
        self._file = file
        self._text = text
        self._build()
    
    @property
    def file(self):
        return self._file
    
    @property
    def text(self):
        return self._text
    
    def _build(self):
        self.container_main = QVBoxLayout(self)
        self.container_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.container_main)

        self.editorview = EditorWidget(self, file = self._file, text = self._text)
        self.container_main.addWidget(self.editorview)
    
    def is_mirror(self, editor):
        pass

    def is_main(self, editor):
        pass

    def set_text(self, editor):
        pass

    def get_text(self, editor):
        pass

    def set_selection(self, editor):
        pass
    
    def get_selection(self, editor):
        pass

    def has_selection(self, editor):
        pass

    def has_text(self, editor):
        pass

    def get_cursor_pos(self, editor):
        pass

    def set_cursor_pos(self, editor):
        pass