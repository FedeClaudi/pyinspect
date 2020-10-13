"""
    This tutorial shows how to use pyinspect's
    "Enhanced" class to add some useful magic
    attributes to your classes
"""

import pyinspect as pi

pi.install_traceback()


# Define a class with a bunch of attributes
class Test(pi.Enhanced):
    a = 1  # a couple variables
    _private = "this is private !!"

    def hi(
        self,
    ):  # define a function
        """
        Say HI!
        """
        print("Hello world")


# instantiate
t = Test()

# Enhanced.__repr__ endows test with nice formatting for printing
pi.console.print(t)

# If you try to access an attribute that doesn't exist,
# Enhanced gives you a list of the attributes that *do* exist
t.doesnt_exist  # this will raise an AttributeError

"""
    P.s.: If you look at the locals panels in the tracebacks you'll notice
    that t's value is:
        "Test" class with 3 attributes
    that's because Enhanced has a __repr__ method that returns the class
    name and number of attributes.
"""
