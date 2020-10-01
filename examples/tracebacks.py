"""
    This tutorial shows how to use pyinspect
    to produce pretty and informative traceback stacks
"""


# import pyinspect and install the traceback handler
import pyinspect

pyinspect.install_traceback()  # use hide_locals=True to hide locals panels

# make some buggy code
import numpy as np


def sum(a, b):
    return a + b


a = np.ones(5)
b = np.zeros(4)

sum(a, b)
