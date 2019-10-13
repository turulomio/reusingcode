from inspect import stack
    
def function_name(clas):
    #    print (inspect.stack()[0][0].f_code.co_name)
    #    print (inspect.stack()[0][3],  inspect.stack())
    #    print (inspect.stack()[1][3],  inspect.stack())
    #    print (clas.__class__.__name__)
    #    print (clas.__module__)
    return "{0}.{1}".format(clas.__class__.__name__, stack()[1][3])