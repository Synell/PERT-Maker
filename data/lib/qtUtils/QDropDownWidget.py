#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton, QGridLayout, QWidget
from PyQt6.QtCore import Qt
#----------------------------------------------------------------------

    # Class
class QDropDownWidget(QWidget):
    def __init__(self, text: str = '', widget: QWidget = None):
        super().__init__()
        self.__layout__ = QGridLayout(self)
        self.__layout__.setSpacing(1)

        self.__layout__.setColumnStretch(1, 1)
        self.__layout__.setRowStretch(2, 1)

        self.__showHideButton__ = QPushButton(text)
        self.__showHideButton__.setCheckable(True)
        self.__showHideButton__.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.__showHideButton__.setProperty('class', 'QDropDownWidget')
        self.__showHideButton__.clicked.connect(self.__showHideButtonClicked__)

        self.showHideWidget = widget

        self.__layout__.addWidget(self.__showHideButton__, 0, 0)
        self.__layout__.setAlignment(self.__showHideButton__, Qt.AlignmentFlag.AlignRight)
        self.__layout__.addWidget(self.showHideWidget , 1, 0)

        self.showHideWidget.hide()

    def __showHideButtonClicked__(self, event = None):
        if self.__showHideButton__.isChecked(): self.showHideWidget.show()
        else: self.showHideWidget.hide()
#----------------------------------------------------------------------
