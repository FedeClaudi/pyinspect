import pyinspect as pi
import sys
import pytest
import numpy as np


def raise_exception():
    try:
        1 / 0
    except Exception:
        exc_type, exc_value, traceback = sys.exc_info()
        sys.excepthook(exc_type, exc_value, traceback)


def raise_exception_with_objs():
    a = "a string"
    b = np.zeros(10)
    c = {"a": a, "b": b}
    d = None

    try:
        a + b + c + d
    except Exception:
        exc_type, exc_value, traceback = sys.exc_info()
        sys.excepthook(exc_type, exc_value, traceback)


def test_install():
    pi.install_traceback()
    raise_exception()
    raise_exception_with_objs()


def test_traceback_args():
    pi.install_traceback(hide_locals=True)
    raise_exception()

    pi.install_traceback(hide_locals=False)
    raise_exception()

    pi.install_traceback(all_locals=True)
    raise_exception()

    pi.install_traceback(all_locals=False)
    raise_exception()

    pi.install_traceback(relevant_only=True)
    raise_exception()

    pi.install_traceback(relevant_only=False)
    raise_exception()

    pi.install_traceback(keep_frames=0)
    raise_exception()

    pi.install_traceback(keep_frames=-1)
    raise_exception()

    pi.install_traceback(keep_frames=5)
    raise_exception()


def test_print_exception():
    with pytest.raises(ZeroDivisionError):
        # try:
        1 / 0
        # except Exception:
        pi.print_exception()
        pi.print_exception(message="Test")

        exc_type, exc_value, traceback = sys.exc_info()
        sys.excepthook(exc_type, exc_value, traceback)
        pi.print_exception(traceback=traceback)


def test_get_locals():
    pi._exceptions.get_locals()
