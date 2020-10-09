import pyinspect as pi
import numpy as np


def test_info_printout():
    pi.whats_pi()


def test_what_variable():
    a = 1
    pi.what(a)

    a = "test"
    pi.what(a)

    a = {"a": "test"}
    pi.what(a)

    a = np.zeros(3)
    pi.what(a)

    a = ["a", {}, np.ones(3)]
    pi.what(a)

    pi.what(pi)


def test_what_locals():
    pi.what()

    a = 1
    pi.what()
