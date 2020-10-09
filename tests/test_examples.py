import sys

sys.path.append("./")

import examples as ex
import pytest
import pyinspect as pi


def test_examples():
    pi.search(ex)  # runs all of them
