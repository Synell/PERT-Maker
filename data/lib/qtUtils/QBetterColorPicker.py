#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QBrush

from data.lib.qtUtils.QGridWidget import QGridWidget
from .QLineEditLeftLabel import QLineEditLeftLabel
from .QSpinBoxLeftLabel import QSpinBoxLeftLabel

from data.lib.utils import Color
#----------------------------------------------------------------------

    # Class
class QBetterColorPicker(QDialog):
    class __rightSide__(QGridWidget):
        def __init__(self, hasAlpha: bool = False) -> None:
            super().__init__()

            self.color = QGraphicsView()
            self.color.setProperty('class', 'color')
            self.color.setFixedWidth(75)
            self.color.setFixedHeight(26)

            self.colorScene = QGraphicsScene()
            self.color.setScene(self.colorScene)
            self.colorRect = self.colorScene.addRect(0, 0, 75, 26, QColor('black'), QBrush())
            self.color.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.color.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.color.keyPressEvent = None

            self.r = QSpinBoxLeftLabel('R')
            self.r.spinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.r.spinBox.setRange(0, 255)
            self.r.spinBox.setFixedWidth(75)

            self.g = QSpinBoxLeftLabel('G')
            self.g.spinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.g.spinBox.setRange(0, 255)
            self.g.spinBox.setFixedWidth(75)

            self.b = QSpinBoxLeftLabel('B')
            self.b.spinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.b.spinBox.setRange(0, 255)
            self.b.spinBox.setFixedWidth(75)

            if hasAlpha:
                self.a = QSpinBoxLeftLabel('A')
                self.a.spinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.a.spinBox.setRange(0, 255)
                self.a.spinBox.setFixedWidth(75)

            self.hex = QLineEditLeftLabel('#')
            self.hex.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hex.lineEdit.setFixedWidth(75)


            self.gridLayout.setHorizontalSpacing(20)
            self.gridLayout.setVerticalSpacing(5)
            self.gridLayout.setContentsMargins(10, 10, 10, 10)
            self.gridLayout.addWidget(self.color, 0, 2)
            self.gridLayout.setAlignment(self.color, Qt.AlignmentFlag.AlignRight)
            self.gridLayout.addWidget(self.r, 1, 2)
            self.gridLayout.setAlignment(self.r, Qt.AlignmentFlag.AlignRight)
            self.gridLayout.addWidget(self.g, 2, 2)
            self.gridLayout.setAlignment(self.g, Qt.AlignmentFlag.AlignRight)
            self.gridLayout.addWidget(self.b, 3, 2)
            self.gridLayout.setAlignment(self.b, Qt.AlignmentFlag.AlignRight)
            if hasAlpha:
                self.gridLayout.addWidget(self.a, 4, 2)
                self.gridLayout.setAlignment(self.a, Qt.AlignmentFlag.AlignRight)
            self.gridLayout.addWidget(self.hex, 5, 2)
            self.gridLayout.setAlignment(self.hex, Qt.AlignmentFlag.AlignRight)





    def __init__(self, parent = None, langData: dict = {}, color: Color = Color('#000000ff'), hasAlpha: bool = False):
        super().__init__(parent = parent)

        self.langData = langData
        self.color = color
        self.hasAlpha = hasAlpha

        #self.setWindowTitle(langData['title'])
        #self.setMinimumWidth(500)
        #self.setMinimumHeight(300)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.acceptVerification)
        self.buttonBox.rejected.connect(self.reject)


        self.__rightPanel__ = self.__rightSide__(hasAlpha)

        self.updateValues()

        self.__rightPanel__.r.spinBox.valueChanged.connect(self.editR)
        self.__rightPanel__.g.spinBox.valueChanged.connect(self.editG)
        self.__rightPanel__.b.spinBox.valueChanged.connect(self.editB)
        if hasAlpha: self.__rightPanel__.a.spinBox.valueChanged.connect(self.editA)
        self.__rightPanel__.hex.lineEdit.textChanged.connect(self.editHex)


        layout = QGridLayout(self)

        layout.addWidget(self.__rightPanel__, 0, 2)
        #layout.addWidget(self.buttonBox, 6, 0, 1, 3)


    def editR(self, event = None):
        self.color.red.value = self.__rightPanel__.r.spinBox.value()
        self.updateValues()

    def editG(self, event = None):
        self.color.green.value = self.__rightPanel__.g.spinBox.value()
        self.updateValues()

    def editB(self, event = None):
        self.color.blue.value = self.__rightPanel__.b.spinBox.value()
        self.updateValues()

    def editA(self, event = None):
        self.color.alpha.value = self.__rightPanel__.a.spinBox.value()
        self.updateValues()

    def editHex(self, event = None):
        try:
            self.color = Color('#' + self.__rightPanel__.hex.lineEdit.text())
            self.updateValues()
        except: pass


    def updateValues(self):
        self.__rightPanel__.r.spinBox.setValue(self.color.red.value)
        self.__rightPanel__.g.spinBox.setValue(self.color.green.value)
        self.__rightPanel__.b.spinBox.setValue(self.color.blue.value)
        if self.hasAlpha: self.__rightPanel__.a.spinBox.setValue(self.color.alpha.value)
        if self.hasAlpha: self.__rightPanel__.hex.lineEdit.setText(self.color.toHexa()[1:])
        else: self.__rightPanel__.hex.lineEdit.setText(self.color.toHex()[1:])

        self.__rightPanel__.colorRect.setBrush(self.color.toQColor())


    def acceptVerification(self, event = None):
        pass

        self.accept()


    def exec(self):
        accept = super().exec()
        if accept: return
#----------------------------------------------------------------------
