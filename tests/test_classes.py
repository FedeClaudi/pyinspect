import pyinspect as pi
import pytest


class Test(pi.Enhanced):
    a = 1  # a couple variables
    _private = "this is private !!"

    def hi(
        self,
    ):  # define a function
        """
        Say HI!
        """
        print("Hello world")


def test_enhanced_repr():
    print(Test())

    str(Test())

    print(Test().__repr__())
    print(Test().__str__())


def test_getattr():
    with pytest.raises(AttributeError):
        Test().no_exist
