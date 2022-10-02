#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QFileDialog, QComboBox
from PyQt6.QtCore import Qt
# from data.lib.qtUtils import QFilePicker
#----------------------------------------------------------------------

    # Class
class QImportTableDialog(QDialog):
    WIDTH = 3
    HEIGHT = 50

    def __init__(self, parent = None, langData: dict = {}, selectedItem: int = 0):
        super().__init__(parent = parent)

        self.langData = langData

        self.setWindowTitle(langData['title'])
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.acceptVerification)
        self.buttonBox.rejected.connect(self.reject)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(50)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([
            langData['QTableWidget']['horizonalHeader']['task'],
            langData['QTableWidget']['horizonalHeader']['previousTasks'],
            langData['QTableWidget']['horizonalHeader']['time']
        ])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.items = []

        for row in range(self.HEIGHT):
            self.items.append([])

            for column in range(self.WIDTH):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(row, column, item)
                self.items[row].append(item)


        self.button = QPushButton(langData['QPushButton']['open'])
        self.button.clicked.connect(self.selectButton)

        self.combobox = QComboBox()
        self.combobox.addItems([
            langData['QComboBox']['tasksAsPathNames'],
            langData['QComboBox']['tasksAsNodeNames']
        ])
        self.combobox.setCurrentIndex(selectedItem)

        layout = QGridLayout(self)
        layout.addWidget(self.tableWidget, 0, 0, 1, 2)
        layout.addWidget(self.combobox, 1, 0, 1, 2)
        layout.addWidget(self.button, 2, 0)
        layout.addWidget(self.buttonBox, 2, 1)


    def selectButton(self, event = None):
        path = QFileDialog.getOpenFileName(
            parent = self,
            directory = './',
            caption = self.langData['QFileDialog']['title'],
            filter = 'CSV (*.csv)'
        )[0]

        if not path: return

        with open(path, 'r', encoding = 'utf-8') as infile:
            lines = list(line.replace('\n', '') for line in infile.readlines())[1:]
            for row in range(min(len(lines), 50)):
                items = lines[row].split(';')
                for column in range(min(len(items), 3)):
                    self.items[row][column].setText(items[column])


    def acceptVerification(self, event = None):
        newLst = [['-1', '', 1]]
        for row in range(self.HEIGHT):
            canPass = False
            for column in range(self.WIDTH):
                if self.items[row][column].text():
                    canPass = True
                    break

            if canPass:
                newLst.append([])
                for column in range(self.WIDTH):
                    if column == self.WIDTH - 1:
                        if self.items[row][column].text().isdigit():
                            newLst[-1].append(int(self.items[row][column].text()))
                        else: newLst[-1].append(0)
                    else:
                        newLst[-1].append(self.items[row][column].text())
                        if column == 1 and newLst[-1][-1] == '': newLst[-1][-1] = '-1'

        self.newLst = newLst

        self.accept()


    def exec(self):
        accept = super().exec()
        if accept: return (self.newLst, self.combobox.currentIndex())
#----------------------------------------------------------------------
