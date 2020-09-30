"""
    This tutorial shows how to use pyinspect.search
    to find a module's function given a search string.
"""

# import the module whose functions you're looking for
import matplotlib.pyplot as plt
import matplotlib

# import pyinspect
import pyinspect

# Find the functions you're looking for
funcs = pyinspect.search(plt, name="subplot")

# Or look for it in the entire package!
funcs = pyinspect.search(matplotlib, name="subplot")
