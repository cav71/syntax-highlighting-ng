# NOTE: see comment in syntax_highlighting_ng/__init__.py
import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

if os.getenv("STANDALONE_ADDON") != "1":
    raise pytest.skip(
        f"to run {__name__} must have STANDALONE_ADDON=1 in the environment",
        allow_module_level=True,
    )

from syntax_highlighting_ng import html_render


def test_invalid_language(fake_anki21):
    text = "a simple one-line"
    style = html_render.Style(language="xxx")

    # wrong style
    pytest.raises(html_render.LanguageNotFound, html_render.render_string, text, style)
    try:
        html_render.render_string(text, style)
    except html_render.LanguageNotFound as e:
        assert e.render() == """
<b>Error</b>: Selected language 'xxx' not found.<br>
If you set a custom lang selection please make sure<br>
you typed all list entries correctly.
"""

def test_invalid_style(fake_anki21):
    text = "a simple one-line"
    style = html_render.Style(style="xxx")

    # wrong style
    pytest.raises(html_render.LanguageNotFound, html_render.render_string, text, style)
    try:
        html_render.render_string(text, style)
    except html_render.InvalidStyle as e:
        assert e.render() == """
<b>Error</b>: Selected style 'xxx' not found.<br>
If you set a custom style please make sure<br>
you typed it correctly.
"""

def test_render_simple(fake_anki21, assets):
    text = "a simple one-line"
    rendered = html_render.render_string(text)
    found = BeautifulSoup(rendered).prettify()
    assert found == assets.read_text("simple.html", fallback=found)


def test_render_conftest(fake_anki21, assets):
    src = Path(__file__).parent / "conftest.py"
    rendered = html_render.render_string(src.read_text())
    found = BeautifulSoup(rendered).prettify()
    assert found == assets.read_text("conftest.html", fallback=found)
