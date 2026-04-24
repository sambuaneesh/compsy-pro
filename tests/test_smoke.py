from compsy import __version__


def test_version_is_set() -> None:
    assert isinstance(__version__, str)
    assert __version__
