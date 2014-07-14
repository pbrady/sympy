from inspect import currentframe, getframeinfo

def get_info():
    cf = currentframe()
    return getframeinfo(cf.f_back.f_back)


class debugger():
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)
            setattr(self,k+'_trigger', False)

    def info_printer(self, var, info, *args):
        # modify filename
        name = '/'.join(info.filename.split('/')[-2:])
        print(var, self.__dict__[var],
              '\nfile: {} function: {} line: {}\n'.\
              format(name, info.function, info.lineno), *args)

    def pi(self, var, *args):
        """ print args and increment var. """
        self.__dict__[var] += 1
        self.info_printer(var, get_info(), *args)


    def cpi(self, cond, var, *args):
        """ print args if triggered is true.  Increment var. """
        if self.__dict__[cond+'_trigger']:
            self.__dict__[var] += 1
            self.info_printer(var, get_info(), *args)


    def set_trigger(self, var, expr):
        """ set a trigger condition. """
        self.__dict__[var+'_trigger'] = (expr)


deb = debugger(main=0, matches=0, s=0, comm=0, basic=0,
               dsolve=0, classify=0)
