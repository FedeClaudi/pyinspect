from inspect import isclass, getsourcelines, isfunction, signature
import inspect

from rich import box, print
from rich.table import Table

from pyinspect._colors import lightgray, lightgreen, yellow, salmon
from pyinspect.utils import clean_doc, get_class_that_defined_method, textify


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
    table.add_column("name", style="bold " + lightgreen)
    table.add_column("Class", justify="left")
    table.add_column("", style="bold " + lightgreen)

    table.add_column("Module", justify="left")
    table.add_column("Signature")

    # list methods
    count = 0
    for obj, methods in found.items():
        for k, v in methods.items():
            if not isfunction(v):
                continue  # skip docstrings etc

            lineno = inspect.getsourcelines(getattr(class_obj, k))[1]
            cs = get_class_that_defined_method(v)
            sig = textify(str(signature(cs)), maxlen=50)

            if cs == class_obj:
                cs = f"[{lightgreen}]{cs.__name__}[/{lightgreen}]"
                method_name = k
            else:
                cs = f"[{salmon}]{cs.__name__}[/{salmon}]"
                method_name = f"[{salmon}]{k}[/{salmon}]"

            module = f"[white]{v.__module__} [dim](line: {lineno})"

            table.add_row(
                str(count), method_name, cs, "", module, sig,
            )
            count += 1

    st = "bold black on yellow"
    print(
        f"\n[yellow]Looking for methods of [{st}] {class_obj.__name__} ({class_obj.__module__}) [/{st}] with query name: [{st}] {name} [/{st}]:",
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
            table.add_row(str(count), f, text, str(signature(func)))
            count += 1

    st = "black bold on yellow"
    print(
        f"[yellow]\nLooking for functions of [{st}] {module.__name__} [/{st}] with query name [{st}] {name if name else 'no-name'} [/{st}]:",
        table,
    )
