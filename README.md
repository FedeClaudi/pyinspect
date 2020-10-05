[![IssuesCount](https://img.shields.io/github/issues-raw/FedeClaudi/pyinspect.svg)](https://img.shields.io/github/issues-raw/FedeClaudi/pyinspect)
[![license](https://img.shields.io/github/license/FedeClaudi/pyinspect.svg)](https://img.shields.io/github/license/FedeClaudi/pyinspect)
[![language](https://img.shields.io/github/languages/top/FedeClaudi/pyinspect.svg)](https://img.shields.io/github/languages/top/FedeClaudi/pyinspect)
[![language](https://img.shields.io/github/last-commit/FedeClaudi/pyinspect/master.svg)](https://img.shields.io/github/last-commit/FedeClaudi/pyinspect/master)
[![language](https://img.shields.io/github/stars/FedeClaudi/pyinspect?style=social.svg)](https://img.shields.io/github/stars/FedeClaudi/pyinspect?style=social)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<img src='coverage.svg'>


[![Twitter Follow](https://img.shields.io/twitter/follow/Federico_claudi.svg?style=social)](https://twitter.com/Federico_claudi)


# pyinspect - the python package for lazy programmers
**Don't remember a function's name?** Use `pyinspect` to look for it.
**Don't remember what a function does?** Use `pyinspect` to print its source code directly to your terminal
**Can't figure out why you keep getting an error?** Use `pyinspect`'s fancy tracebacks to get more info
**Still can't figure it out, but too lazy to google it?** Use `pyinspect` to print Stack Overflow's top answer for your error message directly to your terminal!

<!--! # TODO update GIF -->

[![gif](media/intro_cut.gif)](media/intro_cut.gif)
<p align="center">
An example of how `pyinspect` can be used to find and inspect functions lazily.
</p>

# Table of Contents
1. [Installing pyinspect](https://github.com/FedeClaudi/pyinspect#installing-pyinspect)
2. [Can't remember a variable's name...]((https://github.com/FedeClaudi/pyinspect#finding-functions))
3. [Can't remember a function's name...](https://github.com/FedeClaudi/pyinspect#finding-functions)
4. [Can't remember what a function does](https://github.com/FedeClaudi/pyinspect#inspecting-functions)
5. [Can't fix that bug...](https://github.com/FedeClaudi/pyinspect#tracebacks)
6. [Still can't fix that bug!](https://github.com/FedeClaudi/pyinspect#tracebacks)


## Installing pyinspect
It's as simple as:
``` shell
pip install pyinspect
```

## Can't remember a variable's name...
Allright, you've defined a bunch of variables and now can't remember the name or content of the one you need. Fear not, you can use `pyinspect` to print all variables in your local scope:

``` python

    import pyinspect as pi

    a = 'my variable'
    b = 'another variable'

    pi.what()  # print all local variables
```

or to look at a single variable:
```
    pi.what(a)
```

<!--! # TODO add image with this -->

## Can't remember a function's name...
That's okay! You can use `pyinspect` to search for a function in a module or for a class' method!
E.g. to look for functions with `sin` in their name in `numpy`:

``` python
# import the module whose functions you're looking for
import numpy as np

# import pyinspect
import pyinspect as pi

# Find the functions you're looking for
pyinspect.search(np, name='sin')
```


This results in a table with all the function's matching your search `name`:
<!--! # TODO update -->
<img src='media/find_function.png' style='border-radius:8px; box-shadow: 6px 6px 12px rgba(.2, .2, .2, .4)' width=800px></img>

>**note**: search also looks for functions in sub-modules of the module found.
e.g.  `search(matplotlib...)` will look for methods across the entire `matplotlib` library!


`pyinspect.find` can also be used to find class attributes. For example,
say that you're looking for a method with `export` in the name in `rich.console.Console`:


>**note**: search also looks for methods matching your query 
among the parents of the `class` you passed. Use `include_parents=False`
when calling `search` to restrict the search to just the class you've passed.
Methods of the parent class are highlighted in a different color!

>**PRO TIP:** if you don't pass a search name to `pyinspect.search` (e.g. `pyinspect.find(Console)`), `pyinspect.search` will print **all** functions and methods.


## Can't remember what a function does
Okay, you've found the function you need, that's great. *But how does it work?*
You could open a the file where it's defined, scroll down to it etc... but this `pyinspect`, the package for lazy programmers! Instead of going thruogh that hastle why not printing the function's code directly to terminal:

``` python 
# import pyinspect
import pyinspect as pi

# Look at how pyinspect.search works
pi.showme(pi.search)
```

which yields:
<!--! # TODO update -->

<img src='media/print_function.png' style='border-radius:8px; box-shadow: 6px 6px 12px rgba(.2, .2, .2, .4)' width=800px></img>


## Can't fix that bug...
Sometimes you know what's causing an error, sometimes you don't. When you don't, it helps to know what the variables involved in the error are, possibly without having to go through the extra work of debugging stuff!

Once again `pyinspect` has a labour-saving solution: an advanced `traceback` functionality that gives you all the information you need to fix your bug (hopefully!). Just install `pyinspect`'s traceback at the start of your script

E.g.:
``` python
# import pyinspect and install the traceback handler
import pi

pi.install_traceback()  # use hide_locals=True to hide locals panels

# make some buggy code
import numpy as np

a = np.ones(5)
b = "ignore this"  # a local variable not being used
c = np.zeros(4)  # ooops, wrong size

a + c  # this will give an error
```

and this is the traceback:
<!-- ! #  TODO update -->

<img src='media/traceback.png' style='border-radius:8px; box-shadow: 6px 6px 12px rgba(.2, .2, .2, .4)' width=800px></img>

> **note**: although we defined three variables (`a`, `b`, `c`) only two where in the line causing the error (`a + c`). `pyinspect` then highlights `a` and `c` in the traceback as this is what you need to know to fix your bug. If you want `pyinspect` to **only** show the variables in the error line pass `relevant_only=True` to `pi.install_traceback()`

**pro tips**: 
* if you want to show **all** items in the `local` scope (e.g. also imported modules, not just variables) then you can use `all_locals=True` in `pi.install_traceback()`
* if you don't want the locals to be shown at all, then use `hide_locals=True`
* if you want more or less extensive tracebacks, you can use `keep_frames` to decide how many `frames` to shown in nested tracebacks (i.e when a function `a` calls a function `b` and the error comes up in `b`, do you want to see only the locals in `b` or in `a` *and* `b`?)


## Still can't fix that bug!
Time to do what any real programmer does in this situation... google it / copy-paste an answer from Stack Overflow. But that involves pulling up your browser, opening a new tab, typing stuf... too much work!

When an error comes up, `pyinspect` gives you the opportunity to automate this work away: just type `s` in your terminal and `pyinspect` will give you links to google's top 3 solutions and print out the answer to Stack Overflow's top question related to your error!

<!-- ! #  TODO add image -->


## Contributing
Contributions are welcome! Start a pull request if you have a change you'd like to submit or open an issue to report a bug or request a new feature to be added to `pyinspect`

## Aknowledgements
`pyinspect` is mostly a thin wrapper on top of the **awesome** [`rich`](https://github.com/willmcgugan/rich) library, so a huge thank you goes to @willmcgugan for the great job done with `rich`.
