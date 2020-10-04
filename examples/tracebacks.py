"""
    This tutorial shows how to use pyinspect
    to produce pretty and informative traceback stacks
"""


# import pyinspect and install the traceback handler
import pyinspect

pyinspect.install_traceback()  # use hide_locals=True to hide locals panels

# make some buggy code
import numpy as np

a = np.ones(5)
b = "ignore this"  # a local variable not being used
c = np.zeros(4)  # ooops, wrong size

a + c  # this will give an error

"""
    Note: in the traceback a,b will be highlighted because they are in
    the line causing the error. 'b' will be shown as well though. 
    To only show the variables in the error line
    pass relevant_only=True to `install_traceback`

    To only show relevant variables, pass 'only_relevant=True' to 
    `pyinspect.install_traceback`.
"""
