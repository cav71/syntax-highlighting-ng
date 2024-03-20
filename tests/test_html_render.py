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

DUMPDIR = Path(__file__).parent / "build" / "failures"


def hcompare(assets, name, found):
    from pathlib import Path
    DUMPDIR.mkdir(parents=True, exist_ok=True)
    expected = assets.read_text(name, fallback=found)
    def strip(txt):
        txt = txt.strip()
        if txt.startswith("<html>") and txt.endswith("</html>"):
            return txt[len("<html>"):-len("</html>")]
        return txt

    if found != expected:
        left = strip(expected)
        right = strip(found)
        (DUMPDIR / name).write_text(f"""
<html>
 <head>
  <style>
   table {{ width: 100%; height: 100%; }}
   td {{ vertical-align: top; width: 50% ; border: solid black 3px; }}
  </style>
 </head>
 <body>
  <table>
    <tr><td>{left}</td><td>{right}</td></tr>
  </table>
 </body>
</html>
""")
    return found == expected


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

def test_render_simple(fake_anki21, assets, htmlcompare):
    text = "a simple one-line"
    found = html_render.render_string(text)
    expected = assets.read_text("simple.html", fallback=found)
    assert htmlcompare(expected, found)


def test_render_conftest(fake_anki21, assets, htmlcompare):
    src = assets.lookup("conftest.py")
    found = html_render.render_string(src.read_text())
    expected = assets.read_text("conftest.html", fallback=found)
    assert htmlcompare(expected, found)


def test_issue_9(fake_anki21, assets, htmlcompare):
    # use this: https://pygments.org/demo
    style = html_render.Style(
        language="javascript",
        style="github-dark",
        linenos=False,
        centered=True
    )
    found = html_render.render_string("""
val testing = "a test"
val another_string = "yaaayyy"
""", style)

    expected = assets.read_text("issue_9.html", fallback=found)
    assert htmlcompare(expected, found)
