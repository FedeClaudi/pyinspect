"""
    This tutorial shows how to use pyinspect.search
    to find a class' methods given a search string
"""

# import the class you need to inspect
from rich.console import Console

# import pyinspect
import pyinspect

# find class methods
methods = pyinspect.search(
    Console, "export"
)  # use include_parents=False to skip parents
