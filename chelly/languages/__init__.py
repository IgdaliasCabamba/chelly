from typing import Any
from .any import PygmentsSH
from .python import PythonLanguage
from .java_script import JavaScriptLanguage

LANGUAGES={
    """Oficial suported languages"""

    "python":{
        "class":PythonLanguage,
        "file_extensions":[".py"]
    },
    "javascript":{
        "class":JavaScriptLanguage,
        "file_extensions":[".js"]
    },
    "_any":{
        "class":PygmentsSH,
        "file_extensions":Any
    }
}