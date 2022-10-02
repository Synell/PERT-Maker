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

    def __init__(self, app: QBaseApplication = None, title: str = '', text: str = '', informative_text: str = '', icon: Icon|QIcon = Icon.NoIcon, widget: QWidget = None):
        super().__init__(parent = app.window)
        self._layout = QGridLayout(self)

        self._left = QWidget()
        self._left_layout = QGridLayout(self._left)

        self._right = QWidget()
        self._right_layout = QGridLayout(self._right)
        self._right_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.msg_box_widget = widget

        self._layout.addWidget(self._left, 0, 0)
        self._layout.addWidget(self._right, 0, 1)
        if self.msg_box_widget:
            self._layout.addWidget(self.msg_box_widget, 1, 0, 1, 2)

        if app:
            match icon:
                case QMessageBoxWithWidget.Icon.Warning: app.beep()
                case QMessageBoxWithWidget.Icon.Critical: app.beep()

        pixmap = QLabel()
        pixmap.setPixmap(self.__generatePixmap__(icon))
        self._left_layout.addWidget(pixmap)
        self._left_layout.setAlignment(pixmap, Qt.AlignmentFlag.AlignTop)
        self._left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWindowTitle(title)

        text = QLabel(text)
        informative_text = QLabel(informative_text)

        self._right_layout.addWidget(text, 0, 0)
        self._right_layout.setAlignment(text, Qt.AlignmentFlag.AlignLeft)
        self._right_layout.addWidget(informative_text, 1, 0)
        self._right_layout.setAlignment(informative_text, Qt.AlignmentFlag.AlignLeft)


        QBtn = QDialogButtonBox.StandardButton.Ok

        self._button_box = QDialogButtonBox(QBtn)
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)

        self._layout.addWidget(self._button_box, 2, 1)


    def __generatePixmap__(self, icon: Icon|QIcon = Icon.NoIcon):
        if type(icon) is QMessageBoxWithWidget.Icon:
            style = self.style()
            icon_size = style.pixelMetric(QStyle.PixelMetric.PM_MessageBoxIconSize)
            icon = style.standardIcon(icon.value)
        elif type(icon) is not QIcon:
            return QPixmap()

        if not icon.isNull():
            return icon.pixmap(icon_size)
        return QPixmap()
#----------------------------------------------------------------------
