## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

## Class that return a object to manage listdict
class ListDictObject:
    def __init__(self,ld, name=None):
        self.name=self.__class__.__name__ if name is None else name
        self.ld=ld

    def length(self):
        return len(self.ld)

    def has_key(self,key):
        return listdict_has_key(self.ld,key)

    def print(self):
        listdict_print(self.ld)

    def sum(self, key, ignore_nones=True):
        return listdict_sum(self.ld, key, ignore_nones)

    def list(self, key, sorted=True):
        return listdict2list(self.ld, key, sorted)

    def average_ponderated(self, key_numbers, key_values):
        return listdict_average_ponderated(self.ld, key_numbers, key_values)

def listdict_has_key(listdict, key):
    if len(listdict)==0:
        return False
    return key in listdict

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