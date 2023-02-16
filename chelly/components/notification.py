from typing import Union
from typing_extensions import Self
from qtpy.QtWidgets import (
    QLabel,
    QPushButton,
    QGraphicsDropShadowEffect,
    QFrame,
    QHBoxLayout,
)
from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QColor, QIcon, QPalette
from ..core import Panel
import qtawesome


class NotificationPanel(Panel):
    class CloseButton(QPushButton):
        def __init__(self, *args, **kvargs):
            super().__init__(*args, **kvargs)

    class NotificationCard:
        @property
        def buttons(self) -> list:
            return self.__buttons

        @buttons.setter
        def buttons(self, new_buttons: list):
            if isinstance(new_buttons, list):
                self.__buttons = new_buttons
            else:
                self.__buttons = [new_buttons]

        @property
        def icon(self) -> str:
            return self.__icon

        @icon.setter
        def icon(self, new_icon: str):
            if isinstance(new_icon, QIcon):
                self.__icon = new_icon
            else:
                self.__icon = qtawesome.icon(str(new_icon))

        @property
        def text(self) -> str:
            return self.__text

        @text.setter
        def text(self, new_text: str):
            self.__text = new_text

        def __init__(self, icon: str = QIcon(), text: str = None, buttons: list = None):
            if buttons is None:
                buttons = []

            if isinstance(icon, QIcon):
                self.__icon = icon
            else:
                self.__icon = qtawesome.icon(str(icon))
            self.__text = text
            self.__buttons = buttons

    @property
    def card(self) -> NotificationCard:
        return self.__card

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.scrollable = False
        self.setAutoFillBackground(True)

        self.box = QHBoxLayout(self)
        self.setLayout(self.box)

        self.__icon = qtawesome.IconWidget()
        self.__icon.setMaximumWidth(32)
        self.__display = QLabel(self)
        self.__buttons = QHBoxLayout()
        self.__close_button = NotificationPanel.CloseButton(self)
        self.__close_button.setIcon(qtawesome.icon("mdi.close"))
        self.__close_button.setMaximumWidth(32)
        self.__close_button.clicked.connect(self.hide)

        self.box.addWidget(self.__icon)
        self.box.addWidget(self.__display)
        self.box.addLayout(self.__buttons)
        self.box.addWidget(self.__close_button)

        self.box.setContentsMargins(1, 1, 1, 1)

        self.drop_shadow = QGraphicsDropShadowEffect(self)
        self.drop_shadow.setColor(QColor("#111111"))
        self.drop_shadow.setXOffset(-1)
        self.drop_shadow.setYOffset(3)
        self.drop_shadow.setBlurRadius(6)
        self.setGraphicsEffect(self.drop_shadow)
        self.setVisible(False)
        self.bind()

    def bind(self):
        self.editor.on_painted.connect(self.update_shadow)
        self.update_shadow()

    def update_shadow(self):
        if self.editor.verticalScrollBar().value() > 0:
            self.drop_shadow.setEnabled(True)
        else:
            self.drop_shadow.setEnabled(False)

        return self

    def sizeHint(self) -> QSize:
        """
        Returns the panel size hint. (fixed with of 16px)
        """
        size_hint = QSize()
        size_hint.setWidth(24)
        size_hint.setHeight(24)
        return size_hint

    @card.setter
    def card(self, notication_card: NotificationCard) -> Self:
        self.__icon.setIcon(notication_card.icon)
        self.__display.setText(notication_card.text)

        while self.__buttons.takeAt(0) is not None:
            widget = self.__buttons.itemAt(0).widget()
            self.__buttons.removeWidget(widget)

        for button in notication_card.buttons:
            self.__buttons.addWidget(button)

        self.__card = notication_card

    def clear(self) -> Self:
        self.__card = None
        self.setVisible(False)
        return self


__all__ = ["NotificationPanel"]
