#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QDialog, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QFileDialog, QComboBox
from PyQt6.QtCore import Qt
from data.lib.qtUtils import QGridWidget
#----------------------------------------------------------------------

    # Class
class QImportTableDialog(QDialog):
    WIDTH = 3
    HEIGHT = 50

    def __init__(self, parent = None, lang: dict = {}, selected_item: int = 0):
        super().__init__(parent = parent)

        self.lang = lang

        self.setWindowTitle(lang['title'])
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        right_buttons = QGridWidget()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang['QPushButton']['cancel'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(button, 0, 0)

        button = QPushButton(lang['QPushButton']['import'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept_verification)
        button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(button, 0, 1)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(50)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels([
            lang['QTableWidget']['horizonalHeader']['task'],
            lang['QTableWidget']['horizonalHeader']['previousTasks'],
            lang['QTableWidget']['horizonalHeader']['time']
        ])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.items = []

        for row in range(self.HEIGHT):
            self.items.append([])

            for column in range(self.WIDTH):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_widget.setItem(row, column, item)
                self.items[row].append(item)


        button = QPushButton(lang['QPushButton']['open'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty('color', 'main')
        button.setProperty('transparent', True)
        button.clicked.connect(self.selectButton)

        self.combobox = QComboBox()
        self.combobox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combobox.view().setCursor(Qt.CursorShape.PointingHandCursor)
        self.combobox.addItems([
            lang['QComboBox']['tasksAsPathNames'],
            lang['QComboBox']['tasksAsNodeNames']
        ])
        self.combobox.setCurrentIndex(selected_item)

        layout = QGridLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(self.table_widget, 0, 0, 1, 2)
        layout.addWidget(self.combobox, 1, 0, 1, 2)
        layout.addWidget(button, 2, 0)
        layout.addWidget(right_buttons, 2, 1)


    def selectButton(self, event = None):
        path = QFileDialog.getOpenFileName(
            parent = self,
            directory = './',
            caption = self.lang['QFileDialog']['title'],
            filter = 'CSV (*.csv)'
        )[0]

        if not path: return

        with open(path, 'r', encoding = 'utf-8') as infile:
            lines = list(line.replace('\n', '') for line in infile.readlines())[1:]
            for row in range(min(len(lines), 50)):
                items = lines[row].split(';')
                for column in range(min(len(items), 3)):
                    self.items[row][column].setText(items[column])


    def accept_verification(self, event = None):
        new_lst = [['-1', '', 1]]
        for row in range(self.HEIGHT):
            can_pass = False
            for column in range(self.WIDTH):
                if self.items[row][column].text():
                    can_pass = True
                    break

            if can_pass:
                new_lst.append([])
                for column in range(self.WIDTH):
                    if column == self.WIDTH - 1:
                        if self.items[row][column].text().isdigit():
                            new_lst[-1].append(int(self.items[row][column].text()))
                        else: new_lst[-1].append(0)
                    else:
                        new_lst[-1].append(self.items[row][column].text())
                        if column == 1 and new_lst[-1][-1] == '': new_lst[-1][-1] = '-1'

        self.new_lst = new_lst

        self.accept()


    def exec(self):
        accept = super().exec()
        if accept: return (self.new_lst, self.combobox.currentIndex())
#----------------------------------------------------------------------
