from PySide6.QtCore import Signal
from PySide6 import QtGui
from PySide6.QtWidgets import QPlainTextEdit

from ..core import (ChellyDocument, ChellyDocumentExceptions,
                    FeaturesExceptions, LexerExceptions, PanelsExceptions,
                    Properties, PropertiesExceptions)
from ..managers import FeaturesManager, LanguagesManager, PanelsManager


class ChellyEditor(QPlainTextEdit):

    on_resized = Signal()
    on_painted = Signal(object)
    on_updated = Signal()
    on_key_pressed = Signal(object)
    on_key_released = Signal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self._panels = PanelsManager(self)
        self._features = FeaturesManager(self)
        self._language = LanguagesManager(self)
        self._properties = Properties(self)
        self._chelly_document = ChellyDocument(self)

        self._visible_blocks = list()
        self._properties.default()
        self.setLineWrapMode(self.NoWrap)
    
    def update_state(self):
        self.on_updated.emit()
    
    @property
    def chelly_document(self) -> ChellyDocument:
        return self._chelly_document

    @chelly_document.setter
    def chelly_document(self, new_document: ChellyDocument) -> ChellyDocument:
        if new_document is ChellyDocument:
            self._chelly_document = new_document()
        elif isinstance(new_document, ChellyDocument):
            self._chelly_document = new_document
        else:
            raise ChellyDocumentExceptions.ChellyDocumentValueError(
                f"invalid type: {new_document} expected: {ChellyDocument}")
        self._chelly_document.add_editor(self)

    @property
    def language(self) -> LanguagesManager:
        return self._language

    @language.setter
    def language(self, new_manager: LanguagesManager) -> LanguagesManager:
        if new_manager is LanguagesManager:
            self._language = new_manager()
        elif isinstance(new_manager, LanguagesManager):
            self._language = new_manager
        else:
            raise LexerExceptions.LexerValueError(
                f"invalid type: {new_manager} expected: {LanguagesManager}")

    @property
    def properties(self) -> Properties:
        return self._properties

    @properties.setter
    def properties(self, new_manager: Properties) -> Properties:
        if new_manager is Properties:
            self._properties = new_manager()
        elif isinstance(new_manager, Properties):
            self._properties = new_manager
        else:
            raise PropertiesExceptions.PropertyValueError(
                f"invalid type: {new_manager} expected: {Properties}")

    @property
    def panels(self) -> PanelsManager:
        return self._panels

    @panels.setter
    def panels(self, new_manager: PanelsManager) -> PanelsManager:
        if new_manager is PanelsManager:
            self._panels = new_manager()
        elif isinstance(new_manager, PanelsManager):
            self._panels = new_manager
        else:
            raise PanelsExceptions.PanelValueError(
                f"invalid type: {new_manager} expected: {PanelsManager}")

    @property
    def features(self) -> FeaturesManager:
        return self._features

    @features.setter
    def features(self, new_manager: FeaturesManager) -> FeaturesManager:
        if new_manager is FeaturesManager:
            self._features = new_manager()
        elif isinstance(new_manager, FeaturesManager):
            self._features = new_manager
        else:
            raise FeaturesExceptions.FeatureValueError(
                f"invalid type: {new_manager} expected: {FeaturesManager}")

    @property
    def visible_blocks(self) -> list:
        return self._visible_blocks

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
        """ Updates the list of visible blocks """
        self._visible_blocks[:] = []
        block = self.firstVisibleBlock()
        block_nbr = block.blockNumber()

        top = int(self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top()
        )
        bottom = top + int(self.blockBoundingRect(block).height())
        ebottom_top = 0
        ebottom_bottom = self.height()
        first_block = True

        while block.isValid():
            visible = (top >= ebottom_top and bottom <= ebottom_bottom)

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
    
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        self.on_key_pressed.emit(e)
        return super().keyPressEvent(e)
    
    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        self.on_key_released.emit(e)
        return super().keyReleaseEvent(e)
