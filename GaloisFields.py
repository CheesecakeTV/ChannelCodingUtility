from functools import wraps

class GFn: # Only for typehints
    pass

def mod_izer(mod_by:int,force_type:type=None) -> callable:
    """
    Decorator for dividing returns of the decorated function mod mod_by
    :param force_type: This type will be forced upon the return value
    :param mod_by: What number to do the modulo operation with
    :return:
    """
    def mod_izer_inner(fkt:callable) -> callable:
        @wraps(fkt)
        def new_fkt(*args,**kwargs):
            answer = fkt(*args,**kwargs) % mod_by
            if force_type is None:
                return answer
            return force_type(answer)

        return new_fkt
    return mod_izer_inner

def GF_class(mod_by,force_type:bool=None) -> callable:
    """
    Turns all arithmetic operations inside the class into mod_ized functions.
    Calculations should all be done only with other members of the same class.

    :param force_type: True, if the class shall be applied to every arithmetic return value
    :param mod_by:
    :return:
    """


    def make_GF_class_inner(the_class:type) -> type:
        nonlocal force_type
        if force_type:
            force_type = the_class

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
                    mod_izer(mod_by,force_type=force_type)(getattr(the_class,name))
                )
            # else:
            #     print(name,"not in",parent_class)

        # if include_init:
        #     @wraps(the_class.__init__)
        #     def newInit(self,*args,**kwargs):
        #         super(the_class,self).__init__()#number % mod_by, *args, **kwargs)
        #     the_class.__init__ = newInit
        #
        return the_class

    return make_GF_class_inner

@GF_class(2,force_type=True)
class GF1(int, GFn):
    pass

@GF_class(16,force_type=True)
class GF4(int, GFn):
    pass

@GF_class(256,force_type=True)
class GF8(int, GFn):
    pass

x = GF1(5)
y = GF1(2)

print(x)

print(x * y)









