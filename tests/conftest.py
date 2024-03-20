from __future__ import annotations
import sys
import types
from pathlib import Path
import pytest
from typing import Any, Callable


@pytest.fixture(scope="function")
def assets(request):

    class Asset:
        def __init__(self):
            self.basedir = Path(__file__).parent
            self._candidates = [
                f"assets/{request.node.module.__name__}",
                "assets",
            ]

        @property
        def candidates(self) -> list[Path]:
            result = []
            for candidate in self._candidates:
                result.append(self.basedir / candidate)
            return result

        def search(self, path: Path | str) -> list[Path]:
            result = []
            for candidate in self.candidates:
                if (target := (candidate / path)).exists():
                    result.append(target)
            return result

        def lookup(self, path: Path | str, single: bool = True) -> Path|None:
            found = self.search(path)
            if single and len(found) != 1:
                raise RuntimeError(f"looking up 1 element, found {len(found)}", found)
            return found[0] if found else None

        def read_text(self, path: Path | str, fallback: str|None=None) -> str|None:
            if fallback and not (self.candidates[0] / path).exists():
                dest = self.candidates[0] / path
                dest.parent.mkdir(exist_ok=True, parents=True)
                dest.write_text(fallback)

            dest = self.lookup(path)
            return dest.read_text()


    return Asset()


@pytest.fixture(scope="function")
def fake_anki21(monkeypatch):
    # monkey patch a fake anki21 module

    class Anki(types.ModuleType):
        version = "23.10.1"

        def pointVersion(self):
            return self.point_version()
        def point_version(self):
            return 231001


    class AnkiHooks(types.ModuleType):
        def addHook(self, hook: str, func: Callable) -> None:
            return 999

    class Aqt(types.ModuleType):
        pass

    # form anki.qt.aqt.addons.AddonManager
    class AddonManager:
        def getConfig(self, module: str) -> dict[str, Any] | None:
            return {}

    class AqtMV(types.ModuleType):
        @property
        def addonManager(self):
            self._addon_manager = getattr(self, "_addon_manager", AddonManager())
            return self._addon_manager

        def callme(self):
            return 123

    replacements = [
        ("anki", Anki),
        ("anki.hooks", AnkiHooks),
        ("aqt", Aqt),
        ("aqt.mw", AqtMV),
    ]
    old = {}
    for name, cls in replacements:
        old[name] = sys.modules.get(name)
        sys.modules[name] = cls(name)

    monkeypatch.setenv("STANDALONE_ADDON", "1")
    yield old
    for name, mod in reversed(old.items()):
        if mod:
            sys.modules[name] = mod
        else:
            del sys.modules[name]


@pytest.fixture(scope="function")
def htmlcompare(request):
    from bs4 import BeautifulSoup

    dumpdir = Path(__file__).parent / "build" / "failures"

    destdir = dumpdir / request.node.module.__name__ / request.node.name
    destdir.mkdir(parents=True, exist_ok=True)


    def diff(expected, found):
        nonlocal destdir
        if expected == found:
            return True

        left = BeautifulSoup(expected, "html.parser").prettify(formatter=lambda s: s.strip())
        right = BeautifulSoup(found, "html.parser").prettify(formatter=lambda s: s.strip())

        if left == right:
            return True

        (destdir / "expected.txt").write_text(expected)
        (destdir / "found.txt").write_text(found)

        left = BeautifulSoup(expected, "html.parser").prettify()
        right = BeautifulSoup(found, "html.parser").prettify()
        (destdir / "diff.html").write_text(f"""
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

    return diff
