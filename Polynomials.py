from collections.abc import Iterable
from typing import Self
from GaloisFields import GF1,GF4,GF8,GFn

def map_list(to_type:type,the_list:list|Iterable):
    return type(the_list)(map(to_type,the_list))

class Polynomial:
    """
    Polynomial of some grade
    """

    def __init__(self,*vals:GFn,mod:Self|int=0):
        """
        :param vals: Highest grade first
        :param mod: vals will be modulo-d by this number, if given
        """
        self._vals:list

        self.mod = mod # Must be declared before vals
        self.grade = 0
        self.val_type:type|None = None
        self.vals = list(vals)

    @property
    def vals(self) -> list[int]:
        """

        :return:
        """
        return self._vals

    @vals.setter
    def vals(self,new_vals:Iterable|list):
        if not new_vals:
            self._vals = []
            self.grade = 0
            return

        # if self.mod: # (Done by GF objects)
        #     new_vals = list(map(lambda a:a % self.mod,new_vals))
        self.val_type = type(new_vals[0])

        start_index = 0
        for n, i in enumerate(new_vals):
            if i:
                start_index = n
                break

        self.grade = len(new_vals) - start_index - 1
        self._vals = new_vals#[start_index:]

    def to_grade(self,to_grade:int) -> Self:
        """
        Returns a copy with an extended/shortened value-list
        :param to_grade: New grade
        :return:
        """
        if len(self.vals) == to_grade:
            return self

        if len(self.vals) < to_grade:
            new_vals = (
                    [self.val_type(0) for _ in range(to_grade - len(self.vals))] +
                    self.vals
            )
            return Polynomial(*new_vals)

        return Polynomial(*(self.vals[-to_grade:]))

    def __len__(self):
        return len(self.vals)

    @staticmethod
    def _match_grades(p1,p2):
        """
        Matches Grades of p1 and p2 if necessary then returns them or a copy with matched grade
        :param p1:
        :param p2:
        :return: p1, p2
        """
        if len(p1) > len(p2):
            p2 = p2.to_grade(len(p1))
        elif len(p1) < len(p2):
            p1 = p1.to_grade(len(p2))

        return p1, p2

    def empty_like(self) -> Self:
        """
        Returns a Polynomial of the same structure but filled with 0
        :return:
        """
        return Polynomial(*[self.val_type(0) for _ in self])

    def __iter__(self):
        return iter(self.vals)

    def __add__(self, other:"Polynomial") -> Self:
        ssself,other = self._match_grades(self,other)

        new_vals = list(map(sum, zip(ssself,other)))
        return Polynomial(*new_vals)

    def __sub__(self, other:Self) -> Self:
        ssself,other = self._match_grades(self,other)

        new_vals = list(map(lambda a:a[0] - a[1], zip(ssself,other)))
        return Polynomial(*new_vals)

    def __mul__(self, other:Self) -> Self:
        ssself,other = self._match_grades(self, other)

        summands = [
            other << n for n,v1 in enumerate(ssself.vals[::-1]) if v1
        ]
        # for n,v1 in enumerate(ssself.vals[::-1]):
        #     if v1:
        #         summands.append(other << n)

        if not summands:
            return self.empty_like()

        cum_sum = summands[0]
        for i in summands[1:]:
            cum_sum += i
        return cum_sum

    def __floordiv__(self, other:Self) -> Self:
        ...

    def __mod__(self, other:Self) -> Self:
        ...

    def __str__(self):
        return f"<Poly of type {self.val_type.__name__}: {self.vals} | Grade {self.grade}>"

    def __lshift__(self, other:int) -> Self:
        """
        Multiplies by x ** other
        :param other:
        :return:
        """
        return Polynomial(*(
            self.vals + [self.val_type(0) for _ in range(other)]
        ))

x = Polynomial(*map_list(GF4, [0, 0, 1, 1]))
y = Polynomial(*map_list(GF4, [1, 0, 1, 0]))
z = Polynomial(*map_list(GF4, [0, 0, 1, 0]))

a = Polynomial(*map_list(GF4, [10]))

print(x)
print(y)

print(x * z)
print(x + a)
print(x + a + a)



