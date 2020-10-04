"""
    This tutorial shows how to use pyinspect.search
    to find a module's function given a search string.
"""

# import the module whose functions you're looking for
import matplotlib.pyplot as plt

# import matplotlib

# import pyinspect
import pyinspect as pi

# Find the functions you're looking for
pi.search(plt, name="subplot")

# Or look for it in the entire package!
# pi.search(matplotlib, name="subplot")


"""
    Pro tip: omit the 'name' argument to find *all* functions

    Pro tip: pass 'include_class=False' to pi.search to ignore classes and 
        only look for functions
"""
