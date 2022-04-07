#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QWidget, QGridLayout
#----------------------------------------------------------------------

    # Class
class QGridWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)
#----------------------------------------------------------------------
