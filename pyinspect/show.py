from rich import print
from rich.syntax import Syntax
from rich import inspect as rinspect
from rich.panel import Panel
from rich.table import Table

from inspect import isfunction, ismethod, isclass, getsource, isbuiltin, stack

from pyinspect._colors import mocassin, salmon, Monokai, DimMonokai, lightblue

from pyinspect.utils import (
    _class_name,
    get_class_that_defined_method,
    get_end_of_doc_lineno,
    _name,
    _module,
    _class,
)
from pyinspect._exceptions import (
    render_scope,
    local,
    _get_type_info,
    PANEL_WIDTH,
    _get_type_color,
)


def what_locals(**kwargs):
    """
        Prints all variables, classes and modules in the local scope where `what` was called
    """
    # get relevant stack
    _stack = stack()
    local_stack = _stack[
        -1
    ].frame.f_locals  # vars in teh frame calling what hopefully

    # get local variables in stack frame and the type of each variable
    locs = {
        k: local(
            k,
            l,
            _get_type_info(l, all_locals=True)[0],
            _get_type_info(l, all_locals=True)[1],
            None,
        )
        for k, l in local_stack.items()
    }
    types = {
        k: _get_type_info(l, all_locals=True)[2]
        for k, l in local_stack.items()
    }

    # divide based on object type
    classes = {k: locs[k] for k, t in types.items() if "type" in t}
    variables = {
        k: locs[k]
        for k, t in types.items()
        if "type" not in t and "module" not in t
    }
    modules = {k: locs[k] for k, t in types.items() if "module" in t}

    # create a table to organize the results
    table = Table(show_edge=False, show_lines=False, expand=False, box=None)
    table.add_column()

    # render each group of objects and add to table
    for group, name in zip(
        [variables, classes, modules], ["Variables", "Classes", "Modules"]
    ):
        cleaned_group = {
            k: v for k, v in group.items() if not k.startswith("__")
        }

        if not len(cleaned_group.keys()):
            continue  # nothing to show

        # Get the correct color for the obj type
        obj = list(cleaned_group.items())[0][1].obj
        _type = _get_type_info(obj, all_locals=True)[2]
        type_color = _get_type_color(_type)

        # add to table
        table.add_row(
            f"[bold][{type_color}]{name}[/{type_color}][{mocassin}] in local frame."
        )
        table.add_row(render_scope(cleaned_group, just_table=True))

    # print!
    print(Panel.fit(table, width=PANEL_WIDTH + 10, border_style=lightblue))


def what_var(var, methods=True, private=True, help=True, **kwargs):
    """
        Uses rich inspect to print an overview
        of the object passed
    """
    rinspect(var, methods=methods, private=private, help=help, **kwargs)


def what(var=None, **kwargs):
    """
        Shows the details of a single variable or an
        overview of what's in the local scope.
    """

    if var is None:
        what_locals()
    else:
        what_var(var)


def showme(func):
    """
        Given a pointer to a python function, it prints the code of the function. 

        :param func: pointer to a python get_class_that_defined_method
    """
    if isbuiltin(func):
        print(
            f'[black on {mocassin}]`showme` currently does not work with builtin functions like "{_name(func)}", sorry. '
        )
        return False
    if not (isfunction(func) or isclass(func) or ismethod(func)):
        # check if it's a class instance
        try:
            func = _class(func)
            getsource(func)  # fails on builtins
            if not isclass(func):
                raise TypeError
        except (AttributeError, TypeError):
            print(
                f'[black on {mocassin}]`showme` only accepts functions and classes, not "{_class_name(func)}", sorry. '
            )
            return False

        if isclass(func):
            print(
                f"[{mocassin}]The object passed is a class instance, printing source code for the class definition"
            )

    # Print source class
    class_obj = get_class_that_defined_method(func)

    output = []
    if class_obj is not None:
        # showing a class method, also include class initial definition in the output
        output.append(
            f"\n[bold green] Method [yellow]{_name(func)}[/yellow] from class [blue]{_name(class_obj)}[/blue]"
        )

        # get end of class docstring
        doc_end = get_end_of_doc_lineno(class_obj)
        truncated = False

        if doc_end is None:
            doc_end = 2
        elif doc_end > 10:
            doc_end = 10
            truncated = True

        output.extend(
            [
                f"\n[{salmon}] Class definition {'(first 10 lines)' if truncated else ''}:",
                # class definition
                Syntax(
                    getsource(class_obj),
                    lexer_name="python",
                    line_range=(0, doc_end),
                    line_numbers=True,
                    theme=DimMonokai,
                ),
                f"\n[bold {salmon}]Method code:",
            ]
        )
    else:
        output.append(
            f"\n[bold]Function [yellow]{_name(func)}[/yellow] from [blue]{_module(func)}[/blue]\n"
        )

    print(
        *output,
        Syntax(
            getsource(func),
            lexer_name="python",
            line_numbers=True,
            theme=Monokai,
        ),
    )

    return True
