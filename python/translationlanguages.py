from .libmanagers import ObjectManager_With_IdName_Selectable
## Manages languages
class TranslationLanguageManager(ObjectManager_With_IdName_Selectable):
    def __init__(self):
        ObjectManager_With_IdName_Selectable.__init__(self)
        
    def load_all(self):
        self.append(TranslationLanguage(self.mem, "en","English" ))
        self.append(TranslationLanguage(self.mem, "es","Español" ))
        self.append(TranslationLanguage(self.mem, "fr","Français" ))
        self.append(TranslationLanguage(self.mem, "ro","Rom\xe2n" ))
        self.append(TranslationLanguage(self.mem, "ru",'\u0420\u0443\u0441\u0441\u043a\u0438\u0439' ))

 
class TranslationLanguage:
    def __init__(self, mem, id, name):
        self.id=id
        self.name=name
