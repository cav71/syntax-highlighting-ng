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


def test_render_simple(fake_anki21, assets):
    text = "a simple one-line"
    rendered = html_render.render_string(text)
    found = BeautifulSoup(rendered).prettify()
    assert found == assets.read_text("simple.html")


def test_render_conftest(fake_anki21, assets):
    src = Path(__file__).parent / "conftest.py"
    rendered = html_render.render_string(src.read_text())
    found = BeautifulSoup(rendered).prettify()
    assert found == assets.read_text("conftest.html", fallback=found)
