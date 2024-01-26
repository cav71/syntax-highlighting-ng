def test_import(fake_anki21):
    "test the module import"
    from syntax_highlighting_ng import consts
    assert consts.sys_encoding
    assert consts.addon_path
