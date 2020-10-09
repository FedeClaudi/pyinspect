"""
    This example shows how to use pyinspect
    to look at what a variable is or to get
    an idea of what variables are defined
    in your local scope
"""

import pyinspect as pi


# define a couple variables
a = "this is my variable"
b = "this is another variable"

# to inspect a single variable:
# pi.what(a)

# look at all variables in the scope
pi.what()
