"""
    This tutorial shows how to print
    the source code of a class' method to the consol
"""


# import the class you're using
from rich.console import Console


# import pyinspect
import pyinspect as pi

# Print a function's source code
pi.showme(Console.export_text)
