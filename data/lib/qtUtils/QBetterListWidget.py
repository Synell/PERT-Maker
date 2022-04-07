#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QTreeView, QAbstractItemView, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtCore import Qt, QItemSelectionModel, QModelIndex, QSize
import colorama
#----------------------------------------------------------------------

    # Colorama
colorama.init()

    # Class
class __verification__:
    def goodHeaders(headers = None):
        if type(headers) is not list: return False
        if len(headers) < 1: return False
        for i in headers:
            if type(i) is not str: return False
        return True



class QBetterListWidget(QTreeView):
    def __new__(cls, headers = ['column'], minimumSectionSize: int = 50, alignmentFlag = Qt.AlignmentFlag.AlignCenter):
        if not __verification__.goodHeaders(headers):
            print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Headers must be a list of strings!')
            return None
        return super().__new__(cls)

    def __init__(self, headers: list[str] = None, minimumSectionSize: int = 50, alignmentFlag: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft):
        super().__init__()
        self.headers = headers
        self.treeViewModel = QStandardItemModel()
        self.treeViewModel.setHorizontalHeaderLabels(self.headers)
        self.setModel(self.treeViewModel)
        self.setUniformRowHeights(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setRootIsDecorated(False)
        self.header().setDefaultAlignment(alignmentFlag)
        self.header().resizeSections(QHeaderView.ResizeMode.ResizeToContents)
        self.header().setStretchLastSection(True)
        self.header().setCascadingSectionResizes(True)
        self.header().setMinimumSectionSize(minimumSectionSize)
        self.setIconSize(QSize(16, 16))

    def setHeaders(self, headers = ['column']):
        if not __verification__.goodHeaders(headers): return
        self.headers = headers
        self.treeViewModel.setHorizontalHeaderLabels(self.headers)

    def addHeader(self, header = 'column'):
        if not __verification__.goodHeaders([header]): return
        self.headers.append(header)

    def setHeaderAlignment(self, alignmentFlag: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft):
        self.header().setDefaultAlignment(alignmentFlag)

    def setMinimumSectionSize(self, minimumSectionSize: int = 50):
        self.header().setMinimumSectionSize(minimumSectionSize)

    def getHeaders(self):
        return self.headers

    def getItems(self):
        l = []
        root = self.treeViewModel.invisibleRootItem()
        for i in range(root.rowCount()):
            subL = []
            for j in range(root.columnCount()):
                subL.append(root.child(i, j).text())
            l.append(tuple(subL))

        return tuple(l)

    def getItem(self, index: int = 0):
        l = []
        root = self.treeViewModel.invisibleRootItem()
        for j in range(root.columnCount()):
            l.append(root.child(index, j).text())

        return tuple(l)

    def count(self):
        return len(self.getItems())

    def addItem(self, items: list[str], icon = None, alignmentFlag: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft):
        if not __verification__.goodHeaders(items):
            print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' Items must be strings!')
            return None

        for index in range(min(len(self.headers), len(items))):
            items[index] = QStandardItem(items[index])
            items[index].setTextAlignment(alignmentFlag)

        for index in range(len(self.headers) - len(items)):
            items.append(QStandardItem(''))

        if icon != None:
            items[0].setIcon(QIcon(icon))

        self.treeViewModel.appendRow(items)

    def removeItem(self, index: int = 0):
        self.treeViewModel.removeRow(index)
    
    def removeItems(self, startIndex: int = 0, endIndex: int = 1):
        self.treeViewModel.removeRows(startIndex, endIndex)

    def clear(self):
        self.treeViewModel.removeRows(0, self.treeViewModel.invisibleRootItem().rowCount())

    def select(self, index: int = 0):
        self.deselectAll()
        self.selectionModel().select(self.treeViewModel.index(index, 0, QModelIndex()), QItemSelectionModel.SelectionFlag.Select|QItemSelectionModel.SelectionFlag.Rows)

    def deselectAll(self):
        self.clearSelection()

    def isSelection(self):
        return bool(len(self.selectedIndexes()))

    def getSelectedRow(self):
        return self.selectedIndexes()[0].row()

    def getSelectedItem(self):
        return tuple(self.treeViewModel.data(self.selectedIndexes()[item]) for item in range(len(self.headers)))

    def getSelectedItemIndex(self):
        return self.selectedIndexes()[0].row()
#----------------------------------------------------------------------
