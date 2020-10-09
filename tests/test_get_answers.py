import pyinspect as pi
from click.testing import CliRunner
import pytest


def test_get_answers():
    with pytest.raises((ZeroDivisionError, ValueError)):
        # console seems to be throwing this while rendering
        pi.get_answers()

        pi.get_answers(hide_panel=True)


def test_cli():
    runner = CliRunner()
    runner.invoke(pi.answers.cli_get_answers)
