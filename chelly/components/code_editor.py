from typing import Dict, List, Union

from qtpy import QtGui
from qtpy.QtCore import QPoint, QSize, Qt, Signal
from qtpy.QtWidgets import QLabel, QPlainTextEdit
from typing_extensions import Self

from ..core import BasicCommands, ChellyDocument, ChellyStyle, Properties, TextEngine
from ..internal import (
    ChellyDocumentExceptions,
    FeaturesExceptions,
    LexerExceptions,
    PanelsExceptions,
    PropertiesExceptions,
    StyleExceptions,
    TextExceptions,
)
from ..managers import (
    FeaturesManager,
    LanguagesManager,
    PanelsManager,
    TextDecorationsManager,
)


class __CodeEditorCopy(QPlainTextEdit):

    """This is the same of ChellyEditor"""

    on_resized = Signal()
    on_painted = Signal(object)
    on_updated = Signal()
    on_key_pressed = Signal(object)
    on_key_released = Signal(object)
    on_mouse_moved = Signal(object)
    on_mouse_released = Signal(object)
    on_mouse_double_clicked = Signal(object)
    on_text_setted = Signal(str)
    on_mouse_wheel_activated = Signal(object)
    on_chelly_document_changed = Signal(object)
    post_on_key_pressed = Signal(object)

    @property
    def visible_blocks(self) -> list:
        return self._visible_blocks

    @property
    def commands(self) -> BasicCommands:
        return self.__commands

    @property
    def followers(self) -> List[Self]:
        try:
            return self.__followers_references  # not initialized
        except AttributeError:
            return []

    @property
    def followed(self) -> bool:
        return bool(self.followers)

    @property
    def shareables(self) -> dict:
        return {"panels": self.panels, "features": self.features}

    @property
    def imitables(self) -> dict:
        return {
            "style": self.style,
            "decorations": self.decorations,
            "language": self.language,
            "properties": self.properties,
        }

    def __init__(self, parent):
        super().__init__(parent)

        self._panels = PanelsManager(self)
        self._features = FeaturesManager(self)
        self._language = LanguagesManager(self)
        self._properties = Properties(self)
        self._chelly_document = ChellyDocument(self)
        self._style = ChellyStyle(self)
        self._decorations = TextDecorationsManager(self)

        self.__commands = BasicCommands(self)

        self._visible_blocks = list()
        self._last_mouse_pos = QPoint(0, 0)
        self.__followers_references = []
        self._shared_reference = None
        self.__build()

    def __build(self):
        self._properties.default()
        self.setLineWrapMode(self.NoWrap)
        self.setCenterOnScroll(True)
        self.setMouseTracking(True)
        self._update_visible_blocks(None)

    def update_state(self):
        self.on_updated.emit()

    def update(self):
        self.update_state()
        return super().update()

    @property
    def chelly_document(self) -> ChellyDocument:
        return self._chelly_document

    @chelly_document.setter
    def chelly_document(self, new_document: ChellyDocument) -> ChellyDocument:
        old_document = self._chelly_document

        if old_document is new_document:
            return None

        if new_document is ChellyDocument:
            self._chelly_document = new_document(self)
        elif isinstance(new_document, ChellyDocument):
            self._chelly_document = new_document
        else:
            raise ChellyDocumentExceptions.ChellyDocumentValueError(
                f"invalid type: {new_document} expected: {ChellyDocument}"
            )
        self.__setup_chelly_document(old_document, self._chelly_document)
        self.on_chelly_document_changed.emit(self._chelly_document)

    @property
    def language(self) -> LanguagesManager:
        return self._language

    @language.setter
    def language(self, new_manager: LanguagesManager) -> LanguagesManager:
        if new_manager is LanguagesManager:
            self._language = new_manager(self)
        elif isinstance(new_manager, LanguagesManager):
            self._language = new_manager
        else:
            raise LexerExceptions.LexerValueError(
                f"invalid type: {new_manager} expected: {LanguagesManager}"
            )

    @property
    def properties(self) -> Properties:
        return self._properties

    @properties.setter
    def properties(self, new_manager: Properties) -> Properties:
        if new_manager is Properties:
            self._properties = new_manager(self)
        elif isinstance(new_manager, Properties):
            self._properties = new_manager
        else:
            raise PropertiesExceptions.PropertyValueError(
                f"invalid type: {new_manager} expected: {Properties}"
            )

    @property
    def panels(self) -> PanelsManager:
        return self._panels

    @panels.setter
    def panels(self, new_manager: PanelsManager) -> PanelsManager:
        if new_manager is PanelsManager:
            self._panels = new_manager(self)
        elif isinstance(new_manager, PanelsManager):
            self._panels = new_manager
        else:
            raise PanelsExceptions.PanelValueError(
                f"invalid type: {new_manager} expected: {PanelsManager}"
            )

    @property
    def features(self) -> FeaturesManager:
        return self._features

    @features.setter
    def features(self, new_manager: FeaturesManager) -> FeaturesManager:
        if new_manager is FeaturesManager:
            self._features = new_manager(self)
        elif isinstance(new_manager, FeaturesManager):
            self._features = new_manager
        else:
            raise FeaturesExceptions.FeatureValueError(
                f"invalid type: {new_manager} expected: {FeaturesManager}"
            )

    @property
    def style(self) -> ChellyStyle:
        return self._style

    @style.setter
    def style(self, new_style: ChellyStyle) -> None:
        if new_style is ChellyStyle:
            self._style = new_style(self)
        elif isinstance(new_style, ChellyStyle):
            self._style.imitate(new_style)

        else:
            raise StyleExceptions.StyleValueError(
                f"invalid type: {new_style} expected: {ChellyStyle}"
            )

    @property
    def decorations(self) -> TextDecorationsManager:
        return self._decorations

    @decorations.setter
    def decorations(self, new_decorations: TextDecorationsManager) -> None:
        if new_decorations is TextDecorationsManager:
            self._decorations = new_decorations()
        elif isinstance(new_decorations, TextDecorationsManager):
            self._decorations = new_decorations
        else:
            raise TextExceptions.TextDecorationValueError(
                f"invalid type: {new_decorations} expected: {TextDecorationsManager}"
            )

    def showEvent(self, event):
        super().showEvent(event)
        self.panels.refresh()

    def paintEvent(self, event) -> None:
        self._update_visible_blocks(event)
        super().paintEvent(event)
        self.on_painted.emit(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.on_resized.emit()

    def _update_visible_blocks(self, *args) -> None:
        """Updates the list of visible blocks"""
        self._visible_blocks[:] = []
        block = self.firstVisibleBlock()
        block_nbr = block.blockNumber()

        top = int(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + int(self.blockBoundingRect(block).height())
        editor_bottom_top = 0
        editor_bottom_bottom = self.height()
        first_block = True

        while block.isValid():
            visible = top >= editor_bottom_top and bottom <= editor_bottom_bottom

            if not visible and not first_block:
                break
            first_block = False

            if visible and block.isVisible():
                self._visible_blocks.append((top, block_nbr, block))

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_nbr = block.blockNumber()

        # pprint.pprint(self._visible_blocks)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> Union[None, object]:
        self.on_key_pressed.emit(event)

        if event.key() == Qt.Key_Tab and event.modifiers() == Qt.NoModifier:
            self.__commands.indent()
            return super().keyPressEvent(event)

        elif event.key() == Qt.Key_Backtab and event.modifiers() == Qt.NoModifier:
            self.__commands.un_indent()
            return super().keyPressEvent(event)

        elif (
            event.key() == Qt.Key_Home
            and int(event.modifiers()) & Qt.ControlModifier == 0
        ):
            self.__commands.home_key(event, int(event.modifiers()) & Qt.ShiftModifier)
            return super().keyPressEvent(event)

        super().keyPressEvent(event)
        self.post_on_key_pressed.emit(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        self.on_key_released.emit(event)
        return super().keyReleaseEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.on_mouse_wheel_activated.emit(event)
        return super().wheelEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.on_mouse_moved.emit(event)
        self._last_mouse_pos = event.pos()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.on_mouse_released.emit(event)
        return super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        self.on_mouse_double_clicked.emit(event)
        return super().mouseDoubleClickEvent(event)

    def setPlainText(self, text: str) -> None:
        self.on_text_setted.emit(text)
        self._update_visible_blocks()
        return super().setPlainText(text)

    def __setup_chelly_document(
        self, old_chelly_document: ChellyDocument, new_chelly_document: ChellyDocument
    ):
        self.setPlainText(new_chelly_document.editor.toPlainText())
        self.__cached_block_count = TextEngine(new_chelly_document.editor).line_count
        old_chelly_document.on_contents_changed.disconnect(self._update_contents)
        new_chelly_document.on_contents_changed.connect(self._update_contents)

    def _update_contents(
        self, editor: QPlainTextEdit, pos: int, charsrem: int, charsadd: int
    ):
        line_number = TextEngine(editor).current_line_nbr
        TextEngine(self).move_cursor_to_line(line_number)
        line_count = TextEngine(editor).line_count

        if self.__cached_block_count == line_count:
            text = TextEngine(editor).text_at_line(line_number)
            TextEngine(self).set_text_at_line(self.textCursor().blockNumber(), text)
            TextEngine(self).move_cursor_to_line(line_number)

        elif self.__cached_block_count == line_count - 1:
            cursor = self.textCursor()
            cursor.setPosition(pos)
            cursor.insertText("\n")
            self.setTextCursor(cursor)

        elif self.__cached_block_count == line_count + 1:
            TextEngine(self).move_cursor_to_line(line_number + 1)
            cursor = self.textCursor()
            cursor.deletePreviousChar()
            self.setTextCursor(cursor)

        else:
            cursor = self.textCursor()
            cursor.setPosition(pos)

            if charsrem:
                for _ in range(charsrem):
                    cursor.deleteChar()

            if charsadd:
                calc = pos + charsadd
                start_block = TextEngine(editor).block_from_position(pos)
                end_block = TextEngine(editor).block_from_position(calc)

                new_blocks = list(
                    TextEngine(editor).iterate_blocks_from(
                        start_block, end_block.blockNumber()
                    )
                )
                for nb in new_blocks:
                    cursor.beginEditBlock()
                    cursor.insertText(nb.text())

                    if nb.next().blockNumber() >= 0 and nb != end_block:
                        cursor.insertText("\n")

                    cursor.endEditBlock()

            self.setTextCursor(cursor)

            TextEngine(self).move_cursor_to_line(TextEngine(editor).current_line_nbr)

        self.__cached_block_count = TextEngine(editor).line_count

    def follow(self, other_editor: Self, follow_back: bool = False):
        other_editor.followers.append(self)
        self.chelly_document = other_editor.chelly_document

        for key, value in other_editor.imitables.items():
            imitable = getattr(self, key, None)
            if hasattr(imitable, "imitate"):
                imitable.imitate(value)

        if follow_back:
            self.followers.append(other_editor)

    def unfollow(self, other_editor: Self, unfollow_back: bool = False):
        if self.following(other_editor):
            other_editor.followers.remove(self)
            ...
        if unfollow_back:
            if other_editor.following(self):
                self.followers.remove(other_editor)

    def following(self, other_editor: Self) -> bool:
        return self in other_editor.followers

    @property
    def shared_reference(self) -> list:
        return self.__shared_reference

    @shared_reference.setter
    def shared_reference(self, other_editor: Self):
        self.__shared_reference = other_editor

        for key, from_manager in other_editor.shareables.items():
            if hasattr(self, key):
                try:
                    to_manager = getattr(self, key)
                    to_manager.shared_reference = from_manager
                except AttributeError as e:
                    print(e)

    @shared_reference.deleter
    def shared_reference(self):
        self.__shared_reference = None


class CodeEditor(__CodeEditorCopy):
    ...


__all__ = ["CodeEditor"]
