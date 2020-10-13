from rich.syntax import Syntax
from rich._inspect import Inspect
from rich.panel import Panel
from rich.table import Table
from rich.pretty import Pretty
import numpy as np

from inspect import (
    isfunction,
    ismethod,
    isclass,
    getsource,
    isbuiltin,
    stack,
    getfile,
    getsourcelines,
)

from pyinspect._colors import (
    mocassin,
    salmon,
    Monokai,
    DimMonokai,
    lightblue,
    orange,
)

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
from pyinspect._rich import console
from pyinspect.panels import Report


def _get_local_stacks():
    """
    Returns all variables in locals stack
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
    return locs, local_stack


def _what_locals(**kwargs):
    """
    Prints all variables, classes and modules in the local scope where `what` was called
    """
    locs, local_stack = _get_local_stacks()
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
    console.print(
        Panel.fit(table, width=PANEL_WIDTH + 10, border_style=lightblue)
    )


def _what_variable(obj, **kwargs):
    """
    Prints a detailed report of a variable, including
      - name
      - __repr__
      - definition
      - attributes and methods

    Getting the name for builtins is tricky so it finds the
    variable's name by scooping around in the locals stack.
    Then it get's the corresponding locals frame's file
    and in it it looks for the line definition of the variable.
    """
    # Get variable's source
    try:
        # if it's a function or class
        _file = getfile(obj)
        line_no = getsourcelines(obj)[-1]
        name = _name(obj)

    except TypeError:  # doesn't work for builtins
        # Get all locals frames
        locs = [s.frame for s in stack()]
        locs = locs[::-1]  # start from most superficial and ingnore current

        # look for variable in locals stack
        for loc in locs:
            var = [(k, v) for k, v in loc.f_locals.items() if np.all(v == obj)]
            if var:
                name, value = var[0]
                try:
                    _file = loc.f_locals["__file__"]
                except KeyError:
                    while True:
                        loc = loc.f_back
                        if not loc or loc is None:
                            _file = ""

                        if "__file__" in loc.f_locals.keys():
                            _file = loc.f_locals["__file__"]
                            break
                break

        # look for variable definition in the source file
        _got_line = False
        if _file:
            with open(_file, "r") as source:
                for line_no, line in enumerate(source):
                    line = line.replace('"', "'")

                    if name in line and str(value) in line:
                        line_no += 1
                        _got_line = True
                        break  # We got the source line!

            if not _got_line:  # failed to find obj in source code
                _file = ""

    # Create report
    rep = Report(f"Inspecting variable: {name}", accent=salmon)
    rep.width = 150
    rep.add("[dim]Variable content:\n[/]")
    rep.add(Pretty(obj), "rich")
    rep.spacer()

    # add source
    if _file and _file.endswith(".py"):
        rep.add(f"[dim]Defined in:[/] {_file}:[{mocassin}]{line_no}")
        rep.add(
            _file,
            "code file",
            theme=Monokai,
            line_numbers=True,
            line_range=[line_no - 2, line_no + 2],
            highlight_lines=[line_no],
        )
    else:
        rep.add(f"[{orange}]Failed to get source code for variable")
    rep.spacer()

    # add rich inspect
    rep.add(
        Inspect(
            obj,
            help=False,
            methods=True,
            private=True,
            dunder=False,
            sort=True,
            all=False,
        ),
        "rich",
    )

    console.print(rep)


def what(var=None, **kwargs):
    """
    Shows the details of a single variable or an
    overview of what's in the local scope.
    """

    if var is None:
        _what_locals()
    else:
        _what_variable(var, **kwargs)


def showme(func):
    """
    Given a pointer to a python function, it prints the code of the function.
    Also works for class methods

    :param func: pointer to a python get_class_that_defined_method
    """
    if isbuiltin(func):
        console.print(
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
            console.print(
                f'[black on {mocassin}]`showme` only accepts functions and classes, not "{_class_name(func)}", sorry. '
            )
            return False

        if isclass(func):
            console.print(
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

    console.print(
        *output,
        Syntax(
            getsource(func),
            lexer_name="python",
            line_numbers=True,
            theme=Monokai,
        ),
    )

    return True
