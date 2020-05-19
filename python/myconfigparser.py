from configparser import ConfigParser
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from os import path, makedirs
from Crypto import Random

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
            print("Configuration file {} doesn't exist".format(self.filename))

    def cset(self, section, option, value, key):
        a=AESCipher(key.rjust(16).encode("utf8"));
        ci=a.encrypt(value.encode("utf8"))
        self.set(section,option,ci.decode("utf8"))

    def cget(self, section, option, key, default=None):
        a=AESCipher(key.rjust(16).encode("utf8"));
        value=self.get(section,option,default).encode("utf8")
        deci=a.decrypt(value)
        return deci.decode("utf8")

    def get(self, section, option, default=None):
        if self.config.has_option(section, option)==True:
            return self.config.get(section, option)
        else:
            self.set(section, option, default)
            return self.get(section, option)

    def set(self, section, option, value):
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


if __name__ == '__main__':
    c=MyConfigParser("prueba.ini")
    r=c.get("cpupower", "set_min_freq", "True")
    print("Readed option", r)
    c.set("cpupower", "set_min_freq", "False")
    c.cset("cpupower", "buffer", "Mi texto", "My key")
    c.save()
    print("Readed c option", c.cget("cpupower", "buffer", "My key"))
