from configparser import ConfigParser
from os import path, makedirs

class MyConfigParser:
    def __init__(self, filename):
        self.filename=filename
        self.config=ConfigParser()
        if path.exists(self.filename):
            self.config.read(self.filename)

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
        makedirs(path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w') as f:
            self.config.write(f)


if __name__ == '__main__':
    c=MyConfigParser("prueba.ini")
    r=c.get("cpupower", "set_min_freq", "True")
    print("Readed option", r)
    c.set("cpupower", "set_min_freq", "False")
    c.save()