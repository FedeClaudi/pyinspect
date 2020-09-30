import re
import inspect
from rich import print
from rich.table import Table

from pyinspect.utils import clean_doc


def find_class_method(class_obj, name="", print_table=True):
    """
        Given a python class, it finds allclass methods whose name includes
        the given search string (name)

        :param class_obj: a python Class. Should not be a class instance, but a point to the class object
        :param name: str, optional. Returns only methods which have this string in the name. If not is given returns all methods
        :param print_table: bool, optional. If True it prints a table with all the found methods

        :returns: dict with all the methods found
    """
    if not inspect.isclass(class_obj):
        raise ValueError(
            "find_class_method expects a python Class object as argument"
        )

    found = {k: v for k, v in class_obj.__dict__.items() if name in k}
    if not found:
        print(
            f"[magenta]No methods found in class {class_obj} with query: {name}"
        )
        return None

    if print_table:
        table = Table(show_header=True, header_style="bold magenta",)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("name", style="bold green")
        table.add_column("Line #", width=6, justify="center")
        table.add_column("Source", style="dim")

        for n, (k, v) in enumerate(found.items()):
            if not inspect.isfunction(v):
                continue  # skip docstrings etc
            doc = clean_doc(inspect.getsource(getattr(class_obj, k)), maxn=200)
            lineno = inspect.getsourcelines(getattr(class_obj, k))[1]

            table.add_row(str(n), k, str(lineno), doc)
        print(table)

    return found


def find_module_function(module, name="", print_table=True):
    """
        Given a module (e.g. matplotlib.pyplot) finds all the functions
        in it whose name includes the given search string.

        :param module: python module (e.g. numpy)
        :param name: str, optional. Search string, if none is passed it returns all functions
        :param print_table: bool, optional.  If True it prints a table with all the found functions

        :returns: dict with all the functions found 
    """
    # grab all function names that contain `name` from the module
    p = ".*{}.*".format(name)
    filtered = list(
        filter(lambda x: re.search(p, x, re.IGNORECASE), dir(module))
    )

    if not filtered:
        print(
            f"[magenta]No functions found in module {module} with query: {name}"
        )
        return None

    # Print a table with the results
    if print_table:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("name", style="bold green")
        table.add_column("Docstring", width=52)
        table.add_column("Module", style="dim")

        for n, f in enumerate(filtered):
            attr = getattr(module, f)
            mod = str(inspect.getmodule(attr))
            doc = clean_doc(inspect.getdoc(attr))

            table.add_row(str(n), f, doc, mod)

        print(table)

    # return pointers to the functions
    return {f: getattr(module, f) for f in filtered}


def find(obj, name="", print_table=True):
    """
        General find function, handles both
        find in classes and find in module

        :param obj: object, either a python class or module
        :param name: str, optional. Search query.
        :param print_table: bool, optional. If True it prints a table with all the found items
    """
    if inspect.isclass(obj):
        return find_class_method(obj, name=name, print_table=print_table)
    else:
        return find_module_function(obj, name=name, print_table=print_table)
