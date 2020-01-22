from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSpinBox, QSizePolicy

class wdgDistributeAmountInteger(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent=parent

        self.lbl=QLabel(self)
        self.lbl.setText(self.tr("Distribute amount"))
        self.setup_qspinboxes()

        self.lay = QHBoxLayout(self)
        self.lay.addWidget(self.lbl)
        self.lay.addWidget(self.spnA)
        self.lay.addWidget(self.spnB)
        self.lay.addWidget(self.spnC)
        self.setLayout(self.lay)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        self.lbl.setSizePolicy(sizePolicy)
        
        for spn in [self.spnA, self.spnB, self.spnC]:
            spn.setAlignment(Qt.AlignRight)

    def setup_qspinboxes(self):
        self.spnA=QSpinBox(self)
        self.spnB=QSpinBox(self)
        self.spnC=QSpinBox(self)

    def setAmount(self, a):
        a_3=int(a/3)
        self.spnA.setValue(a_3)
        self.spnB.setValue(a_3)
        self.spnC.setValue(a-2*a_3)

    def setMaximum(self, suffix):
        self.spnA.setMaximum(suffix)
        self.spnB.setMaximum(suffix)
        self.spnC.setMaximum(suffix)

    def setSuffix(self, suffix):
        self.spnA.setSuffix(suffix)
        self.spnB.setSuffix(suffix)
        self.spnC.setSuffix(suffix)

if __name__ == '__main__':
    from sys import exit
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    w = wdgDistributeAmountInteger()
    w.move(300, 300)
    w.setSuffix(" %")
    w.setMaximum(100)
    w.setAmount(100)
    w.setWindowTitle('Simple')
    w.show()

    exit(app.exec_())
    