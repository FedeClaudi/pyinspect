from collections.abc import MutableMapping
import inspect
from rich.pretty import Pretty

from pyinspect.utils import stringify
from pyinspect._colors import mocassin, orange


class List(MutableMapping):
    def __init__(self, *args):
        if len(args) == 1:
            if inspect.isgenerator(args[0]) or isinstance(args[0], list):
                self._list = list(args[0])

            else:
                self._list = [args[0]]
        else:
            self._list = list(args)

    def __repr__(self):
        n = len(self._list)
        info = f'List containing ]{n} item{"s" if n != 1 else ""}{":" if n > 0 else "."}'
        return info

    def __str__(self):
        n = len(self._list)
        info = f'List containing {n} item{"s" if n != 1 else ""}{":" if n > 0 else "."}'
        content = stringify(self._list, maxlen=100)
        if n:
            return info + "\n" + content
        else:
            return info

    def __rich_console__(self, *args):
        n = len(self._list)
        yield f'[{mocassin}]List containing [{orange}]{n}[/{orange}] item{"s" if n != 1 else ""}{":" if n > 0 else "."}'
        if n > 0:
            yield Pretty(self._list)

    def __delitem__(self, item_index):
        del self._list[item_index]

    def __getitem__(self, item_index):
        return self._list[item_index]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self._list):
            item = self._list[self.n]
            self.n += 1
            return item
        else:
            raise StopIteration

    def __eq__(self, other):
        for item in self._list:
            if item not in self._get_iterable(other):
                return False

        for item in self._get_iterable(other):
            if item not in self._list:
                return False

        return True

    def __len__(self):
        return len(self._list)

    def __setitem__(self, item_index, value):
        self._list[item_index] = value

    def __add__(self, iterable):
        self.extend(iterable)
        return self

    def __sub__(self, other):
        raise ValueError("List class does not support subtraction")

    def __mul__(self, value):
        self._list = self._list * value
        return self

    def __imul__(self, value):
        self._list = self._list * value
        return self

    def _get_iterable(self, iterable):
        if isinstance(iterable, List):
            return iterable._list
        else:
            return iterable

    def __nonzero__(self):
        return self._list is True

    def insert(self, item_index, value):
        self._list.insert(item_index, value)

    def append(self, value):
        self.insert(len(self._list), value)

    def extend(self, iterable):
        self._list.extend(self._get_iterable(iterable))

    def copy(self):
        return List(*self._list)


def pilist(*args):
    return List(*args)
