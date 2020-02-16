## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from decimal import Decimal
from logging import warning

def list2string(lista):
        """Covierte lista a string"""
        if  len(lista)==0:
            return ""
        if str(lista[0].__class__) in ["<class 'int'>", "<class 'float'>"]:
            resultado=""
            for l in lista:
                resultado=resultado+ str(l) + ", "
            return resultado[:-2]
        elif str(lista[0].__class__) in ["<class 'str'>",]:
            resultado=""
            for l in lista:
                resultado=resultado+ "'" + str(l) + "', "
            return resultado[:-2]

## Reverse function of list2string where class is a str
def string2list_of_strings(s):
    arr=[]
    if s!="":
        arrs=s.split(", ")
        for a in arrs:
            arr.append(a[1:-1])
    return arr

def string2list_of_integers(s, separator=", "):
    """Convers a string of integer separated by comma, into a list of integer"""
    arr=[]
    if s!="":
        arrs=s.split(separator)
        for a in arrs:
            arr.append(int(a))
    return arr
    
    
## Converts a string  to a decimal
def string2decimal(s, type=1):
    if type==1: #2.123,25
        try:
            return Decimal(s.replace(".","").replace(",", "."))
        except:
            return None

## Converts a decimal to a localized number string
def l10nDecimal(dec, digits=2):
    from PyQt5.QtCore import QLocale
    l=QLocale()
    return l.toCurrencyString(float(dec))

## Converts strings True or False to boolean
## @param s String
## @return Boolean
def str2bool(s):
    if s=="True":
        return True
    return False    

## Converts boolean to  True or False string
## @param s String
## @return Boolean
def bool2string(b):
    if b==True:
        return "VERDADERO"
    return "FALSO"
    
## Function that converts a None value into a Decimal('0')
## @param dec Should be a Decimal value or None
## @return Decimal
def none2decimal0(dec):
    return none2alt(dec,Decimal('0'))

## If a value is None, returns an alternative
def none2alt(value, alternative):
    if value==None:
        return alternative
    return value

## Bytes 2 string
def b2s(b, code='UTF-8'):
    return b.decode(code)
    
def s2b(s, code='UTF8'):
    """String 2 bytes"""
    if s==None:
        return "".encode(code)
    else:
        return s.encode(code)

def c2b(state):
    """QCheckstate to python bool"""
    from PyQt5.QtCore import Qt
    if state==Qt.Checked:
        return True
    else:
        return False

def b2c(booleano):
    """Bool to QCheckstate"""
    from PyQt5.QtCore import Qt
    if booleano==True:
        return Qt.Checked
    else:
        return Qt.Unchecked     

## Returns a list with object in positions removed
def list_remove_positions(l, listindex):
    if l is None:
        warning("I can't remove positions from a None list")
        return None
    r=[]
    for i, o in enumerate(l):
        if i not in listindex:
            r.append(o)
    return r

## LOR is a list of list. Naned List Of Rows, used in myqtablewidget
## @param listindex is a list of column indexes to remove
def lor_remove_columns(rows, listindex):
    r_rows=[]
    for i, row in enumerate(rows):
        r_rows.append(list_remove_positions(row,listindex))
    return r_rows

## LOR is a list of list. Naned List Of Rows, used in myqtablewidget
## @param listindex is a list of column indexes to remove
def lor_remove_rows(rows, listindex):
    return list_remove_positions(rows, listindex) #It's a list but of row

## String to linux shell
#def string2shell(cadena):
#    cadena=str(cadena)
#    cadena=cadena.replace("'","\\'")
#    return cadena

## strint to latex
def string2tex(cadena):
    cadena=str(cadena)
    cadena=cadena.replace('[','$ [ $')
    cadena=cadena.replace(']','$ ] $')
    cadena=cadena.replace('&','\&')
    cadena=cadena.replace('²','$ ^2 $')
    cadena=cadena.replace('#', '\#')
    return cadena

## Converts a string to set inside an XML to a valid XML string
def string2xml(s):
    s=s.replace('"','&apos;' )
    s=s.replace('<','&lt;' )
    s=s.replace('>','&gt;' )
    s=s.replace('&','&amp;' )
    s=s.replace("'",'&apos;' )
    return s

## Converts a string to set inside an XML to a valid XML string
def xml2string(s):
    s=s.replace('&apos;','"')
    s=s.replace('&lt;','<')
    s=s.replace('&gt;','>')
    s=s.replace('&amp;','&')
    s=s.replace('&apos;',"'")
    return s
    
## Converts my common objects to its numeric value
def object2value(o):
    if o.__class__.__name__ in ["int", "float", "Decimal"]:
        return o
    elif o.__class__.__name__ in ["Currency",  "Money"]:
        return o.amount



if __name__ == "__main__":
    def print_lor(lor):
        for row in lor:
            print(row)

    lor=[]
    for i in range(10):
        lor.append([1*i,2*i,3*i,4*i])
    print_lor(lor)

    a=lor_remove_columns(lor,[2,3])
    print_lor(a)
    b=lor_remove_rows(a,[8,9])
    print_lor(b)

    