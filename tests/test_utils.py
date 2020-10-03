import pyinspect as pi
import pytest


def test_timestamp():
    pi.utils.timestamp()


def test_readsingleline():
    with pytest.raises(FileExistsError):
        pi.utils.read_single_line("no path", 0)

    with pytest.raises(ValueError):
        pi.utils.read_single_line("no path", None)


def test_get_submodules():
    pi.utils.get_submodules(pi)
    pi.utils.get_submodules(pi.utils)
