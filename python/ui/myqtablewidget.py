## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import Qt,  pyqtSlot, QObject
from PyQt5.QtGui import QKeySequence, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidget, QFileDialog,  QTableWidgetItem, QWidget, QCheckBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QAction, QMenu, QToolButton
from .. datetime_functions import dtaware2string, dtaware_changes_tz, time2string
from officegenerator import ODS_Write, Currency, Percentage,  Coord
import logging
from datetime import datetime, date,  timedelta
from decimal import Decimal

class myQTableWidget(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.parent=parent
        self.mem=None
        self.sectionname=None
        self._save_settings=True
        self.setAlternatingRowColors(True)
        self.saved_printed=False#To avoid printing a lot of times
        self._last_height=None
        
        
    def setVerticalHeaderHeight(self, height):
        """height, if null default.
        Must be after settings"""
        if height==None:
            self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._last_height=None
        else:
            self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.verticalHeader().setDefaultSectionSize(height) 
            self._last_height=height

    def setSaveSettings(self, state):
        """Used when i don't want my columns with being saved"""
        self._save_settings=state

    def sectionResized(self, logicalIndex, oldSize, newSize):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            for i in range(self.columnCount()):
                self.setColumnWidth(i, newSize)
        elif modifiers == Qt.ControlModifier:
            self.resizeRowsToContents()
            self.resizeColumnsToContents()
        self.save()
            
            
    def save(self):
        if self._save_settings==True:
            self.mem.settings.setValue("{}/{}_horizontalheader_state".format(self.sectionname, self.objectName()), self.horizontalHeader().saveState() )
            if self.saved_printed==False: 
                print("Saved {}/{}_horizontalheader_state".format(self.sectionname, self.objectName()))
                self.saved_printed=True
        
    def settings(self, mem, sectionname,  objectname=None):
        """objectname used for dinamic tables"""
        self.mem=mem
        self.setVerticalHeaderHeight(int(self.mem.settings.value("myQTableWidget/rowheight", 24)))
        self.sectionname=sectionname
        if objectname!=None:
            self.setObjectName(objectname)

    def applySettings(self):
        """settings must be defined before"""
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().sectionResized.connect(self.sectionResized)
        state=self.mem.settings.value("{}/{}_horizontalheader_state".format(self.sectionname, self.objectName()))
        if state:
            self.horizontalHeader().restoreState(state)
        

    def clear(self):
        """Clear table"""
        self.setRowCount(0)
        self.clearContents()

    def verticalScrollbarAction(self,  action):
        """Resizes columns if column width is less than table hint"""
        for i in range(self.columnCount()):
            if self.sizeHintForColumn(i)>self.columnWidth(i):
                self.setColumnWidth(i, self.sizeHintForColumn(i))

    @pyqtSlot()
    def keyPressEvent(self, event):
        if  event.matches(QKeySequence.ZoomIn) and self._last_height!=None:
            height=int(self.mem.settings.value("myQTableWidget/rowheight", 24))
            self.mem.settings.setValue("myQTableWidget/rowheight", height+1)
            logging.info("Setting myQTableWidget/rowheight set to {}".format(self.mem.settings.value("myQTableWidget/rowheight", 24)))
            self.setVerticalHeaderHeight(int(self.mem.settings.value("myQTableWidget/rowheight", 24)))
        elif  event.matches(QKeySequence.ZoomOut) and self._last_height!=None:
            height=int(self.mem.settings.value("myQTableWidget/rowheight", 24))
            self.mem.settings.setValue("myQTableWidget/rowheight", height-1)
            ("Setting myQTableWidget/rowheight set to {}".format(self.mem.settings.value("myQTableWidget/rowheight", 24)))
            self.setVerticalHeaderHeight(int(self.mem.settings.value("myQTableWidget/rowheight", 24)))
        elif event.matches(QKeySequence.Print):
            filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), "table.ods", self.tr("Libreoffice calc (*.ods)"))[0]
            if filename:
                Table2ODS(self.mem,filename, self, "My table")


    def on_orderby_action_triggered(self, action):
        action=QObject.sender(self)#Busca el objeto que ha hecho la signal en el slot en el que está conectado
        print(action.text())
        action_index=self.data_header_horizontal.index(action.text())#Search the position in the headers of the action Text
        attribute=self.attribute_names[action_index]
        self.manager.arr=sorted(self.manager.arr, key=lambda c: getattr(c, attribute),  reverse=False)     
        self.setDataFromManager(self.data_header_horizontal, self.data_header_vertical, self.manager, self.attribute_names)

    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    def setData(self, header_horizontal, header_vertical, data):
        # Creates order actions here after creating data
        self.orderby_actions=[]
        for header in header_horizontal:
            action=QAction(header)
            self.orderby_actions.append(action)
            action.triggered.connect(self.on_orderby_action_triggered)
        
        # Headers
        self.data_header_horizontal=header_horizontal
        self.data_header_vertical=header_vertical
        self.data=data
        self.setColumnCount(len(self.data_header_horizontal))
        for i in range(len(self.data_header_horizontal)):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(self.data_header_horizontal[i]))
        # Data
        self.applySettings()
        self.clearContents()
        self.setRowCount(len(self.data))        
        for row in range(len(self.data)):
            for column in range(len(self.data_header_horizontal)):
                self.setItem(row, column, self.object2qtablewidgetitem(self.data[row][column]))

    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    ## @param manager Manager object from libmanagers
    ## @param object_attribute_names List of Strings with name of the object attributes
    def setDataFromManager(self, header_horizontal, header_vertical, manager, object_attribute_names):
        self.attribute_names=object_attribute_names
        self.manager=manager
        data=[]
        for o in manager.arr:
            row=[]
            for name in object_attribute_names:
                row.append(getattr(o, name))
            data.append(row)
        self.setData(header_horizontal, header_vertical, data)
                    
    ## Converts a objecct class to a qtablewidgetitem
    def object2qtablewidgetitem(self, o):
        if o.__class__ in [int,  float, Decimal]:
            return qright(o)
        else:
            return qleft(o)

    ## Returns a list of strings with the horizontal headers
    def listHorizontalHeaders(self):
        header=[]
        for i in range(self.horizontalHeader().count()):
            header.append(self.horizontalHeaderItem(i).text())
        return header

    ## Returns a list of strings with the horizontal headers
    def listVerticalHeaders(self):
        header=[]
        for i in range(self.verticalHeader().count()):
            header.append(self.verticalHeaderItem(i).text())
        return header

    ## Returns a lisf of rows with the text of the 
    def listText(self):
        data=[]
        for i in range(self.rowCount()):
            row=[]
            for column in range(self.columnCount()):
                data.append(self.item(row,column).text())
        return data

    ## Fills table from a lr of rows
    ## Allowed objects, int, float, text, Currency, Porcentage
    ## @param lr is a list of rows (other list)
    ## @param decimals Integer or List of the size of the columns with the number of decimals to show. Default decimal==2. If Integer all columns has the same number of decimals
    ## @param datetimes with be converted to that timezone
    def fillWithListOfRows(self,lr, decimals=2, zonename="UTC"):
        if decimals.__class__.__name__=="int":
            decimals=[decimals]*len(lr[0])
        for row in range(len(lr)):
            self.fillAppendingRow(row, lr[row], decimals, zonename)


    ## If you don't want to add all rows at the same time you can fill appending row by row
    ## @param rownumber is the row to be added in the table
    def fillAppendingRow(self, rownumber, row, decimals=2, zonename="UTC"):
        if hasattr(self, "lr")==False:#Create list if it doesn't exist
            self.lr=[]
        if decimals.__class__.__name__=="int":
            decimals=[decimals]*len(row)
        self.lr.append(row)
        for column in range(len(row)):
            o=row[column]
            if o.__class__.__name__ in ["int"]:
                self.setItem(rownumber, column, qright(o))
            elif o.__class__.__name__ in ["datetime"]:
                self.setItem(rownumber, column, qdatetime(o,zonename))
            elif o.__class__.__name__ in ["float","Decimal"]:
                self.setItem(rownumber, column, qnumber(o,decimals[column]))
            elif o.__class__.__name__ in ["Percentage","Money","Currency"]:
                self.setItem(rownumber, column, o.qtablewidgetitem(decimals[column]))
            else:
                self.setItem(rownumber, column, qleft(o))
                
class wdgTable(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        self.lay=QVBoxLayout()
        self.laySearch=QHBoxLayout()
        self.lbl=QLabel()
        self.table=myQTableWidget()
        self.lbl.setText(self.tr("Add a string to search in table"))
        self.lbl.hide()
        self.txtSearch=QLineEdit()
        self.txtSearch.hide()
        self.txtSearch.textChanged.connect(self.on_txt_textChanged)
        self.cmdCloseSearch=QToolButton()
        self.cmdCloseSearch.hide()
        self.cmdCloseSearch.released.connect(self.on_cmdCloseSearch_released)
        self.laySearch.addWidget(self.lbl)
        self.laySearch.addWidget(self.txtSearch)
        self.laySearch.addWidget(self.cmdCloseSearch)
        self.lay.addWidget(self.table)
        self.lay.addLayout(self.laySearch)
        self.setLayout(self.lay)
        
        self.actionExport=QAction(self.tr("Export to Libreoffice Calc"))
        self.actionExport.triggered.connect(self.on_actionExport_triggered)
        
        self.actionSearch=QAction(self.tr("Search in table"))
        self.actionSearch.triggered.connect(self.on_actionSearch_triggered)
        self.actionSearch.setShortcut(Qt.CTRL + Qt.Key_F)
        
    ## @param rsActionExport String ":/xulpymoney/save.png" for example
    def setIcons(self, rsActionExport=None):
        if rsActionExport is not None:
            self.actionExport.setIcon(QIcon(rsActionExport))
            
    def on_cmdCloseSearch_released(self):
        self.txtSearch.setText("")
        self.lbl.hide()
        self.txtSearch.hide()
        self.cmdCloseSearch.hide()
            
    def on_actionExport_triggered(self):
        filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), "table.ods", self.tr("Libreoffice calc (*.ods)"))[0]
        if filename:
            Table2ODS(self.mem,filename, self, "My table")
            
    def on_actionSearch_triggered(self):
        self.lbl.show()
        self.txtSearch.show()
        self.cmdCloseSearch.show()
        self.txtSearch.setFocus()
            
    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Table options"):
        menu=QMenu(self.tr(title))
        menu.addAction(self.actionExport)
        menu.addSeparator()
        menu.addAction(self.actionSearch)
        menu.addSeparator()
        order=QMenu(self.tr("Order by"))
        for action in self.table.orderby_actions:
            order.addAction(action)
            menu.addAction(action)
        menu.addMenu(order)     
        return menu
        
    def on_txt_textChanged(self, text):
        for row in range(self.table.rowCount()):
            found=False
            for column in range(self.table.columnCount()):
                if self.table.item(row,column).text().lower().find(text.lower())>=0:
                    found=True
                    break
            if found==False:
                self.table.hideRow(row)
            else:
                self.table.showRow(row)

class Table2ODS(ODS_Write):
    def __init__(self, mem, filename, table, title):
        ODS_Write.__init__(self, filename)
        self.mem=mem
        sheet=self.createSheet(title)
        #Array width
        widths=[]
        if not table.verticalHeader().isHidden():
            widths.append(table.verticalHeader().width()*0.90)
        for i in range(table.columnCount()):
            widths.append(table.columnWidth(i)*0.90)
        sheet.setColumnsWidth(widths)

        #firstcontentletter and firstcontentnumber
        if table.horizontalHeader().isHidden() and not table.verticalHeader().isHidden():
            coord=Coord("B1")
        elif not table.horizontalHeader().isHidden() and table.verticalHeader().isHidden():
            print("A2")
            coord=Coord("A2")
            topleft=Coord("A2") if table.rowCount()<21 else Coord("A2").addRow(table.rowCount()-1-20)
            sheet.freezeAndSelect(coord, Coord("A2").addRow(table.rowCount()-1), topleft)
        elif not table.horizontalHeader().isHidden() and not table.verticalHeader().isHidden():
            coord=Coord("B2")
        elif table.horizontalHeader().isHidden() and table.verticalHeader().isHidden():
            coord=Coord("A1")

        #HH
        if not table.horizontalHeader().isHidden():
            for letter in range(table.columnCount()):
                sheet.add(Coord(coord.letter + "1").addColumn(letter), table.horizontalHeaderItem(letter).text(), "OrangeCenter")
        logging.debug("HH Done")
        #VH
        if not table.verticalHeader().isHidden():
            for number in range(table.rowCount()):
                try:#Caputuro cuando se numera sin items 1, 2, 3
                    sheet.add(Coord("A" + coord.number).addRow(number), table.verticalHeaderItem(number).text(), "YellowLeft")
                except:
                    pass
        logging.debug("VH Done")
        #Items
        for number in range(table.rowCount()):
            for letter in range(table.columnCount()):
                try:
                    o=self.itemtext2object(table.item(number, letter).text())
                    sheet.add(Coord(coord.string()).addColumn(letter).addRow(number),o, self.object2style(o))
                except:#Not a QTableWidgetItem or NOne
                    pass
        logging.debug("Items done")
        self.save()

    def itemtext2object(self, t):
        """
            Convierte t en un Money, Percentage o lo deja como text
        """
        if t[-2:]==" %":
            try:
                number=Decimal(t.replace(" %", ""))
                return Percentage(number, 100)
            except:
                logging.info("Error converting percentage")
                pass
        elif t[-2:] in (" €"," $"):
           try:
                number=Decimal(t.replace(t[-2:], "").replace(".", "").replace(",", "."))
                return Currency(number, self.mem.currencies.find_by_symbol(t[-1:]).id)
           except:
                logging.info("Error converting Money")
        elif t.find(":")!=-1 and t.find("-")!=-1:
            try:
                return datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
            except:
                logging.info("Error convertir datetime {}".format(t))
        elif t.find("-")!=-1:
            try:
                return datetime.strptime(t, "%Y-%m-%d").date()
            except:
                logging.info("Error convertir date {}".format(t))
        elif t.find(".")!=-1:
            try:
                return Decimal(t)
            except:
                logging.info("Error convertir Decimal {}".format(t))
        else:
            try:
                return int(t)
            except:
                logging.info("Error convertir Integer {}".format(t))
        return t


    def object2style(self, o):
        """
            Define el style de un objeto
        """
        if o.__class__==Currency:
            return "WhiteEuro"
        elif o.__class__==Percentage:
            return "WhitePercentage"
        elif o.__class__==datetime:
            return "WhiteDatetime"
        elif o.__class__==date:
            return "WhiteDate"
        elif o.__class__==Decimal:
            return "WhiteDecimal6"
        elif o.__class__==int:
            return "WhiteInteger"
        else:
            return "WhiteLeft"

def qbool(bool):
    """Prints bool and check. Is read only and enabled"""
    if bool==None:
        return qempty()
    a=QTableWidgetItem()
    a.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )#Set no editable
    if bool:
        a.setCheckState(Qt.Checked);
        a.setText(QApplication.translate("Core","True"))
    else:
        a.setCheckState(Qt.Unchecked);
        a.setText(QApplication.translate("Core","False"))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a

## Center checkbox
## You must use with table.setCellWidget(0,0,wdgBool)
## Is disabled to be readonly
def wdgBool(bool):
    pWidget = QWidget()
    pCheckBox = QCheckBox();
    if bool:
        pCheckBox.setCheckState(Qt.Checked);
    else:
        pCheckBox.setCheckState(Qt.Unchecked);
    pLayout = QHBoxLayout(pWidget);
    pLayout.addWidget(pCheckBox);
    pLayout.setAlignment(Qt.AlignCenter);
    pLayout.setContentsMargins(0,0,0,0);
    pWidget.setLayout(pLayout);
    pCheckBox.setEnabled(False)
    return pWidget

## Returns a QTableWidgetItem representing an empty value
def qempty():
    a=QTableWidgetItem("---")
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a

def qcenter(string):
    if string==None:
        return qempty()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a

def qleft(string):
    if string==None:
        return qempty()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
    return a

def qright(string):
    if string==None:
        return qempty()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a
    
## Creates a QTableWidgetItem with the date
def qdate(date):
    if date==None:
        return qempty()
    return qcenter(str(date))
    
    
## dt es un datetime con timezone, que se mostrara con la zone pasado como parametro
## Convierte un datetime a string, teniendo en cuenta los microsehgundos, para ello se convierte a datetime local
def qdatetime(dt, tz_name):
    newdt=dtaware_changes_tz(dt, tz_name)
    if newdt==None:
        return qempty()
    a=QTableWidgetItem(dtaware2string(newdt, "%Y-%m-%d %H:%M:%S"))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a


def qnumber(n, digits=2):
    if n==None:
        return qempty()
    n=round(n, digits)
    a=qright(n)
    if n<0:
        a.setForeground(QColor(255, 0, 0))
    return a

## Colorizes a number comparing it with a limit
def qnumber_limited(n, limit, digits=2, reverse=False):
    if n==None:
        return qempty()
    a=qnumber(n, 2)
    if reverse==True:
        color_above=QColor(148, 255, 148)
        color_under=QColor(255, 148, 148)
    else:        
        color_under=QColor(148, 255, 148)
        color_above=QColor(255, 148, 148)
    if n>=limit:
        a.setBackground(color_above)
    else:
        a.setBackground(color_under)
    return a

## Shows the time of a datetime
## See function time2string of datetime_functions to see formats
## @param ti must be a time object
def qtime(ti, format="HH:MM"):
    if ti==None:
        return qempty()
    item=qright(time2string(ti, format))
    if format=="Xulpymoney":
        if ti.microsecond==5:
            item.setBackground(QColor(255, 255, 148))
        elif ti.microsecond==4:
            item.setBackground(QColor(148, 148, 148))
    return item



if __name__ == '__main__':
    from libmanagers import ObjectManager_With_IdName
    from PyQt5.QtCore import QSettings
    from base64 import b64encode

    class Mem:
        def __init__(self):
            self.settings=QSettings()
            
    class Prueba:
        def __init__(self, id=None, name=None, date=None, datetime=None):
            self.id=id
            self.name=name
            self.date=date
            self.datetime=datetime
                
    class PruebaManager(ObjectManager_With_IdName):
        def __init__(self):
            ObjectManager_With_IdName.__init__(self)
            
    def on_customContextMenuRequested(pos):
        w.qmenu().exec_(w.mapToGlobal(pos))

    manager=PruebaManager()
    for i in range(100):
        manager.append(Prueba(i, b64encode(bytes(str(i).encode('UTF-8'))).decode('UTF-8'), date.today()-timedelta(days=i), datetime.now()+timedelta(seconds=3758*i)))
        
    selected=PruebaManager()
    selected.append(manager.arr[3])
    
    mem=Mem()
    app = QApplication([])

    w = wdgTable()
    w.table.settings(mem, "myqtablewidget", "tblExample")
    w.table.setDataFromManager(["Id", "Name", "Date", "Last update"], None, manager, ["id", "name", "date", "datetime"] )
    w.move(300, 300)
    w.resize(800, 400)
    w.setWindowTitle('myQTableWidget example')
    
    
    w.setContextMenuPolicy(Qt.CustomContextMenu)
    w.customContextMenuRequested.connect(on_customContextMenuRequested)
    w.show()
    
    app.exec()
