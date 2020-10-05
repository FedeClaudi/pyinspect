import pyinspect as pi
from click.testing import CliRunner


def test_get_answers():
    pi.get_answers()


def test_cli():
    runner = CliRunner()
    runner.invoke(pi.answers.cli_get_answers)
