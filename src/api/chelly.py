from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPlainTextEdit
from ..managers import FeaturesManager, LanguagesManager, PanelsManager
from ..core import Properties, LexerExceptions, PropertiesExceptions, PanelsExceptions, FeaturesExceptions


class ChellyEditor(QPlainTextEdit):

    on_resized = Signal()
    on_painted = Signal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self._panels = PanelsManager(self)
        self._features = FeaturesManager(self)
        self._lexer = LanguagesManager(self)
        self._properties = Properties(self)

        self._visible_blocks = list()

    @property
    def lexer(self) -> LanguagesManager:
        return self._lexer

    @lexer.setter
    def lexer(self, new_manager: LanguagesManager) -> LanguagesManager:
        if new_manager is LanguagesManager:
            self._lexer = new_manager()
        elif isinstance(new_manager, LanguagesManager):
            self._lexer = new_manager
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
