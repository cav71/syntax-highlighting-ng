from __future__ import annotations
import sys
import types
from pathlib import Path
import pytest


@pytest.fixture(scope="function")
def assets(request):

    class Asset:
        def __init__(self):
            self.basedir = Path(__file__).parent
            self.candidates = [
                f"assets/{request.node.module.__name__}",
                "assets",
            ]
        def lookup(self, path: Path | str) -> Path | None:
            for candidate in self.candidates:
                if (target := (self.basedir / candidate / path)).exists():
                    return target

        def read_text(self, path: Path | str, fallback: str|None=None) -> str|None:
            dest = self.lookup(path)
            if fallback is not None:
                dest = dest or (self.basedir / self.candidates[0] / path)
                dest.parent.mkdir(exist_ok=True, parents=True)
                dest.write_text(fallback)

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
        def addHook(self):
            return 999

    class Aqt(types.ModuleType):
        pass

    class AqtMV(types.ModuleType):
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
    yield old
    for name, mod in reversed(old.items()):
        if mod:
            sys.modules[name] = mod
        else:
            del sys.modules[name]
