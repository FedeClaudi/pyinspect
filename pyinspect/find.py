import re
import inspect
from rich.syntax import Syntax
from rich import print
from rich.table import Table
from rich import inspect as rinspect

def clean_doc(doc,  maxn=47):
    if doc is None:
        return ''
    else:
        doc = doc.strip()
        if len(doc)>maxn:
            return doc[:maxn] + '...'
        else:
            return doc
    

def find_class_method(class_obj, name, print_table=True):
    found = {k:v for k,v in class_obj.__dict__.items() if name in k}
    if not found:
        print(f'[magenta]No methods found in class {class_obj} with query: {name}')
        return None

    if print_table:
        table = Table(show_header=True, header_style="bold magenta",)
        table.add_column("#", style="dim", width=3, justify='center')
        table.add_column("name", style='bold green')
        table.add_column("Line #", width=6, justify='center')
        table.add_column("Source", style='dim')
        

        for n, (k,v) in enumerate(found.items()):
            doc = clean_doc(inspect.getsource(getattr(class_obj, k)), maxn=200)
            lineno = inspect.getsourcelines(getattr(class_obj, k))[1]

            table.add_row(str(n), k, str(lineno), doc)
        print(table)

    return found

def find_module_function(module, name, print_table=True):
    # grab all function names that contain `name` from the module
    p = ".*{}.*".format(name)
    filtered = list(filter(lambda x: re.search(p, x, re.IGNORECASE), dir(module)))

    if not filtered:
        print(f'[magenta]No functions found in module {module} with query: {name}')
        return None

    # Print a table with the results
    if print_table:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3, justify='center')
        table.add_column("name", style='bold green')
        table.add_column("Docstring", width=52)
        table.add_column("Module", style='dim')
        
        for n, f in enumerate(filtered):
            attr = getattr(module, f)
            mod = str(inspect.getmodule(attr))
            doc = clean_doc(inspect.getdoc(attr))

            table.add_row(str(n), f, doc, mod)

        print(table)

    # return pointers to the functions
    return {f:getattr(module, f) for f in filtered}

