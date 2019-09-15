import time
import warnings
import functools
import socket
from logging import error, debug

## allows you to measure the execution time of the method/function by just adding the @timeit decorator on the method.
## @timeit
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed

## Checks if there is internet
def is_there_internet(method):
    def internet(*args, **kw):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("www.google.com", 80))
            debug("There is Internet connection")
        except OSError:
            error("There is not Internet connection")
        return method(*args, **kw)
    return internet

def deprecated(func):
     """This is a decorator which can be used to mark functions
     as deprecated. It will result in a warning being emitted
     when the function is used."""
     @functools.wraps(func)
     def new_func(*args, **kwargs):
         warnings.simplefilter('always', DeprecationWarning)  # turn off filter
         warnings.warn("Call to deprecated function {}.".format(func.__name__),
                       category=DeprecationWarning,
                       stacklevel=2)
         warnings.simplefilter('default', DeprecationWarning)  # reset filter
         return func(*args, **kwargs)
     return new_func

@is_there_internet
@deprecated
@timeit
def testing_decorators():
    for i in range(10):
        print(i)
        
if __name__ == "__main__":
    testing_decorators()
