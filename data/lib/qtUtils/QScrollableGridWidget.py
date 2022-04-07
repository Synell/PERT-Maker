#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout
from PyQt6.QtCore import Qt
#----------------------------------------------------------------------

    # Class
class QScrollableGridWidget(QScrollArea):
    def __init__(self):
        super(QScrollableGridWidget, self).__init__()
        self.scrollWidget = QWidget()
        self.scrollLayout = QGridLayout(self.scrollWidget)
        self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
#----------------------------------------------------------------------
