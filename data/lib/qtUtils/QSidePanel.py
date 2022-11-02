#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from typing import Callable, Iterator
from PyQt6.QtWidgets import QPushButton, QLabel, QFrame
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from .QScrollableGridFrame import QScrollableGridFrame
#----------------------------------------------------------------------

    # Class
class QSidePanelItem:
    clicked = pyqtSignal()

    def __init__(self, text: str = '', icon: QIcon|str = None, connect: Callable = None) -> None:
        self.__widget__ = QPushButton()
        # self.__widget__.setCheckable(True)
        self.__widget__.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__widget__.setProperty('QSidePanel', True)
        self.text = text
        self.icon = icon
        self.auto_select = True
        self.connect = connect

    @property
    def text(self) -> str:
        return self.__text__

    @text.setter
    def text(self, text: str) -> None:
        self.__text__ = text
        self.__widget__.setText(text)

    @property
    def icon(self) -> QIcon:
        return self.__icon__

    @icon.setter
    def icon(self, icon: QIcon|str) -> None:
        self.__icon__ = icon if isinstance(icon, QIcon) else QIcon(icon)
        if icon is None: self.__widget__.setIcon(QIcon())
        else: self.__widget__.setIcon(self.icon)

    @property
    def auto_select(self) -> bool:
        return self.__auto_select__

    @auto_select.setter
    def auto_select(self, auto_select: bool) -> None:
        self.__auto_select__ = auto_select

    @property
    def connect(self) -> Callable:
        return self.__connect__

    @connect.setter
    def connect(self, connect: Callable) -> None:
        self.__connect__ = connect



class QSidePanelSeparator:
    class Shape(Enum):
        Plain = QFrame.Shadow.Plain
        Raised = QFrame.Shadow.Raised
        Sunken = QFrame.Shadow.Sunken

    def __init__(self, shape: Shape = Shape.Sunken) -> None:
        self.shape = shape
        self.__widget__ = QFrame()
        self.__widget__.setFixedHeight(1)
        self.__widget__.setFrameShape(QFrame.Shape.HLine)

    @property
    def shape(self) -> Shape:
        return self.__shape__

    @shape.setter
    def shape(self, shape: Shape) -> None:
        if type(shape) is QFrame.Shape:
            self.__shape__ = shape
        else: raise ValueError(f'Argument must be a \'QSidePanelSeparator.Shape\'.')


class QSidePanel(QScrollableGridFrame):
    current_index_changed: pyqtSignal = pyqtSignal(int)
    current_item_changed: pyqtSignal = pyqtSignal(QSidePanelItem)

    def __init__(self, parent = None, width: int = 120, transparent: bool = False) -> None:
        super().__init__()
        self.set_transparent(transparent)
        self.setProperty('color', 'main')

        self.__items__ = []

        self.setParent(parent)

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__items__ = []
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.set_width(width)
        self.setProperty('QSidePanel', True)

        self.__current_index__ = 0
        self.update()

    @property
    def transparent(self) -> bool:
        return self.property('transparent')

    def set_transparent(self, transparent: bool) -> None:
        self.setProperty('transparent', transparent)

    @property
    def width(self) -> int:
        return self.width()

    def set_width(self, width: int) -> None:
        self.setFixedWidth(width)

    @property
    def current_index(self) -> int:
        return self.__current_index__

    def set_current_index(self, index: int) -> None:
        if index >= self.count() or index < 0: raise IndexError(f'Index {index} out of range.')
        self.__current_index__ = index
        self.update()

    @property
    def current_item(self) -> QSidePanelItem:
        return self.__items__[self.__current_index__]

    def set_current_item(self, item: QSidePanelItem) -> None:
        self.set_current_index(self.items.index(item))

    def update(self) -> None:
        if self.__current_index__ >= self.count(): self.__current_index__ = self.count() - 1
        if self.__current_index__ < 0: self.__current_index__ = 0

        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        send_param = lambda i: lambda: self.__clicked__(i)

        for index, item in enumerate(self.__items__):
            if type(item) is QSidePanelItem:
                item.__widget__.disconnect()
                item.__widget__.clicked.connect(send_param(index))
                # item.__widget__.setChecked(index == self.__current_index__)
                item.__widget__.setProperty('selected', True) if index == self.__current_index__ else item.__widget__.setProperty('selected', False)
            self.scroll_layout.addWidget(item.__widget__, index, 0)

    def __clicked__(self, index: int) -> None:
        self.current_index_changed.emit(index)
        self.current_item_changed.emit(self.__items__[index])
        if self.__items__[index].auto_select: self.__current_index__ = index
        if self.__items__[index].connect is not None: self.__items__[index].connect()
        self.update()

    def add_item(self, item: QSidePanelItem) -> None:
        self.__items__.append(item)
        self.update()

    def add_items(self, items: Iterator[QSidePanelItem]) -> None:
        for item in items: self.add_item(item)

    def insert_item(self, index: int, item: QSidePanelItem) -> None:
        self.__items__.insert(index, item)
        self.update()

    def insert_items(self, index: int, items: Iterator[QSidePanelItem]) -> None:
        for item in items: self.insert_item(index, item)

    def remove_item(self, item: QSidePanelItem) -> None:
        self.__items__.remove(item)
        self.update()

    def remove_items(self, items: Iterator[QSidePanelItem]) -> None:
        for item in items: self.remove_item(item)

    def pop_item(self, index: int) -> QSidePanelItem:
        item = self.__items__.pop(index)
        self.update()
        return item

    def clear(self) -> None:
        self.__items__ = []
        self.update()

    @property
    def items(self) -> list[QSidePanelItem]:
        return [item for item in self.__items__]

    def item_at(self, index: int) -> QSidePanelItem:
        return self.__items__[index]

    def index_of(self, item: QSidePanelItem) -> int:
        return self.__items__.index(item)

    def count(self) -> int:
        return len(self.__items__)

    def __iter__(self) -> Iterator[QSidePanelItem]:
        return iter(self.__items__)

    def __getitem__(self, index: int) -> QSidePanelItem:
        return self.__items__[index]

    def __setitem__(self, index: int, item: QSidePanelItem) -> None:
        self.__items__[index] = item
        self.update()
#----------------------------------------------------------------------
