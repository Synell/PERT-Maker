#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from data.lib.qtUtils.QUtilsColor import QUtilsColor
from .QColorDialog import QColorDialog
#----------------------------------------------------------------------

    # Class
class QColorButton(QPushButton):
    colorChanged = pyqtSignal(QUtilsColor)

    def __init__(self, parent = None, lang: dict = {}, color: QUtilsColor = QUtilsColor('#FFFFFF')) -> None:
        super().__init__(parent)

        self.__color__ = QUtilsColor.from_rgba(color.rgba)
        self.__lang__ = lang
        self.setProperty('QColorButton', True)
        self.setProperty('color', 'main')
        self.setFixedSize(32, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update()
        self.clicked.connect(self.__clicked__)

    def __clicked__(self) -> None:
        result = QColorDialog(self.parent(), self.__lang__, self.color).exec()
        if result:
            self.color = result

    def update(self) -> None:
        self.setStyleSheet(f'background-color: {self.color.ahex};')
        return super().update()

    @property
    def color(self) -> QUtilsColor:
        return self.__color__

    @color.setter
    def color(self, color: QUtilsColor) -> None:
        self.__color__ = color
        self.update()
        self.colorChanged.emit(self.color)
#----------------------------------------------------------------------
