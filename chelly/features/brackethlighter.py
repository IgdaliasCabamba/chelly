# -*- coding: utf-8 -*-
"""
This module contains the symbol matcher mode
"""
from ..core import Feature, TextDecoration
from qtpy import QtGui

class ParenthesisInfo(object):
    """
    Stores information about a parenthesis in a line of code.
    """

    def __init__(self, pos, char):
        #: Position of the parenthesis, expressed as a number of character
        self.position = pos
        #: The parenthesis character, one of "(", ")", "{", "}", "[", "]"
        self.character = char

def get_block_symbol_data(editor, block):
    """
    Gets the list of ParenthesisInfo for specific text block.
    :param editor: Code edit instance
    :param block: block to parse
    """
    def list_symbols(editor, block, character):
        """
        Retuns  a list of symbols found in the block text
        :param editor: code edit instance
        :param block: block to parse
        :param character: character to look for.
        """
        text = block.text()
        symbols = []
        cursor = QtGui.QTextCursor(block)
        cursor.movePosition(cursor.StartOfBlock)
        pos = text.find(character, 0)
        cursor.movePosition(cursor.Right, cursor.MoveAnchor, pos)

        while pos != -1:
            
            # skips symbols in string literal or comment
            info = ParenthesisInfo(pos, character)
            symbols.append(info)

            pos = text.find(character, pos + 1)
            cursor.movePosition(cursor.StartOfBlock)
            cursor.movePosition(cursor.Right, cursor.MoveAnchor, pos)
        return symbols

    parentheses = sorted(
        list_symbols(editor, block, '(') + list_symbols(editor, block, ')'),
        key=lambda x: x.position)
    square_brackets = sorted(
        list_symbols(editor, block, '[') + list_symbols(editor, block, ']'),
        key=lambda x: x.position)
    braces = sorted(
        list_symbols(editor, block, '{') + list_symbols(editor, block, '}'),
        key=lambda x: x.position)
    return parentheses, square_brackets, braces



#: symbols indices in SymbolMatcherMode.SYMBOLS map
PAREN = 0
SQUARE = 1
BRACE = 2

#: character indices in SymbolMatcherMode.SYMBOLS map
OPEN = 0
CLOSE = 1


class SymbolMatcher(Feature):
    """ Highlights matching symbols (parentheses, braces,...)
    .. note:: This mode requires the document to be filled with
        :class:`pyqode.core.api.TextBlockUserData`, i.e. a
        :class:`pyqode.core.api.SyntaxHighlighter` must be installed on
        the editor instance.
    """
    #: known symbols {SYMBOL: (OPEN, CLOSE)}, you can customise this map to
    #: add support for other symbols
    SYMBOLS = {
        PAREN: ('(', ')'),
        SQUARE: ('[', ']'),
        BRACE: ('{', '}')
    }

    @property
    def match_background(self):
        """
        Background color of matching symbols.
        """
        return self._match_background

    @match_background.setter
    def match_background(self, value):
        self._match_background = value
        self._refresh_decorations()

    @property
    def match_foreground(self):
        """
        Foreground color of matching symbols.
        """
        return self._match_foreground

    @match_foreground.setter
    def match_foreground(self, value):
        self._match_foreground = value
        self._refresh_decorations()


    @property
    def unmatch_background(self):
        """
        Background color of non-matching symbols.
        """
        return self._unmatch_background

    @unmatch_background.setter
    def unmatch_background(self, value):
        self._unmatch_background = value
        self._refresh_decorations()

    @property
    def unmatch_foreground(self):
        """
        Foreground color of matching symbols.
        """
        return self._unmatch_foreground

    @unmatch_foreground.setter
    def unmatch_foreground(self, value):
        self._unmatch_foreground = value
        self._refresh_decorations()

    def __init__(self, editor):
        super().__init__(editor)
        self._decorations = []
        self._match_background = QtGui.QBrush(QtGui.QColor('#B4EEB4'))
        self._match_foreground = QtGui.QColor('red')
        self._unmatch_background = QtGui.QBrush(QtGui.QColor('transparent'))
        self._unmatch_foreground = QtGui.QColor('red')
        self.editor.cursorPositionChanged.connect(self.do_symbols_matching)

    def _clear_decorations(self):
        for deco in self._decorations:
            self.editor.decorations.remove(deco)
        self._decorations[:] = []

    def symbol_pos(self, cursor, character_type=OPEN, symbol_type=PAREN):
        """
        Find the corresponding symbol position (line, column) of the specified
        symbol. If symbol type is PAREN and character_type is OPEN, the
        function will look for '('.
        :param cursor: QTextCursor
        :param character_type: character type to look for (open or close char)
        :param symbol_type: symbol type (index in the SYMBOLS map).
        """
        retval = None, None
        original_cursor = self.editor.textCursor()
        self.editor.setTextCursor(cursor)
        block = cursor.block()
        data = get_block_symbol_data(self.editor, block)
        self._match(symbol_type, data, block.position())
        for deco in self._decorations:
            if deco.character == self.SYMBOLS[symbol_type][character_type]:
                retval = deco.line, deco.column
                break
        self.editor.setTextCursor(original_cursor)
        self._clear_decorations()
        return retval

    def _refresh_decorations(self):
        for deco in self._decorations:
            self.editor.decorations.remove(deco)
            if deco.match:
                deco.set_foreground(self._match_foreground)
                deco.set_background(self._match_background)
            else:
                deco.set_foreground(self._unmatch_foreground)
                deco.set_background(self._unmatch_background)
            self.editor.decorations.append(deco)

    def _match(self, symbol, data, cursor_pos):
        symbols = data[symbol]
        for i, info in enumerate(symbols):
            pos = (self.editor.textCursor().position() -
                   self.editor.textCursor().block().position())
            if info.character == self.SYMBOLS[symbol][OPEN] and \
                    info.position == pos:
                self._create_decoration(
                    cursor_pos + info.position,
                    self._match_left(
                        symbol, self.editor.textCursor().block(), i + 1, 0))
            elif info.character == self.SYMBOLS[symbol][CLOSE] and \
                    info.position == pos - 1:
                self._create_decoration(
                    cursor_pos + info.position,
                    self._match_right(
                        symbol, self.editor.textCursor().block(), i - 1, 0))

    def _match_left(self, symbol, current_block, i, cpt):
        while current_block.isValid():
            data = get_block_symbol_data(self.editor, current_block)
            parentheses = data[symbol]
            for j in range(i, len(parentheses)):
                info = parentheses[j]
                if info.character == self.SYMBOLS[symbol][OPEN]:
                    cpt += 1
                    continue
                if info.character == self.SYMBOLS[symbol][CLOSE] and cpt == 0:
                    self._create_decoration(current_block.position() +
                                            info.position)
                    return True
                elif info.character == self.SYMBOLS[symbol][CLOSE]:
                    cpt -= 1
            current_block = current_block.next()
            i = 0
        return False

    def _match_right(self, symbol, current_block, i, nb_right_paren):
        while current_block.isValid():
            data = get_block_symbol_data(self.editor, current_block)
            parentheses = data[symbol]
            for j in range(i, -1, -1):
                if j >= 0:
                    info = parentheses[j]
                if info.character == self.SYMBOLS[symbol][CLOSE]:
                    nb_right_paren += 1
                    continue
                if info.character == self.SYMBOLS[symbol][OPEN]:
                    if nb_right_paren == 0:
                        self._create_decoration(
                            current_block.position() + info.position)
                        return True
                    else:
                        nb_right_paren -= 1
            current_block = current_block.previous()
            data = get_block_symbol_data(self.editor, current_block)
            parentheses = data[symbol]
            i = len(parentheses) - 1
        return False

    def do_symbols_matching(self):
        """
        Performs symbols matching.
        """
        self._clear_decorations()
        current_block = self.editor.textCursor().block()
        data = get_block_symbol_data(self.editor, current_block)
        pos = self.editor.textCursor().block().position()
        for symbol in [PAREN, SQUARE, BRACE]:
            self._match(symbol, data, pos)

    def _create_decoration(self, pos, match=True):
        cursor = self.editor.textCursor()
        cursor.setPosition(pos)
        cursor.movePosition(cursor.NextCharacter, cursor.KeepAnchor)
        deco = TextDecoration(cursor, draw_order=10)
        deco.line = cursor.blockNumber()
        deco.column = cursor.columnNumber()
        deco.character = cursor.selectedText()
        deco.match = match
        if match:
            deco.set_foreground(self._match_foreground)
            deco.set_background(self._match_background)
        else:
            deco.set_foreground(self._unmatch_foreground)
            deco.set_background(self._unmatch_background)
        self._decorations.append(deco)
        self.editor.decorations.append(deco)
        return cursor

    def clone_settings(self, original):
        self.match_background = original.match_background
        self.match_foreground = original.match_foreground
        self.unmatch_background = original.unmatch_background
        self.unmatch_foreground = original.unmatch_foreground