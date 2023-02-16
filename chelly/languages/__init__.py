from .python import PythonLanguage
from .java_script import JavaScriptLanguage

LANGUAGES = {
    """Oficial suported languages"""
    "python": {"class": PythonLanguage, "file_extensions": [".py"]},
    "javascript": {"class": JavaScriptLanguage, "file_extensions": [".js"]},
}


__all__ = ["LANGUAGES"]
