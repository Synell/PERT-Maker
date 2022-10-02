#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout
from PyQt6.QtCore import Qt
#----------------------------------------------------------------------

    # Class
class QScrollableGridWidget(QScrollArea):
    def __init__(self):
        super(QScrollableGridWidget, self).__init__()
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
#----------------------------------------------------------------------
