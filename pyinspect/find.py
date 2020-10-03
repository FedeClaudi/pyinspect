import inspect
from inspect import isfunction, isclass
from rich import print


from pyinspect.utils import get_submodules
from pyinspect._find import print_funcs_table, print_methods_table


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
    if not isclass(class_obj):
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
        print_methods_table(found, class_obj, name)


def search_module_function(
    module, name="", print_table=True, include_class=True, **kwargs
):
    """
        Given a module (e.g. matplotlib.pyplot) finds all the functions
        in it whose name includes the given search string.

        :param module: python module (e.g. numpy)
        :param name: str, optional. Search string, if none is passed it returns all functions
        :param print_table: bool, optional.  If True it prints a table with all the found functions

        :returns: dict with all the functions found 
    """

    def same_module(obj, module):
        return inspect.getmodule(obj) == module

    # Get all the submodules
    modules = get_submodules(module)

    # grab all function names that contain `name` from the module
    found = {}
    for modname, mod in modules.items():
        # get only functions
        funcs = [
            o
            for o in inspect.getmembers(mod)
            if isfunction(o[1]) or isclass(o[1])
        ]

        if not include_class:
            funcs = [o for o in funcs if not isclass(o[1])]

        # keep only functions from this module
        mod_funcs = [o for o in funcs if same_module(o[1], mod)]

        # keep only functions matching the query name
        filtered = [o[0] for o in mod_funcs if name.lower() in o[0].lower()]

        found[(modname, mod)] = filtered
    found = {k: v for k, v in found.items() if v}

    if not len(found.keys()):
        print(
            f"[magenta]No functions found in module {module} with query: {name}"
        )
        return None

    # Print a table with the results
    if print_table:
        print_funcs_table(found, module, name)


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
