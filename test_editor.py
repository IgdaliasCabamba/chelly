import sys
sys.dont_write_bytecode = True
from src import ChellyEditor
from src.features import CaretLineHighLighter, IndentationGuides
from src.components import LineNumberMargin
from src.managers import FeaturesManager, LanguagesManager, PanelsManager
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import pytest

app = QApplication(sys.argv)

editor = ChellyEditor(None)
editor.setStyleSheet("""QPlainTextEdit{font-family:'Consolas'; color: #ccc; background-color: #2b2b2b;}""")
editor.features.append(CaretLineHighLighter)
editor.features.append(IndentationGuides)
editor.panels.append(LineNumberMargin)
editor.resize(300, 500)
editor.show()

def test_lexer_set():
	new_lexer = LanguagesManager(editor)
	editor.lexer = new_lexer
	assert editor.lexer == new_lexer

def test_feature_set():
	new_features = FeaturesManager(editor)
	editor.features = new_features
	assert editor.features == new_features

app.exec()

#import src.languages.python_highlighter as python_lexer
#highlight = python_lexer.Highlighter(editor.editorview.get_editor("main").document())

#Load chelly.py into the editor for demo purposes
#infile = open('src/chelly.py', 'r')
#editor.editorview.get_editor("main").setPlainText(infile.read())