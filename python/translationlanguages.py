## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from .libmanagers import ObjectManager_With_IdName_Selectable
## Manages languages
class TranslationLanguageManager(ObjectManager_With_IdName_Selectable):
    def __init__(self):
        ObjectManager_With_IdName_Selectable.__init__(self)
        
    def load_all(self):
        self.append(TranslationLanguage("en","English" ))
        self.append(TranslationLanguage("es","Español" ))
        self.append(TranslationLanguage("fr","Français" ))
        self.append(TranslationLanguage("ro","Rom\xe2n" ))
        self.append(TranslationLanguage("ru",'\u0420\u0443\u0441\u0441\u043a\u0438\u0439' ))

 
class TranslationLanguage:
    def __init__(self, id, name):
        self.id=id
        self.name=name
