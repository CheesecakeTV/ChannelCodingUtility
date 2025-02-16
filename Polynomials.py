from collections.abc import Iterable
from typing import Self
from functools import total_ordering


from GaloisFields import GF1,GF4,GF8,GFn,GF_class

def map_list(to_type:type,the_list:list|Iterable):
    return type(the_list)(map(to_type,the_list))

@total_ordering
class Polynomial:
    """
    Polynomial of some grade
    """

    def __init__(self,*vals:GFn|int,map_type:type=None):
        """
        :param vals: Highest grade first
        :param map_type: vals will be mapped to this type if given
        """
        if vals and isinstance(vals[0],(list,tuple)):
            vals = vals[0]

        if map_type is not None:
            vals = map_list(map_type,vals)

        self._vals:list

        self.grade = -1 # -1, if Polynomial is empty (all factors 0)
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
            self.grade = -1
            return

        # if self.mod: # (Done by GF objects)
        #     new_vals = list(map(lambda a:a % self.mod,new_vals))
        self.val_type = type(new_vals[0])

        self._vals = new_vals

        start_index = 0
        for n, i in enumerate(new_vals):
            if i:
                start_index = n
                break
        else:
            self.grade = -1
            return

        self.grade = len(new_vals) - start_index - 1

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

    def __mul__(self, other:Self|int) -> Self:
        if isinstance(other,(float,int,self.val_type)):
            return Polynomial(*[i * other for i in self.vals])

        ssself,other = self._match_grades(self, other)

        summands = [
            (other << n) * v1 for n,v1 in enumerate(ssself.vals[::-1]) if v1
        ]
        # for n,v1 in enumerate(ssself.vals[::-1]): # Same thing, just not list comprehension
        #     if v1:
        #         summands.append(other << n)

        if not summands:
            return self.empty_like()

        cum_sum = summands[0]
        for i in summands[1:]:
            cum_sum = cum_sum + i
        return cum_sum

    def __divmod__(self, other) -> (Self,Self):
        """More like __floordivmod__"""
        assert other, "Can't divide by an empty polynomial"

        if other.grade > self.grade:
            return Polynomial(),other

        dividend:Self = self.shortened()
        divisor = other.shortened() # dividend is divided by the divisor
        quotient = list()

        while dividend.grade >= divisor.grade:
            eq = self.val_type(dividend.vals[0] / divisor.vals[0])
            quotient.append(eq)

            temp = (dividend.grade - divisor.grade)
            temp = (divisor << temp)
            temp = temp * eq

            dividend = dividend - temp
            dividend = dividend.shortened()

        return Polynomial(*quotient),dividend

    def __floordiv__(self, other:Self) -> Self:
        return divmod(self,other)[0]

    def __mod__(self, other:Self) -> Self:
        return divmod(self,other)[1]

    def __str__(self):
        val_type = self.val_type
        if val_type is None:
            val_type = "???"
        else:
            val_type = val_type.__name__

        return f"<Poly with element-type {val_type}: {self.vals} | Grade {self.grade}>"

    def __lshift__(self, other:int) -> Self:
        """
        Multiplies by x ** other
        :param other:
        :return:
        """
        return Polynomial(*(
            self.vals + [self.val_type(0) for _ in range(other)]
        ))

    def shortened(self):
        """
        Returns an identical polynomial with shortened vals to match its grade
        :return:
        """
        if self.grade == -1:
            return Polynomial()

        return Polynomial(*self.vals[-self.grade - 1:])

    def __hash__(self) -> hash:
        return hash(tuple(self.shortened().vals))

    def __eq__(self, other:Self) -> bool:
        """
        Equality is based on values, not reference
        :param other:
        :return:
        """
        return tuple(self.shortened().vals) == tuple(other.shortened().vals)

    def __bool__(self):
        return self.grade != -1

    def __gt__(self, other:Self):
        if self.grade > other.grade: # Most common cases
            return True

        if self.grade < other.grade: # Most common cases
            return False

        for v1,v2 in zip(self.shortened(),other.shortened()):
            if abs(v1) > abs(v2):
                return True

            if abs(v1) < abs(v2):
                return False

        return False # Equality

    def __call__(self, x_val:int) -> int:
        """
        Insert a numerical value into the polynomial-function
        :param x_val: Value to be plottet in
        :return:
        """
        summands = [a * (x_val ** b) for b,a in enumerate(self.vals[::-1])]
        return sum(summands)

    def __pow__(self, power:int, modulo=None):
        if power == 0:
            return Polynomial(self.val_type(1))

        sol = self

        for _ in range(power - 1):
            sol = sol * self

        return sol

x = Polynomial(*map_list(GF1, [0, 0, 1, 1]))
y = Polynomial(*map_list(GF1, [1, 0, 1, 0]))
z = Polynomial(*map_list(GF1, [0, 0, 1, 0]))

a = Polynomial(*map_list(GF1, [0, 1]))

b = Polynomial(*map_list(GF1, [1, 0]))

# print(x)
# print(y)

x = Polynomial(1,0,0,0,1)
y = Polynomial(1,1)

i1,i2 = divmod(x,y)
print(i1)
print(i2)

x = Polynomial(1,2,3,4,5,map_type=GF4)
print(x ** 2)
print(x ** 3)
print(x ** 4)

