import pyinspect as pi
import numpy as np
import pytest


def test_info_printout():
    pi.whats_pi()


class Test:
    a = 1  # a couple variables
    _private = "this is private !!"

    def hi(
        self,
    ):  # define a function
        """
        Say HI!
        """
        print("Hello world")


def functest():
    return


def test_what_variable():
    # Test with builtins
    a = 1
    pi.what(a)

    a = "test"
    pi.what(a)

    a = {"a": "test"}
    pi.what(a)

    with pytest.raises(FutureWarning):
        a = np.zeros(3)
        pi.what(a)

        a = ["a", {}, np.ones(3)]
        pi.what(a)

    a = ["a", {}]
    pi.what(a)

    a = ("a", {})
    pi.what(a)

    # Test with modules
    pi.what(pi)
    pi.what(pi.find)

    # Test with classes
    pi.what(Test)
    pi.what(Test.hi)
    pi.what(Test().hi)
    pi.what(Test.a)
    pi.what(Test().a)

    # Test with functions
    pi.what(functest)
    pi.what(pi.what)


def test_what_locals():
    pi.what()

    a = 1
    pi.what()
