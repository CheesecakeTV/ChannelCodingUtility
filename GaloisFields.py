from functools import wraps

def mod_izer(mod_by:int) -> callable:
    """
    Decorator for dividing returns of the decorated function mod mod_by
    :param mod_by: What number to do the modulo operation with
    :return:
    """
    def mod_izer_inner(fkt:callable) -> callable:
        @wraps(fkt)
        def new_fkt(*args,**kwargs):
            return fkt(*args,**kwargs) % mod_by

        return new_fkt
    return mod_izer_inner

def GF_class(mod_by) -> callable:
    """
    Turns all arithmetic operations inside the class into mod_ized functions.
    Calculations should all be done only with other members of the same class.
    :param mod_by:
    :return:
    """

    def make_GF_class_inner(the_class:type) -> type:

        to_decorate = [ # All arithmetic functions
            'add','radd','iadd',
            'sub','rsub','isub',
            'mul','rmul','imul',
            'truediv','rtruediv','itruediv',
            'mod','rmod','imod',
            'floordiv','rfloordiv','ifloordiv',
            'pow','rpow','ipow',
            'matmul','rmatmul','imatmul',
            'and','rand','iand',
            'or','ror','ior',
            'xor','rxor','ixor',
            'rshift','rrshift','irshift',
            'lshift','rlshift','ilshift',
            'neg','pos',
            'invert',
            'abs',
            'index',
            'round',
            'trunc',
            'floor',
            'ceil',
        ]

        for name in to_decorate:
            name = "__" + name + "__"
            if hasattr(the_class,name):
                setattr(
                    the_class,
                    name,
                    mod_izer(mod_by)(getattr(the_class,name))
                )
            # else:
            #     print(name,"not in",parent_class)

        return the_class

    return make_GF_class_inner

@GF_class(2)
class GF2(int):
    pass

x = GF2(5)
y = GF2(2)

print(x * y)









