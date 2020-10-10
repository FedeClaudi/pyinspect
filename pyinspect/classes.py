from rich._inspect import Inspect
from pyinspect.utils import _class_name, stringify, textify


class Enhanced:
    def __repr__(self):
        """
        Returns a string with the class name and
        the number of attributes in the class
        """
        keys = dir(self)
        total_items = len(keys)
        keys_not_shown = [key for key in keys if key.startswith("__")]
        n_keys_not_shown = len(keys_not_shown)

        return f'"{_class_name(self)}" class with {total_items - n_keys_not_shown} attributes'

    def __str__(self):
        """
        Returns a formatted string with
        a summary of the class' attributes
        """
        return stringify(
            Inspect(
                self,
                help=True,
                methods=True,
                private=True,
                dunder=False,
                sort=True,
                all=False,
            ),
            maxlen=-1,
        )

    def __getattr__(self, attr):
        """
        Gets called when a class inheriting from Enhanced
        can't find the attribute the user requested.

        Raises a AttributeError but also shows the attributes
        that *do* exist.
        """
        inspect = Inspect(
            self,
            help=True,
            methods=True,
            private=True,
            dunder=True if "__" in attr else False,
            sort=True,
            all=False,
        )

        raise AttributeError(
            textify(
                f"Attribute [bold red]{attr}[/bold red] does not exist in {_class_name(self)}.\n"
                + f"These are the attributes in {_class_name(self)}:\n",
                maxlen=-1,
            )
            + stringify(inspect, maxlen=-1),
        )
