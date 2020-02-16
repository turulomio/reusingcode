## @brief my Percentage object
## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from logging import error
from sys import exit
from decimal import Decimal

## Class to manage currencies in officegenerator
##
## The symbol is defined by code with self.symbol()
class Currency:
    def __init__(self, amount=None,  currency=None) :
        if amount==None:
            self.amount=Decimal(0)
        else:
            self.amount=Decimal(str(amount))
        if currency==None:
            self.currency='EUR'
        else:
            self.currency=currency


    def __add__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return Currency(self.amount+money.amount, self.currency)
        else:
            error("Before adding, please convert to the same currency")
            raise "OdfMoneyOperationException"

    def __sub__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return Currency(self.amount-money.amount, self.currency)
        else:
            error("Before substracting, please convert to the same currency")
            raise "CurrencyOperationException"

    def __lt__(self, money):
        if self.currency==money.currency:
            if self.amount < money.amount:
                return True
            return False
        else:
            error("Before lt ordering, please convert to the same currency")
            exit(1)

    ## Si las divisas son distintas, queda el resultado con la divisa del primero
    ##
    ## En caso de querer multiplicar por un numero debe ser despues. For example: money*4
    def __mul__(self, money):
        if money.__class__.__name__ in ("int",  "float", "Decimal"):
            return Currency(self.amount*money, self.currency)
        if self.currency==money.currency:
            return Currency(self.amount*money.amount, self.currency)
        else:
            error("Before multiplying, please convert to the same currency")
            exit(1)

    def __truediv__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return Currency(self.amount/money.amount, self.currency)
        else:
            error("Before true dividing, please convert to the same currency")
            exit(1)

    def __repr__(self):
        return self.string(2)

    ## Returs a typical currency string
    ## @param digits int that defines the number of decimals. 2 by default
    ## @return string
    def string(self,   digits=2):
        return "{} {}".format(round(self.amount, digits), self.symbol())






    def isZero(self):
        if self.amount==Decimal(0):
            return True
        else:
            return False

    def isGETZero(self):
        if self.amount>=Decimal(0):
            return True
        else:
            return False

    def isGTZero(self):
        if self.amount>Decimal(0):
            return True
        else:
            return False

    def isLTZero(self):
        if self.amount<Decimal(0):
            return True
        else:
            return False

    def isLETZero(self):
        if self.amount<=Decimal(0):
            return True
        else:
            return False

    def __neg__(self):
        """Devuelve otro money con el amount con signo cambiado"""
        return Currency(-self.amount, self.currency)

    def round(self, digits=2):
        return round(self.amount, digits)

    def qtablewidgetitem(self, decimals=2):
        from .. ui.myqtablewidget import qcurrency
        return qcurrency(self, decimals=2)

    ## returns a qtablewidgetitem colored in red is amount is smaller than target or green if greater
    def qtablewidgetitem_with_target(self, target, digits=2):
        item=self.qtablewidgetitem(digits)
        if self.amount<target:   
            item.setBackground(eQColor.Red)
        else:
            item.setBackground(eQColor.Green)
        return item

## Returns the symbol of the currency
def symbol(currency):
    if currency=="EUR":
        return "€"
    elif currency=="USD":
        return "$"
    elif currency in ["CNY",  "JPY"]:
        return "¥"
    elif currency=="GBP":
        return "£"
    elif currency=="u":
            return "u"## Returns the symbol of the currency

def name(name):
    if name=="EUR":
        return "Euro"
    elif name=="USD":
        return "American Dolar"
    elif name=="CNY":
        return "Chinese Yoan"
    elif name=="JPY":
        return "Japanes Yen"
    elif name=="GBP":
        return "Pound"
    elif name=="u":
            return "Unit"
            
            
def MostCommonCurrencyTypes():
    return ['CNY', 'USD', 'JPY', 'u', 'EUR', 'GBP']

## @param selectedcurrency is an currency
def qcombobox(self, combo, selectedcurrency=None):
    """Función que carga en un combo pasado como parámetro las currencies"""
    for currency in MostCommonCurrencyTypes:
        combo.addItem("{0} - {1} ({2})".format(currency, name(currency), symbol(currency)), currency)
    if selectedcurrency!=None:
            combo.setCurrentIndex(combo.findData(selectedcurrency))

