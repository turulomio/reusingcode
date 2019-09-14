## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

## This file must be in a directory ui in the package
## In the parent  directory we need
## package_resources
## connection_pg
## libmanagers


from PyQt5.QtCore import pyqtSlot, QTranslator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, qApp, QMessageBox
from .Ui_frmAccess import Ui_frmAccess
from .. connection_pg_qt import ConnectionQt
from .. translationlanguages import TranslationLanguageManager
from .. package_resources import package_filename
from logging import info



class frmAccess(QDialog, Ui_frmAccess):
    def __init__(self, qsettings, settings_root,  qtranslator, qpixmap, parent = None):
        QDialog.__init__(self,  parent)
        self.settings=qsettings
        self.translator=QTranslator()
        self.settingsroot=settings_root
        self.qpixmap=qpixmap
        
        self.setModal(True)
        self.setupUi(self)
        self.parent=parent
        
        self.cmbLanguages.disconnect()
        self.languages=TranslationLanguageManager()
        self.languages.selected=self.languages.find_by_id(self.settings.value(self.settingsroot+"/language", "en"))
        self.languages.qcombobox(self.cmbLanguages, self.languages.selected)
        self.cmbLanguages.currentIndexChanged.connect(self.on_cmbLanguages_currentIndexChanged)
        
        self.setPixmap(self.qpixmap)
        self.setTitle(self.tr("Login in PostreSQL database"))
        
        self.con=ConnectionQt()#Pointer to connection


    def setPixmap(self, qpixmap):
        icon = QIcon()
        icon.addPixmap(qpixmap, QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)        
        
    def setTitle(self, text):
        self.setWindowTitle(text)
        
    def setLabel(self, text):
        self.lbl.setText(text)
        
    def showLanguage(self, boolean):
        if boolean==False:
            self.cmbLanguages.hide()
            self.lblLanguage.hide()
        
        
    def config_load(self):
        self.txtDB.setText(self.mem.settings.value(self.settingsroot +"/db", "xulpymoney" ))
        self.txtPort.setText(self.mem.settings.value(self.settingsroot +"/port", "5432"))
        self.txtUser.setText(self.mem.settings.value(self.settingsroot +"/user", "postgres" ))
        self.txtServer.setText(self.mem.settings.value(self.settingsroot +"/server", "127.0.0.1" ))
        self.txtPass.setFocus()
        
    def config_save(self):
        self.mem.settings.setValue(self.settingsroot +"/db", self.txtDB.text() )
        self.mem.settings.setValue(self.settingsroot +"/port",  self.txtPort.text())
        self.mem.settings.setValue(self.settingsroot +"/user" ,  self.txtUser.text())
        self.mem.settings.setValue(self.settingsroot +"/server", self.txtServer.text())   
        self.mem.settings.setValue(self.settingsroot+"/language", self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.mem.language=self.mem.languages.find_by_id(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))

    @pyqtSlot(int)      
    def on_cmbLanguages_currentIndexChanged(self, stri):
        self.mem.language=self.mem.languages.find_by_id(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.mem.settings.setValue(self.settingsroot+"/language", self.mem.language.id)
        self.mem.languages.cambiar(self.mem.language.id)
        self.retranslateUi(self)

    def make_connection(self):
        """Función que realiza la conexión devolviendo true o false con el éxito"""
        try:
            self.con.init__create(self.txtUser.text(), self.txtPass.text(), self.txtServer.text(), self.txtPort.text(), self.txtDB.text())
            self.con.connect()
            return self.con.is_active()
        except:
            print ("Error in function make_connection",  self.mem.con)
            return False
    
    @pyqtSlot() 
    def on_cmdYN_accepted(self):
        self.con.init__create(self.txtUser.text(), self.txtPass.text(), self.txtServer.text(), self.txtPort.text(), self.txtDB.text())
        self.con.connect()
        if self.con.is_active():
            self.config_save()
            self.accept()
        else:
            self.qmessagebox(self.tr("Error conecting to {} database in {} server").format(self.con.db, self.con.server))
            self.reject()

    @pyqtSlot() 
    def on_cmdYN_rejected(self):
        self.reject()

    def qmessagebox(self,  text):
        m=QMessageBox()
        m.setWindowIcon(QIcon(self.qpixmap))
        m.setIcon(QMessageBox.Information)
        m.setText(text)
        m.exec_()   
        
    def qcombobox(self, combo, selected=None):
        """Selected is the object"""
        self.order_by_name()
        for l in self.arr:
            combo.addItem(l.name, l.id)
        if selected!=None:
                combo.setCurrentIndex(combo.findData(selected.id))

    ## @param id String
    def cambiar(self, id):
        filename=package_filename("caloriestracker", "i18n/caloriestracker_{}.qm".format(id))
        self.qtranslator.load(filename)
        info("TranslationLanguage changed to {}".format(id))
        qApp.installTranslator(self.qtranslator)
