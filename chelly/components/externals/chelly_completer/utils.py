import re

_HTML_ESCAPE_TABLE = \
{
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    " ": "&nbsp;",
    "\t": "&nbsp;&nbsp;&nbsp;&nbsp;",
}


def htmlEscape(text):
    """Replace special HTML symbols with escase sequences
    """
    return "".join(_HTML_ESCAPE_TABLE.get(c,c) for c in text)


wordPattern = "\w+"
wordRegExp = re.compile(wordPattern)
wordAtEndRegExp = re.compile(wordPattern + '$')
wordAtStartRegExp = re.compile('^' + wordPattern)

MAX_VISIBLE_WORD_COUNT = 256