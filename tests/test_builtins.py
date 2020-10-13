from pyinspect import List
import pyinspect as pi
import pytest


def test_tuple():
    mytup = pi.Tuple("a, b, c")
    assert len(mytup) == 3

    filled = mytup(1, 2, 3)
    assert len(filled) == 3

    with pytest.raises(ValueError):
        filled(1, 2)
        filled(1, 4, 5, 6)

    filled2 = mytup(2, 3, 1)
    assert filled != filled2

    filled3 = filled2.copy()
    assert filled3 == filled2
    assert filled3 == filled2._tuple

    print(mytup)
    print(filled)
    pi.console.print(mytup)
    pi.console.print(filled)

    mytup2 = pi.Tuple("a, b, c, d, e, f, g")
    print(mytup2)


def test_list_maker():
    l = pi.list(1, 2, 3)
    assert len(l) == 3

    assert pi.list("a", "c") == pi.list("c", "a").reverse()

    my2 = pi.list("a", "c")
    assert len(my2) == 2

    my2 = pi.list("a")
    assert len(my2) == 1


def test_list():
    pi.List("b", "a")
    my = pi.List("a")
    print(my)
    pi.console.print(my)

    assert len(my) == 1

    my.append("b")

    assert len(my) == 2

    my.extend(["c"])

    assert len(my) == 3

    my.extend(pi.List(2))

    assert len(my) == 4

    my.extend(pi.List())

    assert len(my) == 4

    my = my + [3]
    assert len(my) == 5

    my * 2
    assert len(my) == 10

    my *= 2
    my = my * 2
    assert len(my) == 40

    for item in my:
        print(item)

    my2 = pi.List([i for i in range(10)])
    my3 = pi.List((i for i in range(10)))

    assert len(my2) == 10
    assert len(my3) == 10
    assert my2 == my3

    assert len(pi.List(("a", 2))) == 1

    my2 = pi.List("a")
    my3 = pi.List("a")
    assert (my2 == my3) == True
    assert (["a"] == my2) == True
    assert (list("a") == my2) == True

    my2 = pi.List("a")
    my3 = my2.copy()
    assert (my2 == my3) == True

    sorted(my2, reverse=True)
