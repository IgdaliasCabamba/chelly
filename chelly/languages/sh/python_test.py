import builtins
from pprint import pprint
import re
from ...core import Language
from ...core import TextBlockHelper
import yaml
import pathlib

with open(
    pathlib.Path.cwd().joinpath(
        "chelly", "languages", "grammars", "python.syntax.yaml"
    ),
    "r",
) as fp:
    pytohn_syntax = yaml.safe_load(fp)


def any(name, alternates):
    """Return a named group pattern matching list of alternates."""
    return f"(?P<{name}>" + "|".join(alternates) + ")"


kwlist = pytohn_syntax["static"]["keywords_list"]
kw_namespace_list = pytohn_syntax["static"]["keywords_namespace_list"]
wordop_list = pytohn_syntax["static"]["wordop_list"]


def make_python_patterns(additional_keywords=None, additional_builtins=None):
    """Strongly inspired from idlelib.ColorDelegator.make_pat"""

    if additional_keywords is None:
        additional_keywords = []

    if additional_builtins is None:
        additional_builtins = []

    kw = r"\b" + any("keyword", kwlist + additional_keywords) + r"\b"
    kw_namespace = r"\b" + any("namespace", kw_namespace_list) + r"\b"
    word_operators = r"\b" + any("operator_word", wordop_list) + r"\b"
    builtinlist = [
        str(name) for name in dir(builtins) if not name.startswith("_")
    ] + additional_builtins
    for v in ["None", "True", "False"]:
        builtinlist.remove(v)
    builtin = r"([^.'\"\\#]\b|^)" + any("builtin", builtinlist) + r"\b"
    builtin_functions = any("builtin_functions", [r"_{2}[a-zA-Z_]*_{2}"])
    comment = any("comment", [r"#[^\n]*"])
    instance = any("instance", [r"\bself\b", r"\bcls\b"])
    decorator = any("decorator", [r"@\w*", r".setter"])
    number = any(
        "number",
        [
            r"\b[+-]?[0-9]+[lLjJ]?\b",
            r"\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b",
            r"\b[+-]?0[oO][0-7]+[lL]?\b",
            r"\b[+-]?0[bB][01]+[lL]?\b",
            r"\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?[jJ]?\b",
        ],
    )
    sqstring = r"(\b[rRuU])?'[^'\\\n]*(\\.[^'\\\n]*)*'?"
    dqstring = r'(\b[rRuU])?"[^"\\\n]*(\\.[^"\\\n]*)*"?'
    uf_sqstring = r"(\b[rRuU])?'[^'\\\n]*(\\.[^'\\\n]*)*(\\)$(?!')$"
    uf_dqstring = r'(\b[rRuU])?"[^"\\\n]*(\\.[^"\\\n]*)*(\\)$(?!")$'
    sq3string = r"(\b[rRuU])?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
    dq3string = r'(\b[rRuU])?"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
    uf_sq3string = r"(\b[rRuU])?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(\\)?(?!''')$"
    uf_dq3string = r'(\b[rRuU])?"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(\\)?(?!""")$'
    string = any("string", [sq3string, dq3string, sqstring, dqstring])
    ufstring1 = any("uf_sqstring", [uf_sqstring])
    ufstring2 = any("uf_dqstring", [uf_dqstring])
    ufstring3 = any("uf_sq3string", [uf_sq3string])
    ufstring4 = any("uf_dq3string", [uf_dq3string])
    return "|".join(
        [
            instance,
            decorator,
            kw,
            kw_namespace,
            builtin,
            word_operators,
            builtin_functions,
            comment,
            ufstring1,
            ufstring2,
            ufstring3,
            ufstring4,
            string,
            number,
            any("SYNC", [r"\n"]),
        ]
    )


class PythonLanguageNew(Language):
    """
    Highlights python syntax in the editor.
    """

    # Syntax highlighting rules:
    PROG = re.compile(make_python_patterns(), re.S)
    IDPROG = re.compile(r"\s+(\w+)", re.S)
    ASPROG = re.compile(r".*?\b(as)\b")
    # Syntax highlighting states (from one text block to another):
    (
        NORMAL,
        INSIDE_SQ3STRING,
        INSIDE_DQ3STRING,
        INSIDE_SQSTRING,
        INSIDE_DQSTRING,
    ) = list(range(5))

    # Comments suitable for Outline Explorer
    OECOMMENT = re.compile(pytohn_syntax["rules"]["outline_explorer_comments"])

    def __init__(self, editor, color_scheme=None):
        super().__init__(editor, color_scheme)
        self.import_statements = []
        self.global_import_statements = []
        self.docstrings = []

    def highlight_block(self, text, block):
        prev_block = block.previous()
        prev_state = TextBlockHelper.get_state(prev_block)
        if prev_state == self.INSIDE_DQ3STRING:
            offset = -4
            text = r'""" ' + text
        elif prev_state == self.INSIDE_SQ3STRING:
            offset = -4
            text = r"''' " + text
        elif prev_state == self.INSIDE_DQSTRING:
            offset = -2
            text = r'" ' + text
        elif prev_state == self.INSIDE_SQSTRING:
            offset = -2
            text = r"' " + text
        else:
            offset = 0

        import_stmt = None
        # set docstring dynamic attribute, used by the fold detector.
        block.docstring = False

        self.setFormat(0, len(text), self.formats["normal"])

        state = self.NORMAL
        match = self.PROG.search(text)
        while match:
            for key, value in list(match.groupdict().items()):
                if value:
                    start, end = match.span(key)
                    start = max([0, start + offset])
                    end = max([0, end + offset])
                    if key == "uf_sq3string":
                        self.setFormat(start, end - start, self.formats["docstring"])
                        block.docstring = True
                        state = self.INSIDE_SQ3STRING
                    elif key == "uf_dq3string":
                        self.setFormat(start, end - start, self.formats["docstring"])
                        block.docstring = True
                        state = self.INSIDE_DQ3STRING
                    elif key == "uf_sqstring":
                        self.setFormat(start, end - start, self.formats["string"])
                        state = self.INSIDE_SQSTRING
                    elif key == "uf_dqstring":
                        self.setFormat(start, end - start, self.formats["string"])
                        state = self.INSIDE_DQSTRING
                    elif key == "builtin_functions":
                        # trick to highlight __init__, __add__ and so on with
                        # builtin color
                        self.setFormat(start, end - start, self.formats["constant"])
                    else:
                        if ('"""' in value or "'''" in value) and key != "comment":
                            # highlight docstring with a different color
                            block.docstring = True
                            self.setFormat(
                                start, end - start, self.formats["docstring"]
                            )
                        elif key == "decorator":
                            # highlight decorators
                            self.setFormat(
                                start, end - start, self.formats["decorator"]
                            )
                        elif value in ["self", "cls"]:
                            # highlight self attribute
                            self.setFormat(start, end - start, self.formats["self"])
                        else:
                            # highlight all other tokens
                            self.setFormat(start, end - start, self.formats[key])
                        if key == "keyword":
                            if value in ("def", "class"):
                                match1 = self.IDPROG.match(text, end)
                                if match1:
                                    start1, end1 = match1.span(1)
                                    fmt_key = (
                                        "definition" if value == "class" else "function"
                                    )
                                    fmt = self.formats[fmt_key]
                                    self.setFormat(start1, end1 - start1, fmt)
                        if key == "namespace":
                            import_stmt = text.strip()
                            # color all the "as" words on same line, except
                            # if in a comment; cheap approximation to the
                            # truth
                            if "#" in text:
                                endpos = text.index("#")
                            else:
                                endpos = len(text)
                            while True:
                                match1 = self.ASPROG.match(text, end, endpos)
                                if not match1:
                                    break
                                start, end = match1.span(1)
                                self.setFormat(
                                    start, end - start, self.formats["namespace"]
                                )
            # next match
            match = self.PROG.search(text, match.end())
        TextBlockHelper.set_state(block, state)

        # update import zone
        if import_stmt is not None:
            block.import_stmt = import_stmt
            self.import_statements.append(block)
            block.import_stmt = True
        elif block.docstring:
            self.docstrings.append(block)

    def rehighlight(self):
        self.import_statements[:] = []
        self.global_import_statements[:] = []
        self.docstrings[:] = []
        super().rehighlight()


__all__ = [
    "PythonLanguageNew",
    "any",
    "kw_namespace_list",
    "kwlist",
    "make_python_patterns",
    "pytohn_syntax",
    "wordop_list",
]
