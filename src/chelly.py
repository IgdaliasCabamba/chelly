from PyQt6.QtWidgets import QTextEdit, QSplitter, QWidget, QVBoxLayout
from .components import CodeEditor
from typing import Union

class ImageViewer(QSplitter):
    pass

class EditorWidget(QSplitter):
    def __init__(self, parent, *args, **kvargs):
        super().__init__(parent, *args, **kvargs)    
        self._editors = {
            "names":{},
            "ids":{},
            "mains":{},
            "mirrors":{}
        }
        self._id_editor = 0
        self._build()
    
    def _build(self):
        self.new_editor("main")
        self.new_editor("mirror", mirror=True, mirror_of = "main")
    
    def new_editor(self, name:str, mirror:bool = False, mirror_of:Union[str, int]=None):
        editor = CodeEditor(self)
        self._editors["names"][name] = editor
        self._editors["ids"][self._id_editor] = editor
        if mirror:
            if (
                mirror_of in self._editors["names"].keys()
                or
                mirror_of in self._editors["ids"].keys()
            ):
                if isinstance(mirror_of, int):
                    main = self._editors["ids"][mirror_of]
                elif isinstance(mirror_of, str):
                    main = self._editors["names"][mirror_of]

                if mirror_of in self._editors["mains"].keys():
                    self._editors["mains"][mirror_of].append(editor)
                    
                else:
                    self._editors["mains"][mirror_of] = [editor]
                self._editors["mirrors"][name] = editor

        self.addWidget(editor)
        self._id_editor += 1

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
        self.container_main.setContentsMargins(left=0, top=0, right=0, bottom = 0)
        self.setLayout(self.container_main)

        self.editorview = EditorWidget(self)
    
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

    
