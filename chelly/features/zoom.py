from ..core import Feature
from qtpy import QtCore, QtGui, QtWidgets

class ZoomMode(Feature):
    def __init__(self, editor):
        super().__init__(editor)
        self.prev_delta = 0

        self.editor.on_mouse_wheel_activated.connect(self._on_wheel_event)

    def _on_wheel_event(self, event: QtGui.QWheelEvent):
        delta = event.angleDelta().y()
        if int(event.modifiers()) & QtCore.Qt.ControlModifier > 0:
            if delta < self.prev_delta:
                self.editor.properties.zoom_out()
            else:
                self.editor.properties.zoom_in()