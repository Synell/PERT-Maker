#----------------------------------------------------------------------

    # Libraries
import cv2
import numpy as np
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QScrollArea, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QImage, QPixmap, QColor, QPainter, QPen
from data.lib.qtUtils import QFilePicker, QComboBoxWithLabel, QColorButton
from data.lib.utils import Color
#----------------------------------------------------------------------

    # Class
class QExportImageDialog(QDialog):
    def __init__(self, parent = None, langData: dict = {}, selectedBgMode: int = 0, bgColor: Color = Color('#000000'), image: QImage = None, progressBar: QProgressBar = None):
        super().__init__(parent = parent)

        self.langData = langData
        self.image = image
        self.newImage = None
        self.progressBar = progressBar

        self.setWindowTitle(langData['title'])
        self.setFixedWidth(700)
        self.setFixedHeight(500)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.acceptVerification)
        self.buttonBox.rejected.connect(self.reject)

        self.combobox = QComboBoxWithLabel(langData['QComboBoxWithLabel']['QLabel']['bgMode'])
        self.combobox.comboBox.addItems([
            langData['QComboBoxWithLabel']['QComboBox']['default'],
            langData['QComboBoxWithLabel']['QComboBox']['color'],
            langData['QComboBoxWithLabel']['QComboBox']['transparent']
        ])
        self.combobox.comboBox.setCurrentIndex(selectedBgMode)
        self.combobox.comboBox.currentIndexChanged.connect(self.indexChanged)

        self.colorButton = QColorButton(langData['QColorButton']['bg'])
        self.colorButton.color = bgColor.toQColor()
        self.oldColor = QColor(self.colorButton.color.rgba())
        self.colorButton.clicked.connect(self.clickEvent)

        self.label = QLabel()
        self.label.setStyleSheet('background-color: black;')
        self.preview = QScrollArea()
        self.label.setPixmap(QPixmap().fromImage(self.image))
        self.preview.setWidget(self.label)

        self.indexChanged()

        self.filename = QFilePicker(
            langData['QFilePicker'],
            QFilePicker.Type.SaveFileName,
            './image.png',
            QFilePicker.Extension.combine(
                QFilePicker.Extension.Image.PNG,
                QFilePicker.Extension.Image.JPEG,
                QFilePicker.Extension.Image.TIFF,
                QFilePicker.Extension.Image.BMP
            ),
            False
        )


        layout = QGridLayout(self)
        layout.addWidget(self.combobox, 0, 0)
        layout.addWidget(self.colorButton, 0, 1)
        layout.addWidget(self.preview, 1, 0, 1, 2)
        layout.addWidget(self.filename, 2, 0)
        layout.addWidget(self.buttonBox, 2, 1)


    def clickEvent(self, event = None):
        if self.oldColor.rgba() != self.colorButton.color.rgba():
            self.newImage = self.applyColor()
            self.label.setPixmap(QPixmap().fromImage(self.newImage))
        self.oldColor = self.colorButton.color


    def indexChanged(self, event = None):
        match self.combobox.comboBox.currentIndex():
            case 0:
                self.colorButton.setDisabled(True)
                self.label.setPixmap(QPixmap().fromImage(self.image))
            case 1:
                self.colorButton.setDisabled(False)
                self.newImage = self.applyColor()
                self.label.setPixmap(QPixmap().fromImage(self.newImage))

            case 2:
                self.colorButton.setDisabled(True)
                self.newImage = self.applyTransparency()
                self.label.setPixmap(QPixmap().fromImage(self.newImage))


    def applyColor(self):
        image = self.image.copy()

        w, h = image.width(), image.height()
        s = image.bits().asstring(w * h * 4)

        def getPixel(x, y):
            i = (x + (y * w)) * 4
            return s[i:i+3]

        target_color = getPixel(0, 0)

        p = QPainter(image)
        p.setPen(QPen(self.colorButton.color))

        queue = list((x, y) for x in range(image.width()) for y in range(image.height()))

        if self.progressBar:
            length = len(queue)
            self.progressBar.setHidden(False)
            self.progressBar.setRange(0, length)
            self.progressBar.setValue(0)

        while queue:
            x, y = queue.pop()
            if getPixel(x, y) == target_color:
                p.drawPoint(QPoint(x, y))
            elif self.progressBar:
                self.progressBar.setValue(length - len(queue))

        if self.progressBar: self.progressBar.setHidden(True)

        return image

    def applyTransparency(self):
        image = self.image.copy()

        w, h = image.width(), image.height()
        s = image.bits().asstring(w * h * 4)

        def getPixel(x, y):
            i = (x + (y * w)) * 4
            return s[i:i+3]

        targetColor = getPixel(0, 0)

        p = QPainter(image)
        p.setPen(QPen(QColor(0, 0, 0, 0)))
        p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)

        queue = list((x, y) for x in range(image.width()) for y in range(image.height()))

        if self.progressBar:
            length = len(queue)
            self.progressBar.setHidden(False)
            self.progressBar.setRange(0, length)
            self.progressBar.setValue(0)

        while queue:
            x, y = queue.pop()
            if getPixel(x, y) == targetColor:
                p.eraseRect(x, y, 1, 1)
            elif self.progressBar:
                self.progressBar.setValue(length - len(queue))

        if self.progressBar: self.progressBar.setHidden(True)

        return image


    def acceptVerification(self, event = None):
        match self.combobox.comboBox.currentIndex():
            case 0:
                self.image.save(self.filename.path(), self.filename.path().split('.')[-1])
            case 1:
                self.newImage.save(self.filename.path(), self.filename.path().split('.')[-1])
            case 2:
                self.newImage.save(self.filename.path(), self.filename.path().split('.')[-1])

        self.accept()


    def exec(self):
        accept = super().exec()
        if accept: return self.combobox.comboBox.currentIndex(), Color(self.colorButton.color.red(), self.colorButton.color.green(), self.colorButton.color.blue(), self.colorButton.color.alpha())
#----------------------------------------------------------------------
