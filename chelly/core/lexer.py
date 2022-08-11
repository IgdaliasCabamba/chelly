from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtCore import QRegularExpression, Qt

class Highlighter(QSyntaxHighlighter):
    
    class HighlightingRule():
        pattern = QRegularExpression()
        format = QTextCharFormat()
    
    class Format(QTextCharFormat):
        def __init__(self, *args, **kvargs):
            super().__init__(*args, **kvargs)

    class Expression(QRegularExpression):
        def __init__(self, *args, **kvargs):
            super().__init__(*args, **kvargs)

    highlighting_rules = []