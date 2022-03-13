from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from sys import exit
from math import *
import json
from pyautogui import *
import os

from data.lib import *




class SaveData(QSaveData):
    def __init__(self) -> None:
        self.maxLoop = 5000

        self.alignToGrid = False

        self.gridMode = 0
        self.gridSize = 50

        self.liveRefreshConnectionView = False
        self.liveGenerateCriticalPath = False
        self.liveMinMax = False

        super().__init__()


    def settingsMenuExtra(self):
        lang = self.languageData['QSettingsDialog']['editorTab']

        widget = QScrollableGridWidget()

        widget.maxLoopSpinbox = QSpinBoxWithLabel(lang['QSpinBoxWithLabel']['QLabel']['maxLoop'])
        widget.maxLoopSpinbox.spinBox.setRange(255, 65535)
        widget.maxLoopSpinbox.spinBox.setValue(self.maxLoop)

        widget.gridSizeSpinbox = QSpinBoxWithLabel(lang['QSpinBoxWithLabel']['QLabel']['gridSize'])
        widget.gridSizeSpinbox.spinBox.setRange(10, 200)
        widget.gridSizeSpinbox.spinBox.setValue(self.gridSize)

        widget.scrollLayout.addWidget(widget.maxLoopSpinbox, 0, 0)
        widget.scrollLayout.addWidget(widget.gridSizeSpinbox, 0, 1)

        return {lang['title']: widget}, self.getExtra

    def getExtra(self, extraTabs: dict = {}):
        lang = self.languageData['QSettingsDialog']['editorTab']

        self.maxLoop = extraTabs[lang['title']].maxLoopSpinbox.spinBox.value()
        self.gridSize = extraTabs[lang['title']].gridSizeSpinbox.spinBox.value()


    def saveExtraData(self) -> dict:
        return {
            'maxLoop': self.maxLoop,

            'alignToGrid': self.alignToGrid,

            'gridMode': self.gridMode,
            'gridSize': self.gridSize,

            'liveRefreshConnectionView': self.liveRefreshConnectionView,
            'liveGenerateCriticalPath': self.liveGenerateCriticalPath,
            'liveMinMax': self.liveMinMax
        }

    def loadExtraData(self, extraData: dict = ...) -> None:
        self.maxLoop = extraData['maxLoop']

        self.alignToGrid = extraData['alignToGrid']

        self.gridMode = extraData['gridMode']
        self.gridSize = extraData['gridSize']

        self.liveRefreshConnectionView = extraData['liveRefreshConnectionView']
        self.liveGenerateCriticalPath = extraData['liveGenerateCriticalPath']
        self.liveMinMax = extraData['liveMinMax']



class Application(QBaseApplication):
    BUILD = '07e63f6a'
    VERSION = 'Experimental'

    DELTA = 80

    COLOR_NORMAL = Color()
    COLOR_FOCUS = Color()
    COLOR_SELECTED = Color()
    COLOR_GRID = Color()
    COLOR_LINK = Color()

    SAVE_PATH = None

    def __init__(self):
        super().__init__()

        self.selectedItem = None
        self.selectedNode = None
        self.unsaved = False

        self.shiftKey = False

        self.cameraPos = Vector2()
        self.oldMousePos = Vector2()

        self.graph = Graph()

        self.saveData = SaveData()

        self.saveData.setStyleSheet(self)

        self.setWindowIcon(QIcon('./data/themes/logo.ico'))

        self.createWidgets()
        self.fileMenu_newAction()

    def notImplemented(self, text = ''):
        if text:
            w = QDropDownWidget(text = lang['details'], widget = QLabel(text))
        else: w = None

        lang = self.saveData.languageData['QMessageBox']['critical']['notImplemented']

        QMessageBoxWithWidget(
            app = self,
            windowTitle = lang['title'],
            text = lang['text'],
            icon = QMessageBoxWithWidget.Icon.Critical,
            widget = w
        ).exec()

    def createWidgets(self):
        self.root = QGridWidget()
        self.root.gridLayout.setSpacing(0)
        self.root.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.canvas = QWidget()
        self.canvas.setMinimumSize(600, 400)
        self.root.gridLayout.addWidget(self.canvas, 0, 0)


        self.propertiesMenu = QScrollableGridWidget()
        self.propertiesMenu.setMinimumWidth(300)
        self.propertiesMenu.setMinimumHeight(200)
        self.propertiesMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.propertiesMenu.scrollWidget.setProperty('class', 'dockWidget')
        
        self.propertiesMenuDockWidget = QDockWidget(self.saveData.languageData['QDockWidget']['properties']['title'])
        self.propertiesMenuDockWidget.setWidget(self.propertiesMenu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.propertiesMenuDockWidget)


        self.connectionViewMenu = QScrollableGridWidget()
        self.connectionViewMenu.setMinimumWidth(450)
        self.connectionViewMenu.setMinimumHeight(200)
        self.connectionViewMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.connectionViewMenu.scrollWidget.setProperty('class', 'dockWidget')
        
        self.connectionViewMenuDockWidget = QDockWidget(self.saveData.languageData['QDockWidget']['connectionView']['title'])
        self.connectionViewMenuDockWidget.setWidget(self.connectionViewMenu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.connectionViewMenuDockWidget)

        self.createConnectionViewMenu()


        self.criticalPathViewMenu = QScrollableGridWidget()
        self.criticalPathViewMenu.setMinimumWidth(450)
        self.criticalPathViewMenu.setMinimumHeight(200)
        self.criticalPathViewMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.criticalPathViewMenu.scrollWidget.setProperty('class', 'dockWidget')
        
        self.criticalPathViewMenuDockWidget = QDockWidget(self.saveData.languageData['QDockWidget']['criticalPathView']['title'])
        self.criticalPathViewMenuDockWidget.setWidget(self.criticalPathViewMenu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.criticalPathViewMenuDockWidget)

        self.createCriticalPathViewMenu()


        self.window.tabifyDockWidget(self.connectionViewMenuDockWidget, self.criticalPathViewMenuDockWidget)
        self.connectionViewMenuDockWidget.raise_()


        self.generationMenu = QScrollableGridWidget()
        self.generationMenu.setMinimumWidth(450)
        self.generationMenu.setMinimumHeight(200)
        self.generationMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.generationMenu.scrollWidget.setProperty('class', 'dockWidget')
        
        self.generationMenuDockWidget = QDockWidget(self.saveData.languageData['QDockWidget']['generation']['title'])
        self.generationMenuDockWidget.setWidget(self.generationMenu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.generationMenuDockWidget)

        self.createGenerationMenu()


        self.window.setCentralWidget(self.root)


        self.canvas.installEventFilter(self)
        self.window.keyPressEvent = self.keyPressEvent
        self.window.keyReleaseEvent = self.keyReleaseEvent

        self.createMenuBar()

        self.loadColors()
        self.canvas.update()

    def createMenuBar(self):
        menuBar = self.window.menuBar()

        def createFileMenu():
            lang = self.saveData.languageData['QMainWindow']['QMenuBar']['fileMenu']['QAction']

            fileMenu: QMenu = menuBar.addMenu(self.saveData.languageData['QMainWindow']['QMenuBar']['fileMenu']['title'])

            newAction = QAction(self.saveData.getIcon('menubar/new.png'), lang['new'], self.window)
            newAction.setShortcut('Ctrl+N')
            newAction.triggered.connect(self.fileMenu_newAction)

            openAction = QAction(self.saveData.getIcon('menubar/open.png'), lang['open'], self.window)
            openAction.setShortcut('Ctrl+O')
            openAction.triggered.connect(self.fileMenu_openAction)

            saveAction = QAction(self.saveData.getIcon('menubar/save.png'), lang['save'], self.window)
            saveAction.setShortcut('Ctrl+S')
            saveAction.triggered.connect(self.fileMenu_saveAction)

            saveAsAction = QAction(self.saveData.getIcon('menubar/saveAs.png'), lang['saveAs'], self.window)
            saveAsAction.setShortcut('Ctrl+Shift+S')
            saveAsAction.triggered.connect(self.fileMenu_saveAsAction)

            settingsAction = QAction(self.saveData.getIcon('menubar/settings.png'), lang['settings'], self.window)
            settingsAction.setShortcut('Ctrl+Alt+S')
            settingsAction.triggered.connect(self.fileMenu_settingsAction)

            exitAction = QAction(self.saveData.getIcon('menubar/exit.png'), lang['exit'], self.window)
            exitAction.setShortcut('Alt+F4')
            exitAction.triggered.connect(self.window.close)


            fileMenu.addAction(newAction)
            fileMenu.addAction(openAction)
            fileMenu.addSeparator()
            fileMenu.addAction(saveAction)
            fileMenu.addAction(saveAsAction)
            fileMenu.addSeparator()
            fileMenu.addAction(settingsAction)
            fileMenu.addSeparator()
            fileMenu.addAction(exitAction)

        def createViewMenu():
            lang = self.saveData.languageData['QMainWindow']['QMenuBar']['viewMenu']['QAction']

            viewMenu: QMenu = menuBar.addMenu(self.saveData.languageData['QMainWindow']['QMenuBar']['viewMenu']['title'])

            gridSwitchAction = QAction(self.saveData.getIcon('menubar/grid.png'), lang['gridSwitch'], self.window)
            gridSwitchAction.triggered.connect(self.viewMenu_gridSwitchAction)

            gridAlignAction = QAction(self.saveData.getIcon('menubar/gridAlign.png'), lang['gridAlign'], self.window)
            gridAlignAction.triggered.connect(self.viewMenu_gridAlignAction)


            viewMenu.addAction(gridSwitchAction)
            viewMenu.addAction(gridAlignAction)

        def createHelpMenu():
            lang = self.saveData.languageData['QMainWindow']['QMenuBar']['helpMenu']['QAction']

            helpMenu: QMenu = menuBar.addMenu(self.saveData.languageData['QMainWindow']['QMenuBar']['helpMenu']['title'])

            aboutAction = QAction(QIcon('./data/themes/logo.ico'), lang['about'], self.window)
            aboutAction.triggered.connect(self.helpMenu_aboutAction)

            tipsAction = QAction(self.saveData.getIcon('menubar/tips.png'), lang['tips'], self.window)
            tipsAction.triggered.connect(self.helpMenu_tipsAction)

            aboutQtAction = QAction(self.saveData.getIcon('menubar/qt.png', mode = QSaveData.IconMode.Global), lang['aboutQt'], self.window)
            aboutQtAction.triggered.connect(self.helpMenu_aboutQtAction)


            helpMenu.addAction(aboutAction)
            helpMenu.addAction(tipsAction)
            helpMenu.addAction(aboutQtAction)


        createFileMenu()
        createViewMenu()
        createHelpMenu()

    def refreshConnectionView(self):
        self.connectionTable.clear()
        paths = {}
        nodes = []
        beginNodes = []
        errors = []

        for node in self.graph.nodes:
            if len(list(self.graph.node(node).next.keys())) > 0:
                if len(list(self.graph.node(node).previous.keys())) > 0: nodes.append(self.graph.node(node))
                else: beginNodes.append(self.graph.node(node))

        for i in range(len(nodes)):
            for x in list(nodes[i].next.keys()):
                if nodes[i].next[x].name:
                    paths[nodes[i].next[x].name] = {'value': nodes[i].next[x].value, 'previous': []}
            for y in list(nodes[i].previous.keys()):
                p = self.graph.findPath(y, nodes[i].name)
                if p:
                    if p.name:
                        for x in list(nodes[i].next.keys()):
                            if nodes[i].next[x].name:
                                if not p.name in paths[nodes[i].next[x].name]['previous']: paths[nodes[i].next[x].name]['previous'].append(p.name)
                    else:
                        for x in list(nodes[i].next.keys()):
                            for z in list(nodes[i].previous.keys()):
                                if nodes[i].name in list(self.graph.node(z).next.keys()):
                                    if self.graph.node(z).next[nodes[i].name].name == '' and self.graph.node(z).next[nodes[i].name].value == 0:
                                        for w in list(self.graph.node(z).previous.keys()):
                                            if z in list(self.graph.node(w).next.keys()):
                                                l = self.graph.node(w).next[z].name
                                                try:
                                                    if not l in paths[nodes[i].next[x].name]['previous']: paths[nodes[i].next[x].name]['previous'].append(l)
                                                except: errors.append((nodes[i].name, x))
        for i in range(len(beginNodes)):
            for x in list(beginNodes[i].next.keys()):
                paths[beginNodes[i].next[x].name] = {'value': beginNodes[i].next[x].value, 'previous': []}


        pathsLst = list(paths.keys())
        pathsLst.sort()

        for n in pathsLst:
            prevLst: list[str] = paths[n]['previous']
            prevLst.sort()

            self.connectionTable.addItem(
                items = [
                    n,
                    ', '.join(prevLst),
                    str(paths[n]['value'])
                ],
                alignmentFlag = Qt.AlignmentFlag.AlignCenter
            )

        if len(errors) > 0 and not self.saveData.liveRefreshConnectionView:
            lang = self.saveData.languageData['QMessageBox']['warning']['refreshConnectionView']

            listWidget = QBetterListWidget(headers = [lang['startNode'], lang['endNode']], minimumSectionSize = 100, alignmentFlag = Qt.AlignmentFlag.AlignCenter)
            listWidget.setMinimumHeight(100)
            for e in errors:
                listWidget.addItem(items = [str(e[0]), str(e[1])], alignmentFlag = Qt.AlignmentFlag.AlignCenter)

            dropDownWidget = QDropDownWidget(text = lang['details'], widget = listWidget)
            msgBox = QMessageBoxWithWidget(
                app = self,
                windowTitle = lang['title'],
                text = lang['text'],
                informativeText = lang['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning,
                widget = dropDownWidget
            ).exec()

    def generateMinMaxTime(self):
        for k in self.graph.nodes:
            self.graph.node(k).minTime = 0
            self.graph.node(k).maxTime = 0

        maxLoop1 = self.saveData.maxLoop
        maxLoop2 = self.saveData.maxLoop

        nodes = []
        for k in self.graph.nodes:
            if (not self.graph.node(k).previous) and self.graph.node(k).next:
                nodes.append(k)
        if not nodes: return

        while nodes and maxLoop1 > 0:
            maxLoop1 -= 1
            for n in nodes.copy():
                nodes.remove(n)
                for k in list(self.graph.node(n).next.keys()):
                    nodes.append(k)

                values = []

                for k in list(self.graph.node(n).previous.keys()):
                    values.append(self.graph.node(k).minTime + self.graph.node(k).next[n].value)
                if not values: values = [0]
                if (self.graph.node(n).minTime == 0) or (max(values) > self.graph.node(n).minTime):
                    self.graph.node(n).minTime = max(values)


        maxi = max(values)
        for k in self.graph.nodes:
            self.graph.node(k).maxTime = maxi

        nodes = []
        for k in self.graph.nodes:
            if (not self.graph.node(k).next) and self.graph.node(k).previous:
                nodes.append(k)

        while nodes and maxLoop2 > 0:
            maxLoop2 -= 1

            for n in nodes.copy():
                nodes.remove(n)
                for k in list(self.graph.node(n).previous.keys()):
                    nodes.append(k)

                values = []

                for k in list(self.graph.node(n).next.keys()):
                    values.append(self.graph.node(k).maxTime - self.graph.node(k).previous[n].next[k].value)
                if not values: values = [maxi]
                if (self.graph.node(n).maxTime == maxi) or (min(values) < self.graph.node(n).maxTime):
                    self.graph.node(n).maxTime = min(values)


        self.setUnsaved()
        self.canvas.update()

        if (maxLoop1 == 0 or maxLoop2 == 2) and not self.saveData.liveMinMax:
            lang = self.saveData.languageData['QMessageBox']['warning']['generateMinMaxTime']

            label = QLabel(
                StringUtils.replaceFirst(
                    StringUtils.replaceFirst(
                        StringUtils.replaceFirst(lang['label'], '%s', str(self.saveData.maxLoop)),
                        '%s', str(maxLoop1)
                    ),
                    '%s', str(maxLoop2)
                )
            )

            dropDownWidget = QDropDownWidget(text = lang['details'], widget = label)
            QMessageBoxWithWidget(
                app = self,
                windowTitle = lang['title'],
                text = lang['text'],
                informativeText = lang['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning,
                widget = dropDownWidget
            ).exec()

    def generateCriticalPath(self):
        if not self.saveData.liveMinMax: self.generateMinMaxTime()

        startNode = None
        for n in self.graph.nodes:
            if (not list(self.graph.node(n).previous.keys())) and (self.graph.node(n).minTime == self.graph.node(n).maxTime == 0):
                startNode = n
                break
        if not startNode: return

        endNode = startNode
        for n in self.graph.nodes:
            if (not list(self.graph.node(n).next.keys())) and (self.graph.node(n).minTime == self.graph.node(n).maxTime) and (self.graph.node(n).minTime > self.graph.node(endNode).minTime):
                endNode = n
        if endNode == startNode: return

        maxLoop = self.saveData.maxLoop
        path = [startNode]
        node = startNode
        while node != endNode and maxLoop > 0:
            maxLoop -= 1
            allNodes = []
            for n in list(self.graph.node(node).next.keys()):
                if self.graph.node(n).minTime == self.graph.node(n).maxTime:
                    allNodes.append(n)

            if not allNodes: continue
            minNode = allNodes[0]
            allNodes.pop()
            for n in allNodes:
                if self.graph.node(n).minTime < self.graph.node(minNode).minTime:
                    minNode = n

            path.append(minNode)
            node = minNode

        self.criticalPathTable.clear()

        for n in path:
            self.criticalPathTable.addItem(items = [n], alignmentFlag = Qt.AlignmentFlag.AlignCenter)


        if (maxLoop == 0) and not self.saveData.liveGenerateCriticalPath:
            lang = self.saveData.languageData['QMessageBox']['warning']['generateCriticalPath']

            label = QLabel(StringUtils.replaceFirst(lang['label'], '%s', str(self.saveData.maxLoop)))

            dropDownWidget = QDropDownWidget(text = lang['details'], widget = label)
            QMessageBoxWithWidget(
                app = self,
                windowTitle = lang['title'],
                text = lang['text'],
                informativeText = lang['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning,
                widget = dropDownWidget
            ).exec()


    def createConnectionViewMenu(self):
        lang = self.saveData.languageData['QDockWidget']['connectionView']['QBetterListWidget']

        self.connectionTable = QBetterListWidget(headers = [lang['task'], lang['previousTasks'], lang['time']], minimumSectionSize = 100, alignmentFlag = Qt.AlignmentFlag.AlignCenter)
        self.connectionViewMenu.scrollLayout.addWidget(self.connectionTable, 0, 0)

    def createCriticalPathViewMenu(self):
        lang = self.saveData.languageData['QDockWidget']['criticalPathView']['QBetterListWidget']

        self.criticalPathTable = QBetterListWidget(headers = [lang['criticalPath']], minimumSectionSize = 100, alignmentFlag = Qt.AlignmentFlag.AlignCenter)
        self.criticalPathViewMenu.scrollLayout.addWidget(self.criticalPathTable, 0, 0)

    def createGenerationMenu(self):
        lang = self.saveData.languageData['QDockWidget']['generation']

        def rcvValueChanged(value: int):
            if value: self.saveData.liveRefreshConnectionView = True
            else: self.saveData.liveRefreshConnectionView = False

        def mmValueChanged(value: int):
            if value: self.saveData.liveMinMax = True
            else: self.saveData.liveMinMax = False

        def gcpValueChanged(value: int):
            if value: self.saveData.liveGenerateCriticalPath = True
            else: self.saveData.liveGenerateCriticalPath = False

        refreshConnectionViewButton = QPushButton(lang['QPushButton']['refreshConnectionView'])
        refreshConnectionViewButton.clicked.connect(self.refreshConnectionView)
        liveRefreshConnectionViewCheckbox = QCheckBox(lang['QCheckBox']['liveRefreshConnectionView'])
        if self.saveData.liveRefreshConnectionView: liveRefreshConnectionViewCheckbox.setCheckState(Qt.CheckState.Checked)
        liveRefreshConnectionViewCheckbox.stateChanged.connect(rcvValueChanged)

        generateMinMaxTimeButton = QPushButton(lang['QPushButton']['generateMinMaxTime'])
        generateMinMaxTimeButton.clicked.connect(self.generateMinMaxTime)
        liveGenerateMinMaxCheckbox = QCheckBox(lang['QCheckBox']['liveGenerateMinMax'])
        if self.saveData.liveMinMax: liveGenerateMinMaxCheckbox.setCheckState(Qt.CheckState.Checked)
        liveGenerateMinMaxCheckbox.stateChanged.connect(mmValueChanged)

        generateCriticalPathButton = QPushButton(lang['QPushButton']['generateCriticalPath'])
        generateCriticalPathButton.clicked.connect(self.generateCriticalPath)
        liveGenerateCriticalPathCheckbox = QCheckBox(lang['QCheckBox']['liveGenerateCriticalPath'])
        if self.saveData.liveGenerateCriticalPath: liveGenerateCriticalPathCheckbox.setCheckState(Qt.CheckState.Checked)
        liveGenerateCriticalPathCheckbox.stateChanged.connect(gcpValueChanged)


        self.generationMenu.scrollLayout.addWidget(refreshConnectionViewButton, 0, 0)
        self.generationMenu.scrollLayout.addWidget(liveRefreshConnectionViewCheckbox, 0, 1)
        self.generationMenu.scrollLayout.addWidget(generateMinMaxTimeButton, 1, 0)
        self.generationMenu.scrollLayout.addWidget(liveGenerateMinMaxCheckbox, 1, 1)
        self.generationMenu.scrollLayout.addWidget(generateCriticalPathButton, 2, 0)
        self.generationMenu.scrollLayout.addWidget(liveGenerateCriticalPathCheckbox, 2, 1)

    def propertiesMenuLoad(self):
        lang = self.saveData.languageData['QDockWidget']['properties']

        def editName(name: str):
            if not name: return
            if name in self.graph.nodes: return
            self.graph.rename(self.selectedItem.name, name)
            self.canvas.update()
            self.setUnsaved()

        def editMinTime(value: float):
            if value.as_integer_ratio()[1] == 1: self.selectedItem.minTime = int(value)
            else: self.selectedItem.minTime = value
            self.canvas.update()
            self.setUnsaved()

        def editMaxTime(value: float):
            if value.as_integer_ratio()[1] == 1: self.selectedItem.maxTime = int(value)
            else: self.selectedItem.maxTime = value
            self.canvas.update()
            self.setUnsaved()

        for i in reversed(range(self.propertiesMenu.scrollLayout.count())):
            self.propertiesMenu.scrollLayout.itemAt(i).widget().deleteLater()
        if not self.selectedItem: return

        minTimeSpinbox = QDoubleSpinBoxWithLabel(lang['QSpinBoxWithLabel']['QLabel']['minTime'])
        minTimeSpinbox.spinBox.setValue(self.selectedItem.minTime)
        minTimeSpinbox.spinBox.valueChanged.connect(editMinTime)

        self.propertiesMenu.scrollLayout.addWidget(minTimeSpinbox, 0, 0)
        self.propertiesMenu.scrollLayout.setAlignment(minTimeSpinbox, Qt.AlignmentFlag.AlignTop)


        maxTimeSpinbox = QDoubleSpinBoxWithLabel(lang['QSpinBoxWithLabel']['QLabel']['maxTime'])
        maxTimeSpinbox.spinBox.setValue(self.selectedItem.maxTime)
        maxTimeSpinbox.spinBox.valueChanged.connect(editMaxTime)

        self.propertiesMenu.scrollLayout.addWidget(maxTimeSpinbox, 0, 1)
        self.propertiesMenu.scrollLayout.setAlignment(maxTimeSpinbox, Qt.AlignmentFlag.AlignTop)


        nameEntry = QLineEditWithLabel(lang['QLineEditWithLabel']['QLabel']['displayName'])
        nameEntry.lineEdit.setText(self.selectedItem.name)
        nameEntry.lineEdit.textChanged.connect(editName)

        self.propertiesMenu.scrollLayout.addWidget(nameEntry, 1, 0)
        self.propertiesMenu.scrollLayout.setAlignment(nameEntry, Qt.AlignmentFlag.AlignTop)


        lst = list(self.selectedItem.next.keys())
        if not lst: return

        nodeCombobox = QComboBoxWithLabel(lang['QComboBoxWithLabel']['QLabel']['node'])

        self.propertiesMenu.scrollLayout.addWidget(nodeCombobox, 1, 1)
        self.propertiesMenu.scrollLayout.setAlignment(nodeCombobox, Qt.AlignmentFlag.AlignTop)


        nodeGroupbox = QGridGroupBox()

        nodeCombobox.comboBox.addItems(lst)
        if lst:
            nodeCombobox.comboBox.setCurrentIndex(0)
            self.propertiesMenuNodeGroupboxLoad(nodeGroupbox, lst[0])
            self.selectedNode = lst[0]

        nodeCombobox.comboBox.currentIndexChanged.connect(lambda i: self.propertiesMenuNodeGroupboxLoad(nodeGroupbox, lst[i]))

        self.propertiesMenu.scrollLayout.addWidget(nodeGroupbox, 2, 0, 1, 2)
        self.propertiesMenu.scrollLayout.setAlignment(nodeGroupbox, Qt.AlignmentFlag.AlignTop)
    
    def propertiesMenuNodeGroupboxLoad(self, groupbox: QGridGroupBox, key: str):
        lang = self.saveData.languageData['QDockWidget']['properties']
        self.selectedNode = key

        def editName(name: str):
            self.selectedItem.next[key].name = name
            self.canvas.update()
            self.setUnsaved()

        def editValue(value: float):
            if value.as_integer_ratio()[1] == 1: self.selectedItem.next[key].value = int(value)
            else: self.selectedItem.next[key].value = value
            self.canvas.update()
            self.setUnsaved()

        def removeConnection(event = None):
            self.graph.removeConnection(self.selectedItem.name, key)
            self.canvas.update()
            self.propertiesMenuLoad()
            self.setUnsaved()

        for i in reversed(range(groupbox.gridLayout.count())):
            groupbox.gridLayout.itemAt(i).widget().deleteLater()

        groupbox.setTitle(lang['QGroupBox']['pathToNodeX'].replace('%s', key))

        nameEntry = QLineEditWithLabel(lang['QLineEditWithLabel']['QLabel']['displayName'])
        nameEntry.lineEdit.setText(self.selectedItem.next[key].name)
        nameEntry.lineEdit.textChanged.connect(editName)
        valueSpinbox = QDoubleSpinBoxWithLabel(lang['QSpinBoxWithLabel']['QLabel']['id'])
        valueSpinbox.spinBox.setValue(self.selectedItem.next[key].value)
        valueSpinbox.spinBox.valueChanged.connect(editValue)

        deleteButton = QPushButton(lang['QPushButton']['deleteConnection'])
        deleteButton.clicked.connect(removeConnection)

        groupbox.gridLayout.addWidget(nameEntry, 0, 0)
        groupbox.gridLayout.setAlignment(nameEntry, Qt.AlignmentFlag.AlignTop)
        groupbox.gridLayout.addWidget(valueSpinbox, 0, 1)
        groupbox.gridLayout.setAlignment(valueSpinbox, Qt.AlignmentFlag.AlignTop)
        groupbox.gridLayout.addWidget(deleteButton, 1, 0, 1, 2)
        groupbox.gridLayout.setAlignment(deleteButton, Qt.AlignmentFlag.AlignTop)

        self.canvas.update()

    def loadColors(self):
        def find(keyWord: str = ''):
            keyWord += '{'

            start = data.find(keyWord)
            if start == -1: return ''

            end = data[start:].find('}')
            if end == -1: return ''

            return data[start + len(keyWord) : start + end]


        def getVariable(qss: str = '', varName: str = ''):
            varName += ':'

            start = qss.find(f'{varName}')
            if start == -1: return ''

            end = qss[start:].find(';')
            if end == -1: return ''

            return qss[start + len(varName) : start + end]


        data = (
            self.saveData.getStyleSheet(app = self, mode = QSaveData.StyleSheetMode.Local) + '\n' +
            self.saveData.getStyleSheet(app = self, mode = QSaveData.StyleSheetMode.Global)
        ).replace(' ', '').replace('\t', '').replace('\n', '')

        normalColor = getVariable(find('QPen'), 'color')
        focusColor = getVariable(find('QPen:focus'), 'color')
        selectedColor = getVariable(find('QPen:selected'), 'color')
        gridColor = getVariable(find('QPen::grid'), 'color')
        linkColor = getVariable(find('QLabel::link'), 'color')

        if normalColor: self.COLOR_NORMAL = Color(normalColor)
        if focusColor: self.COLOR_FOCUS = Color(focusColor)
        if selectedColor: self.COLOR_SELECTED = Color(selectedColor)
        if gridColor: self.COLOR_GRID = Color(gridColor)
        if linkColor: self.COLOR_LINK = Color(linkColor)


    def setUnsaved(self):
        self.unsaved = True
        self.updateTitle()

    def setSaved(self):
        self.unsaved = False
        self.updateTitle()

    def updateTitle(self):
        s = ''
        if self.unsaved: s = '*'
        if self.SAVE_PATH: self.window.setWindowTitle(self.saveData.languageData['QMainWindow']['title'] + f' | Version: {self.VERSION} | Build: {self.BUILD} - {self.SAVE_PATH}{s}')
        else: self.window.setWindowTitle(self.saveData.languageData['QMainWindow']['title'] + f' | Version: {self.VERSION} | Build: {self.BUILD} - NewPERT{s}')



    def eventFilter(self, source, event: QMouseEvent|QWheelEvent):
        if source is self.canvas:
            match event.type():
                case QEvent.Type.MouseButtonPress:
                    if event.button() == Qt.MouseButton.LeftButton: self.canvasLMBPressEvent(event)
                    elif event.button() == Qt.MouseButton.RightButton: self.canvasRMBPressEvent(event)
                    elif event.button() == Qt.MouseButton.MiddleButton: self.canvasMMBPressEvent(event)

                case QEvent.Type.MouseMove:
                    if event.buttons() == Qt.MouseButton.LeftButton: self.canvasLMBMoveEvent(event)
                    #elif event.buttons() == Qt.MouseButton.RightButton: self.canvasRMBMoveEvent(event)
                    elif event.buttons() == Qt.MouseButton.MiddleButton: self.canvasMMBMoveEvent(event)

                case QEvent.Type.MouseButtonRelease:
                    #if event.button() == Qt.MouseButton.LeftButton: self.canvasLMBReleaseEvent(event)
                    #elif event.button() == Qt.MouseButton.RightButton: self.canvasRMBReleaseEvent(event)
                    if event.button() == Qt.MouseButton.MiddleButton: self.canvasMMBReleaseEvent(event)

                case QEvent.Type.Paint: self.canvasPaintEvent(event)

                case QEvent.Type.Wheel:
                    self.canvasWheelEvent(event)
            

        return super(Application, self).eventFilter(source, event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete:
            if self.selectedItem:
                self.graph.removeNode(self.selectedItem.name)
                self.selectedItem = None
                self.selectedNode = None
                self.propertiesMenuLoad()
                self.canvas.update()
        elif event.key() == Qt.Key.Key_Shift:
            self.shiftKey = True

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Shift:
            self.shiftKey = False



    def Vector2ToQPoint(self, vect2: Vector2 = Vector2()):
        return QPoint(int(vect2.x), int(vect2.y))

    def canvasPaintEvent(self, event: QMouseEvent):
        qp = QPainter()
        qp.begin(self.canvas)
        self.canvasDrawPoints(qp)
        qp.end()

    def canvasDrawPoints(self, qp: QPainter):
        if self.saveData.gridMode > 0:
            size = Vector2(self.canvas.size().width(), self.canvas.size().height())
            startPos = self.cameraPos % self.saveData.gridSize
            nb = (size // self.saveData.gridSize) + 1

            if self.saveData.gridMode == 1:
                offset = self.cameraPos // self.saveData.gridSize

                for n in range(int(nb.x)):
                    if (n - offset.x) % 5 == 0:
                        qp.setPen(QPen(self.COLOR_GRID.toQColor(), 2))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.SolidLine)
                        qp.setPen(pen)
                    else:
                        qp.setPen(QPen(self.COLOR_GRID.toQColor(), 1))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.CustomDashLine)
                        pen.setDashPattern([4, 4])
                        qp.setPen(pen)
                    qp.drawLine(
                        self.Vector2ToQPoint(Vector2((n * self.saveData.gridSize) + startPos.x, 0)),
                        self.Vector2ToQPoint(Vector2((n * self.saveData.gridSize) + startPos.x, size.y))
                    )

                for n in range(int(nb.y)):
                    if (n - offset.y) % 5 == 0:
                        qp.setPen(QPen(self.COLOR_GRID.toQColor(), 2))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.SolidLine)
                        qp.setPen(pen)
                    else:
                        qp.setPen(QPen(self.COLOR_GRID.toQColor(), 1))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.CustomDashLine)
                        pen.setDashPattern([4, 4])
                        qp.setPen(pen)
                    qp.drawLine(
                        self.Vector2ToQPoint(Vector2(0, (n * self.saveData.gridSize) + startPos.y)),
                        self.Vector2ToQPoint(Vector2(size.x, (n * self.saveData.gridSize) + startPos.y))
                    )

            elif self.saveData.gridMode == 2:
                offset = (self.cameraPos // self.saveData.gridSize) % 2

                qp.setPen(QPen(self.COLOR_GRID.toQColor(), 1))
                brush = QBrush(self.COLOR_GRID.toQColor())
                brush.setStyle(Qt.BrushStyle.SolidPattern)
                qp.setBrush(brush)
                for x in range(-int(offset.x), int(nb.x) + 1, 2):
                    for y in range(-1, int(nb.y) + 1):
                        rectPos = Vector2((x * self.saveData.gridSize) + startPos.x - self.saveData.gridSize, (y * self.saveData.gridSize) + startPos.y - self.saveData.gridSize)
                        if (y % 2) == 0: rectPos.x += self.saveData.gridSize
                        if offset.y: rectPos.y += self.saveData.gridSize
                        qp.drawRect(int(rectPos.x), int(rectPos.y), self.saveData.gridSize, self.saveData.gridSize)




        if self.saveData.liveRefreshConnectionView: self.refreshConnectionView()
        if self.saveData.liveGenerateCriticalPath: self.generateCriticalPath()
        if self.saveData.liveMinMax: self.generateMinMaxTime()

        for k in self.graph.nodes:
            p = self.graph.node(k)
            if p == self.selectedItem: qp.setPen(QPen(self.COLOR_FOCUS.toQColor(), 3))
            else: qp.setPen(QPen(self.COLOR_NORMAL.toQColor(), 2))
            qp.drawEllipse(int(self.cameraPos.x + p.pos.x) - (self.DELTA // 2), int(self.cameraPos.y + p.pos.y) - (self.DELTA // 2), self.DELTA, self.DELTA)
            qp.drawLine(self.Vector2ToQPoint(self.cameraPos + p.pos), self.Vector2ToQPoint(self.cameraPos + Vector2(p.pos.x, p.pos.y - (self.DELTA / 2))))
            qp.drawLine(self.Vector2ToQPoint(self.cameraPos + Vector2(p.pos.x - (self.DELTA / 2), p.pos.y)), self.Vector2ToQPoint(self.cameraPos + Vector2(p.pos.x + (self.DELTA / 2), p.pos.y)))
            qp.drawText(self.Vector2ToQPoint(self.cameraPos + Vector2(p.pos.x - (qp.font().weight() / 135 * len(p.name)), p.pos.y + (self.DELTA / 4))), p.name)
            qp.drawText(self.Vector2ToQPoint(self.cameraPos + Vector2(p.pos.x - (self.DELTA / 5) - (qp.font().weight() / 135 * len(str(p.minTime))), p.pos.y - (self.DELTA / 6))), str(p.minTime))
            qp.drawText(self.Vector2ToQPoint(self.cameraPos + Vector2(p.pos.x + (self.DELTA / 5) - (qp.font().weight() / 135 * len(str(p.maxTime))), p.pos.y - (self.DELTA / 6))), str(p.maxTime))

            for pathKey in list(p.next.keys()):
                if p == self.selectedItem:
                    if pathKey == self.selectedNode: qp.setPen(QPen(self.COLOR_SELECTED.toQColor(), 3))
                    else: qp.setPen(QPen(self.COLOR_FOCUS.toQColor(), 3))
                path = p.next[pathKey]
                if (path.value == 0 and path.name == ''):
                    pen = qp.pen()
                    pen.setStyle(Qt.PenStyle.CustomDashLine)
                    pen.setDashPattern([4, 4])
                    qp.setPen(pen)

                vect2 = (path.node.pos - p.pos).normalized * (self.DELTA // 2)
                qp.drawLine(self.Vector2ToQPoint(self.cameraPos + p.pos + vect2), self.Vector2ToQPoint(self.cameraPos + path.node.pos - vect2))

                pen = qp.pen()
                pen.setStyle(Qt.PenStyle.SolidLine)
                qp.setPen(pen)

                qp.drawLine(self.Vector2ToQPoint(self.cameraPos + path.node.pos - vect2), self.Vector2ToQPoint(self.cameraPos + path.node.pos - vect2 - (deg2Vector2(absoluteDeg(vect2.normalized.convert2Deg + 25)) * 10)))
                qp.drawLine(self.Vector2ToQPoint(self.cameraPos + path.node.pos - vect2), self.Vector2ToQPoint(self.cameraPos + path.node.pos - vect2 - (deg2Vector2(absoluteDeg(vect2.normalized.convert2Deg - 25)) * 10)))
                if not (path.value == 0 and path.name == ''): qp.drawText(self.Vector2ToQPoint(self.cameraPos + path.node.pos - ((path.node.pos - p.pos) / 2) - (deg2Vector2(absoluteDeg(vect2.normalized.convert2Deg + 90)) * 20)), f'{path.name} {path.value}')

    def canvasGetPoint(self, event: QMouseEvent):
        return Vector2(event.pos().x(), event.pos().y())

    def canvasGetNode(self, event: QMouseEvent):
        point = self.canvasGetPoint(event) - self.cameraPos

        nodeLst = self.graph.nodes
        dist = nodeLst[0]
        for p in nodeLst[1:]:
            if (self.graph.node(p).pos - point).magnitude < (self.graph.node(dist).pos - point).magnitude: dist = p

        if (self.graph.node(dist).pos - point).magnitude <= (self.DELTA // 2):
            return self.graph.node(dist)

    def canvasRMBPressEvent(self, event: QMouseEvent):
        if self.selectedItem:
            node = self.canvasGetNode(event)
            if node: self.graph.addConnection(self.selectedItem.name, node.name)
            else: self.canvasCreateNode(event)
        else: self.canvasCreateNode(event)
        self.propertiesMenuLoad()
        self.canvas.update()
        self.setUnsaved()

    def canvasCreateNode(self, event: QMouseEvent):
        s = '0'
        while s in self.graph.nodes:
            s = str(int(s) + 1)
        self.graph.addNode(name = s, pos = self.canvasGetPoint(event) - self.cameraPos)
        if self.selectedItem: self.graph.addConnection(self.selectedItem.name, s)
        self.selectedItem = self.graph.node(s)
        if self.saveData.alignToGrid: self.selectedItem.pos -= (self.selectedItem.pos % self.saveData.gridSize)

    def canvasLMBPressEvent(self, event: QMouseEvent):
        self.selectedItem = None
        self.selectedNode = None
        if not self.graph.nodes:
            self.propertiesMenuLoad()
            return self.canvas.update()

        self.selectedItem = self.canvasGetNode(event)

        self.propertiesMenuLoad()
        self.canvas.update()

    def canvasLMBMoveEvent(self, event: QMouseEvent):
        if not self.selectedItem: return
        self.selectedItem.pos = self.canvasGetPoint(event) - self.cameraPos
        if self.saveData.alignToGrid: self.selectedItem.pos -= (self.selectedItem.pos % self.saveData.gridSize)

        self.canvas.update()
        self.setUnsaved()

    def canvasMMBPressEvent(self, event: QMouseEvent):
        self.setOverrideCursor(Qt.CursorShape.SizeAllCursor)
        self.oldMousePos = self.canvasGetPoint(event)

    def canvasMMBMoveEvent(self, event: QMouseEvent):
        pos = self.canvasGetPoint(event)
        self.cameraPos += pos - self.oldMousePos
        self.oldMousePos = pos

        self.canvas.update()

    def canvasMMBReleaseEvent(self, event: QMouseEvent):
        self.setOverrideCursor(Qt.CursorShape.ArrowCursor)

    def canvasWheelEvent(self, event: QWheelEvent):
        if self.shiftKey: self.cameraPos += Vector2(event.angleDelta().y(), event.angleDelta().x())
        else: self.cameraPos += Vector2(event.angleDelta().x(), event.angleDelta().y())
        self.canvas.update()


    def fileMenu_newAction(self):
        self.selectedItem = None
        self.selectedNode = None
        del self.graph
        self.graph = Graph()
        self.SAVE_PATH = None

        self.propertiesMenuLoad()
        self.canvas.update()
        self.setUnsaved()

    def fileMenu_openAction(self):
        lang = self.saveData.languageData['QFileDialog']['open']

        path = QFileDialog.getOpenFileName(
            parent = self.window,
            directory = './',
            caption = lang['title'],
            filter = 'Python PERT (*.pypert)'
        )[0]

        if not path: return
        self.SAVE_PATH = path
        self.selectedNode = None
        self.selectedItem = None

        with open(self.SAVE_PATH, 'r', encoding = 'utf-8') as infile:
            self.graph.loadFromDict(json.load(infile))

        self.propertiesMenuLoad()
        self.canvas.update()

        self.setSaved()

    def fileMenu_saveAction(self):
        if not self.SAVE_PATH:
            return self.fileMenu_saveAsAction()

        with open(self.SAVE_PATH, 'w', encoding = 'utf-8') as outfile:
            json.dump(self.graph.toDict(), outfile, indent = 4, sort_keys = True, ensure_ascii = False)

        self.setSaved()

    def fileMenu_saveAsAction(self):
        lang = self.saveData.languageData['QFileDialog']['saveAs']

        path = QFileDialog.getSaveFileName(
            parent = self.window,
            directory = './',
            caption = lang['title'],
            filter = 'Python PERT (*.pypert)'
        )[0]

        if not path: return
        self.SAVE_PATH = path
        self.fileMenu_saveAction()

    def fileMenu_settingsAction(self):
        self.saveData.settingsMenu(self)
        self.loadColors()


    def viewMenu_gridSwitchAction(self):
        self.saveData.gridMode += 1
        if self.saveData.gridMode > 2: self.saveData.gridMode = 0
        self.saveData.save()

        self.canvas.update()

    def viewMenu_gridAlignAction(self):
        self.saveData.alignToGrid = not self.saveData.alignToGrid
        self.saveData.save()


    def helpMenu_aboutAction(self):
        lang = self.saveData.languageData['QAbout']['pertMaker']
        QAboutBox(
            app = self,
            windowTitle = lang['title'],
            logo = './data/themes/logoNoBg.ico',
            texts = [
                QLabel(lang['texts'][0]),
                QLabel(lang['texts'][1].replace('%s', f'<a href=\"https://github.com/Synell\" style=\"color: {self.COLOR_LINK.toHex()};\">Synel</a>')),
                QLabel(lang['texts'][2].replace('%s', f'<a href=\"https://github.com/Synell/PERT-Maker\" style=\"color: {self.COLOR_LINK.toHex()};\">PERT Maker Github</a>'))
            ]
        ).exec()

    def helpMenu_tipsAction(self):
        QDesktopServices.openUrl(QUrl('https://github.com/Synell/PERT-Maker/blob/main/README.md'))

    def helpMenu_aboutQtAction(self):
        self.aboutQt()




class ApplicationError(QApplication):
    def __init__(self, err: str = ''):
        super().__init__(argv)
        self.window = QMainWindow()
        self.window.setWindowTitle('PERT Maker - Error')
        QMessageBoxWithWidget(
            app = self,
            title = 'PERT Maker - Error',
            text = 'Oups, something went wrong...',
            informativeText = str(err),
            icon = QMessageBoxWithWidget.Icon.Critical
        ).exec()
        exit(argv)



try:
    app = Application()
    app.window.showMaximized()

    exit(app.exec())

except Exception as err:
    print(err)
    app = ApplicationError(err)
