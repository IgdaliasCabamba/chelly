import sys
from src import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import src.languages.python_highlighter as python_lexer

app = QApplication(sys.argv)

editor = Chelly(None,text="HELLO")
editor.setStyleSheet("""QPlainTextEdit{
	font-family:'Consolas'; 
	color: #ccc; 
	background-color: #2b2b2b;}""")
highlight = python_lexer.Highlighter(editor.editorview.get_editor("main").document())

#Load chelly.py into the editor for demo purposes
infile = open('src/chelly.py', 'r')
editor.editorview.get_editor("main").setPlainText(infile.read())

editor.resize(300, 500)
editor.show()

app.exec()