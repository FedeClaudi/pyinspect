from collections.abc import MutableMapping, Reversible, Mapping
import inspect
from rich.pretty import Pretty
from rich._inspect import Inspect
from rich.table import Table
from rich import box

from pyinspect.utils import stringify, textify
from pyinspect._colors import mocassin, orange, green
from pyinspect._rich import console
from pyinspect.classes import Enhanced


def pilist(*args):
    return List(*args)


class TupleKeys(Mapping, Enhanced):
    def __init__(self, keys, ctype="", dtype=""):
        self._tuple = tuple(keys)
        self.ctype = ctype
        self.dtype = dtype

    def __repr__(self):
        return f"{self.ctype} {self.dtype} [{len(self._tuple)} {self.dtype}]"

    def __str__(self):
        return f"{self.ctype} {self.dtype} [{len(self._tuple)} {self.dtype}]"

    def __rich_console__(self, *args):
        yield f"[{green}]{self.ctype}[/{green}] [{mocassin}]{self.dtype} [[{orange}]{len(self._tuple)}[/{orange}] {self.dtype}]"

    def __len__(self):
        return len(self._tuple)

    def __getitem__(self, item_index):
        return self._tuple[item_index]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self._tuple):
            item = self._tuple[self.n]
            self.n += 1
            return item
        else:
            raise StopIteration


class Dict(MutableMapping):
    def __init__(self, **kwargs):
        self._dict = {k: v for k, v in kwargs.items()}

    def __repr__(self):
        return f"pyinspect.builtins.Dict with {len(self)} items."

    def __str__(self):
        return f"pyinspect.builtins.Dict with {len(self)} items."

    def __rich_console__(self, *args):
        yield f"[{green}]pyinspect.builtins.Dict[/{green}][{mocassin}] with [{orange}]{len(self)}[/{orange}] items."

    def __getattr__(self, key):
        """
        Getting an attribute that doesn't exist
        returns the _dict entry with the same name as the attr.
        """
        try:
            return self._dict[key]
        except KeyError:
            if key == "__rich__":
                return

            inspect = Inspect(
                self,
                help=False,
                methods=True,
                private=True,
                dunder=False,
                sort=True,
                all=False,
            )
            console.print(inspect)
            raise AttributeError(
                textify(
                    stringify(
                        f"Attribute [bold red]{key}[/bold red] does not exist in pyinspect.builtins.Dict.\n"
                        + "Scroll up to see the attributes in pyinspect.builtins.Dict.",
                        maxlen=-1,
                    ),
                    maxlen=-1,
                )
            )

    def __setattr__(self, key, value):
        """
        Setting an attribute updates the
        dictionary content
        """
        if "_dict" in self.__dict__.keys():
            self.__dict__["_dict"][key] = value
        else:
            self.__dict__[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __getitem__(self, key):
        return self._dict[key]

    def __len__(self):
        return len(self._dict)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self._keys):
            item = self._tuple[self.n]
            self.n += 1
            return item
        else:
            raise StopIteration

    @property
    def keys(self):
        return TupleKeys(self._dict.keys(), "Dict", "keys")

    @property
    def values(self):
        return TupleKeys(self._dict.values(), "Dict", "values")

    @property
    def items(self):
        return ((k, v) for k, v in self._dict.items())

    def show(self):
        """ Renders a rich table with dict contents """
        tb = Table(
            box=box.SIMPLE,
            title="Dict content",
            title_style="magenta",
            show_lines=True,
            show_edge=True,
            show_footer=True,
            footer_style="dim",
        )
        tb.add_column(
            header="key",
            header_style="yellow",
            justify="center",
            footer=f"{len(self)} entries",
            width=20,
        )
        tb.add_column(
            header="value", header_style="yellow", justify="center", width=30
        )

        for k, v in self.items:
            tb.add_row(f"[{orange}]{k}", f"[{mocassin}]{v}")

        console.print(tb)


class Tuple(Mapping, Reversible, Enhanced):
    """
    Tuple-Like object similar to named tuples.
    When a Tuple object is crated a "names" string
    should be passed to specify the name of each class attribute.

    This will return a Tuple instance which can be used to create
    namedtuples-like objects
    """

    def __init__(self, names):
        names = names.split(", ")
        self._keys = names.copy()
        self.keys = TupleKeys(names.copy(), "Tuple", "keys")

        self._tuple = None

    @classmethod
    def _from_keys(cls, keys, values):
        """
        Returns an instance of Tuple
        filled in with both keys and values
        """
        # Create instance
        _new = cls(", ".join(keys))
        _new.values = TupleKeys(values, "Tuple", "values")

        # Create internal tuple
        _new._tuple = tuple(values)

        # Set attributes
        for k, v in zip(_new._keys, values):
            setattr(_new, k, v)

        # Create a dictionary representation
        _new.dict = {k: v for k, v in zip(_new._keys, values)}

        return _new

    def __call__(self, *values):
        """
        When an instance of Tuple is called
        with a list of functions, __call__ returns
        a new instance filled in with values
        """
        if len(values) != len(self._keys):
            raise ValueError(
                f"Tuple expected {len(self._keys)} values but got {len(values)} instead."
            )

        return self._from_keys(self._keys, values)

    def __str__(self):
        base = f"pyinspect.builtins.Tuple with {len(self._keys)} keys"
        keys = (
            f": {self._keys}"
            if len(self._keys) < 5
            else f': {str([k for n,k in enumerate(self._keys) if n<5])[:-1] + ", ..."}'
        )
        return base + keys

    def __repr__(self):
        return f"pyinspect.builtins.Tuple with {len(self._keys)} keys."

    def __rich_console__(self, *args):
        base = f"[{mocassin}]pyinspect.builtins.[green]Tuple[/green] with [{orange}]{len(self._keys)}[/{orange}] keys:"
        keys = (
            f"{self._keys}"
            if len(self._keys) < 5
            else f': {str([k for n,k in enumerate(self._keys) if n<5])[:-1] + ", ..."}'
        )
        yield base
        yield Pretty(keys)

    def __getattr__(self, name):
        raise AttributeError(
            f'pyinspect.builtins.Tuple does not have attribute "{name}".\n     Tuple keys: {self._keys}'
        )

    def __len__(self):
        return len(self._keys)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self._keys):
            item = self._tuple[self.n]
            self.n += 1
            return item
        else:
            raise StopIteration

    def __getitem__(self, item_index):
        return self._tuple[item_index]

    def __eq__(self, other):
        if isinstance(other, Tuple):
            for k, v in self.dict.items():
                if k not in other.keys:
                    return False
                if other.dict[k] != v:
                    return False

            for k, v in other.dict.items():
                if k not in self.keys:
                    return False
                if self.dict[k] != v:
                    return False

            return True
        elif isinstance(other, tuple):
            for n, v in enumerate(other):
                if v != self.values[n]:
                    return False

            return True
        else:
            raise TypeError(
                f'"==" operator not defined between objects ot type {Tuple} and {type(other)}'
            )

    def copy(self):
        return Tuple._from_keys(self.keys, self.values)

    def showkeys(self):
        console.print(f"{len(self._keys)} keys: ", Pretty(self._keys))


class List(MutableMapping, Reversible, Enhanced):
    """
    list-like object with better printing
    """

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
        yield f'[{green}]pyinspect.builtins.List[/{green}] [{mocassin}]containing [{orange}]{n}[/{orange}] item{"s" if n != 1 else ""}{":" if n > 0 else "."}'
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

    def reverse(self):
        self._list.reverse()
        return self
