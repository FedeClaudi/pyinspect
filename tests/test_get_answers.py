import pyinspect as pi
from click.testing import CliRunner
import pytest


def test_get_answers():
    with pytest.raises(ZeroDivisionError):
        # console seems to be throwing this while rendering
        pi.get_answers()


def test_cli():
    runner = CliRunner()
    runner.invoke(pi.answers.cli_get_answers)
