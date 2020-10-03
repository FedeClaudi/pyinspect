import pyinspect as pi
from rich.console import Console


def test_search_module():
    pi.search(pi, "search")


def test_search_module_noname():
    pi.search(pi)


def test_search_module_args():
    pi.search(pi, "search", print_table=False)
    pi.search(pi, "search", print_table=True)

    pi.search(pi, "search", include_class=False)
    pi.search(pi, "search", include_class=True)


def test_search_class():
    pi.search(Console, "export")


def test_search_class_noname():
    pi.search(Console)


def test_search_class_args():
    pi.search(Console, "search", print_table=False)
    pi.search(Console, "search", print_table=True)

    pi.search(Console, "search", include_parents=False)
    pi.search(Console, "search", include_parents=True)
