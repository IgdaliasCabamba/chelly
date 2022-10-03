from pprint import pprint
from typing import Any, Union
from typing_extensions import Self
from qtpy.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QWidget, QSizePolicy
from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QColor, QIcon
from ..core import Panel, sanitize_html, icon_to_base64
import qtawesome


class BreadcrumbNav(Panel):

    class BreadcrumbBlock:
        def __init__(self, action: str = None, style: str = None, icon: str = None, content: str = None, *args, **kvargs):
            self.__action = action
            self.__style = style
            self.__icon = icon
            self.__content = content
            self.__index = -1
            self.__breadcrumb_item_layout = None
        
        @property
        def index(self) -> int:
            return self.__index

        @index.setter
        def index(self, index: int) -> None:
            self.__index = index

        @property
        def breadcrumb_item_layout(self) -> Union[QWidget, None]:
            return self.__breadcrumb_item_layout

        @breadcrumb_item_layout.setter
        def breadcrumb_item_layout(self, item_layout: QWidget) -> None:
            self.__breadcrumb_item_layout = item_layout

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
        
        @property
        def as_dict(self) -> dict:
            return {
                "action":self.action,
                "breadcrumb_item_layout":self.breadcrumb_item_layout,
                "content":self.content,
                "icon":self.icon,
                "index":self.index,
                "style":self.style
            }
        
        def update_properties(self, new_properties:dict) -> Self:
            for prop, value in new_properties.items():
                if isinstance(prop, str):
                    if hasattr(self, prop) and value is not None:
                        setattr(self, prop, value)
            return self


    class BreadcrumbIcon(QLabel):
        def __init__(self, parent=None):
            super().__init__(parent)
        
        def set_icon(self, block_icon:Union[bytes, str, QIcon]) -> Self:
            base64_icon = str()
            
            if block_icon is not None:
                if isinstance(block_icon, bytes):
                    base64_image:str = block_icon.decode("utf-8")
                elif isinstance(block_icon, str):
                    base64_image:str = block_icon
                elif isinstance(block_icon, QIcon):
                    base64_image:str = icon_to_base64(block_icon, 18, "PNG")

                base64_icon = f'<img src="data:image/png;base64,{base64_image}"></img>'
            
            if base64_icon.startswith("<img"):
                self.setText(base64_icon)
            
            return self
    
    class BreadcrumbNextArrow(QLabel):
        def __init__(self, parent = None, name = "ri.arrow-right-s-line", size = 18):
            super().__init__(parent)
            self.update_icon(name, size)
        
        def update_icon(self, icon_name:str, icon_size:int = 18) -> Self:
            _icon:QIcon = qtawesome.icon(icon_name)
            base64_image:str = icon_to_base64(_icon, icon_size, "PNG")
            self.setText(f'<img src="data:image/png;base64,{base64_image}"></img>')
            return self
    
    class BreadcrumbItem(QLabel):
        def __init__(self, parent, data:dict = {}, *args, **kvargs) -> None:
            super().__init__(parent, *args, **kvargs)
            
            self.__data = data

            self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.refresh()
        
        def set_data(self, new_data:dict):
            for key, value in new_data.items():
                self.__data[key] = value
            self.refresh()

        def refresh(self) -> Self:
            new_text = str()
            content = self.__data.get("content", None)
            action = self.__data.get("action", None)
            style = self.__data.get("style", None)

            if content is not None:
                content = sanitize_html(str(content), valid_tags=["span", "img"])

            if action is None:
                new_text += f"<span style={style}>{content}</span>"
            else:
                new_text += f"<a href={action} style='text-decoration:none; {style}'>{content}</a>"

            self.setText(new_text)
            
            return self

    class BreadcrumbItemLayout(QHBoxLayout):

        @property
        def icon(self):
            return self.__icon

        @property
        def breadcrumb_item(self):
            return self.__breadcrumb_item

        @property
        def next_arrow(self):
            return self.__next_arrow

        def __init__(self, *args, **kvargs):
            super().__init__(*args, **kvargs)
            self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.setContentsMargins(0, 0, 0, 0)
            self.__icon = None
            self.__breadcrumb_item = None
            self.__next_arrow = None

        def set_icon(self, icon_widget: QWidget) -> Self:
            self.__icon = icon_widget
            self.addWidget(icon_widget)
            return self

        def set_breadcrumb_item(self, label: QLabel) -> Self:
            self.__breadcrumb_item = label
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
    
    def new_breadcrumb(self, block: BreadcrumbBlock) -> BreadcrumbItemLayout:
        breadcrumb_item = BreadcrumbNav.BreadcrumbItem(self, block.as_dict)
        breadcrumb_icon = BreadcrumbNav.BreadcrumbIcon(self)
        next_breadcrumb_arrow = BreadcrumbNav.BreadcrumbNextArrow(self)

        breadcrumb_icon.set_icon(block.icon)

        return (BreadcrumbNav.BreadcrumbItemLayout()
                      .set_icon(breadcrumb_icon)
                      .set_breadcrumb_item(breadcrumb_item)
                      .set_next_arrow(next_breadcrumb_arrow))

    def _setup_breadcrumb(self, block: BreadcrumbBlock, breadcrumb: BreadcrumbItemLayout):
        block.index = lambda: self._box.indexOf(breadcrumb) # index can change
        block.breadcrumb_item_layout = breadcrumb
        return block

    def append_breadcrumb(self, block: BreadcrumbBlock) -> BreadcrumbBlock:
        breadcrumb = self.new_breadcrumb(block)
        self._box.addLayout(breadcrumb)
        self.__blocks.append(block)
        return self._setup_breadcrumb(block, breadcrumb)
    
    def insert_breadcrumb(self, block: BreadcrumbBlock, index = 0):
        breadcrumb = self.new_breadcrumb(block)
        self._box.insertLayout(index, breadcrumb)
        self.__blocks.insert(index, block)
        return self._setup_breadcrumb(block, breadcrumb)


    def update_breadcrumb(self, block: BreadcrumbBlock, new_block: Union[dict, BreadcrumbBlock]) -> Self:
        
        if isinstance(new_block, dict):
            block.update_properties(new_block)
        
        elif isinstance(new_block, BreadcrumbNav.BreadcrumbBlock):
            block.update_properties(new_block.as_dict)
        
        breadcrumb_item:BreadcrumbNav.BreadcrumbItem = block.breadcrumb_item_layout.breadcrumb_item
        breadcrumb_item.set_data(block.as_dict)

        return self

    def remove_breadcrumb(self, block: BreadcrumbBlock, remove_from_list = True) -> Self:    
        idx:int = self._box.indexOf(block.breadcrumb_item_layout)
        breadcrumb_item_layout:BreadcrumbNav.BreadcrumbItemLayout = self._box.itemAt(idx).layout()
        
        for idx in range(breadcrumb_item_layout.count()):
            widget = breadcrumb_item_layout.itemAt(idx).widget()
            widget.setVisible(False)
            widget.deleteLater()
        
        if remove_from_list:
            self.__blocks.remove(block)

        return self

    def clear_all_breadcrumbs(self) -> Self:
        for block in self.__blocks:
            self.remove_breadcrumb(block, remove_from_list=False)
        
        self.__blocks.clear()

        while self._box.takeAt(0) is not None:
            ...

        return self
