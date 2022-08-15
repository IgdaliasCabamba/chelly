import sys
sys.dont_write_bytecode = True

from chelly.api import ChellyEditor
from chelly.features import CaretLineHighLighter, IndentationGuides, AutoIndentMode
from chelly.components import LineNumberMargin, MiniChellyMap, HorizontalScrollBar, VerticalScrollBar
from chelly.managers import FeaturesManager, LanguagesManager, PanelsManager
from chelly.languages import PythonLexer
from chelly.core import Panel
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
editor.setStyleSheet("""QPlainTextEdit{color: #ccc; background-color: #2b2b2b;}""")
editor.features.append(CaretLineHighLighter)
editor.features.append(IndentationGuides)
editor.features.append(AutoIndentMode)
editor.panels.append(LineNumberMargin, Panel.Position.LEFT)

h_scrollbar1 = HorizontalScrollBar(editor)
v_scrollbar1 = VerticalScrollBar(editor)
editor.setHorizontalScrollBar(h_scrollbar1.scrollbar)
editor.setVerticalScrollBar(v_scrollbar1.scrollbar)
editor.panels.append(h_scrollbar1, Panel.Position.BOTTOM)
editor.panels.append(v_scrollbar1, Panel.Position.RIGHT)

minimap = editor.panels.append(MiniChellyMap, Panel.Position.RIGHT)
editor.language.lexer = PythonLexer
minimap.code_viewer.language.lexer = PythonLexer

editor1 = ChellyEditor(div)
#editor1.setStyleSheet(\t"""QPlainTextEdit{font-family:'Consolas'; color: #ccc; background-color: #2b2b2b;}""")
editor1.features.append(CaretLineHighLighter)
editor1.features.append(IndentationGuides)
editor1.panels.append(LineNumberMargin, Panel.Position.LEFT)

h_scrollbar1 = HorizontalScrollBar(editor1)
v_scrollbar1 = VerticalScrollBar(editor1)
editor1.setHorizontalScrollBar(h_scrollbar1.scrollbar)
editor1.setVerticalScrollBar(v_scrollbar1.scrollbar)
editor1.panels.append(h_scrollbar1, Panel.Position.BOTTOM)
editor1.panels.append(v_scrollbar1, Panel.Position.RIGHT)

minimap1 = editor1.panels.append(MiniChellyMap, Panel.Position.RIGHT)
editor1.language.lexer = PythonLexer
minimap1.code_viewer.language.lexer = PythonLexer

div.addWidget(editor)
div.addWidget(editor1)
div.resize(700, 500)
div.show()

editor1.properties.indent_with_spaces = True
editor.setVerticalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
editor.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAsNeeded)

editor1.setVerticalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
editor1.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAsNeeded)

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