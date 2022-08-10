from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtCore import QRegularExpression, Qt

class Highlighter(QSyntaxHighlighter):

    class HighlightingRule():
        pattern = QRegularExpression()
        format = QTextCharFormat()

    highlighting_rules = []
    commentStartExpression = QRegularExpression()
    commentEndExpression = QRegularExpression()
    keywordFormat = QTextCharFormat()
    classFormat = QTextCharFormat()
    singleLineCommentFormat = QTextCharFormat()
    multiLineCommentFormat = QTextCharFormat()
    quotationFormat = QTextCharFormat()
    functionFormat = QTextCharFormat()
    
    def __init__(self, parent):
        super().__init__(parent)

        rule = Highlighter.HighlightingRule()
        self.keywordFormat.setForeground(Qt.GlobalColor.darkBlue)
        self.keywordFormat.setFontWeight(QFont.Weight.Bold)
        keywordPatterns = {
            "\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
            "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b",
            "\\bfriend\\b", "\\binline\\b", "\\bint\\b",
            "\\blong\\b", "\\bnamespace\\b", "\\boperator\\b",
            "\\bprivate\\b", "\\bprotected\\b", "\\bpublic\\b",
            "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
            "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
            "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
            "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b",
            "\\bvoid\\b", "\\bvolatile\\b", "\\bbool\\b"
        }

        for pattern in keywordPatterns:
            rule = Highlighter.HighlightingRule()
            rule.pattern = QRegularExpression(pattern)
            rule.format = self.keywordFormat
            self.highlighting_rules.append(rule)
        
        self.classFormat.setFontWeight(QFont.Weight.Bold)
        self.classFormat.setForeground(Qt.GlobalColor.darkMagenta)
        rule.pattern = QRegularExpression("\\bQ[A-Za-z]+\\b")
        rule.format = self.classFormat
        self.highlighting_rules.append(rule)
        self.quotationFormat.setForeground(Qt.GlobalColor.darkGreen)
        rule.pattern = QRegularExpression("\".*\"")
        rule.format = self.quotationFormat
        self.highlighting_rules.append(rule)
        self.functionFormat.setFontItalic(True)
        self.functionFormat.setForeground(Qt.GlobalColor.blue)
        rule.pattern = QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()")
        rule.format = self.functionFormat
        self.highlighting_rules.append(rule)

        self.singleLineCommentFormat.setForeground(Qt.GlobalColor.red)
        rule.pattern = QRegularExpression("//[^\n]*")
        rule.format = self.singleLineCommentFormat
        self.highlighting_rules.append(rule)
        self.multiLineCommentFormat.setForeground(Qt.GlobalColor.red)
        self.commentStartExpression = QRegularExpression("/\\*")
        self.commentEndExpression = QRegularExpression("\\*/")

    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            matchIterator = rule.pattern.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)
        
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

            self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
            match = self.commentStartExpression.match(text, startIndex + commentLength)
            startIndex = match.capturedStart()