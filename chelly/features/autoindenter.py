from ..core import Feature, TextEngine, Character
from qtpy.QtCore import Qt


class AutoIndent(Feature):
    """ Indents text automatically.
    Generic indenter mode that indents the text when the user press RETURN.
    You can customize this mode by overriding
    :meth:`pyqode.core.modes.AutoIndentMode._get_indent`
    """

    def __init__(self, editor):
        super().__init__(editor)
        self.editor.on_key_released.connect(self.__key_released)

    @property
    def _indent_char(self) -> Character:
        if self.editor.properties.indent_with_spaces:
            return Character.SPACE.value
        return Character.TAB.value

    @property
    def _single_indent(self):
        if self.editor.properties.indent_with_spaces:
            return self.editor.indent_size * Character.SPACE.value
        return Character.TAB.value

    def _get_indent(self, last_line: bool = True) -> tuple:
        """
        Return the indentation text (a series of spaces or tabs)
        :param cursor: QTextCursor
        :returns: Tuple (text before new line, text after new line)
        """
        if last_line:
            indent = (
                TextEngine(self.editor).line_indent(
                    TextEngine(self.editor).current_line_nbr-1,
                    self._indent_char
                ) * self._indent_char
            )
        else:
            indent = (TextEngine(self.editor).line_indent(indent_char=self._indent_char)
                      * self._indent_char)
        return (str(), indent)

    def __key_released(self, event):
        """
        Auto indent if the released key is the return key.
        :param event: the key event
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.editor.textCursor()
            pre, post = self._get_indent(last_line=True)
            cursor.beginEditBlock()
            cursor.insertText(f"{pre}{post}")

            # eats possible whitespaces
            cursor.movePosition(cursor.WordRight, cursor.KeepAnchor)
            text: str = cursor.selectedText()

            if text.startswith(Character.SPACE.value):
                new_txt: str = text.replace(
                    Character.SPACE.value, Character.EMPTY.value)
                if len(text) > len(new_txt):
                    cursor.insertText(new_txt)

            cursor.endEditBlock()
