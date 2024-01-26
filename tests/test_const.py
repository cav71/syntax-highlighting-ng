

def test_import(fake_anki21):
    "test the module import"
    import syntax_highlighting_ng
    from syntax_highlighting_ng import consts
    assert consts.sys_encoding
    assert consts.addon_path
    assert syntax_highlighting_ng.STANDALONE
