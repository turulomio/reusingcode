## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode/python/myconfigparser.py
## IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT AND DOWNLOAD FROM IT
## DO NOT UPDATE IT IN YOUR CODE
# Crypto belongs to pycryptodome

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from base64 import b64encode, b64decode
from configparser import ConfigParser
from datetime import date, datetime, timedelta
from decimal import Decimal
from logging import debug
from os import path, makedirs

## BEGIN OF COPIES
## To make independient modules I copy this from reusing/casts
def str2bool(value):
    if value=="0" or value.lower()=="false":
        return False
    elif value=="1" or value.lower()=="true":
        return True

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

def string2list_of_strings(s, separator=", "):
    arr=[]
    if s!="":
        arrs=s.split(separator)
        for a in arrs:
            arr.append(a[1:-1])
    return arr

def string2list_of_integers(s, separator=", "):
    arr=[]
    if s!="":
        arrs=s.split(separator)
        for a in arrs:
            arr.append(int(a))
    return arr
## To make independient modules I copy this from reusing/datetime_functions
def string2dtnaive(s, format):
    allowed=["%Y%m%d%H%M","%Y-%m-%d %H:%M:%S","%d/%m/%Y %H:%M","%d %m %H:%M %Y","%Y-%m-%d %H:%M:%S.","%H:%M:%S", '%b %d %H:%M:%S']
    if format in allowed:
        if format=="%Y%m%d%H%M":
            dat=datetime.strptime( s, format )
            return dat
        if format=="%Y-%m-%d %H:%M:%S":#2017-11-20 23:00:00
            return datetime.strptime( s, format )
        if format=="%d/%m/%Y %H:%M":#20/11/2017 23:00
            return datetime.strptime( s, format )
        if format=="%d %m %H:%M %Y":#27 1 16:54 2017. 1 es el mes convertido con month2int
            return datetime.strptime( s, format)
        if format=="%Y-%m-%d %H:%M:%S.":#2017-11-20 23:00:00.000000  ==>  microsecond. Notice the point in format
            arrPunto=s.split(".")
            s=arrPunto[0]
            micro=int(arrPunto[1]) if len(arrPunto)==2 else 0
            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S" )
            dt=dt+timedelta(microseconds=micro)
            return dt
        if format=="%H:%M:%S": 
            tod=date.today()
            a=s.split(":")
            return datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
        if format=='%b %d %H:%M:%S': #Apr 26 07:50:44. Year is missing so I set to current
            s=f"{date.today().year} {s}"
            return datetime.strptime(s, '%Y %b %d %H:%M:%S')
    else:
        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))

## END OF COPIES





BS = 16
pad = lambda s: s + (BS - len(s) % BS) * bytes(chr(BS - len(s) % BS).encode("utf8") )
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
       def __init__( self, key ):
           self.key = key

       ## @param raw bytes
       def encrypt( self, raw ):
           raw = pad(raw)
           iv = Random.new().read( AES.block_size )
           cipher = AES.new( self.key, AES.MODE_CBC, iv )
           return b64encode( iv + cipher.encrypt( raw ) ) 

       ## @param enc bytes
       def decrypt( self, enc ):
           enc = b64decode(enc)
           iv = enc[:16]
           cipher = AES.new(self.key, AES.MODE_CBC, iv )
           return unpad(cipher.decrypt( enc[16:] ))

class MyConfigParser:
    def __init__(self, filename):
        self.filename=filename
        self.config=ConfigParser()
        if path.exists(self.filename):
            self.config.read(self.filename)
        else:
            print("Creating a new configuration file: {}".format(self.filename))
        self.__generate_id()
        self.id=self.get("MyConfigParser","id")[:16]

    def cset(self, section, option, value):
        a=AESCipher(self.id.encode("utf8"));
        ci=a.encrypt(value.encode("utf8"))
        self.set(section,option,ci.decode("utf8"))

    def cget(self, section, option, default=None):
        a=AESCipher(self.id.encode("utf8"));
        value=self.get(section,option,default).encode("utf8")
        deci=a.decrypt(value)
        return deci.decode("utf8")

    def get(self, section, option, default=None):
        if self.config.has_option(section, option)==True:
            return self.config.get(section, option)
        else:
            self.set(section, option, default)
            return self.get(section, option)

    def getDecimal(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return Decimal(value)
        except:
            debug("I couldn't convert to Decimal {} ({})".format(value, value.__class__))

    def getFloat(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return float(value)
        except:
            debug("I couldn't convert to float {} ({})".format(value, value.__class__))

    def getInteger(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return int(value)
        except:
            debug("I couldn't convert to int {} ({})".format(value, value.__class__))

    def getBoolean(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return str2bool(value)
        except:
            debug("I couldn't convert to boolean {} ({})".format(value, value.__class__))

    ## Example: self.value_datetime_naive("Version", "197001010000", "%Y%m%d%H%M")
    def getDatetimeNaive(self, section, option, default=None, format="%Y%m%d%H%M"):
        try:
            value=self.get(section, option, default)
            return string2dtnaive(value, format)
        except:
            debug("I couldn't convert to datetime naive {} ({})".format(value, value.__class__))

    def getList(self, section, option, default):
        try:
            value=self.get(section, option, default)
            return string2list_of_strings(value)
        except:
            debug("I couldn't convert to list of strings {} ({})".format(value, value.__class__))

    def getListOfIntegers(self, section, option, default):
        try:
            value=self.get(section, option, default)
            return string2list_of_integers(value)
        except:
            debug("I couldn't convert to list of integers {} ({})".format(value, value.__class__))

    def set(self, section, option, value):
        if isinstance(value, list):
            value=list2string(value)
        if section not in self.config:
            self.config.add_section(section)
            self.config[section]={}
        self.config.set(section, option, str(value))

    def save(self):
        dirname=path.dirname(self.filename)
        if dirname != "":
            makedirs(dirname, exist_ok=True)
        with open(self.filename, 'w') as f:
            self.config.write(f)

    ## Generate a [MyConfigParser] -> id if it's not created yet
    def __generate_id(self):
        if self.config.has_option("MyConfigParser","id") is False:
            h = SHA256.new()
            h.update(str(datetime.now()).encode("utf8"))
            self.set("MyConfigParser","id", h.hexdigest())

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser=ArgumentParser()
    parser.description="Configura las keys en ficheros de MyConfigParser"
    parser.add_argument("--file", required=True)
    parser.add_argument("--section", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--value", required=True)
    parser.add_argument("--secure", help="Encode setting", action="store_true", default=False)
    args=parser.parse_args()

    config=MyConfigParser(args.file)
    if args.secure:
        config.cset(args.section, args.key, args.value)
    else:
        config.set(args.section, args.key, args.value)
    config.save()

