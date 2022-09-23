import re
from ..core import Language
from ..core import TextBlockHelper

class JavaScriptSH(Language):
    def __init__(self, editor, color_scheme=None):
        super().__init__(editor, color_scheme)
        
class JavaScriptLanguage(JavaScriptSH):
    ...