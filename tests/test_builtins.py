from pyinspect import List
import pyinspect as pi


def test_list():
    pi.List("b", "a")
    my = pi.List("a")

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

    my2 = pi.pilist("a", "c")
    assert len(my2) == 2

    my2 = pi.pilist("a")
    assert len(my2) == 1
