import sys
sys.dont_write_bytecode = True

from src import ChellyEditor
from src.features import CaretLineHighLighter, IndentationGuides
from src.components import LineNumberMargin, MiniChellyMap
from src.managers import FeaturesManager, LanguagesManager, PanelsManager
from src.core import Panel
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import pytest
import logging
import os
import pathlib

DEBUG_OUTPUT_FILE = os.path.join("dev","chelly.log")
pathlib.Path(DEBUG_OUTPUT_FILE).touch(exist_ok=True)

logging.basicConfig(filename=DEBUG_OUTPUT_FILE, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

app = QApplication(sys.argv)

div = QSplitter()

editor = ChellyEditor(div)
editor.setStyleSheet("""QPlainTextEdit{font-family:'Consolas'; color: #ccc; background-color: #2b2b2b;}""")
editor.features.append(CaretLineHighLighter)
#editor.features.append(IndentationGuides)
editor.panels.append(LineNumberMargin, Panel.Position.LEFT)
minimap = editor.panels.append(MiniChellyMap, Panel.Position.RIGHT)

editor1 = ChellyEditor(div)
editor1.setStyleSheet("""QPlainTextEdit{font-family:'Consolas'; color: #ccc; background-color: #2b2b2b;}""")
editor1.features.append(CaretLineHighLighter)
#editor1.chelly_document = editor.chelly_document
editor1.panels.append(LineNumberMargin, Panel.Position.LEFT)
minimap = editor1.panels.append(MiniChellyMap, Panel.Position.RIGHT)

div.addWidget(editor)
div.addWidget(editor1)
div.resize(700, 500)
div.show()


def test_lexer_set():
	new_lexer = LanguagesManager(editor)
	editor.lexer = new_lexer
	assert editor.lexer == new_lexer

def test_feature_set():
	new_features = FeaturesManager(editor)
	editor.features = new_features
	assert editor.features == new_features

def test_load_file():
	with open(__file__, "r") as infile:
		content = infile.read()

	editor.properties.text = content
	assert editor.properties.text == content

if __name__ == "__main__":
	test_load_file()

app.exec()

#import src.languages.python_highlighter as python_lexer
#highlight = python_lexer.Highlighter(editor.editorview.get_editor("main").document())