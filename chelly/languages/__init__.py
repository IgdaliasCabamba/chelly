from typing import Any
from .any import PygmentsSH
from .python import PythonLanguage

LANGUAGES={
    """Oficial suported languages"""

    "python":{
        "class":PythonLanguage,
        "file_extensions":[".py"]
    },
    "_any":{
        "class":PygmentsSH,
        "file_extensions":Any
    }
}