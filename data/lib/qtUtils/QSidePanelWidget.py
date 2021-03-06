#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt
from .QSidePanel import QSidePanel
#----------------------------------------------------------------------

    # Class
class QSidePanelWidget(QWidget):
    def __init__(self, parent = None, widget: QWidget = None, width: int = 120, direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight, sideMerge: bool = False):
        super().__init__(parent)
        self.__layout__ = QGridLayout(self)

        self.sidepanel = QSidePanel(self, width = width, direction = direction, sideMerge = sideMerge)
        self.widget = widget

        self.__layout__.setSpacing(0)
        self.__layout__.setContentsMargins(0, 0, 0, 0)

        self.__layout__.addWidget(self.sidepanel, 0, 0)
        self.__layout__.addWidget(self.widget, 0, 1)
#----------------------------------------------------------------------
