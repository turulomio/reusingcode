## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README






## El objetivo es crear un objeto list_dict que se almacenera en self.ld con funciones set
## set_from_db #Todo se carga desde base de datos con el minimo parametro posible
## set_from_db_and_variables #Preguntara a base datos aquellas variables que falten. Aunque no estén en los parámetros p.e. money_convert
## set_from_variables #Solo con variables
## set #El listdict ya está hecho pero se necesita el objeto para operar con el
##class Do:
##    def __init__(self,d):
##        self.d=d
##        self.create_attributes()
##
##    def number_keys(self):
##        return len(self.d)
##
##    def has_key(self,key):
##        return key in self.d
##
##    def print(self):
##        listdict_print(self.d)
##
##    ## Creates an attibute from a key
##    def create_attributes(self):
##        for key, value in self.d.items():
##            setattr(self, key, value)




## Class that return a object to manage listdict
## El objetivo es crear un objeto list_dict que se almacenera en self.ld con funciones set
## set_from_db #Todo se carga desde base de datos con el minimo parametro posible
## set_from_db_and_variables #Preguntara a base datos aquellas variables que falten. Aunque no estén en los parámetros p.e. money_convert
## set_from_variables #Solo con variables
## set #El listdict ya está hecho pero se necesita el objeto para operar con el
class Ldo:
    def __init__(self, name=None):
        self.name=self.__class__.__name__ if name is None else name
        self.ld=[]

    def length(self):
        return len(self.ld)

    def has_key(self,key):
        return listdict_has_key(self.ld,key)

    def print(self):
        listdict_print(self.ld)

    def print_first(self):
        listdict_print_first(self.ld)

    def sum(self, key, ignore_nones=True):
        return listdict_sum(self.ld, key, ignore_nones)

    def list(self, key, sorted=True):
        return listdict2list(self.ld, key, sorted)

    def average_ponderated(self, key_numbers, key_values):
        return listdict_average_ponderated(self.ld, key_numbers, key_values)

    def set(self, ld):
        del self.ld
        self.ld=ld
        return self

    def is_set(self):
        if hasattr(self, "ld"):
            return True
        print(f"You must set your listdict in {name}")
        return False

    def append(self,o):
        self.ld.append(o)

def listdict_has_key(listdict, key):
    if len(listdict)==0:
        return False
    return key in listdict[0]

def listdict_print(listdict):
    for row in listdict:
        print(row)

def listdict_print_first(listdict):
    print("Printing first dict in a listdict")
    for key, value in listdict[0].items():
        print(f"    - {key}: {value}")

def listdict_sum(listdict, key, ignore_nones=True):
    r=0
    for d in listdict:
        if ignore_nones is True and d[key] is None:
            continue
        r=r+d[key]
    return r


def listdict_sum_negatives(listdict, key):
    r=0
    for d in listdict:
        if d[key] is None or d[key]>0:
            continue
        r=r+d[key]
    return r

def listdict_sum_positives(listdict, key):
    r=0
    for d in listdict:
        if d[key] is None or d[key]<0:
            continue
        r=r+d[key]
    return r


def listdict_average_ponderated(listdict, key_numbers, key_values):
    prods=0
    for d in listdict:
        prods=prods+d[key_numbers]*d[key_values]
    return prods/listdict_sum(listdict, key_numbers)


## Converts a listdict to a dict using key as new dict key
def listdict2dict(listdict, key):
    d={}
    for ld in listdict:
        d[ld[key]]=ld
    return d

## Returns a list from a listdict key
def listdict2list(listdict, key, sorted=True):
    r=[]
    for ld in listdict:
        r.append(ld[key])
    if sorted is True:
        r.sort()
    return r