# TODO: consolidate all rendering functions here!
# from pygments import highlight
# from pygments.lexers import get_lexer_by_name, get_all_lexers
#
import pygments
import pygments.lexers


def render_string(txt: str) -> str:
    from pygments.formatters import HtmlFormatter

    lexer = pygments.lexers.get_lexer_by_name("Python", stripall=True)

    formatter = HtmlFormatter(
        linenos=True, noclasses=True, font_size=16, style="default"
    )
    return pygments.highlight(txt, lexer, formatter)
