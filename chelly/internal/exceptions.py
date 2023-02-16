class LexerExceptions:
    class LexerValueError(Exception):
        pass


class PropertiesExceptions:
    class PropertyValueError(Exception):
        pass


class PanelsExceptions:
    class PanelValueError(Exception):
        pass


class FeaturesExceptions:
    class FeatureValueError(Exception):
        pass


class ChellyDocumentExceptions:
    class ChellyDocumentValueError(Exception):
        pass


class StyleExceptions:
    class StyleValueError(Exception):
        pass


class TextExceptions:
    class TextDecorationValueError(Exception):
        pass


__all__ = [
    "ChellyDocumentExceptions",
    "FeaturesExceptions",
    "LexerExceptions",
    "PanelsExceptions",
    "PropertiesExceptions",
    "StyleExceptions",
    "TextExceptions",
]
