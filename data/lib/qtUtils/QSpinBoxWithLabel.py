#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QSpinBox, QGridLayout, QWidget, QLabel
#----------------------------------------------------------------------

    # Class
class QSpinBoxWithLabel(QWidget):
    def __init__(self, labelText: str = ''):
        super().__init__()
        self.__layout__ = QGridLayout(self)
        self.__layout__.setSpacing(1)

        self.__layout__.setColumnStretch(1, 1)
        self.__layout__.setRowStretch(2, 1)

        self.spinBox = QSpinBox()
        self.label = QLabel(labelText)
        self.label.setProperty('class', 'small')

        self.__layout__.addWidget(self.label, 0, 0)
        self.__layout__.addWidget(self.spinBox, 1, 0)
#----------------------------------------------------------------------
