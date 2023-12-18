from __future__ import annotations
import sys
import types

import pytest


@pytest.fixture(scope="function")
def fake_anki21(monkeypatch):
    # monkey patch a fake anki21 module

    class Anki(types.ModuleType):
        version = "23.10.1"

        def pointVersion(self):
            return self.point_version()
        def point_version(self):
            return 231001

    name = "anki"
    old = sys.modules.get(name)
    sys.modules[name] = Anki(name)
    yield old
    if old:
        sys.modules[name] = old
    else:
        del sys.modules[name]
    
