# import pyinspect and install the traceback handler
import pyinspect as pi

pi.install_traceback()  # use hide_locals=True to hide locals panels

# make some buggy code
import numpy as np

a = np.ones(5)
b = "ignore this"  # a local variable not being used
c = np.zeros(4)  # ooops, wrong size

a + c  # this will give an error
