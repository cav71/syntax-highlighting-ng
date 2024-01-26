# This tests the conftest fake_anki21 fixture,
# to have tests not depend on an installed anki

def test_plain_import():
    "this test must fail"
    try:
        import anki  # noqa: F401
        raise RuntimeError("the module anki shouldn't be available")
    except ModuleNotFoundError:
        pass

def test_import_anki(fake_anki21):
    "test the module import"
    import anki
    assert anki.point_version() == 231001


def test_import_anki_hooks(fake_anki21):
    "test the module import"
    from anki.hooks import addHook
    assert addHook("setupEditorButtons", lambda: None) == 999

def test_import_aqt(fake_anki21):
    #    from aqt import mw
    import aqt  # noqa: F401

def test_import_mw_from_aqt(fake_anki21):
    from aqt import mw
    assert mw.callme() == 123


