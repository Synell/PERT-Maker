#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton, QLabel, QFileDialog
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QIcon
from .QGridWidget import QGridWidget
from .QFiles import QFiles
#----------------------------------------------------------------------

    # Class
class QFileButton(QGridWidget):
    normal_color = '#FFFFFF'
    hover_color = '#FFFFFF'

    path_changed = pyqtSignal(str)

    def __init__(self, parent = None, lang: dict = {}, default_path: str = './', icon: str = None, type: QFiles.Dialog = QFiles.Dialog.ExistingDirectory, filter: str = '', end_with: str = ''):
        super().__init__(parent)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty('QFileButton', True)

        self.lang = lang
        self.type = type
        self.__path__ = default_path
        if self.__path__ == None: self.__path__ = './'
        self.filter = filter
        self.end_with = end_with

        self.push_button = QPushButton()
        self.push_button.setIcon(QIcon(icon))
        self.push_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.push_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.grid_layout.addWidget(self.push_button, 0, 0)
        self.label = QLabel(lang['title'])
        self.grid_layout.addWidget(self.label, 0, 0)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.label.setProperty('hover', False)

        self.push_button.clicked.connect(self.button_clicked)
        self.update_path()

    def enterEvent(self, event: QEvent = None):
        self.label.setProperty('hover', True)
        self.label.setStyleSheet(f'color: {self.hover_color}')

    def leaveEvent(self, event: QEvent = None):
        self.label.setProperty('hover', False)
        self.label.setStyleSheet(f'color: {self.normal_color}')

    def button_clicked(self):
        path = None

        match self.type:
            case QFiles.Dialog.OpenFileName:
                path = QFileDialog.getOpenFileName(
                    parent = self,
                    directory = self.__path__,
                    caption = self.lang['dialog'],
                    filter = self.filter
                )[0]
            case QFiles.Dialog.OpenFileUrl:
                path = QFileDialog.getOpenFileUrl(
                    parent = self,
                    directory = self.__path__,
                    caption = self.lang['dialog'],
                    filter = self.filter
                )[0]
            case QFiles.Dialog.SaveFileName:
                path = QFileDialog.getSaveFileName(
                    parent = self,
                    directory = self.__path__,
                    caption = self.lang['dialog'],
                    filter = self.filter
                )[0]
            case QFiles.Dialog.SaveFileUrl:
                path = QFileDialog.getSaveFileUrl(
                    parent = self,
                    directory = self.__path__,
                    caption = self.lang['dialog'],
                    filter = self.filter
                )[0]
            case _:
                path = QFileDialog.getExistingDirectory(
                    parent = self,
                    directory = self.__path__,
                    caption = self.lang['dialog']
                )

        if not path: return
        old_path = self.__path__
        self.__path__ = path
        self.update_path()
        if self.__path__ != old_path: self.path_changed.emit(self.__path__)

    def update_path(self):
        self.__path__ = self.__path__.replace('\\', '/')
        while self.__path__[-1] == '/': self.__path__ = self.__path__[:-1]
        #while self.__path__.find('//') != -1: self.__path__ = self.__path__.replace('//', '/')
        self.__path__ = self.__path__[0].upper() + self.__path__[1:]
        if len(self.__path__) > 24: self.push_button.setText('/'.join(self.__path__.split('/')[:1]) + '/.../' + '/'.join(self.__path__.split('/')[-2:]) + self.end_with)
        else: self.push_button.setText(self.__path__ + self.end_with)

    def path(self) -> str:
        return self.__path__ + self.end_with

    def setPath(self, value: str):
        self.__path__ = value.replace('\\', '/')
        self.update_path()
#----------------------------------------------------------------------
