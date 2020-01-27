from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from .Ui_frmSelector import Ui_frmSelector
#from .. myqwidgets import qmessagebox

## Managers must use the same objects in arrays (same address)
## They are considered as objects, and it's representation is from __repr__ method
class frmManagerSelector(QDialog, Ui_frmSelector):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setObjectName("frmManagerSelector")

    def setLabel(self, s):
        self.lbl.setText(s)
        
    def setManagers(self, mem, section,  objectname, manager, selected, *initparams):
        self.mem=mem
        self.section=section
        self.objectname=objectname
        self.tbl.settings(self.mem, self.section, "{}_tbl".format(self.objectname))
        self.tblSelected.settings(self.mem, self.section, "{}_tblSelected".format(self.objectname))
        
        self.manager=manager.clone(*initparams)#Clone manager to delete safely objects
        self.selected=selected
        
        #removes selected objects from manager
        for o in self.selected.arr:
            self.manager.remove(o)
        
        self._load_tbl()
        self._load_tblSelected()

    def _load_tblSelected(self):       
        self.tblSelected.setColumnCount(1)
        self.tblSelected.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Object")))
        self.tblSelected.applySettings() 
        self.tblSelected.setRowCount(self.selected.length())
        for i, o in enumerate(self.selected.arr):
            self.tblSelected.setItem(i, 0, QTableWidgetItem(str(o)))
        
    def _load_tbl(self):  
        self.tbl.setColumnCount(1)
        self.tbl.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Object")))
        self.tbl.applySettings()
        self.tbl.setRowCount(self.manager.length())
        for i, o in enumerate(self.manager.arr):
                self.tbl.setItem(i, 0, QTableWidgetItem(str(o)))

    def on_cmdLeft_released(self):
        for i in self.tblSelected.selectedItems():
            selected=self.selected.arr[i.row()]
            self.manager.append(selected)       
            self.selected.remove(selected) 
        self._load_tbl()
        self._load_tblSelected()
        
    def on_cmdRight_released(self):
        for i in self.tbl.selectedItems():
            selected=self.manager.arr[i.row()]
            self.selected.append(selected)
            self.manager.remove(selected)
        self._load_tbl()
        self._load_tblSelected()   
        
        
    def on_cmd_released(self):
        print("Selected",  self.selected.arr)
        self.done(0)
        
    def on_cmdUp_released(self):
        pos=None
        for i in self.tblSelected.selectedItems():
            pos=i.row()
        tmp=self.selected.arr[pos]
        self.selected.arr[pos]=self.selected.arr[pos-1]
        self.selected.arr[pos-1]=tmp
        self._load_tbl()
        self._load_tblSelected()             
        
    def on_cmdDown_released(self):
        pos=None
        for i in self.tblSelected.selectedItems():
            pos=i.row()
        tmp=self.selected.arr[pos+1]
        self.selected.arr[pos+1]=self.selected.arr[pos]
        self.selected.arr[pos]=tmp
        self._load_tbl()
        self._load_tblSelected()        
        
    def on_tbl_cellDoubleClicked(self, row, column):
        self.on_cmdRight_released()
        
    def on_tblSelected_cellDoubleClicked(self, row, column):
        self.on_cmdLeft_released()
        

if __name__ == '__main__':
    from libmanagers import ObjectManager_With_IdName
    from PyQt5.QtCore import QSettings
    class Mem:
        def __init__(self):
            self.settings=QSettings()
            
    class Prueba:
        def __init__(self, id=None, name=None):
            self.id=id
            self.name=name
    
    class PruebaManager(ObjectManager_With_IdName):
        def __init__(self):
            ObjectManager_With_IdName.__init__(self)
            
    d={'one':1, 'two':2, 'three':3, 'four':4}
    manager=PruebaManager()
    for k, v in d.items():
        manager.append(Prueba(v, k))
        
    selected=PruebaManager()
    selected.append(manager.arr[3])
    
    mem=Mem()
        
    from sys import exit
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    w = frmManagerSelector()
    w.setManagers(mem,"frmSelectorExample", "frmSelector", manager, selected)
    w.move(300, 300)
    w.setWindowTitle('frmSelector example')
    w.show()

    exit(app.exec_())
