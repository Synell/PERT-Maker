#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QLineEdit, QCheckBox

from .QGridFrame import QGridFrame
from .QNamedLineEdit import QNamedLineEdit
#----------------------------------------------------------------------

    # Class
class QLoginWidget(QGridFrame):
    def __init__(self, parent = None , lang: dict = {}, username: str = '', password: str = '', remember_checkbox: bool = True, remember: bool = False):
        super().__init__(parent)

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(20)
        self.setMinimumWidth(300)

        self.username = QNamedLineEdit(None, '', lang['QNamedLineEdit']['username'])
        self.username.line_edit.setProperty('small', True)
        self.username.setText(username)
        self.grid_layout.addWidget(self.username, 0, 0)

        self.password = QNamedLineEdit(None, '', lang['QNamedLineEdit']['password'])
        self.password.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setText(password)
        self.grid_layout.addWidget(self.password, 1, 0)

        if remember_checkbox:
            self.remember = QCheckBox(lang['QCheckBox']['remember'])
            self.remember.setChecked(remember)
            self.grid_layout.addWidget(self.remember, 2, 0)
        else: self.remember = None
#----------------------------------------------------------------------
