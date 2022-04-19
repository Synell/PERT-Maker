#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton, QColorDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QColor, QImage
#----------------------------------------------------------------------

    # Class
class QColorButton(QPushButton):
    def __init__(self, buttonText: str = '', colorPickerLangData: dict = {}, color: QColor = QColor('#ffffff')):
        super().__init__()
        self.__color__ = color
        self.setText(buttonText)
        self.updateColor()
        self.clicked.connect(self.clickEvent)

    @property
    def color(self):
        return self.__color__

    @color.setter
    def color(self, color):
        if type(color) is QColor:
            self.__color__ = color
            self.updateColor()

    def updateColor(self):
        pxmp = QPixmap.fromImage(QImage(64, 64, QImage.Format.Format_Mono))
        pxmp.fill(self.color)
        self.setIcon(QIcon(pxmp))

    def clickEvent(self, checked: bool = None) -> None:
        '''self.color = QColorDialog().getColor(self.color, self.parent())
        if self.color:
            self.updateColor()'''

        colorDialog = QColorDialog(self.color, self.parent())
        if colorDialog.exec():
            self.color = colorDialog.currentColor()
            self.updateColor()
#----------------------------------------------------------------------
