import re
import inspect
from rich import print
from rich.table import Table
import pkgutil
import importlib
from pyinspect.utils import clean_doc, get_class_that_defined_method


def search_class_method(
    class_obj, name="", print_table=True, include_parents=True, **kwargs
):
    """
        Given a python class, it finds allclass methods whose name includes
        the given search string (name)

        :param class_obj: a python Class. Should not be a class instance, but a point to the class object
        :param name: str, optional. Returns only methods which have this string in the name. If not is given returns all methods
        :param print_table: bool, optional. If True it prints a table with all the found methods
        :param bool: if true it looks for methods in parents of the class_obj as well

        :returns: dict with all the methods found
    """
    if not inspect.isclass(class_obj):
        raise ValueError(
            "find_class_method expects a python Class object as argument"
        )

    # Look for methods in the class and in the parents
    objs = [class_obj]

    if include_parents:

        def get_parent_classes(obj):
            if obj is None:
                return
            parents = obj.__base__
            if parents is None:
                return
            for p in [parents]:
                get_parent_classes(p)
            objs.append(parents)

        get_parent_classes(class_obj)

    found = {}
    for obj in objs:
        found[obj] = {k: v for k, v in obj.__dict__.items() if name in k}
    found = {k: v for k, v in found.items() if v.keys()}

    if not found.keys():
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
        table.add_column("Class", justify="center", style="bold green")
        table.add_column("Line #", justify="center")
        table.add_column("Source", style="dim")

        # list methods
        for n, (obj, methods) in enumerate(found.items()):
            for k, v in methods.items():
                if not inspect.isfunction(v):
                    continue  # skip docstrings etc

                source = clean_doc(
                    inspect.getsource(getattr(class_obj, k)), maxn=125
                )
                lineno = inspect.getsourcelines(getattr(class_obj, k))[1]
                class_obj = get_class_that_defined_method(v)

                # is_parent = (
                #     "[green]:heavy_check_mark:[/green]"
                #     if obj == class_obj
                #     else ""
                # )

                table.add_row(
                    str(n),
                    k,
                    v.__module__,
                    class_obj.__name__,
                    # is_parent,
                    str(lineno),
                    source,
                )
        print(
            f"[yellow]Looking for methods of [magenta]{class_obj.__name__} ({class_obj.__module__})[/magenta] with query name: [magenta]{name}:",
            table,
        )

    return found


def search_module_function(module, name="", print_table=True, **kwargs):
    """
        Given a module (e.g. matplotlib.pyplot) finds all the functions
        in it whose name includes the given search string.

        :param module: python module (e.g. numpy)
        :param name: str, optional. Search string, if none is passed it returns all functions
        :param print_table: bool, optional.  If True it prints a table with all the found functions

        :returns: dict with all the functions found 
    """
    try:
        path = module.__path__
    except Exception:
        path = [inspect.getfile(module)]

    modules = {module.__name__: module}
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=path, prefix=module.__name__ + ".", onerror=lambda x: None,
    ):
        try:
            modules[modname] = importlib.import_module(modname)
        except (ImportError, OSError):
            pass

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

        print(
            f"[yellow]Looking for functions of [magenta]{module.__name__}[/magenta] with query name: [magenta]{name}:",
            table,
        )

    # return pointers to the functions
    return {
        modname: [getattr(mod, f) for f in ff]
        for (modname, mod), ff in found.items()
    }


def search(obj, name="", print_table=True, **kwargs):
    """
        General find function, handles both
        find in classes and find in module

        :param obj: object, either a python class or module
        :param name: str, optional. Search query.
        :param print_table: bool, optional. If True it prints a table with all the found items
    """
    if inspect.isclass(obj):
        return search_class_method(
            obj, name=name, print_table=print_table, **kwargs
        )
    else:
        return search_module_function(
            obj, name=name, print_table=print_table, **kwargs
        )
