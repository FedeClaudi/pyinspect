import inspect
from rich import print
from rich.syntax import Syntax

import time

def timestamp():
    """
        Returns a formatted timestamp
    """
    return time.strftime("%y%m%d_%H%M%S")



def print_function(func):
    """
        Given a pointer to a python function, it prints the code of the function. 

        :param func: pointer to a python function
    """
    if not inspect.isfunction(func):
        raise ValueError('print_function expects a function as argument')
    
    module = inspect.getfile(inspect.getmodule(func))
    print(f'\n[bold] function [yellow]{func.__name__}[/yellow] from {module}\n',
            Syntax(inspect.getsource(func), lexer_name='python'))