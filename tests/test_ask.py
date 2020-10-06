import pytest
from pyinspect import ask


def test_ask():
    with pytest.raises(ZeroDivisionError):  # not sure why
        ask("Python strip string")

    ask("cleaning the kitchen")  # shouldn't return anything

    ask("")

    with pytest.raises(ValueError):
        ask(1)  # should give error
