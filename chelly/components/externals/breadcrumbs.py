# UNDER CONTRUCTION

from typing import Union
from typing_extensions import Self
from PySide6.QtWidgets import QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QWidget
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor
from ...core import Panel, sanitize_html
import qtawesome

class BreadcrumbBlock:
    def __init__(self, action:str = None, style:str=None, icon:str=None, content:str = None, *args, **kwargs):
        self.__action = action 
        self.__style = style
        self.__icon = icon
        self.__content = content

    @property
    def action(self) -> str:
        return self.__action

    @action.setter
    def action(self, action:str) -> None:
        self.__action = action
    
    @property
    def style(self) -> str:
        return self.__style
    
    @style.setter
    def style(self, style:str) -> None:
        self.__style = style
    
    @property
    def icon(self) -> str:
        return self.__icon
    
    @icon.setter
    def icon(self, icon:str) -> None:
        self.__icon = icon
    
    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, content:str) -> None:
        self.__content = content

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

        block["content"] = sanitize_html(block["content"], valid_tags=["span", "img"])

        if block["action"] is None:
            new_text += f"<span style={block['style']}>{block['content']}&nbsp;>&nbsp;</span>"
        else:
            new_text += f"<a href={block['action']} style='text-decoration:none; {block['style']}'>{block['content']}&nbsp;>&nbsp;</a>"
        
        new_text += '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />'
        new_text += "&nbsp;"

        self._breadcrumb.setText(new_text)
        self.__blocks.append(block)
        
        #fa5_icon = qtawesome.icon('fa5.flag')
        #print(fa5_icon)

        return self
    
    def update_block(self, block:Union[int, dict], new_block:dict) -> Self:
        if isinstance(block, int):
            new_text = self._breadcrumb.text().replace(self.__blocks[block]["content"], new_block["content"])
            self._breadcrumb.setText(new_text)
            self.__blocks.pop(block)

        elif isinstance(block, dict) and block in self.__blocks:
            new_text = self._breadcrumb.text().replace(block["content"], new_block["content"])
            self._breadcrumb.setText(new_text)
            self.__blocks.remove(block)

        return self
    
    def remove_block(self, block:Union[int, dict]) -> Self:
        new_block = {
            "action":None,
            "content":str(),
            "style": "",
        }
        self.update_block(block, new_block)
        return self

    def clear(self) -> Self:
        self._breadcrumb.clear()
        self.__blocks.clear()
        return self
