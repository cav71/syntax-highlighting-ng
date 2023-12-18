def test_plain_import():
    "this test must fail"
    try:
        import anki
        raise RuntimeError("the module anki shouldn't be available")
    except ModuleNotFoundError:
        pass

def test_import(fake_anki21):
    "test the module import"
    import anki
    assert anki.point_version() == 231001

