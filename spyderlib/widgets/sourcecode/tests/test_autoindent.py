# -*- coding: utf-8 -*-
#
# Copyright © 2009- The Spyder Development Team
# Licensed under the terms of the MIT License
#

"""
Tests for the autoindent features
"""

# Third party imports
from qtpy.QtGui import QTextCursor
import pytest

# Local imports
from spyderlib.utils.qthelpers import qapplication
from spyderlib.py3compat import to_text_string
from spyderlib.widgets.sourcecode.codeeditor import CodeEditor


# --- Fixtures
# -----------------------------------------------------------------------------
def get_indent_fix(text):
    app = qapplication()
    editor = CodeEditor(parent=None)
    editor.setup_editor(language='Python')

    editor.set_text(text)
    cursor = editor.textCursor()
    cursor.movePosition(QTextCursor.End)
    editor.setTextCursor(cursor)
    editor.fix_indent()
    return to_text_string(editor.toPlainText())


# --- Tests
# -----------------------------------------------------------------------------
def test_simple_tuple():
    text = get_indent_fix("this_tuple = (1, 2)\n")
    assert text == "this_tuple = (1, 2)\n"


def test_def_with_newline():
    text = get_indent_fix("\ndef function():\n")
    assert text == "\ndef function():\n    ", repr(text)


def test_def_with_indented_comment():
    text = get_indent_fix("def function():\n    # Comment\n")
    assert text == "def function():\n    # Comment\n    ", repr(text)


# --- Failing tests
# -----------------------------------------------------------------------------
@pytest.mark.xfail
def test_simple_def():
    text = get_indent_fix("def function():\n")
    assert text == "def function():\n    ", repr(text)


@pytest.mark.xfail
def test_def_with_unindented_comment():
    text = get_indent_fix("def function():\n# Comment\n")
    assert text == "def function():\n# Comment\n    ", repr(text)


@pytest.mark.xfail
def test_open_parenthesis():
    text = get_indent_fix("open_parenthesis(\n")
    assert text == "open_parenthesis(\n    ", repr(text)


@pytest.mark.xfail
def test_brackets_alone():
    text = get_indent_fix("def function():\n    print []\n")
    assert text == "def function():\n    print []\n    ", repr(text)


if __name__ == "__main__":
    pytest.main()
