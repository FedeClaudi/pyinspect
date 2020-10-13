[![IssuesCount](https://img.shields.io/github/issues-raw/FedeClaudi/pyinspect.svg)](https://img.shields.io/github/issues-raw/FedeClaudi/pyinspect)
[![license](https://img.shields.io/github/license/FedeClaudi/pyinspect.svg)](https://img.shields.io/github/license/FedeClaudi/pyinspect)
[![language](https://img.shields.io/github/languages/top/FedeClaudi/pyinspect.svg)](https://img.shields.io/github/languages/top/FedeClaudi/pyinspect)
[![language](https://img.shields.io/github/last-commit/FedeClaudi/pyinspect/master.svg)](https://img.shields.io/github/last-commit/FedeClaudi/pyinspect/master)
[![language](https://img.shields.io/github/stars/FedeClaudi/pyinspect?style=social.svg)](https://img.shields.io/github/stars/FedeClaudi/pyinspect?style=social)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<img src='coverage.svg'>


[![Twitter Follow](https://img.shields.io/twitter/follow/Federico_claudi.svg?style=social)](https://twitter.com/Federico_claudi)

# pyinspect - the python package for lazy programmers
**Don't remember a function's name?** Use `pyinspect` to look for it. \
**Don't remember what a function does?** Use `pyinspect` to print its source code directly to your terminal. \
**Can't figure out why you keep getting an error?** Use `pyinspect`'s fancy tracebacks to figure it out\
**Still can't figure it out, but too lazy to google it?** Use `pyinspect` to print Stack Overflow's top answer for your error message directly to your terminal!

... and a bunch of other features to make your life easier when coding.


[![gif](media/intro_cut.gif)](https://github.com/FedeClaudi/pyinspect/blob/master/media/intro_cut.gif)
<p align="center">
An example of how `pyinspect` can be used to find and inspect functions lazily.
</p>

# Table of Contents 
1. [Installing pyinspect](https://github.com/FedeClaudi/pyinspect#installing-pyinspect)
2. [When you can't remember a variable's name...](https://github.com/FedeClaudi/pyinspect#when-you-cant-remember-a-variables-name)
3. [When you can't remember a function's name...](https://github.com/FedeClaudi/pyinspect#when-you-cant-remember-a-functions-name)
4. [When you can't remember what a function does](https://github.com/FedeClaudi/pyinspect#when-you-cant-remember-what-a-function-does)
5. [When you can't fix that bug...](https://github.com/FedeClaudi/pyinspect#when-you-cant-fix-that-bug)
6. [When you **still** can't fix that bug...](https://github.com/FedeClaudi/pyinspect#tracebacks)
7. [When you got a question, ask Google](https://github.com/FedeClaudi/pyinspect#when-you-got-a-question-ask-google)
8. [When you... ](https://github.com/FedeClaudi/pyinspect#when-you)

## Installing pyinspect
It's as simple as:
``` shell
pip install pyinspect
```

## When you can't remember a variable's name..
Allright, you've defined a bunch of variables and now can't remember the name or content of the one you need. Fear not, becuse you can use `pyinspect` to print all variables in your local scope:

``` python

    import pyinspect as pi

    a = 'my variable'
    b = 'another variable'

    pi.what()  # print all local variables
```

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/what.png' width=800px></img>


or to look at a single variable in detail with:
``` python

    my_favourite_number = 21
    pi.what(a)
```

This will show you the variable content, where it has been defined and some of its attributes and methods. Something like:

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/what_var.png' width=800px></img>



## When you can't remember a function's name...
That's okay! You can use `pyinspect` to search for a function by its name!
E.g. to look for functions with `searc` in their name in `pyinspect`:

``` python
# import pyinspect
import pyinspect as pi

# Find the functions you're looking for
pi.search(pi, name='what')
```


This results in a table with all the function's matching your search `name`:

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/find_function.png' width=800px></img>

>**note**: search also looks for functions in sub-modules of the module given.
e.g.  `search(matplotlib, 'plot')` will look for methods across the entire `matplotlib` library!


`pyinspect.find` can also be used to find class methods. For example to look for a method with `export` in the name in `rich.console.Console`:
``` python
pi.search(Console, 'export')
```

>**note**: `search` also looks for methods matching your query 
among the parents of the `class` you passed. Use `include_parents=False`
when calling `search` to restrict the search to just the class you've passed.
Methods of the parent class are highlighted in a different color!

>**PRO TIP:** if you don't pass a search name to `pyinspect.search` (e.g. `pyinspect.find(Console)`), `pyinspect.search` will print **all** functions and methods.


## When you can't remember what a function does
Okay, you've found the function you need, that's great. *But how does it work?*
You could openthe file where it's defined, scroll down to it etc... but this `pyinspect`, the package for lazy programmers! Instead of going thruogh that hastle why not printing the function's code directly to your terminal with a simple command:

``` python 
# import pyinspect
import pyinspect as pi

# Look at how pyinspect.search works
pi.showme(pi.search)
```

which yields:

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/print_function.png' width=800px></img>


## When you can't fix that bug...
Sometimes you know what's causing an error, sometimes you don't. When you don't, it helps to know what the variables involved in the error are, possibly without having to go through the extra work of debugging stuff!

Once again `pyinspect` has a labour-saving solution: an advanced `traceback` functionality that gives you all the information you need to fix your bug (hopefully!). Just install `pyinspect`'s `traceback` at the start of your script: when get an error you'll get a helpful summary of what's going on with your code!

E.g.:
``` python
# import pyinspect and install the traceback handler
import pyinspect as pi

pi.install_traceback()  # use hide_locals=True to hide locals panels from your traceback

# make some buggy code
import numpy as np

a = np.ones(5)
b = "ignore this"  # a local variable not being used
c = np.zeros(4)  # ooops, wrong size

a + c  # this will give an error
```

and this is the traceback:

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/traceback.png' width=800px></img>

> **note**: although we defined three variables (`a`, `b`, `c`) only two where in the line causing the error (`a + c`). `pyinspect` then highlights `a` and `c` in the traceback as this is what you need to know to fix your bug. If you want `pyinspect` to **only** show the variables in the error line pass `relevant_only=True` to `pi.install_traceback()`

**pro tips**: 
* if you want to show **all** items in the `local` scope (e.g. also imported modules, not just variables) then you can use `all_locals=True` in `pi.install_traceback()`
* if you don't want the locals to be shown at all, then use `hide_locals=True`
* if you want more or less extensive tracebacks, you can use `keep_frames` to decide how many `frames` to shown in nested tracebacks (i.e when a function `a` calls a function `b` and the error comes up in `b`, do you want to see only the locals in `b` or in `a` *and* `b`?)


## When you **still** can't fix that bug...
Time to do what any real programmer does in this situation... google it / copy-paste an answer from Stack Overflow. But that involves pulling up your browser, opening a new tab, typing stuf... too much work!

When an error comes up, `pyinspect` gives you the opportunity to automate this work away by doing the googling for you. 
You can do that in two ways:

1. passing `enable_prompt=True` to `install_traceback`: after the error traceback a prompt will come up asking if you want to look for solutions online, type `y`. 
2. In a terminal window use the `why` command and `pyinspect` will automatically lookup solutions to the last error you've had [note you need to have installed `pyinspect`'s tracebacks for it to record errors].

Either way, you get 3 things:
* A description of your error
* Links to the top 3 results on Google
* A neat render of a Stack Overflow question and answer related to your error. 

Check it out:

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/why.png'></img>

## When you got a question, ask Google
Ever found yourself googling the same basic command over and over because you keep forgetting what the syntax is?
If you do (and I know you do), or if you have any other question, now you can look for answers directly in python with `pynspect.ask`.
Using it is fairly simple:

```python
pi.ask("python Concatenate two lists?")
```

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/ask.png' width=800px></img>

>**note**: you can also use `ask` in your terminal to lookup answers to your questions. E.g.:
``` 
ask "Python how to concatenate strings"
```


## When you... 
`pyinspect` has a few more useful little features you might find yourself using from time to time. One of our favourites is `panels`: a simple why to print neat messages to terminal, for when you need to communicate with your users.

```python

import pyinspect as pi


pi.warn('This is a warning', 'Ooops, something might be wrong!')


pi.ok('You got this!', 'Panels are simple, but nice. Checkout `pyinspect.panels` to see what other kind of panels there are!')
```

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/panels.png' width=800px></img>

You can also use `Report`, a more advanced panel which allows you to create a more structured and detailed panel (see `pi.whats_pi()`):

<img src='https://github.com/FedeClaudi/pyinspect/blob/master/media/showpi.png' width=800px></img>

As an example, see how I've used `Report` to render [my CV](https://github.com/FedeClaudi/My_CV)

## Contributing
Contributions are welcome! Start a pull request if you have a change you'd like to submit or open an issue to report a bug or request a new feature to be added to `pyinspect`

## Aknowledgements
`pyinspect` is mostly a thin wrapper on top of the **awesome** [`rich`](https://github.com/willmcgugan/rich) library, so a huge thank you goes to @willmcgugan for the great job done with `rich`.
