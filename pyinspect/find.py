import re
import inspect
from rich.syntax import Syntax
from rich import print

# TODO add code to find method/function definition and print nicely + location

# TODO add nice traceback stuff?

def find_class_method(class_obj, name, display=True, just_docstring=False, max_lines=20):
    found = [(k,v) for k,v in class_obj.__dict__.items() if name in k]

    if display:
        for fon in found:
            if not just_docstring:
                source = inspect.getsource(getattr(class_obj, fon[0]))
            else:
                source = inspect.getdoc(getattr(class_obj, fon[0]))
                print(Syntax(f'def {fon[0]}(...', lexer_name='python'))

            if source is not None:
                print(Syntax(source, lexer_name='python', line_range=[1, max_lines], line_numbers=True),'\n...', '\n\n')

def find_module_function(module, name):
    # grab all function names that contain `name` from the module
    p = ".*{}.*".format(name)
    filtered = filter(lambda x: re.search(p, x, re.IGNORECASE), dir(module))

    return list(filtered)
