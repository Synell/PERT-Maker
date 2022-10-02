#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QLabel, QFileDialog
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from .QFiles import QFiles
from .QGridFrame import QGridFrame
from .QIconWidget import QIconWidget
from .QLinkLabel import QLinkLabel
#----------------------------------------------------------------------

    # Class
class QFileZone(QGridFrame):
    drag_and_drop_used = pyqtSignal()
    dialog_used = pyqtSignal()
    item_added = pyqtSignal(str)
    items_added = pyqtSignal(list)

    def __init__(self, parent = None, lang: dict = {}, icon: str = None, icon_size: int = 96, type: QFiles.Dialog = QFiles.Dialog.OpenFileName, directory: str = '', filter: str = '') -> None:
        super().__init__(parent)
        self.__icon__ = icon
        self.__lang__ = lang
        self.__type__ = type
        self.__directory__ = directory
        self.set_filter(filter)
        self.__icon_size__ = icon_size

        match type:
            case QFiles.Dialog.OpenFileUrl: type = QFiles.Dialog.OpenFileName
            case QFiles.Dialog.OpenFileUrls: type = QFiles.Dialog.OpenFileNames
            case QFiles.Dialog.ExistingDirectoryUrl: type = QFiles.Dialog.ExistingDirectory
            case QFiles.Dialog.SaveFileName: type = QFiles.Dialog.OpenFileName
            case QFiles.Dialog.SaveFileUrl: type = QFiles.Dialog.OpenFileName
        self.__type__ = type

        self.setProperty('QFileZone', True)

        icon_widget = QIconWidget(self, self.__icon__, icon_size)
        self.grid_layout.addWidget(icon_widget, 0, 0)

        widget = QGridFrame()
        widget.setProperty('transparent', True)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        widget.grid_layout.setSpacing(5)

        label = QLabel(lang['QLabel']['dragAndDrop' + ('File' if type == QFiles.Dialog.OpenFileName else 'Files' if type == QFiles.Dialog.OpenFileNames else 'Directory')])
        label.setProperty('class', 'h2')
        widget.grid_layout.addWidget(label, 0, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        label = QLinkLabel(lang['QLinkLabel']['select' + ('File' if type == QFiles.Dialog.OpenFileName else 'Files' if type == QFiles.Dialog.OpenFileNames else 'Directory')])
        label.setProperty('class', 'bold')
        label.clicked.connect(self.__clicked__)
        widget.grid_layout.addWidget(label, 1, 0)
        widget.grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(widget, 1, 0)
        self.grid_layout.setAlignment(widget, Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(90, 60, 90, 60)

        self.setAcceptDrops(True)


    @property
    def filter(self):
        return self.__filter__

    def set_filter(self, filter: str) -> None:
        self.__filter__ = filter

        self.__extension_list__ = []
        for ext in self.__filter__.split(';;'):
            ext = ext.split('(')[-1].replace('.', '').replace('*', '').replace(')', '').replace(' ', '').replace('.', '').split(',')
            for i in ext:
                if i: self.__extension_list__.append(i)


    def __clicked__(self, action: str) -> None:
        path = None

        match action:
            case 'file':
                path = QFileDialog.getOpenFileName(self, directory = self.__directory__, filter = self.__filter__, caption = self.__lang__['QFileDialog']['file'])[0]
            case 'files':
                path = QFileDialog.getOpenFileNames(self, directory = self.__directory__, filter = self.__filter__, caption = self.__lang__['QFileDialog']['files'])[0]
            case 'directory':
                path = QFileDialog.getExistingDirectory(self, directory = self.__directory__, caption = self.__lang__['QFileDialog']['directory'])[0]

        if not path: return

        self.dialog_used.emit()

        if type(path) is not list:
            path = [path]

        for p in path:
            self.item_added.emit(p)

        self.items_added.emit(path)


    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if not event.mimeData().hasUrls(): return event.ignore()

        for e in event.mimeData().urls():
            if not e.isLocalFile():
                return event.ignore()
    
            if not e.toLocalFile().split('.')[-1] in self.__extension_list__:
                return event.ignore()

        event.accept()


    def dropEvent(self, event: QDropEvent) -> None:
        self.drag_and_drop_used.emit()
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.item_added.emit(f)
        self.items_added.emit(files)
#----------------------------------------------------------------------
