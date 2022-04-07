#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from PyQt6.QtWidgets import QGridLayout, QWidget, QDialog, QDialogButtonBox, QStyle, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from .QBaseApplication import QBaseApplication
#----------------------------------------------------------------------

    # Class
class QMessageBoxWithWidget(QDialog):
    class Icon(Enum):
        NoIcon = None
        Information = QStyle.StandardPixmap.SP_MessageBoxInformation
        Warning = QStyle.StandardPixmap.SP_MessageBoxWarning
        Critical = QStyle.StandardPixmap.SP_MessageBoxCritical
        About = QStyle.StandardPixmap.SP_MessageBoxQuestion

    def __init__(self, app: QBaseApplication = None, title: str = '', text: str = '', informativeText: str = '', icon: Icon|QIcon = Icon.NoIcon, widget: QWidget = None):
        super().__init__(parent = app.window)
        self.__layout__ = QGridLayout(self)

        self.__left__ = QWidget()
        self.__leftLayout__ = QGridLayout(self.__left__)

        self.__right__ = QWidget()
        self.__rightLayout__ = QGridLayout(self.__right__)
        self.__rightLayout__.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.msgBoxWidget = widget

        self.__layout__.addWidget(self.__left__, 0, 0)
        self.__layout__.addWidget(self.__right__, 0, 1)
        if self.msgBoxWidget:
            self.__layout__.addWidget(self.msgBoxWidget, 1, 0, 1, 2)

        if app:
            match icon:
                case QMessageBoxWithWidget.Icon.Warning: app.beep()
                case QMessageBoxWithWidget.Icon.Critical: app.beep()

        pixmap = QLabel()
        pixmap.setPixmap(self.__generatePixmap__(icon))
        self.__leftLayout__.addWidget(pixmap)
        self.__leftLayout__.setAlignment(pixmap, Qt.AlignmentFlag.AlignTop)
        self.__leftLayout__.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWindowTitle(title)

        text = QLabel(text)
        informativeText = QLabel(informativeText)

        self.__rightLayout__.addWidget(text, 0, 0)
        self.__rightLayout__.setAlignment(text, Qt.AlignmentFlag.AlignLeft)
        self.__rightLayout__.addWidget(informativeText, 1, 0)
        self.__rightLayout__.setAlignment(informativeText, Qt.AlignmentFlag.AlignLeft)


        QBtn = QDialogButtonBox.StandardButton.Ok

        self.__buttonBox__ = QDialogButtonBox(QBtn)
        self.__buttonBox__.accepted.connect(self.accept)
        self.__buttonBox__.rejected.connect(self.reject)

        self.__layout__.addWidget(self.__buttonBox__, 2, 1)


    def __generatePixmap__(self, icon: Icon|QIcon = Icon.NoIcon):
        if type(icon) is QMessageBoxWithWidget.Icon:
            style = self.style()
            iconSize = style.pixelMetric(QStyle.PixelMetric.PM_MessageBoxIconSize)
            icon = style.standardIcon(icon.value)
        elif type(icon) is not QIcon:
            return QPixmap()

        if not icon.isNull():
            return icon.pixmap(iconSize)
        return QPixmap()
#----------------------------------------------------------------------
