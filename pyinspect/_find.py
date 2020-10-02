from inspect import isclass, getsourcelines, isfunction
import inspect

from rich import box, print
from rich.table import Table

from pyinspect._colors import lightgray, lightgreen, yellow
from pyinspect.utils import clean_doc, get_class_that_defined_method


def print_methods_table(found, class_obj, name):
    """
        Prints a table with the methods found by search_class_method

        :param found: dictionary with found functions
        :param class_obj: class obj. Where the methods where searched in
        :param name: str, None. Query string
    """

    # make rich table
    table = Table(
        show_header=True, header_style="bold magenta", box=box.SIMPLE,
    )
    table.add_column("#", style="dim", width=3, justify="center")
    table.add_column("name", style="bold green")
    table.add_column("Module", justify="center")
    table.add_column("Class", justify="center", style="bold green")
    table.add_column("Line #", justify="center")
    table.add_column("Source", style="dim")

    # list methods
    count = 0
    for obj, methods in found.items():
        for k, v in methods.items():
            if not isfunction(v):
                continue  # skip docstrings etc

            source = clean_doc(
                inspect.getsource(getattr(class_obj, k)), maxn=125
            )
            lineno = inspect.getsourcelines(getattr(class_obj, k))[1]
            cs = get_class_that_defined_method(v)

            # TODO sort columns
            # TODO color things according to parent/original
            # TODO add line in module name
            # TODO replace source with signature

            table.add_row(
                str(count),
                k,
                v.__module__,
                cs.__name__,
                # is_parent,
                str(lineno),
                source,
            )
            count += 1
    print(
        f"[yellow]Looking for methods of [magenta]{class_obj.__name__} ({class_obj.__module__})[/magenta] with query name: [magenta]{name}:",
        table,
    )


def print_funcs_table(found, module, name):
    """
        Prints a table with the functions found by search_module_function

        :param found: dictionary with found functions
        :param module: module obj. Where the functions where searched in
        :param name: str, None. Query string
    """
    table = Table(
        show_header=True, header_style="bold magenta", box=box.SIMPLE,
    )
    table.add_column("#", style="dim", width=3, justify="center")
    table.add_column("name", style="bold " + lightgreen)
    table.add_column("Module")
    table.add_column("Arguments", style=lightgray)

    count = 0
    for (modname, mod), funcs in found.items():
        for f in funcs:
            # Get clean docstring
            func = getattr(mod, f)
            doc = clean_doc(inspect.getdoc(func), maxn=101)

            if not doc or doc is None:
                doc = "no docstring"

            # Get clickable link to module file
            if not isclass(func):
                lineno = getsourcelines(func)[-1]
                text = f"{modname} [dim](line: {lineno})"
            else:
                f = f"[{yellow}]{f}[/{yellow}]"
                text = f"[{yellow}]{modname}[/{yellow}]"

            # add to table
            table.add_row(str(count), f, text, str(inspect.signature(func)))
            count += 1

    st = "black bold on white"
    print(
        f"[yellow]\nLooking for functions of [{st}] {module.__name__} [/{st}] with query name [{st}] {name if name else 'no-name'} [/{st}]:",
        table,
    )
