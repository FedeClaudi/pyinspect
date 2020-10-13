import pyinspect as pi
import pytest

import numpy
import matplotlib
import pandas
import os
from pathlib import Path


def test_timestamp():
    pi.utils.timestamp()


def test_readsingleline():
    with pytest.raises(FileExistsError):
        pi.utils.read_single_line("no path", 0)

    with pytest.raises(ValueError):
        pi.utils.read_single_line("no path", None)


def test_submodules():
    pi.utils.get_submodules(pi)
    pi.utils.get_submodules(pi.utils)

    # tougher stuff
    pi.utils.get_submodules(numpy)
    pi.utils.get_submodules(matplotlib)
    pi.utils.get_submodules(pandas)

    print("done")


def test_listdir():
    pi.utils.listdir(os.curdir)
    pi.utils.listdir(os.curdir, extension="py", sortby="ext")
    pi.utils.listdir(os.curdir, sortby="size")
    pi.utils.listdir(os.curdir, sortby="extensions")

    with pytest.raises(TypeError):
        pi.utils.listdir(1)

    with pytest.raises(TypeError):
        pi.utils.subdirs(os.curdir)

    pi.utils.subdirs(Path(os.curdir))
