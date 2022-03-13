#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QGroupBox, QGridLayout
#----------------------------------------------------------------------

    # Class
class QGridGroupBox(QGroupBox):
    def __init__(self, title = '', parent = None):
        super().__init__(title, parent)
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)
#----------------------------------------------------------------------
