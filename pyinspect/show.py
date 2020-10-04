from rich import print
from rich.syntax import Syntax

from inspect import isfunction, ismethod, isclass, getsource, isbuiltin

from pyinspect._colors import mocassin, salmon, MonokaiStyle
from pyinspect.utils import (
    _class_name,
    get_class_that_defined_method,
    get_end_of_doc_lineno,
    _name,
    _module,
)


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
        print(
            f'[black on {mocassin}]`showme` only accepts functions and classes, not "{_class_name(func)}", sorry. '
        )
        return False

    # Print source class
    class_obj = get_class_that_defined_method(func)

    output = []
    if class_obj is not None:
        # showing a class method, also include class initial definition in the output
        output.append(
            f"\n[boldreen] Method [yellow]{_name(func)}[/yellow] from class [blue]{_name(class_obj)}[/blue]"
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
                    theme=MonokaiStyle,
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
            theme=MonokaiStyle,
        ),
    )

    return True
