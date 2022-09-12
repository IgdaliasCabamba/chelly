from tkinter import N
from typing import Any, Union
from typing_extensions import Self
from PySide6.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QFrame, QWidget, QSizePolicy
from PySide6.QtCore import QSize, Qt, QByteArray, QBuffer
from PySide6.QtGui import QColor, QIcon
from ...core import Panel, sanitize_html, icon_to_base64
import qtawesome


class BreadcrumbNav(Panel):

    class BreadcrumbBlock:
        def __init__(self, action: str = None, style: str = None, icon: str = None, content: str = None, *args, **kvargs):
            self.__action = action
            self.__style = style
            self.__icon = icon
            self.__content = content
            self.__index = -1
            self.__widget = None

        @property
        def index(self) -> int:
            return self.__index

        @index.setter
        def index(self, index: int) -> None:
            self.__index = index

        @property
        def widget(self) -> Union[QWidget, None]:
            return self.__widget

        @widget.setter
        def widget(self, widget: QWidget) -> None:
            self.__widget = widget

        @property
        def action(self) -> str:
            return self.__action

        @action.setter
        def action(self, action: str) -> None:
            self.__action = action

        @property
        def style(self) -> str:
            return self.__style

        @style.setter
        def style(self, style: str) -> None:
            self.__style = style

        @property
        def icon(self) -> Union[QIcon, bytes, str]:
            return self.__icon

        @icon.setter
        def icon(self, icon: Union[QIcon, bytes, str]) -> None:
            if isinstance(icon, (QIcon, bytes)):
                self.__icon = icon
            elif isinstance(icon, str):
                self.__icon = qtawesome.icon(str(icon))
            ...

        @property
        def content(self) -> str:
            return self.__content

        @content.setter
        def content(self, content: str) -> None:
            self.__content = content

    class BreadcrumbItem(QLabel):
        def __init__(self, parent, block, *args, **kvargs) -> None:
            super().__init__(parent, *args, **kvargs)
            self.__block = block

            self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.__update()

        @property
        def block(self) -> Any:
            return self.__block

        @block.setter
        def block(self, breadcrumb_block: Any) -> None:
            self.__block = breadcrumb_block
            self.__update()

        def __update(self) -> None:
            new_text = str()
            block = self.block
            content = sanitize_html(block.content, valid_tags=["span", "img"])

            if block.action is None:
                new_text += f"<span style={block.style}>{content}</span>"
            else:
                new_text += f"<a href={block.action} style='text-decoration:none; {block.style}'>{content}</a>"

            self.setText(new_text)

    class BreadcrumbItemLayout(QHBoxLayout):

        @property
        def icon(self):
            return self.__icon

        @property
        def breadcrumb(self):
            return self.__breadcrumb
        
        @property
        def next_arrow(self):
            return self.__next_arrow

        def __init__(self, *args, **kvargs):
            super().__init__(*args, **kvargs)
            self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setContentsMargins(0, 0, 0, 0)
            self.__icon = None
            self.__breadcrumb = None
            self.__next_arrow = None

        def set_icon(self, icon_widget: QWidget) -> Self:
            self.__icon = icon_widget
            self.addWidget(icon_widget)
            return self

        def set_breadcrumb(self, label: QLabel) -> Self:
            self.__breadcrumb = label
            self.addWidget(label)
            return self

        def set_next_arrow(self, icon: QWidget) -> Self:
            self.__next_arrow = icon
            self.addWidget(icon)
            return self

    def __init__(self, editor) -> None:
        super().__init__(editor)
        self.scrollable = False
        self.__blocks = []
        self.__items = []

        self._box = QHBoxLayout(self)
        self._box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._box)

        self.drop_shadow = QGraphicsDropShadowEffect(self)
        self.drop_shadow.setColor(QColor("#111111"))
        self.drop_shadow.setXOffset(-1)
        self.drop_shadow.setYOffset(3)
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
        size_hint = QSize()
        size_hint.setWidth(20)
        size_hint.setHeight(20)
        return size_hint

    def add_block(self, block: BreadcrumbBlock) -> BreadcrumbBlock:
        new_item = BreadcrumbNav.BreadcrumbItem(self, block)
        breadcrumb_icon = QLabel()
        next_breadcrumb_arrow = QLabel()

        def build_breadcrumb_icon() -> None:
            block_icon = block.icon
        
            if block_icon is not None:
                if isinstance(block_icon, bytes):
                    _image = block_icon.decode("utf-8")
                elif isinstance(block_icon, str):
                    _image = block_icon
                elif isinstance(block_icon, QIcon):
                    _image = icon_to_base64(block_icon, 18, "PNG")

                _icon_markup = f'<span><img src="data:image/png;base64,{_image}"></img></span>'
                breadcrumb_icon.setText(_icon_markup)
        
        def build_next_arrow() -> None:
            _icon = qtawesome.icon("ri.arrow-right-s-line")
            _image = icon_to_base64(_icon, 18, "PNG")
            _icon_markup = f'<span><img src="data:image/png;base64,{_image}"></img></span>'
            next_breadcrumb_arrow.setText(_icon_markup)

        build_breadcrumb_icon()
        build_next_arrow()

        breadcrumb = (BreadcrumbNav.BreadcrumbItemLayout()
                       .set_icon(breadcrumb_icon)
                       .set_breadcrumb(new_item)
                       .set_next_arrow(next_breadcrumb_arrow))

        self._box.addLayout(breadcrumb)
        
        block.index = self._box.indexOf(breadcrumb)
        block.widget = new_item

        self.__blocks.append(block)
        self.__items.append(new_item)

        return block

    def update_block(self, block: Union[int, BreadcrumbBlock], new_block: Union[dict, BreadcrumbBlock]) -> Self:
        if isinstance(block, int):
            layout = self._box.itemAt(block).layout()
            
            if isinstance(layout, BreadcrumbNav.BreadcrumbItemLayout):
                widget = layout.breadcrumb

                if isinstance(new_block, dict):
                    ...
                    """for prop, value in new_block.items():
                        if isinstance(prop, str):
                            if not prop.startswith("_"):
                                setattr(widget, prop, value)"""

                elif isinstance(new_block, BreadcrumbNav.BreadcrumbBlock):
                    widget.block = new_block

        elif isinstance(block, BreadcrumbNav.BreadcrumbBlock):
            widget = block.widget
            if isinstance(new_block, dict):
                ...
                for key, value in new_block.items():
                    setattr(block, key, value)

            elif isinstance(new_block, BreadcrumbNav.BreadcrumbBlock):
                widget.block = new_block

        return self

    def remove_block(self, block: Union[int, BreadcrumbBlock]) -> Self:
        if isinstance(block, int):
            widget = self._box.itemAt(block).widget()
            self.__blocks.remove(widget)
            self._box.removeWidget(widget)

        elif isinstance(block, BreadcrumbNav.BreadcrumbBlock):
            idx = self._box.indexOf(block)
            return self.remove_block(idx)

        return self

    def clear(self) -> Self:
        while self._box.takeAt(0) is not None:
            widget = self._box.itemAt(0).widget()
            self._box.removeWidget(widget)

        self.__blocks.clear()

        return self
