import sys

from chelly.components.externals.chelly_completer.manager import CompleterManager
from chelly.components.externals.chelly_completer.text_completer import Completer
sys.dont_write_bytecode = True

import os
os.environ["QT_API"] = "PySide6"
os.environ["QT_QPA_PLATFORM"] = "xcb" # Wayland scale issue

from pygments.styles.dracula import DraculaStyle
from pygments.styles.monokai import MonokaiStyle
from pygments.styles.paraiso_dark import ParaisoDarkStyle
from pygments.styles.onedark import OneDarkStyle

import qtawesome
from dev.libs.qtmodern import windows as qtmodern_windows
from dev.libs.qtmodern import styles as qtmodern_styles
from chelly.managers import FeaturesManager, LanguagesManager, PanelsManager
from chelly.languages import PythonLanguage, JavaScriptLanguage
from chelly.languages.sh.python_test import PythonLanguageNew
from chelly.features import (AutoIndent, CaretLineHighLighter, CursorHistory,
							 IndentationGuides, SmartBackSpace, IndentationMarks, EdgeLine, AutoComplete, ZoomMode, SymbolMatcher)
from chelly.core import Panel
from chelly.components import (NotificationPanel, HorizontalScrollBar,
							   LineNumberMargin, MarkerObject, MarkerMargin, MiniMap,
							   VerticalScrollBar, BreadcrumbNav, EditionMargin)
from chelly.api import ChellyEditor
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import pytest
import pathlib
import logging
import sys

sys.dont_write_bytecode = True
DEBUG_OUTPUT_FILE = os.path.join("dev", "chelly.log")
pathlib.Path(DEBUG_OUTPUT_FILE).touch(exist_ok=True)

logging.basicConfig(filename=DEBUG_OUTPUT_FILE, filemode='a',
					format='%(name)s - %(levelname)s - %(message)s')

app = QApplication(sys.argv)
qtmodern_styles.dark(app)

div = QSplitter()

modern_window = qtmodern_windows.ModernWindow(div)

editor = ChellyEditor(div)
editor.setCornerWidget(None)
div.setStyleSheet(
	"""
	LineNumberMargin, QLabel, MiniMap MiniMapEditor, ChellyEditor {
		color: #ccc;
		background-color: #1e1e1e;
		border:none
	}
	LineNumberMargin, QLabel, MiniMap {
		font-family:Monaco;
		font-size:10pt;
	}
	BreadcrumbNav{
		background-color: #1e1e1e;
		border:none
	}
	NotificationPanel{
		background-color: rgb(2, 109, 196);
	}
	NotificationPanel QPushButton{
		background-color: #0d0d0d;
	}
	NotificationPanel QLabel, NotificationPanel CloseButton{
		background-color: transparent;
		border:none
	}
	MiniMap{
		border: none;
	}

	QListView{
		background-color: #222;
		border: 1px solid #333;
		font-family:Monaco;
		font-size:10pt;
	}

	QSplitter::handle {background-color:#252526}
	QSplitter::handle:horizontal {width: 2px}
	QSplitter::handle:vertical {height: 2px}
	QSplitter::handle:pressed {background-color:#00a2e8}

	ChellyEditor QScrollBar:vertical {
		border: none;
		border-left: 0.5px solid rgb(60, 60, 60);
		border-top: 0.5px solid rgb(60, 60, 60);
		background: transparent;
	}
	ChellyEditor QScrollBar::handle:vertical {
		min-height: 24px;
		background:rgba(180, 180, 180, 70);
	}
	ChellyEditor QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {height: 0;}
	ChellyEditor QScrollBar:left-arrow:vertical, QScrollBar::right-arrow:vertical {
		height: 0;
		width: 0;
	}
	ChellyEditor QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}
	ChellyEditor QScrollBar:horizontal {
		border: none;
		background: transparent;
	}
	ChellyEditor QScrollBar::handle:horizontal {
		background:rgba(180, 180, 180, 70);
	}
	ChellyEditor QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {width: 0;}
	ChellyEditor QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
		border: none;
		width: 0;
		height: 0;
	}
	ChellyEditor QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {background: none;}
	ChellyEditor QScrollBar::handle:hover {background:rgba(200, 200, 200, 100)}
"""
)

caret_line = editor.features.append(CaretLineHighLighter)
indentation_guides1: IndentationGuides = editor.features.append(IndentationGuides)
auto_indent1: AutoIndent = editor.features.append(AutoIndent)
editor.features.append(CursorHistory)
editor.features.append(SmartBackSpace)
editor.features.append(IndentationMarks)
editor.features.append(EdgeLine)
editor.features.append(AutoComplete)
editor.features.append(ZoomMode)
editor.features.append(SymbolMatcher)
symbol_margin: MarkerMargin = editor.panels.append(MarkerMargin, Panel.Position.LEFT, Panel.WidgetSettings(level = 2))
editor.panels.append(LineNumberMargin, Panel.Position.LEFT, Panel.WidgetSettings(level = 2))
editor.panels.append(EditionMargin, Panel.Position.LEFT, Panel.WidgetSettings(level = 2))

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
minimap: MiniMap = editor.panels.append(MiniMap, Panel.Position.RIGHT, Panel.WidgetSettings(level = 2))
minimap.chelly_editor.features.append(CaretLineHighLighter)
minimap.chelly_editor.panels.append(EditionMargin, Panel.Position.LEFT, Panel.WidgetSettings(level = 2))
breadcrumbs: BreadcrumbNav = editor.panels.append(
	BreadcrumbNav, Panel.Position.TOP, Panel.WidgetSettings(level = 2))

editor1 = ChellyEditor(div)
editor1.features.append(EdgeLine)
editor1.features.append(AutoComplete)
editor1.features.append(ZoomMode)
editor1.features.append(CaretLineHighLighter)
editor1.features.append(IndentationGuides)
editor1.features.append(AutoIndent)
editor1.features.append(CursorHistory)
editor1.features.append(SmartBackSpace)
editor1.features.append(IndentationMarks)
editor1.features.append(SymbolMatcher)
editor1.panels.append(MarkerMargin, Panel.Position.LEFT)
editor1.panels.append(LineNumberMargin, Panel.Position.LEFT)
editor1.panels.append(EditionMargin, Panel.Position.LEFT, Panel.WidgetSettings(level = 2))

h_scrollbar1 = HorizontalScrollBar(editor1)
v_scrollbar1 = VerticalScrollBar(editor1)
editor1.setCursorWidth(2)
editor1.panels.append(h_scrollbar1, Panel.Position.BOTTOM)
editor1.panels.append(v_scrollbar1, Panel.Position.RIGHT)
minimap1: MiniMap = editor1.panels.append(MiniMap, Panel.Position.RIGHT, Panel.WidgetSettings(level = 2))
minimap1.chelly_editor.features.append(CaretLineHighLighter)
minimap1.chelly_editor.panels.append(EditionMargin, Panel.Position.LEFT, Panel.WidgetSettings(level = 2))
notify: NotificationPanel = editor1.panels.append(
	NotificationPanel, Panel.Position.TOP, Panel.WidgetSettings(level = 1))

notification = NotificationPanel.NotificationCard()
notification.text = "Hey idiot, are u sleeping? LOL, ur <strong>githoob</strong> account got hacked"
notification.icon = "fa5b.github"
notification_action1 = QPushButton("Take me to it")
notification_action1.setMaximumWidth(100)
notification.buttons = [notification_action1]

notify.card = notification
notify.setVisible(True)

editor.language.lexer = {"language": PythonLanguage, "style": ParaisoDarkStyle}

with minimap as m:
	m.language.lexer = [PythonLanguage, MonokaiStyle]

#editor1.language.lexer = (JavaScriptLanguage, "github-dark")
editor1.language.lexer = (PythonLanguageNew, OneDarkStyle)
#PythonLanguageNew(editor1, OneDarkStyle)
minimap1.chelly_editor.language.lexer = (PythonLanguage, DraculaStyle)

div.addWidget(editor)
div.addWidget(editor1)

editor1.properties.indent_with_spaces = True
editor.setVerticalScrollBarPolicy(
	Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
editor.setHorizontalScrollBarPolicy(
	Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

editor1.setVerticalScrollBarPolicy(
	Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
editor1.setHorizontalScrollBarPolicy(
	Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

def add_mark_at_line(sm:MarkerMargin, line: int):
	if sm == symbol_margin:
		sm.add_marker(
			MarkerObject(
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
	else:
		mark_icon = qtawesome.icon("msc.debug-stackframe-dot", options=[{
                'scale_factor': 2.0,
                'active': 'fa5s.balance-scale',
				'color': 'red'
            }])
		sm.add_marker(MarkerObject(line, mark_icon))


def rem_mark_at_line(sm:MarkerMargin, line: int):
	sm.remove_marker(
		sm.marker_for_line(line)
	)


symbol_margin.on_add_marker.connect(
	lambda line: add_mark_at_line(symbol_margin, line))
symbol_margin.on_remove_marker.connect(
	lambda line: rem_mark_at_line(symbol_margin, line))
symbol_margin1 = editor1.panels.get(MarkerMargin)
symbol_margin1.on_add_marker.connect(
	lambda line: add_mark_at_line(symbol_margin1, line))
symbol_margin1.on_remove_marker.connect(
	lambda line: rem_mark_at_line(symbol_margin1, line))


def create_breadcrumbs():
	foo_block = BreadcrumbNav.BreadcrumbBlock()
	foo_block.content = "foo"
	foo_block.icon = qtawesome.icon("msc.symbol-variable")

	bar_block = BreadcrumbNav.BreadcrumbBlock()
	bar_block.content = "bar"
	bar_block.icon = qtawesome.icon("msc.symbol-class")

	foobar_block = BreadcrumbNav.BreadcrumbBlock()
	foobar_block.content = "FooBar"
	foobar_block.icon = qtawesome.icon("msc.symbol-property")

	bad_block = BreadcrumbNav.BreadcrumbBlock(content="I'm a bad block hahaha")

	breadcrumbs.append_breadcrumb(foo_block)
	breadcrumbs.append_breadcrumb(bad_block)
	breadcrumbs.append_breadcrumb(bar_block)
	breadcrumbs.append_breadcrumb(foobar_block)

	new_foobar_block = BreadcrumbNav.BreadcrumbBlock()
	new_foobar_block.content = "fooba"
	new_foobar_block.icon = qtawesome.icon("msc.symbol-property")

	breadcrumbs.update_breadcrumb(foobar_block, new_foobar_block)
	breadcrumbs.update_breadcrumb(foobar_block, {"content": "foobar"})

	breadcrumbs.remove_breadcrumb(bad_block)
	# breadcrumbs.remove_breadcrumb(foo_block)

	breadcrumbs.insert_breadcrumb(bad_block, 0)
	# breadcrumbs.clear_all_breadcrumbs()


create_breadcrumbs()

# TODO
#editor.commands.zoom_in(15)
#editor.commands.zoom_out(10) # -> 5
#editor.commands.reset_zoom() # -> 0
line_number_margin:LineNumberMargin = editor.panels.get(LineNumberMargin)
line_number_margin.styles.highlight = QColor("#72c3f0")

# Use these functions to share references:
#editor1.panels.get(LineNumberMargin).shared_reference = editor.panels.get(LineNumberMargin).shared_reference
#editor1.panels.shared_reference = editor.panels

editor1.shared_reference = editor

# TODO: fix style shared reference

#editor.shared_reference = editor1 BUG: autocomplete change focus
#editor1.style.shared_reference = editor.style

#dont: editor1.style = editor.style
#do: editor1.style.theme = editor.style.theme

#editor1.style.theme = editor.style.theme
#minimap.chelly_editor.style.theme = editor.style.theme

editor1.style.theme.selection_foreground = QColor("#2b2b2b")
editor.style.theme.selection_background = QColor(Qt.GlobalColor.red)
print(editor.style.theme == editor1.style.theme)

modern_window.resize(1000, 600)
modern_window.move(200, 100)
modern_window.setWindowTitle("ChellyEditor Preview")
modern_window.show()
#div.resize(1000, 600)
#div.move(200, 100)
#div.setWindowTitle("ChellyEditor Preview")
#div.show()

x = CompleterManager(editor)
y: Completer = x.set_completion_list(Completer)
y.setCustomCompletions({"ola", "hello", "hi", "thanks", "more", "love"})

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

if __name__ == "__main__":
	def fake_benchmark(any):
		return any()
	test_load_file(fake_benchmark)

app.exec()