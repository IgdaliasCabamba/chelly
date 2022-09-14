from pygments.formatters.html import HtmlFormatter
from pygments.lexer import Error, RegexLexer, Text, _TokenType
from pygments.lexers import get_lexer_for_filename, get_lexer_for_mimetype
from pygments.lexers.agile import PythonLexer
from pygments.lexers.compiled import CLexer, CppLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.lexers.special import TextLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.styles import get_style_by_name, get_all_styles
from pygments.token import Whitespace, Comment, Token
from pygments.util import ClassNotFound

from pygments.lexer import Error, RegexLexer, Text, _TokenType

def get_tokens_unprocessed(self, text, stack=('root',)):
    """ Split ``text`` into (tokentype, text) pairs.
        Monkeypatched to store the final stack on the object itself.
    """
    pos = 0
    tokendefs = self._tokens
    if hasattr(self, '_saved_state_stack'):
        statestack = list(self._saved_state_stack)
    else:
        statestack = list(stack)
    statetokens = tokendefs[statestack[-1]]
    while 1:
        for rexmatch, action, new_state in statetokens:
            m = rexmatch(text, pos)
            if m:
                if action is not None:
                    if type(action) is _TokenType:
                        yield pos, action, m.group()
                    else:
                        for item in action(self, m):
                            yield item
                pos = m.end()
                if new_state is not None:
                    # state transition
                    if isinstance(new_state, tuple):
                        for state in new_state:
                            if state == '#pop':
                                statestack.pop()
                            elif state == '#push':
                                statestack.append(statestack[-1])
                            else:
                                statestack.append(state)
                    elif isinstance(new_state, int):
                        # pop
                        del statestack[new_state:]
                    elif new_state == '#push':
                        statestack.append(statestack[-1])
                    else:
                        assert False, "wrong state def: %r" % new_state
                    statetokens = tokendefs[statestack[-1]]
                break
        else:
            try:
                if text[pos] == '\n':
                    # at EOL, reset state to "root"
                    pos += 1
                    statestack = ['root']
                    statetokens = tokendefs['root']
                    yield pos, Text, '\n'
                    continue
                yield pos, Error, text[pos]
                pos += 1
            except IndexError:
                break
    self._saved_state_stack = list(statestack)

# Monkeypatch!
RegexLexer.get_tokens_unprocessed = get_tokens_unprocessed

# Even with the above monkey patch to store state, multiline comments do not
# work since they are stateless (Pygments uses a single multiline regex for
# these comments, but Qt lexes by line). So we need to append a state for
# comments # to the C and C++ lexers. This means that nested multiline
# comments will appear to be valid C/C++, but this is better than the
# alternative for now.
def replace_pattern(tokens, new_pattern):
    """ Given a RegexLexer token dictionary 'tokens', replace all patterns that
        match the token specified in 'new_pattern' with 'new_pattern'.
    """
    for state in tokens.values():
        for index, pattern in enumerate(state):
            if isinstance(pattern, tuple) and pattern[1] == new_pattern[1]:
                state[index] = new_pattern

# More monkeypatching!
COMMENT_START = (r'/\*', Comment.Multiline, 'comment')
COMMENT_STATE = [(r'[^*/]', Comment.Multiline),
                 (r'/\*', Comment.Multiline, '#push'),
                 (r'\*/', Comment.Multiline, '#pop'),
                 (r'[*/]', Comment.Multiline)]
replace_pattern(CLexer.tokens, COMMENT_START)
replace_pattern(CppLexer.tokens, COMMENT_START)
replace_pattern(JavascriptLexer.tokens, COMMENT_START)
CLexer.tokens['comment'] = COMMENT_STATE
CppLexer.tokens['comment'] = COMMENT_STATE
CSharpLexer.tokens['comment'] = COMMENT_STATE
JavascriptLexer.tokens['comment'] = COMMENT_STATE