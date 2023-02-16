from qtpy.QtGui import QFont
from qtpy.QtCore import Qt
from ...core import Highlighter


class PythonHighlighter(Highlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.comment_start_expression = Highlighter.Expression()
        self.comment_end_expression = Highlighter.Expression()

        self.keyword_format = Highlighter.Format()
        self.class_format = Highlighter.Format()
        self.single_line_comment_format = Highlighter.Format()
        self.multi_line_comment_format = Highlighter.Format()
        self.quotation_format = Highlighter.Format()
        self.function_format = Highlighter.Format()

        rule = Highlighter.HighlightingRule()
        self.keyword_format = Highlighter.Format()

        self.keyword_format.setForeground(Qt.GlobalColor.darkBlue)
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        keywordPatterns = {
            "\\bstr\\b",
            "\\bclass\\b",
            "\\bdef\\b",
            "\\bfloat\\b",
            "\\bwhile\\b",
            "\\bint\\b",
            "\\bTrue\\b",
            "\\bNone\\b",
            "\\bFalse\\b",
            "\\blong\\b",
            "\\bnamespace\\b",
            "\\boperator\\b",
            "\\bprivate\\b",
            "\\bprotected\\b",
            "\\bpublic\\b",
            "\\bshort\\b",
            "\\bsignals\\b",
            "\\bsigned\\b",
            "\\bslots\\b",
            "\\bstatic\\b",
            "\\bstruct\\b",
            "\\btemplate\\b",
            "\\btypedef\\b",
            "\\btypename\\b",
            "\\bunion\\b",
            "\\bunsigned\\b",
            "\\bvirtual\\b",
            "\\bvoid\\b",
            "\\bvolatile\\b",
            "\\bbool\\b",
        }

        for pattern in keywordPatterns:
            rule = Highlighter.HighlightingRule()
            rule.pattern = Highlighter.Expression(pattern)
            rule.format = self.keyword_format
            self.highlighting_rules.append(rule)

        self.class_format.setFontWeight(QFont.Weight.Bold)
        self.class_format.setForeground(Qt.GlobalColor.darkMagenta)
        rule.pattern = Highlighter.Expression("\\bQ[A-Za-z]+\\b")
        rule.format = self.class_format
        self.highlighting_rules.append(rule)
        self.quotation_format.setForeground(Qt.GlobalColor.darkGreen)
        rule.pattern = Highlighter.Expression('".*"')
        rule.format = self.quotation_format
        self.highlighting_rules.append(rule)
        self.function_format.setFontItalic(True)
        self.function_format.setForeground(Qt.GlobalColor.blue)
        rule.pattern = Highlighter.Expression("\\b[A-Za-z0-9_]+(?=\\()")
        rule.format = self.function_format
        self.highlighting_rules.append(rule)

        self.single_line_comment_format.setForeground(Qt.GlobalColor.red)
        rule.pattern = Highlighter.Expression("//[^\n]*")
        rule.format = self.single_line_comment_format
        self.highlighting_rules.append(rule)
        self.multi_line_comment_format.setForeground(Qt.GlobalColor.red)
        self.commentStartExpression = Highlighter.Expression("/\\*")
        self.commentEndExpression = Highlighter.Expression("\\*/")

    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            matchIterator = rule.pattern.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(
                    match.capturedStart(), match.capturedLength(), rule.format
                )

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            match = self.commentStartExpression.match(text)
            startIndex = match.capturedStart()

        while startIndex >= 0:
            match = self.commentEndExpression.match(text, startIndex)
            endIndex = match.capturedStart()
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + match.capturedLength()

            self.setFormat(startIndex, commentLength, self.multi_line_comment_format)
            match = self.commentStartExpression.match(text, startIndex + commentLength)
            startIndex = match.capturedStart()


__all__ = ["PythonHighlighter"]
