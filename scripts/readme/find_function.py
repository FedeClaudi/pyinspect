# import the module whose functions you're looking for
import numpy as np

import pyinspect as pi

# Find the functions you're looking for
pi.search(np, name="sin")
