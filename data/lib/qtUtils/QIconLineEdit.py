#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QIcon, QAction
#----------------------------------------------------------------------

    # Class
class QIconLineEdit(QLineEdit):
    def __init__(self, parent = None, icon: str = None, placeholder: str = ''):
        super().__init__(parent)
        self.setClearButtonEnabled(True)
        self.addAction(QAction(QIcon(icon), '', self), QLineEdit.ActionPosition.LeadingPosition)
        self.setPlaceholderText(placeholder)
#----------------------------------------------------------------------
