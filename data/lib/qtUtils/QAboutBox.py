#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QGridLayout, QDialog, QDialogButtonBox, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from .QBaseApplication import QBaseApplication
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QAboutBox(QDialog):
    def __init__(self, app: QBaseApplication = None, windowTitle: str = '', logo: str = '', texts: list[QLabel] = []):
        super().__init__(parent = app.window)
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint, True)

        self.__layout__ = QGridLayout(self)

        self.__left__ = QGridWidget()

        self.__right__ = QGridWidget()
        self.__right__.gridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__right__.gridLayout.setSpacing(20)

        self.__down__ = QGridWidget()

        self.__layout__.addWidget(self.__left__, 0, 0)
        self.__layout__.addWidget(self.__right__, 0, 1)


        pixmap = QLabel()
        pixmap.setPixmap(QPixmap(logo))
        #TODO: pixmap.setFixedSize(100, 100)
        self.__left__.gridLayout.addWidget(pixmap)
        self.__left__.gridLayout.setAlignment(pixmap, Qt.AlignmentFlag.AlignTop)
        self.__left__.gridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWindowTitle(windowTitle)


        text = QLabel(windowTitle)
        text.setProperty('class', 'bold')
        self.__right__.gridLayout.addWidget(text, 0, 0)
        self.__right__.gridLayout.setAlignment(text, Qt.AlignmentFlag.AlignTop)

        self.__right__.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for textID in range(len(texts)):
            texts[textID].setOpenExternalLinks(True)
            self.__right__.gridLayout.addWidget(texts[textID], textID + 1, 0)
            self.__right__.gridLayout.setAlignment(texts[textID], Qt.AlignmentFlag.AlignTop)


        QBtn = QDialogButtonBox.StandardButton.Ok

        self.__buttonBox__ = QDialogButtonBox(QBtn)
        self.__buttonBox__.accepted.connect(self.accept)
        self.__buttonBox__.rejected.connect(self.reject)

        self.__layout__.addWidget(self.__buttonBox__, 1, 1)
#----------------------------------------------------------------------
