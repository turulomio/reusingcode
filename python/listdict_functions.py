## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

def listdict_has_key(listdict, key):
    if len(listdict)==0:
        return False
    return key in listdict

def listdict_print(listdict):
    for row in listdict:
        print(row)

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
