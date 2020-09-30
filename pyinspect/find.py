import re
import inspect
from rich import print
from rich.table import Table
import pkgutil
import importlib
from pyinspect.utils import clean_doc, get_class_that_defined_method


def search_class_method(class_obj, name="", print_table=True):
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

    # Look for methods
    found = {k: v for k, v in class_obj.__dict__.items() if name in k}
    if not found:
        print(
            f"[magenta]No methods found in class {class_obj} with query: {name}"
        )
        return None

    if print_table:
        # make rich table
        table = Table(show_header=True, header_style="bold magenta",)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("name", style="bold green")
        table.add_column("Module", justify="center")
        table.add_column("Class", justify="center")
        table.add_column("Line #", justify="center")
        table.add_column("Source", style="dim")

        # list methods
        for n, (k, v) in enumerate(found.items()):
            if not inspect.isfunction(v):
                continue  # skip docstrings etc
            doc = clean_doc(inspect.getsource(getattr(class_obj, k)), maxn=100)
            lineno = inspect.getsourcelines(getattr(class_obj, k))[1]
            class_obj = get_class_that_defined_method(v)

            table.add_row(
                str(n), k, v.__module__, class_obj.__name__, str(lineno), doc
            )
        print(table)

    return found


def search_module_function(module, name="", print_table=True):
    """
        Given a module (e.g. matplotlib.pyplot) finds all the functions
        in it whose name includes the given search string.

        :param module: python module (e.g. numpy)
        :param name: str, optional. Search string, if none is passed it returns all functions
        :param print_table: bool, optional.  If True it prints a table with all the found functions

        :returns: dict with all the functions found 
    """
    modules = {module.__name__: module}
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=module.__path__,
        prefix=module.__name__ + ".",
        onerror=lambda x: None,
    ):
        modules[modname] = importlib.import_module(modname)

    # grab all function names that contain `name` from the module
    p = ".*{}.*".format(name)
    found = {}
    for modname, mod in modules.items():

        found[(modname, mod)] = list(
            filter(lambda x: re.search(p, x, re.IGNORECASE), dir(mod))
        )
    found = {k: v for k, v in found.items() if v}

    if not len(found.keys()):
        print(
            f"[magenta]No functions found in module {module} with query: {name}"
        )
        return None

    # Print a table with the results
    if print_table:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("name", style="bold green")
        table.add_column("Module")
        table.add_column("Docstring", style="dim")

        count = 0
        for (modname, mod), funcs in found.items():
            for f in funcs:
                attr = getattr(mod, f)
                doc = clean_doc(inspect.getdoc(attr), maxn=101)

                table.add_row(str(count), f, modname, doc)

                count += 1

        print(table)

    # return pointers to the functions
    return {
        modname: [getattr(mod, f) for f in ff]
        for (modname, mod), ff in found.items()
    }


def search(obj, name="", print_table=True):
    """
        General find function, handles both
        find in classes and find in module

        :param obj: object, either a python class or module
        :param name: str, optional. Search query.
        :param print_table: bool, optional. If True it prints a table with all the found items
    """
    if inspect.isclass(obj):
        return search_class_method(obj, name=name, print_table=print_table)
    else:
        return search_module_function(obj, name=name, print_table=print_table)
