#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .QScrollableGridWidget import QScrollableGridWidget
from enum import Enum
import colorama
#----------------------------------------------------------------------

    # Colorama
colorama.init()

    # Class
class QSidePanelSeparator:
    class Shape(Enum):
        NoSeparator = 0
        Line = 1
        DoubleLine = 2
        TripleLine = 3
        DotLine = 4
        DotLineLarge = 5
        SquareDotLine = 6

    def __init__(self, shape = Shape.Line):
        if type(shape) is QSidePanelSeparator.Shape:
            self.__shape__ = shape
        else: self.__shape__ = QSidePanelSeparator.Shape.Line


    @property
    def shape(self):
        return self.__shape__

    def setShape(self, shape: Shape = Shape.Line):
        if type(shape) is QSidePanelSeparator.Shape:
            self.__shape__ = shape
        else: print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a \'QSidePanelSeparator.Shape\'.')



class QSidePanelItem:
    def __init__(self, displayName: str = 'button', icon: str = None, clickEvent = None):
        self.setDisplayName(displayName)
        self.setIcon(icon)
        self.setClickedEvent(clickEvent)


    def setDisplayName(self, displayName: str = 'button'):
        if type(displayName) is str:
            self.__displayName__ = displayName
        else: raise ValueError(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a string.')

    @property
    def displayName(self):
        return self.__displayName__


    def setIcon(self, icon: str = None):
        if type(icon) is str:
            self.__icon__ = icon
        elif icon == None:
            self.__icon__ = './data/lib/qtUtils/themes/winRounded/dark/icons/sidepanel/noIcon.png'
        else: raise ValueError(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a string.')

    @property
    def icon(self):
        return self.__icon__


    def setClickedEvent(self, clickEvent = None):
        if callable(clickEvent):
            self.__clickEvent__ = clickEvent
        elif clickEvent == None:
            self.__clickEvent__ = self.__uselessFunction__
        else: raise ValueError(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a function.')

    @property
    def clickedEvent(self):
        return self.__clickEvent__

    def __uselessFunction__(self):
        pass



class QSidePanel(QScrollableGridWidget):
    def __init__(self, parent = None, width: int = 120, direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight, sideMerge: bool = True):
        super().__init__()
        self.scrollWidget.setProperty('class', 'QSidePanel')

        self.__direction__ = direction
        if direction == Qt.LayoutDirection.LeftToRight:
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        elif direction == Qt.LayoutDirection.RightToLeft:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.__items__ = []

        self.__selectedItem__ = None
        self.__width__ = width
        self.__sideMerge__ = sideMerge

        self.setParent(parent)

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        if sideMerge:
            if direction == Qt.LayoutDirection.LeftToRight:
                self.scrollLayout.setContentsMargins(13, 7, 5, 7)
            elif direction == Qt.LayoutDirection.RightToLeft:
                self.scrollLayout.setContentsMargins(5, 7, 13, 7)
        else:
            self.scrollLayout.setContentsMargins(5, 5, 5, 5)
        self.scrollLayout.setSpacing(3)
        self.setFrameShape(QFrame.Shape.NoFrame)

    def showEvent(self, event = None):
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().maximum())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setDisabled(True)

    def addSeparator(self, separator: QSidePanelSeparator = QSidePanelSeparator()):
        if type(separator) is QSidePanelSeparator:
            self.__items__.append(separator)
        else: print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Argument must be a QSidePanelSeparator.')

    def setSelectedItem(self, index):
        if not (index >= -len(self.__items__) and index < len(self.__items__)): return print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Index out of range.')
        self.__selectedItem__ = index
        self.update()

    def getSelectedItem(self):
        return self.__selectedItem__

    def addItem(self, item: QSidePanelItem = QSidePanelItem()):
        if type(item) is QSidePanelItem or type(item) is QSidePanelSeparator:
            self.__items__.append(item)
            self.update()
        else: raise ValueError('Argument must be a QSidePanelItem.')

    def addItems(self, *items: QSidePanelItem):
        for item in items:
            self.addItem(item)

    def insertItem(self, index: int = 0, item: QSidePanelItem = QSidePanelItem()):
        if (type(item) is QSidePanelItem or type(item) is QSidePanelSeparator) and type(index) is int:
            self.__items__.append(item)
            self.update()
        else: raise ValueError('Argument must be an integer and a QSidePanelItem.')

    def insertItems(self, index: int = 0, *items: QSidePanelItem):
        for item in items:
            self.insertItem(index, item)

    @property
    def items(self):
        return self.__items__

    def clear(self):
        self.__items__ = []
        self.update()

    def pop(self, index: int = 0):
        if type(index) is int:
            self.__items__.pop(index)
            self.update()
        else: raise ValueError('Argument must be an integer.')

    def update(self):
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().deleteLater()

        for i in reversed(range(self.scrollLayout.count())): # Cuz fucking buttons were not deleted
            self.scrollLayout.itemAt(i).widget().setParent(None)

        for index, item in enumerate(self.__items__):
            match item:
                case QSidePanelItem():
                    button = QPushButton(item.displayName)
                    if index == self.__selectedItem__:
                        button.setProperty('class', 'QSidePanelSelected')
                    else:
                        button.setProperty('class', 'QSidePanel')
                        button.clicked.connect(item.clickedEvent)
                    button.setIcon(QIcon(item.icon))
                case QSidePanelSeparator():
                    match item.shape:
                        case QSidePanelSeparator.Shape.NoSeparator: button = QPushButton()
                        case QSidePanelSeparator.Shape.Line: button = QPushButton('─' * 25)
                        case QSidePanelSeparator.Shape.DoubleLine: button = QPushButton('═' * 25)
                        case QSidePanelSeparator.Shape.TripleLine: button = QPushButton('≡' * 25)
                        case QSidePanelSeparator.Shape.SquareDotLine: button = QPushButton('┅' * 25)
                        case QSidePanelSeparator.Shape.DotLine: button = QPushButton('∙' * 60)
                        case QSidePanelSeparator.Shape.DotLineLarge: button = QPushButton('•' * 30)
                    button.setDisabled(True)
                    button.setProperty('class', 'QSidePanelSeparator')
                case _: button = QPushButton()

            if self.__sideMerge__:
                button.setFixedWidth(self.__width__)
            else:
                button.setFixedWidth(self.__width__ - 10)

            if self.__direction__ == Qt.LayoutDirection.RightToLeft:
                button.setObjectName('right')

            button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.scrollLayout.addWidget(button, index, 0)

        self.horizontalScrollBar().setValue(self.horizontalScrollBar().maximum())
#----------------------------------------------------------------------
