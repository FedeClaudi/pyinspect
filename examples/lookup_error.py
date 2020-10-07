"""
    This tutorial shows how to use pyinspect
    to look up an error and get links to
    relevant answers on google and stack overflow.

    Note: for this to work, you need to have
    had at least one error using pyinspect's traceback's.
    It's advisable to run the tracebacks examples first,
    just in case.
"""

import pyinspect as pi


# To get links to answers for your error you just need to:
pi.get_answers()

# not you can also use `why` in your terminal to do the same
