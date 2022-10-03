import weakref
from qtpy import QtCore, QtWidgets, QtGui
from ..core import Feature, TextEngine

class MoveCursorCommand(QtGui.QUndoCommand):
    def __init__(self, new_pos, prev_pos, editor):
        super(MoveCursorCommand, self).__init__(
            '(Goto line %d)' % (new_pos[0] + 1))
        self._new_pos = new_pos
        self._prev_pos = prev_pos
        self._editor = weakref.ref(editor)

    # TODO: update caret higlight
    def _move(self, line, column):
        self._editor().blockSignals(True)
        TextEngine(self._editor()).goto_line(line, column)
        self._editor().blockSignals(False)
        self._editor().update()

    def redo(self):
        self._move(*self._new_pos)

    def undo(self):
        self._move(*self._prev_pos)

class CursorHistory(Feature):
    def __init__(self, editor):
        super().__init__(editor)
        self._prev_pos = 0, 0
        self.undo_stack = QtGui.QUndoStack()
        self.undo_stack.setUndoLimit(100)

        self.action_undo = self.undo_stack.createUndoAction(self.editor)
        self.action_undo.setShortcut('Ctrl+Alt+Z')
        self.action_undo.setEnabled(True)

        self.action_redo = self.undo_stack.createRedoAction(self.editor)
        self.action_redo.setShortcut('Ctrl+Alt+Y')

        self.editor.cursorPositionChanged.connect(self._on_cursor_position_changed)
        self.editor.on_key_pressed.connect(self._on_key_pressed)

    def _on_cursor_position_changed(self):
        if self.editor.textCursor().hasSelection():
            return

        new_pos = TextEngine(self.editor).cursor_position
        if abs(new_pos[0] - self._prev_pos[0]) > 1:
            # only record when line changed and don't record change if the user
            # just wen to the previous/next line
            cmd = MoveCursorCommand(new_pos, self._prev_pos, self.editor)
            self.undo_stack.push(cmd)
        self._prev_pos = new_pos

    def _on_key_pressed(self, event):
        control = event.modifiers() & QtCore.Qt.ControlModifier
        alt = event.modifiers() & QtCore.Qt.AltModifier

        if event.key() == 90 and control and alt:
            self.undo_stack.undo()
        
        elif event.key() == 89 and control and alt:
            self.undo_stack.redo()
        
        event.accept()