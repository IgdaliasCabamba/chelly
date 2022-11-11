import sys
sys.dont_write_bytecode = True

import os
 
# Setup path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from latest import *

def test_share_references(benchmark):
    ...
    #editor1.shared_reference = editor


def test_follow_style(benchmark):
    if not editor1.following(editor):
        editor1.follow(editor, follow_back=True)
    
    editor.style.selection_foreground = QColor("purple")
    editor1.style.selection_background = QColor(Qt.GlobalColor.green)
        
    assert editor.style.selection_background == editor1.style.selection_background
    assert editor.style.selection_foreground == editor1.style.selection_foreground