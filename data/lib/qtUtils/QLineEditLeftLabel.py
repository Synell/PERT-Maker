#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QLineEdit, QGridLayout, QWidget, QLabel
#----------------------------------------------------------------------

    # Class
class QLineEditLeftLabel(QWidget):
    def __init__(self, labelText: str = ''):
        super().__init__()
        self.__layout__ = QGridLayout(self)
        self.__layout__.setHorizontalSpacing(5)
        self.__layout__.setVerticalSpacing(0)
        self.__layout__.setContentsMargins(0, 0, 0, 0)

        self.__layout__.setColumnStretch(2, 1)
        self.__layout__.setRowStretch(1, 1)

        self.lineEdit = QLineEdit()
        self.label = QLabel(labelText)
        self.label.setProperty('class', 'bold')

        self.__layout__.addWidget(self.label, 0, 0)
        self.__layout__.addWidget(self.lineEdit, 0, 1)
#----------------------------------------------------------------------
