"""
    This tutorial shows how to print
    the source code of a class' method to the consol
"""


# import the class you're using
from rich.console import Console


# import pyinspect
import pyinspect

# Print a function's source code
pyinspect.print_function(Console.export_text)
