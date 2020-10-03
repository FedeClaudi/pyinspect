from pyinspect.exceptions import install_traceback, print_exception
from pyinspect.utils import showme
from pyinspect.find import search

from rich import inspect as rinspect


def inspect_obj(obj, **kwargs):
    return rinspect(obj, methods=True, **kwargs)
