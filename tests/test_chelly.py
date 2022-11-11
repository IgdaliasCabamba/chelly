import sys
sys.dont_write_bytecode = True

import os
 
# Setup path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from latest import *

def test_lexer_set(benchmark):
    new_lexer = benchmark(LanguagesManager, editor)
    editor.lexer = new_lexer
    assert editor.lexer == new_lexer

def test_singleton_panel(benchmark):
    minimap = benchmark(editor.panels.get, MiniMap)
    assert minimap == editor.panels.append(MiniMap, Panel.Position.RIGHT)


def test_feature_set(benchmark):
    new_features = benchmark(FeaturesManager, editor)
    editor.features = new_features
    assert editor.features == new_features


def test_load_file(benchmark):
    with open(__file__, "r") as infile:
        content = benchmark(infile.read)

    editor.properties.text = content
    assert editor.properties.text == content