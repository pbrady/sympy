from inspect import currentframe

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_back.f_lineno

class debugger():
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)

    def pi(self, var, *args):
        """ print args and increment var. """
        self.__dict__[var] += 1
        print(var, self.__dict__[var], 'line: ', get_linenumber(), *args)


    def cpi(self, var, triggered, *args):
        """ print args if triggered is true.  Increment var. """
        self.__dict__[var] += 1
        if triggered:
            print(var, self.__dict__[var], 'line: ', get_linenumber(), *args)



deb = debugger(main=0, matches=0, s=0)
