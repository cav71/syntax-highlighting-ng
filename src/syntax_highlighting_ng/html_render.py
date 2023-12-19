# TODO: consolidate all rendering functions here!
# from pygments import highlight
# from pygments.lexers import get_lexer_by_name, get_all_lexers
#
from __future__ import annotations
import dataclasses as dc
import pygments
import pygments.lexers


@dc.dataclass
class Style:
    linenos: str = "inline"
    noclasses: bool = True
    style: str = "default"
    language: str = "Python"


class RenderError(Exception):
    def render(self) -> str:
        raise NotImplementedError("adds .render method")


class LanguageNotFound(RenderError):
    def render(self) -> str:
        return f"""
<b>Error</b>: Selected language '{self.args[0]}' not found.<br>
If you set a custom lang selection please make sure<br>
you typed all list entries correctly.
"""


class InvalidStyle(LanguageNotFound):
    def render(self) -> str:
        return f"""
<b>Error</b>: Selected style '{self.args[0]}' not found.<br>
If you set a custom style please make sure<br>
you typed it correctly.
"""


def render_string(txt: str, style: Style = Style()) -> str:
    from pygments.formatters import HtmlFormatter
    from pygments import util

    try:
        lexer = pygments.lexers.get_lexer_by_name(style.language, stripall=True)
    except util.ClassNotFound as exc:
        raise LanguageNotFound(style.language) from exc

    try:
        formatter = HtmlFormatter(
            linenos=style.linenos, noclasses=style.noclasses, style=style.style
        )
    except util.ClassNotFound as exc:
        raise InvalidStyle(style.style) from exc

    return pygments.highlight(txt, lexer, formatter)
