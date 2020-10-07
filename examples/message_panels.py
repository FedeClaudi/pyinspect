"""
    This example shows how to use pyinspect to
    print nice, simple message panels for warning,
    errors etc..
"""


import pyinspect as pi

pi.message("Message", "this is a message panel")
print("\n")  # make some space
pi.warn("Warning: something is weird", "this is a warning panel")
print("\n")  # make some space
pi.ok("All good, relax", "this is an okay panel")
print("\n")  # make some space
pi.error("Alarm, it went wrong!", "this is an error panel, oooops")
print("\n")  # make some space
