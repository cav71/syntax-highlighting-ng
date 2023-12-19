# NOTE: see comment in syntax_highlighting_ng/__init__.py
import os
import pytest

if os.getenv("STANDALONE_ADDON") != "1":
    raise pytest.skip(
        "for this moduleneed to set STANDALONE_ADDON=1 in the environment",
        allow_module_level=True,
    )

from syntax_highlighting_ng import html_render


def test_render_simple(fake_anki21, assets):
    text = "a simple one-line"
    found = html_render.render_string(text)
    assert found == assets.read_text("simple.html")
