import sys
from src import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


app = QApplication(sys.argv)

editor = Chelly(None,text="HELLO")
editor.resize(300, 500)
editor.show()

app.exec()