from typing import Union
from typing_extensions import Self
from PySide6.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QWidget
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor
from ..core import Panel, sanitize_html

class BreadcrumbNav(Panel):
    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.scrollable = False
        self.__blocks = []

        self.setStyleSheet("QLabel{background:#2b2b2b}")
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)

        self._breadcrumb = QLabel(self)
        (
            self.add_block({"action": "#",
                            "style": "color:gray",
                            "content": "Foo"
                            })
            .add_block({"action": None,
                        "style": "color:gray",
                        "content": "bar"
                        })
            .add_block({"action": "#",
                        "style": "color:gray",
                        "content": "Hello"
                        })
            .add_block({"action": None,
                        "style": "color:gray",
                        "content": "world"
                        })
            .add_block({"action": None,
                        "style": "color:gray",
                        "content": "foobar"
                        })
        )

        self.box.addWidget(self._breadcrumb)
        self.setLayout(self.box)

        self.drop_shadow = QGraphicsDropShadowEffect(self)
        self.drop_shadow.setColor(QColor("#111111"))
        self.drop_shadow.setXOffset(-1)
        self.drop_shadow.setYOffset(2)
        self.drop_shadow.setBlurRadius(6)
        self.setGraphicsEffect(self.drop_shadow)

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
        size_hint = QSize(w=20, h=20)
        size_hint.setWidth(20)
        size_hint.setHeight(20)
        return size_hint

    def add_block(self, block: dict) -> Self:

        new_text = self._breadcrumb.text()
        if len(new_text) == 0:
            new_text += "&nbsp;&nbsp;"

        clean_block = sanitize_html(block["content"])

        if block["action"] is None:
            new_text += f"<span style={block['style']}>{clean_block}&nbsp;>&nbsp;</span>"
        else:
            new_text += f"<a href={block['action']} style='text-decoration:none; {block['style']}'>{clean_block}&nbsp;>&nbsp;</a>"

        self._breadcrumb.setText(new_text)
        self.__blocks.append(block)
        return self

    def remove_block(self, block) -> Self:
        if block in self.__blocks:
            self.__blocks.remove(block)
            new_text = self._breadcrumb.text().replace(block, str())
            self._breadcrumb.setText(new_text)

        return self

    def clear(self) -> Self:
        self._breadcrumb.clear()
        self.__blocks.clear()
        return self
