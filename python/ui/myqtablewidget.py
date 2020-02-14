## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import Qt,  pyqtSlot, QObject
from PyQt5.QtGui import QKeySequence, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidget, QFileDialog,  QTableWidgetItem, QWidget, QCheckBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QAction, QMenu, QToolButton, QAbstractItemView
from .. datetime_functions import dtaware2string, dtaware_changes_tz, time2string
from officegenerator import ODS_Write, Currency, Percentage,  Coord
from logging import info, debug
from datetime import datetime, date,  timedelta
from decimal import Decimal
                
class myQTableWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        self.lay=QVBoxLayout()
        self.laySearch=QHBoxLayout()
        self.lbl=QLabel()
        self.table=QTableWidget()
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.verticalScrollBar().valueChanged.connect(self.on_table_verticalscrollbar_value_changed)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lbl.setText(self.tr("Add a string to filter rows"))
        self.txtSearch=QLineEdit()
        self.txtSearch.textChanged.connect(self.on_txt_textChanged)
        self.cmdCloseSearch=QToolButton()
        self.showSearchOptions(False)
        self.cmdCloseSearch.released.connect(self.on_cmdCloseSearch_released)
        self.laySearch.addWidget(self.lbl)
        self.laySearch.addWidget(self.txtSearch)
        self.laySearch.addWidget(self.cmdCloseSearch)
        self.lay.addWidget(self.table)
        self.lay.addLayout(self.laySearch)
        self.setLayout(self.lay)
        
        self.actionExport=QAction(self.tr("Export to Libreoffice Calc"))
        self.actionExport.setIcon(QIcon(":/reusingcode/libreoffice_calc.png"))
        self.actionExport.triggered.connect(self.on_actionExport_triggered)
        
        self.actionSizeMinimum=QAction(self.tr("Minimum column size"))
        self.actionSizeMinimum.triggered.connect(self.on_actionSizeMinimum_triggered)
        self.actionSizeNeeded=QAction(self.tr("Needed column size"))
        self.actionSizeNeeded.triggered.connect(self.on_actionSizeNeeded_triggered)
        
        self.actionSearch=QAction(self.tr("Search in table"))
        self.actionSearch.setIcon(QIcon(":/reusingcode/search.png"))
        self.actionSearch.triggered.connect(self.on_actionSearch_triggered)
        self.actionSearch.setShortcut(Qt.CTRL + Qt.Key_F)
        self.table.setAlternatingRowColors(True)
        self._last_height=None
        self._none_at_top=True
                
    def setVerticalHeaderHeight(self, height):
        """height, if null default.
        Must be after settings"""
        if height==None:
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._last_height=None
        else:
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.table.verticalHeader().setDefaultSectionSize(height) 
            self._last_height=height

    def sectionResized(self, logicalIndex, oldSize, newSize):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, newSize)
            self.settings.setValue("{}/{}_horizontalheader_state".format(self.settingsSection, self.settingsObject), self.table.horizontalHeader().saveState() )
            debug("Saved {}/{}_horizontalheader_state".format(self.settingsSection, self.settingsObject))
        elif modifiers == Qt.ControlModifier:
            self.on_actionSizeMinimum_triggered()
    
    @pyqtSlot(int)
    def on_table_verticalscrollbar_value_changed(self, value):
        if value % 8 ==1:
            self.on_actionSizeNeeded_triggered()
        
        
    def settings(self, settings, settingsSection,  objectname):
        self.settings=settings
        #For all myQTableWidget in settings app
        self.setVerticalHeaderHeight(int(self.settings.value("myQTableWidget/rowheight", 24)))
        self.settingsSection=settingsSection
        self.settingsObject=objectname
        self.setObjectName(self.settingsObject)


    def clear(self):
        """Clear table"""
        self.table.setRowCount(0)
        self.table.clearContents()

    
    ## Resizes columns if column width is less than table hint
    #def verticalScrollbarAction(self,  action):
    def wheelEvent(self, event):
        self.on_actionSizeNeeded_triggered()
        event.accept()

    @pyqtSlot()
    def keyPressEvent(self, event):
        if  event.matches(QKeySequence.ZoomIn) and self._last_height!=None:
            height=int(self.settings.value("myQTableWidget/rowheight", 24))
            self.settings.setValue("myQTableWidget/rowheight", height+1)
            info("Setting myQTableWidget/rowheight set to {}".format(self.settings.value("myQTableWidget/rowheight", 24)))
            self.table.setVerticalHeaderHeight(int(self.settings.value("myQTableWidget/rowheight", 24)))
        elif  event.matches(QKeySequence.ZoomOut) and self._last_height!=None:
            height=int(self.settings.value("myQTableWidget/rowheight", 24))
            self.settings.setValue("myQTableWidget/rowheight", height-1)
            ("Setting myQTableWidget/rowheight set to {}".format(self.settings.value("myQTableWidget/rowheight", 24)))
            self.table.setVerticalHeaderHeight(int(self.settings.value("myQTableWidget/rowheight", 24)))
        elif event.matches(QKeySequence.Print):
            filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), "table.ods", self.tr("Libreoffice calc (*.ods)"))[0]
            if filename:
                Table2ODS(self.mem,filename, self, "My table")


    ## Order data columns. None values are set at the beginning
    def on_orderby_action_triggered(self, action):
        action=QObject.sender(self)#Busca el objeto que ha hecho la signal en el slot en el que está conectado
        action_index=self.data_header_horizontal.index(action.text().replace(" (desc)",""))#Search the position in the headers of the action Text

        # Sets if its reverse or not and renames action
        if action.text().find(self.tr(" (desc)"))>0:
             reverse=True
             action.setText(action.text().replace(self.tr(" (desc)"),""))
        else: #No encontrado
             reverse=False
             action.setText(action.text() + " (desc)")

        nonull=[]
        null=[]
        for row in self.data:
            if row[action_index] is None:
                null.append(row)
            else:
                nonull.append(row)
        nonull=sorted(nonull, key=lambda c: c[action_index],  reverse=reverse)
        if self._none_at_top==True:#Set None at top of the list
            self.data=null+nonull
        else:
            self.data=nonull+null
        self.setData(self.data_header_horizontal, self.data_header_vertical, self.data)


    def applySettings(self):
        """settings must be defined before"""
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().sectionResized.connect(self.sectionResized)
        state=self.settings.value("{}/{}_horizontalheader_state".format(self.settingsSection, self.settingsObject))
        if state:
            self.table.horizontalHeader().restoreState(state)
        
    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    ## @param decimals int or list with the columns decimals
    def setData(self, header_horizontal, header_vertical, data, decimals=2, zonename='UTC'):
        if decimals.__class__.__name__=="int":
            decimals=[decimals]*len(header_horizontal)
        # Creates order actions here after creating data
        if hasattr(self,"actionListOrderBy")==False:
            self.actionListOrderBy=[]
            for header in header_horizontal:
                action=QAction("{}".format(header))
                self.actionListOrderBy.append(action)
                action.triggered.connect(self.on_orderby_action_triggered)

        # Headers
        self.data_header_horizontal=header_horizontal
        self.data_header_vertical=header_vertical
        self.data=data
        self.table.setColumnCount(len(self.data_header_horizontal))
        for i in range(len(self.data_header_horizontal)):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.data_header_horizontal[i]))
        # Data
        self.applySettings()
        self.table.clearContents()
        self.table.setRowCount(len(self.data))        
        for row in range(len(self.data)):
            for column in range(len(self.data_header_horizontal)):
                self.table.setItem(row, column, self.object2qtablewidgetitem(self.data[row][column], decimals[column], zonename))

    ## If true None values are set at the top of the list after sorting. If not at the bottom of the list
    def setNoneAtTop(self,boolean):
        self._none_at_top=boolean

    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    ## @param manager Manager object from libmanagers
    ## @param manager_attributes List of Strings with name of the object attributes, order by appareance
    def setDataFromManager(self, header_horizontal, header_vertical, manager, manager_attributes, decimals=2, zonename='UTC'):
        self.manager_attributes=manager_attributes
        self.manager=manager
        data=[]
        for o in manager.arr:
            row=[]
            for attribute in self.manager_attributes:
                row.append(self._attribute_to_command(o,attribute))
            data.append(row)
        self.setData(header_horizontal, header_vertical, data, decimals, zonename)


    ## @param attribute str or list
    ## Class Person, has self.name, self.age(), self.age_years_ago(year) self.son (another Person object)
    ## manager_attributes of setDataFromManager must be called in a PersonManager
    ## - ["name", ["age",[]], ["age_years_ago", [year]], ["son.age",[]]
    def _attribute_to_command(self, o, attribute):
        ## Returns an object 
        def str_attribute_with_points(o, attribute):
            for s in attribute.split("."):
                o=getattr(o, s)
            return o
        # --------------------------------------
        if attribute.__class__.__name__=="str":
            return str_attribute_with_points(o,attribute)
        else:#List
            function=str_attribute_with_points(o, attribute[0])
            parameters=attribute[1]
            return function(*parameters)

                    
    ## Converts a objecct class to a qtablewidgetitem
    def object2qtablewidgetitem(self, o, decimals=2, zonename="UTC"):
        if o.__class__.__name__ in ["int"]:
            return qright(o)
        elif o.__class__.__name__ in ["datetime"]:
            return qdatetime(o,zonename)
        elif o.__class__.__name__ in ["float","Decimal"]:
            return qnumber(o,decimals)
        elif o.__class__.__name__ in ["Percentage","Money","Currency"]:
            return o.qtablewidgetitem(decimals)
        elif o.__class__.__name__ in ["bool", ]:
            return qbool(o)
        else:
            return qleft(o)

    ## Returns a list of strings with the horizontal headers
    def listHorizontalHeaders(self):
        header=[]
        for i in range(self.table.horizontalHeader().count()):
            header.append(self.table.horizontalHeaderItem(i).text())
        return header

    ## Returns a list of strings with the horizontal headers
    def listVerticalHeaders(self):
        header=[]
        for i in range(self.table.verticalHeader().count()):
            header.append(self.table.verticalHeaderItem(i).text())
        return header

    ## Returns a lisf of rows with the text of the 
    def listText(self):
        data=[]
        for i in range(self.table.rowCount()):
            row=[]
            for column in range(self.table.columnCount()):
                data.append(self.table.item(row,column).text())
        return data

    ## @param rsActionExport String ":/xulpymoney/save.png" for example
    def setIcons(self, rsActionExport=None):
        if rsActionExport is not None:
            self.actionExport.setIcon(QIcon(rsActionExport))
            
    def on_cmdCloseSearch_released(self):
        self.txtSearch.setText("")
        self.showSearchOptions(False)
        
    def showSearchOptions(self, boolean):
        if boolean==True:
            self.lbl.show()
            self.txtSearch.show()
            self.cmdCloseSearch.show()
        else:
            self.lbl.hide()
            self.txtSearch.hide()
            self.cmdCloseSearch.hide()
            
    def showSearchCloseButton(self, boolean):
        if boolean==True:
            self.cmdCloseSearch.show()
        else:
            self.cmdCloseSearch.hide()

    def on_actionExport_triggered(self):
        filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), "table.ods", self.tr("Libreoffice calc (*.ods)"))[0]
        if filename:
            Table2ODS(filename, self, "My table")

    def on_actionSizeMinimum_triggered(self):
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.settings.setValue("{}/{}_horizontalheader_state".format(self.settingsSection, self.settingsObject), self.table.horizontalHeader().saveState() )
        debug("Saved {}/{}_horizontalheader_state".format(self.settingsSection, self.settingsObject))

    def on_actionSizeNeeded_triggered(self):
        for i in range(self.table.columnCount()):
            if self.table.sizeHintForColumn(i)>self.table.columnWidth(i):
                self.table.setColumnWidth(i, self.table.sizeHintForColumn(i))
        self.settings.setValue("{}/{}_horizontalheader_state".format(self.settingsSection, self.settingsObject), self.table.horizontalHeader().saveState() )
        debug("Saved {}/{}_horizontalheader_state".format(self.settingsSection, self.settingsObject))

    def on_actionSearch_triggered(self):
        self.lbl.show()
        self.txtSearch.show()
        self.cmdCloseSearch.show()
        self.txtSearch.setFocus()

    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Table options"):
        menu=QMenu(self.parent)
        menu.setTitle(self.tr(title))
        menu.addAction(self.actionExport)
        menu.addSeparator()
        menu.addAction(self.actionSearch)
        menu.addSeparator()
        order=QMenu(menu)
        order.setTitle(self.tr("Order by"))
        for action in self.actionListOrderBy:
            order.addAction(action)
        menu.addMenu(order)
        size=QMenu(menu)
        size.setTitle(self.tr("Columns size"))
        size.addAction(self.actionSizeMinimum)
        size.addAction(self.actionSizeNeeded)
        menu.addMenu(size)
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
    def __init__(self, filename, table, title):
        ODS_Write.__init__(self, filename)
        sheet=self.createSheet(title)
        #Array width
        widths=[]
        if not table.table.verticalHeader().isHidden():
            widths.append(table.table.verticalHeader().width()*0.90)
        for i in range(table.table.columnCount()):
            widths.append(table.table.columnWidth(i)*0.90)
        sheet.setColumnsWidth(widths)

        #firstcontentletter and firstcontentnumber
        if table.table.horizontalHeader().isHidden() and not table.table.verticalHeader().isHidden():
            coord=Coord("B1")
        elif not table.table.horizontalHeader().isHidden() and table.table.verticalHeader().isHidden():
            print("A2")
            coord=Coord("A2")
            topleft=Coord("A2") if table.table.rowCount()<21 else Coord("A2").addRow(table.table.rowCount()-1-20)
            sheet.freezeAndSelect(coord, Coord("A2").addRow(table.table.rowCount()-1), topleft)
        elif not table.table.horizontalHeader().isHidden() and not table.table.verticalHeader().isHidden():
            coord=Coord("B2")
        elif table.table.horizontalHeader().isHidden() and table.table.verticalHeader().isHidden():
            coord=Coord("A1")

        #HH
        if not table.table.horizontalHeader().isHidden():
            for letter in range(table.table.columnCount()):
                sheet.add(Coord(coord.letter + "1").addColumn(letter), table.table.horizontalHeaderItem(letter).text(), "OrangeCenter")
        #VH
        if not table.table.verticalHeader().isHidden():
            for number in range(table.table.rowCount()):
                try:#Caputuro cuando se numera sin items 1, 2, 3
                    sheet.add(Coord("A" + coord.number).addRow(number), table.table.verticalHeaderItem(number).text(), "YellowLeft")
                except:
                    pass
        #Items
        for number, row in enumerate(table.data):
            for letter, column in enumerate(row):
                try:
                    sheet.add(Coord(coord.string()).addColumn(letter).addRow(number), column, self.object2style(column))
                except:#None
                    pass
        self.save()

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
    
## Currency object from reusingcode
def qcurrency(currency, decimals=2):
    a=QTableWidgetItem(currency.string(decimals))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    if currency.amount==None:
        a.setForeground(QColor(0, 0, 255))
    elif currency.amount<0:
        a.setForeground(QColor(255, 0, 0))
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
            self.name="namemem"
        def age(self, integer):
            return integer
            
    class Prueba:
        def __init__(self, id=None, name=None, date=None, datetime=None):
            self.id=id
            self.name=name
            self.date=date
            self.datetime=datetime
            self.pruebita=Mem()
                
    class PruebaManager(ObjectManager_With_IdName):
        def __init__(self):
            ObjectManager_With_IdName.__init__(self)
            
    def on_customContextMenuRequested(pos):
        w.qmenu().exec_(w.mapToGlobal(pos))

    manager=PruebaManager()
    for i in range(100):
        manager.append(Prueba(i, b64encode(bytes(str(i).encode('UTF-8'))).decode('UTF-8'), date.today()-timedelta(days=i), datetime.now()+timedelta(seconds=3758*i)))
    manager.append(Prueba(None,"Con None",date.today(),datetime.now()))
        
    selected=PruebaManager()
    selected.append(manager.arr[3])
    
    mem=Mem()
    app = QApplication([])

    w = myQTableWidget()
    w.settings(mem.settings, "myqtablewidget", "tblExample")
    w.setDataFromManager(["Id", "Name", "Date", "Last update","Mem.name", "Mmem.age (i)"], None, manager, ["id", "name", "date", "datetime","pruebita.name", ["pruebita.age", [22,]], ] )
    w.move(300, 300)
    w.resize(800, 400)
    w.setWindowTitle('myQTableWidget example')
    
    
    w.setContextMenuPolicy(Qt.CustomContextMenu)
    w.table.customContextMenuRequested.connect(on_customContextMenuRequested)
    w.show()
    
    app.exec()
