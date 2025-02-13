from collections.abc import Iterable
from typing import Self

class Polynomial:
    """
    Polynomial of some grade
    """

    def __init__(self,*vals,mod:int=0):
        """
        :param vals: Highest grade first
        :param mod: vals will be modulo-d by this number, if given
        """
        self.mod = mod # Must be declared before vals
        self.vals = list(vals)
        self.grade = 0

    @property
    def vals(self):
        """

        :return:
        """
        return self._vals

    @vals.setter
    def vals(self,new_vals:Iterable):
        if not new_vals:
            self._vals = []
            self.grade = 0
            return

        if self.mod:
            new_vals = list(map(lambda a:a % self.mod,new_vals))

        start_index = 0
        for n, i in enumerate(new_vals):
            if i:
                start_index = n
                break

        self.grade = start_index
        self._vals = new_vals[start_index:]

    def __add__(self, other:Self) -> Self:
        ...

    def __sub__(self, other:Self) -> Self:
        ...

    def __mul__(self, other:Self) -> Self:
        ...

    def __floordiv__(self, other:Self) -> Self:
        ...

    def __mod__(self, other:Self) -> Self:
        ...

x = Polynomial(0,8,2,0)
print(x.vals)
