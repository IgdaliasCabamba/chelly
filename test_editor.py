import sys
sys.dont_write_bytecode = True

import logging
import os
import pathlib

import pytest
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from chelly.api import ChellyEditor
from chelly.components import (HorizontalScrollBar, LineNumberMargin, Marker,
                               MarkerMargin, MiniMap, VerticalScrollBar, BreadcrumbNav)
from chelly.core import Panel
from chelly.features import (AutoIndent, CaretLineHighLighter,
                             IndentationGuides, SmartBackSpace, CursorHistory)
from chelly.languages import PygmentsSH, PythonLanguage
from chelly.managers import FeaturesManager, LanguagesManager, PanelsManager

DEBUG_OUTPUT_FILE = os.path.join("dev", "chelly.log")
pathlib.Path(DEBUG_OUTPUT_FILE).touch(exist_ok=True)

logging.basicConfig(filename=DEBUG_OUTPUT_FILE, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

app = QApplication(sys.argv)

div = QSplitter()

editor = ChellyEditor(div)
editor.setCornerWidget(None)
div.setStyleSheet(
"""
	QLabel, ChellyEditor, MiniMap MiniMapEditor {
		font-family:Monaco;
		color: #ccc;
		background-color: #2b2b2b;
		/*background-color: #dbdbdb;*/
		border:none
	}
	ChellyEditor{
		font-size:10pt;
	}
	MiniMap{
		border: none;
	}
	QSplitter::handle {background-color:#252526}
	QSplitter::handle:horizontal {width: 2px}
	QSplitter::handle:vertical {height: 2px}
	QSplitter::handle:pressed {background-color:#00a2e8}

	QScrollBar:vertical {
		border: none;
		border-left: 0.5px solid rgb(60, 60, 60);
		border-top: 0.5px solid rgb(60, 60, 60);
		background: transparent;
	}
	QScrollBar::handle:vertical {
		background:rgba(180, 180, 180, 70);
	}
	QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {height: 0;}
	QScrollBar:left-arrow:vertical, QScrollBar::right-arrow:vertical {
		height: 0;
		width: 0;
	}
	QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}
	QScrollBar:horizontal {
		border: none;
		background: transparent;
	}
	QScrollBar::handle:horizontal {
		background:rgba(180, 180, 180, 70);
	}
	QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {width: 0;}
	QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
		border: none;
		width: 0;
		height: 0;
	}
	QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {background: none;}
	QScrollBar::handle:hover {background:rgba(200, 200, 200, 100)}
"""
)

caret_line = editor.features.append(CaretLineHighLighter)
editor.features.append(IndentationGuides)
editor.features.append(AutoIndent)
editor.features.append(CursorHistory)
editor.features.append(SmartBackSpace)
symbol_margin = editor.panels.append(MarkerMargin, Panel.Position.LEFT, 1)
editor.panels.append(LineNumberMargin, Panel.Position.LEFT, 1)

# dont:
#	editor.panels.append(LineNumberMargin, Panel.Position.LEFT)
#	editor.panels.append(LineNumberMargin, Panel.Position.LEFT)

# do:
#	editor.panels.append(LineNumberMargin, Panel.Position.LEFT)
#	class LNM(LineNumberMargin):
#		pass
#	editor.panels.append(LNM, Panel.Position.LEFT)

h_scrollbar = editor.panels.append(HorizontalScrollBar, Panel.Position.BOTTOM)
v_scrollbar = editor.panels.append(VerticalScrollBar, Panel.Position.RIGHT)
editor.setCursorWidth(2)
minimap = editor.panels.append(MiniMap, Panel.Position.RIGHT, 2)
editor.panels.append(BreadcrumbNav, Panel.Position.TOP, 1)

editor1 = ChellyEditor(div)
editor1.features.append(CaretLineHighLighter)
editor1.features.append(IndentationGuides)
editor1.features.append(AutoIndent)
editor1.features.append(CursorHistory)
editor1.features.append(SmartBackSpace)
editor1.panels.append(MarkerMargin, Panel.Position.LEFT)
editor1.panels.append(LineNumberMargin, Panel.Position.LEFT)

h_scrollbar1 = HorizontalScrollBar(editor1)
v_scrollbar1 = VerticalScrollBar(editor1)
editor1.setCursorWidth(2)
editor1.panels.append(h_scrollbar1, Panel.Position.BOTTOM)
editor1.panels.append(v_scrollbar1, Panel.Position.RIGHT)
minimap1 = editor1.panels.append(MiniMap, Panel.Position.RIGHT, 2)
editor1.panels.append(BreadcrumbNav, Panel.Position.TOP, 1)

editor.language.lexer = {"language":PythonLanguage, "style":"one-dark"}

with minimap as m:
	m.language.lexer = [PythonLanguage, "one-dark"]

editor1.language.lexer = (PythonLanguage, "one-dark")
PygmentsSH(minimap1.code_viewer, color_scheme="one-dark")

div.addWidget(editor)
div.addWidget(editor1)
div.resize(700, 500)
div.show()

editor1.properties.indent_with_spaces = True
editor.setVerticalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
editor.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

editor1.setVerticalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
editor1.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

def test_lexer_set(benchmark):
	new_lexer = benchmark(LanguagesManager, editor)
	editor.lexer = new_lexer
	assert editor.lexer == new_lexer

def test_singleton_panel(benchmark):
	minimap = benchmark(editor.panels.get, MiniMap)
	assert minimap == editor.panels.append(MiniMap, Panel.Position.RIGHT)

def test_feature_set(benchmark):
	new_features = benchmark(FeaturesManager, editor)
	editor.features = new_features
	assert editor.features == new_features

def test_load_file(benchmark):
	with open(__file__, "r") as infile:
		content = benchmark(infile.read)

	editor.properties.text = content
	assert editor.properties.text == content

def add_mark_at_line(sm, line:int):
	sm.add_marker(
		Marker(
			line,
			QIcon(
				pathlib.Path.cwd()
				.joinpath("dev")
				.joinpath("local_resources")
				.joinpath("mark-test.png")
				.as_posix()
			),
			"An example mark"
		)
	)

def rem_mark_at_line(sm, line:int):
	sm.remove_marker(
		sm.marker_for_line(line)
	)

symbol_margin.on_add_marker.connect(lambda line: add_mark_at_line(symbol_margin, line))
symbol_margin.on_remove_marker.connect(lambda line: rem_mark_at_line(symbol_margin, line))
symbol_margin1 = editor1.panels.get(MarkerMargin)
symbol_margin1.on_add_marker.connect(lambda line: add_mark_at_line(symbol_margin1, line))
symbol_margin1.on_remove_marker.connect(lambda line: rem_mark_at_line(symbol_margin1, line))

editor.style.theme.set_margin_style(LineNumberMargin)
editor.style.theme.set_margin_highlight(LineNumberMargin, QColor("#72c3f0"))

#dont: editor1.style = editor.style
#do: editor1.style.theme = editor.style.theme
editor1.style.theme = editor.style.theme
#editor1.style.theme.selection.foreground = QColor("#2b2b2b")

if __name__ == "__main__":
	def fake_benchmark(any):
		return any()
	test_load_file(fake_benchmark)

app.exec()