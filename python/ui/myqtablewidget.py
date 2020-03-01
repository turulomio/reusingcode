## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import Qt,  pyqtSlot, QObject,  pyqtSignal
from PyQt5.QtGui import QKeySequence, QColor, QIcon, QBrush
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidget, QFileDialog,  QTableWidgetItem, QWidget, QCheckBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QAction, QMenu, QToolButton, QAbstractItemView
from .. datetime_functions import dtaware2string, dtaware_changes_tz, time2string
from .. libmanagers import ManagerSelectionMode
from officegenerator import ODS_Write
from logging import info, debug
from datetime import datetime, date,  timedelta
                
class myQTableWidget(QWidget):
    setDataFinished=pyqtSignal()
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
        self.table.verticalScrollBar().valueChanged.connect(self.on_table_verticalscrollbar_value_changed)
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
        if value % 3 ==1:
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
    
    ## Resizes columns if column width is less than table hin
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
                ods=ODS_Write(filename)
                self.officegeneratorModel( "My table").ods_sheet(ods)
                ods.save()

    ## Affeter selection an action of the OrderByAction list, returns its information, to be used in several classes
    def _get_triggered_action_information(self):
        action=QObject.sender(self)#Busca el objeto que ha hecho la signal en el slot en el que está conectado
        action_index=self.hh.index(action.text().replace(" (desc)",""))#Search the position in the headers of the action Text

        # Sets if its reverse or not and renames action
        if action.text().find(self.tr(" (desc)"))>0:
             reverse=True
             action.setText(action.text().replace(self.tr(" (desc)"),""))
        else: #No encontrado
             reverse=False
             action.setText(action.text() + " (desc)")
             
        # Remover others (desc), to the rest of actions
        for i, other_action in enumerate(self.actionListOrderBy):
            if i!=action_index:# Different to selected action index
                other_action.setText(other_action.text().replace(self.tr(" (desc)"),""))
                
        self.on_orderby_action_triggered(action,  action_index, reverse)

    ## Order data columns. None values are set at the beginning
    def on_orderby_action_triggered(self, action, action_index, reverse):
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
        self.setData(self.hh, self.hv, self.data)


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
        self.data_decimals=decimals
        self.data_zonename=zonename
        # Creates order actions here after creating data
        if hasattr(self,"actionListOrderBy")==False:
            self.actionListOrderBy=[]
            for header in header_horizontal:
                action=QAction("{}".format(header))
                self.actionListOrderBy.append(action)
                action.triggered.connect(self._get_triggered_action_information)

        # Headers
        self.hh=header_horizontal
        self.hv=header_vertical
        self.data=data
        self.table.setColumnCount(len(self.hh))
        if self.hh is not None:
            for i in range(len(self.hh)):
                self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.hh[i]))
        if self.hv is not None:
            self.table.verticalHeader().show()
            self.table.setRowCount(len(self.data))# To do not lose data
            for i in range(len(self.hv)):
                self.table.setVerticalHeaderItem(i, QTableWidgetItem(self.hv[i]))

        # Data
        self.applySettings()
        self.table.clearContents()
        self.table.setRowCount(len(self.data))        
        for row in range(len(self.data)):
            for column in range(len(self.hh)):
                wdg=self.object2qtablewidgetitem(self.data[row][column], decimals[column], zonename)
                if wdg.__class__.__name__=="QWidget":#wdgBool
                    self.table.setCellWidget(row, column, wdg)
                else:#qtablewidgetitem
                    self.table.setItem(row, column, wdg)
        self.setDataFinished.emit()

    def print(self, hh, hv, data):
        print(hh)
        for i, row in enumerate(data):
            print (hv[i] , row)
            
        print ("Len hh:", len(hh))
        print ("Len hv:", len(hv))
        print ("Len data:", len(data[0]), "x", len(data))
            
    ## If true None values are set at the top of the list after sorting. If not at the bottom of the list
    def setNoneAtTop(self,boolean):
        self._none_at_top=boolean

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
            return wdgBool(o)
        elif o is None:
            return qnone()
        elif o=="":
            return qempty()
        elif o=="#crossedout":
            return qcrossedout()
        else:            
            return qleft(o)

    ## Returns a list of strings with the horizontal headers
    def listHorizontalHeaders(self):
        if self.hh is None:
            return None
        header=[]
        for i in range(self.table.horizontalHeader().count()):
            header.append(self.table.horizontalHeaderItem(i).text())
        return header

    ## Returns a list of strings with the horizontal headers
    def listVerticalHeaders(self):
        if self.hv is None:
            return None
        header=[]
        for i in range(self.table.verticalHeader().count()):
            if self.table.verticalHeaderItem(i) is not None:
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
            ods=ODS_Write(filename)
            self.officegeneratorModel("My table").ods_sheet(ods)
            ods.save()

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

    def officegeneratorModel(self, title="sheet"):
        def pixel2cm(pixels):
            #Converts size in pixels to cm
            PixelWidthDimension = self.logicalDpiX()# width dots per inch
            inch = pixels/PixelWidthDimension
            cm= inch*2.54*(1+0.05)
            return cm
        # # # # # # # # # #
        widths=[]
        vwidth=pixel2cm(self.table.verticalHeader().width())
        for i in range(self.table.columnCount()):
            widths.append(pixel2cm(self.table.columnWidth(i)))

        from officegenerator.standard_sheets import Model
        m=Model()
        m.setTitle(title)
        m.setHorizontalHeaders(self.listHorizontalHeaders(), widths)
        m.setVerticalHeaders(self.listVerticalHeaders(),vwidth)
        m.setData(self.data)
        return m
## Acronim of myQTableWidget
## Used for readibility improvement
class mqtw(myQTableWidget):
    def __init__(self, parent):
        myQTableWidget.__init__(self, parent)
        
class mqtwManager(myQTableWidget):
    def __init__(self, parent):
        myQTableWidget.__init__(self, parent)
        self._manager_selection_mode=ManagerSelectionMode.Object
        self.table.itemSelectionChanged.connect(self.on_itemSelectionChanged)

    def on_itemSelectionChanged(self):
        self.manager.cleanSelection()
        for i in self.table.selectedItems():#itera por cada item no row.
            if i.column()==0:
                if self.manager.selectionMode()==ManagerSelectionMode.Object:
                    self.manager.selected=self.manager.object(i.row())
                elif self.manager.selectionMode()==ManagerSelectionMode.List:
                    self.manager.selected.append(self.manager.object(i.row()))
        debug("{} selection: {}".format(self.manager.__class__.__name__,  self.manager.selected))

    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    ## @param manager Manager object from libmanagers
    ## @param manager_attributes List of Strings with name of the object attributes, order by appareance
    ## @param additional Function without it's call, to add additional table information like Total Rows or icons
    def setDataFromManager(self, header_horizontal, header_vertical, manager, manager_attributes, decimals=2, zonename='UTC', additional=None):
        self.manager_attributes=manager_attributes
        self.manager=manager
        self.additional=additional

        #Sets manager selection mode and table
        self.manager.setSelectionMode(self._manager_selection_mode)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        if self._manager_selection_mode==ManagerSelectionMode.Object:
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            self.table.setSelectionMode(QAbstractItemView.MultiSelection)

        # Sets data
        data=[]
        for o in manager.arr:
            row=[]
            for attribute in self.manager_attributes:
                row.append(self.manager._string_or_tuple_to_command(o,attribute))
            data.append(row)
        self.setData(header_horizontal, header_vertical, data, decimals, zonename)

        self.additional(self)

    def setSelectionMode(self, manager_selection_mode):
        self._manager_selection_mode=manager_selection_mode

    ## Order data columns. None values are set at the beginning
    def on_orderby_action_triggered(self, action, action_index, reverse):
        self.manager.order_with_none(self.manager_attributes[action_index], reverse=reverse, none_at_top=self._none_at_top)
        self.setDataFromManager(self.hh, self.hv, self.manager, self.manager_attributes, self.data_decimals, self.data_zonename, additional=self.additional)

## @return qtablewidgetitem
def qbool(bool):
    """Prints bool and check. Is read only and enabled"""
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
## @return qwidget
def wdgBool(bool):
    pWidget = QWidget()
    pCheckBox = QCheckBox();
    pCheckBox.setAttribute(Qt.WA_TransparentForMouseEvents);
    pCheckBox.setFocusPolicy(Qt.NoFocus)
    if bool:
        pCheckBox.setCheckState(Qt.Checked);
    else:
        pCheckBox.setCheckState(Qt.Unchecked);
    pLayout = QHBoxLayout(pWidget);
    pLayout.addWidget(pCheckBox);
    pLayout.setAlignment(Qt.AlignCenter);
    pLayout.setContentsMargins(0,0,0,0);
    pWidget.setLayout(pLayout)
    return pWidget

## Returns a QTableWidgetItem representing an empty value
def qnone():
    return qcenter("- - -")

## Returns a QTableWidgetItem representing an empty value
def qempty():
    return qleft("")

def qcenter(string):
    if string==None:
        return qnone()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a
    
def qcrossedout():
    a=qempty()
    brush = QBrush(QColor(0, 0, 0))
    brush.setStyle(Qt.BDiagPattern)
    a.setBackground(brush)
    return a

## Currency object from reusingcode
def qcurrency(currency, decimals=2):
    if currency is None or currency.amount is None:
        return qnone()
    a=QTableWidgetItem(currency.string(decimals))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    if currency.amount==None:
        a.setForeground(QColor(0, 0, 255))
    elif currency.amount<0:
        a.setForeground(QColor(255, 0, 0))
    return a

def qleft(string):
    if string==None:
        return qnone()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
    return a

def qright(string):
    if string==None:
        return qnone()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a
    
## Creates a QTableWidgetItem with the date
def qdate(date):
    if date==None:
        return qnone()
    return qcenter(str(date))
    
    
## dt es un datetime con timezone, que se mostrara con la zone pasado como parametro
## Convierte un datetime a string, teniendo en cuenta los microsehgundos, para ello se convierte a datetime local
def qdatetime(dt, tz_name):
    newdt=dtaware_changes_tz(dt, tz_name)
    if newdt==None:
        return qnone()
    a=QTableWidgetItem(dtaware2string(newdt, "%Y-%m-%d %H:%M:%S"))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a


def qnumber(n, digits=2):
    if n==None:
        return qnone()
    n=round(n, digits)
    a=qright(n)
    if n<0:
        a.setForeground(QColor(255, 0, 0))
    return a

## Colorizes a number comparing it with a limit
def qnumber_limited(n, limit, digits=2, reverse=False):
    if n==None:
        return qnone()
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
        return qnone()
    item=qright(time2string(ti, format))
    if format=="Xulpymoney":
        if ti.microsecond==5:
            item.setBackground(QColor(255, 255, 148))
        elif ti.microsecond==4:
            item.setBackground(QColor(148, 148, 148))
    return item

def qpercentage(percentage, decimals=2):
    if percentage is None:
        return qnone()
    a=QTableWidgetItem(percentage.string(decimals))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    if percentage.value==None:
        a.setForeground(QColor(0, 0, 255))
    elif percentage.value<0:
        a.setForeground(QColor(255, 0, 0))
    return a
    

if __name__ == '__main__':
    from libmanagers import ObjectManager_With_IdName_Selectable
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

    class PruebaManager(ObjectManager_With_IdName_Selectable):
        def __init__(self):
            ObjectManager_With_IdName_Selectable.__init__(self)

        def prueba(self, wdg):
            print("ICONS", wdg)

    def on_mqtw_data_customContextMenuRequested(pos):
        mqtw_data.qmenu().exec_(mqtw_data.mapToGlobal(pos))
    def on_mqtw_manager_customContextMenuRequested(pos):
        mqtw_manager.qmenu().exec_(mqtw_manager.mapToGlobal(pos))

    manager_manager=PruebaManager()
    for i in range(100):
        manager_manager.append(Prueba(i, b64encode(bytes(str(i).encode('UTF-8'))).decode('UTF-8'), date.today()-timedelta(days=i), datetime.now()+timedelta(seconds=3758*i)))

    manager_data=PruebaManager()
    manager_data.append(Prueba(None,"Con None",date.today(),datetime.now()))
    manager_data.append(Prueba(None, "", None, None))
    manager_data.append(Prueba(None, None, None, None))
    manager_data.append(Prueba(None, "#crossedout", None, None))
    manager_data.append(Prueba(None, False, None, None))
    manager_data.append(Prueba(None, True, None, None))

    data=[]
    for o in manager_data.arr:
        data.append([o.id, o.name,  o.date,  o.datetime,  o.pruebita.name, o.pruebita.age(1)])

    mem=Mem()
    app = QApplication([])
    w=QWidget()
    hv=None

    #mqtw
    lay=QHBoxLayout(w)
    mqtw_data = mqtw(w)
    hv=["Johnny be good"]*len(data)
    mqtw_data.settings(mem.settings, "myqtablewidget", "tblExample")
    hh=["Id", "Name", "Date", "Last update","Mem.name", "Age"]
    mqtw_data.setData(hh, hv, data )

    mqtw_data.setContextMenuPolicy(Qt.CustomContextMenu)
    mqtw_data.table.customContextMenuRequested.connect(on_mqtw_data_customContextMenuRequested)

    #mqtwManager
    mqtw_manager = mqtwManager(w)    
    mqtw_manager.setSelectionMode(ManagerSelectionMode.List)
    mqtw_manager.settings(mem.settings, "myqtablewidget", "tblExample")
    hh=["Id", "Name", "Date", "Last update","Mem.name", "Age"]

    mqtw_manager.setDataFromManager(hh, None, manager_manager, ["id", "name", "date", "datetime", "pruebita.name", ("pruebita.age", [1, ])], additional=manager_manager.prueba)

    mqtw_manager.setContextMenuPolicy(Qt.CustomContextMenu)
    mqtw_manager.table.customContextMenuRequested.connect(on_mqtw_manager_customContextMenuRequested)

    lay.addWidget(mqtw_data)
    lay.addWidget(mqtw_manager)
    w.setWindowTitle('myQTableWidget example')
    w.move(300, 300)
    w.resize(1400, 600)
    w.show()

    app.exec()
