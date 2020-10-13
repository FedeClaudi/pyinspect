from pyinspect import List
import pyinspect as pi
import pytest


def test_dict_maker():
    d1 = pi.pidict(a=1, b=2)


def test_dict():
    d = pi.Dict(a=1, b=2)

    assert len(d.keys) == len(d.values)

    for i in d:
        pass

    assert len(d) == 2
    assert d.a == 1
    assert d.a == d["a"]

    d.a = 2
    assert d.a == 2
    assert d.a == d["a"]

    print(d, d.keys, d.values)
    pi.console.print(d, d.keys, d.values)

    for k, v in d.items:
        pass

    d2 = pi.Dict({k: k for k in range(20)})
    d2.show()

    d == d2

    with pytest.raises(AttributeError):
        d.no

    with pytest.raises(KeyError):
        d["no"]


def test_tuple():
    mytup = pi.Tuple("a, b, c")
    assert len(mytup) == 3

    filled = mytup(1, 2, 3)
    assert len(filled) == 3

    for val in filled:
        print(val)
    print(filled[0])

    with pytest.raises(ValueError):
        filled(1, 2)
        filled(1, 4, 5, 6)

    filled2 = mytup(2, 3, 1)
    assert filled != filled2

    filled3 = filled2.copy()
    filled3 == filled2
    filled3 == filled2._tuple

    filled2 == filled

    filled2.showkeys()

    print(mytup)
    print(filled)
    pi.console.print(mytup)
    pi.console.print(filled)

    mytup2 = pi.Tuple("a, b, c, d, e, f, g")
    print(mytup2)


def test_list_maker():
    l = pi.pilist(1, 2, 3)
    assert len(l) == 3

    assert pi.pilist("a", "c") == pi.pilist("c", "a").reverse()

    my2 = pi.pilist("a", "c")
    assert len(my2) == 2

    my2 = pi.pilist("a")
    assert len(my2) == 1


def test_list():
    pi.List("b", "a")
    my = pi.List("a")
    print(my)
    for val in pi.List(1, 2, 3, 4, 5):
        print(val)
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

    my[2]

    assert len(my2) == 10
    assert len(my3) == 10
    assert my2 == my3

    del my[2]

    my[1] = 2

    if my:
        pass

    assert len(pi.List(("a", 2))) == 1

    my2 = pi.List("a")
    my3 = pi.List("a")
    my2 == my3

    my2 = pi.List("a")
    my3 = my2.copy()
    assert (my2 == my3) == True

    sorted(my2, reverse=True)
