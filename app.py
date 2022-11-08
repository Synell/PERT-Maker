#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtSvg import *
from math import *
from datetime import datetime, timedelta
import json, sys
from data.lib import *
#----------------------------------------------------------------------

    # Class
class Application(QBaseApplication):
    BUILD = '07e6e939'
    VERSION = 'Experimental'

    DELTA = 80

    COLOR_NORMAL = QUtilsColor()
    COLOR_FOCUS = QUtilsColor()
    COLOR_SELECTED = QUtilsColor()
    COLOR_GRID = QUtilsColor()

    SAVE_PATH = None

    MESSAGE_DURATION = 5000

    ALERT_RAISE_DURATION = 350
    ALERT_PAUSE_DURATION = 2300
    ALERT_FADE_DURATION = 350

    UPDATE_LINK = 'https://github.com/Synell/PERT-Maker'

    KEY_WORDS = ['Start', 'End']

    ZOOM_MIN = 0.25
    ZOOM_MAX = 4.0

    def __init__(self, platform: QPlatform) -> None:
        super().__init__(platform = platform)

        self.must_update = None
        self.must_update_link = None

        self.selected_item = None
        self.selected_node = None
        self.unsaved = False

        self.use_node_names = True

        self.shift_key = False
        self.control_key = False

        self.zoom = 1 # TODO: find the freaking formula to do this

        self.camera_pos = Vector2()
        self.old_mouse_pos = Vector2()

        self.graph = Graph()

        self.save_data = SaveData()

        self.window.setProperty('color', 'magenta')

        self.save_data.setStyleSheet(self)

        self.load_colors()

        self.setWindowIcon(QIcon('./data/themes/logo.ico'))

        self.create_widgets()
        self.file_menu_new_action()

        if self.save_data.check_for_updates == 4: self.check_updates()
        elif self.save_data.check_for_updates > 0 and self.save_data.check_for_updates < 4:
            deltatime = datetime.now() - self.save_data.last_check_for_updates

            match self.save_data.check_for_updates:
                case 1:
                    if deltatime > timedelta(days = 1): self.check_updates()
                case 2:
                    if deltatime > timedelta(weeks = 1): self.check_updates()
                case 3:
                    if deltatime > timedelta(weeks = 4): self.check_updates()

    def not_implemented(self, text = ''):
        if text:
            w = QDropDownWidget(text = lang['details'], widget = QLabel(text))
        else: w = None

        lang = self.save_data.language_data['QMessageBox']['critical']['notImplemented']

        QMessageBoxWithWidget(
            app = self,
            title = lang['title'],
            text = lang['text'],
            icon = QMessageBoxWithWidget.Icon.Critical,
            widget = w
        ).exec()

    def create_widgets(self):
        self.root = QGridWidget()
        self.root.grid_layout.setSpacing(0)
        self.root.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.canvas = QWidget()
        self.canvas.setMinimumSize(600, 400)
        self.root.grid_layout.addWidget(self.canvas, 0, 0)
        self.canvas.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.canvas.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)


        self.status_bar = QStatusBar()
        self.window.setStatusBar(self.status_bar)


        self.status_bar.coordinates_label = QLabel()
        self.status_bar.coordinates_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.addPermanentWidget(self.status_bar.coordinates_label, 2)


        empty_widget = QGridWidget()
        empty_widget.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setSpacing(0)
        self.status_bar.addPermanentWidget(empty_widget, 2)

        self.update_button = QPushButton(self.save_data.language_data['QStatusBar']['QPushButton']['update'])
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.clicked.connect(self.update_click)
        self.update_button.setProperty('color', 'main')
        self.update_button.setProperty('transparent', True)
        empty_widget.grid_layout.addWidget(self.update_button, 0, 0)
        self.update_button.setVisible(False)


        empty_widget = QGridWidget()
        empty_widget.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setSpacing(0)
        self.status_bar.addPermanentWidget(empty_widget, 12)


        empty_widget = QGridWidget()
        empty_widget.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setSpacing(0)
        self.status_bar.addPermanentWidget(empty_widget, 3)

        self.status_bar.progress_bar = QProgressBar()
        self.status_bar.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.progress_bar.setRange(0, 100)
        self.status_bar.progress_bar.setValue(0)
        self.status_bar.progress_bar.setProperty('class', 'small')
        self.status_bar.progress_bar.setHidden(True)
        empty_widget.grid_layout.addWidget(self.status_bar.progress_bar)


        empty_widget = QGridWidget()
        empty_widget.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        empty_widget.grid_layout.setSpacing(0)
        self.status_bar.addPermanentWidget(empty_widget, 1)


        self.status_bar.zoom = QGridWidget()
        self.status_bar.zoom.setContentsMargins(0, 0, 0, 0)
        self.status_bar.zoom.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.status_bar.zoom.grid_layout.setSpacing(0)

        self.status_bar.zoom.zoom_min = QToolButton()
        self.status_bar.zoom.zoom_min.setIcon(self.save_data.getIcon('statusbar/zoomMin.png'))
        self.status_bar.zoom.zoom_min.clicked.connect(self.zoom_min)
        self.status_bar.zoom.grid_layout.addWidget(self.status_bar.zoom.zoom_min, 0, 0)

        self.status_bar.zoom.zoom_out = QToolButton()
        self.status_bar.zoom.zoom_out.setIcon(self.save_data.getIcon('statusbar/zoomOut.png'))
        self.status_bar.zoom.zoom_out.clicked.connect(self.zoom_out)
        self.status_bar.zoom.grid_layout.addWidget(self.status_bar.zoom.zoom_out, 0, 1)

        self.status_bar.zoom.zoom_slider = QSlider()
        self.status_bar.zoom.zoom_slider.setOrientation(Qt.Orientation.Horizontal)
        self.status_bar.zoom.zoom_slider.setRange(25, 400)
        self.status_bar.zoom.zoom_slider.valueChanged.connect(self.zoom_slider_value_changed)
        self.status_bar.zoom.grid_layout.addWidget(self.status_bar.zoom.zoom_slider, 0, 2)

        self.status_bar.zoom.zoom_in = QToolButton()
        self.status_bar.zoom.zoom_in.setIcon(self.save_data.getIcon('statusbar/zoomIn.png'))
        self.status_bar.zoom.zoom_in.clicked.connect(self.zoom_in)
        self.status_bar.zoom.grid_layout.addWidget(self.status_bar.zoom.zoom_in, 0, 3)

        self.status_bar.zoom.zoom_max = QToolButton()
        self.status_bar.zoom.zoom_max.setIcon(self.save_data.getIcon('statusbar/zoomMax.png'))
        self.status_bar.zoom.zoom_max.clicked.connect(self.zoom_max)
        self.status_bar.zoom.grid_layout.addWidget(self.status_bar.zoom.zoom_max, 0, 4)

        self.status_bar.zoom.zoom_level = QLabel()
        self.status_bar.zoom.grid_layout.addWidget(self.status_bar.zoom.zoom_level, 0, 5)

        self.update_zoom()

        self.status_bar.addPermanentWidget(self.status_bar.zoom, 6)



        self.properties_menu = QScrollableGridWidget()
        self.properties_menu.setProperty('wide', True)
        self.properties_menu.setMinimumWidth(300)
        self.properties_menu.setMinimumHeight(200)
        self.properties_menu.setFrameShape(QFrame.Shape.NoFrame)
        self.properties_menu.scroll_widget.setProperty('QDockWidget', True)
        
        self.properties_menu_dock_widget = QDockWidget(self.save_data.language_data['QDockWidget']['properties']['title'])
        self.properties_menu_dock_widget.setWidget(self.properties_menu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_menu_dock_widget)


        self.connection_view_menu = QScrollableGridWidget()
        self.connection_view_menu.setMinimumWidth(450)
        self.connection_view_menu.setMinimumHeight(200)
        self.connection_view_menu.setFrameShape(QFrame.Shape.NoFrame)
        self.connection_view_menu.scroll_widget.setProperty('QDockWidget', True)
        
        self.connection_view_menu_dock_widget = QDockWidget(self.save_data.language_data['QDockWidget']['connectionView']['title'])
        self.connection_view_menu_dock_widget.setWidget(self.connection_view_menu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.connection_view_menu_dock_widget)

        self.create_connection_view_menu()


        self.critical_path_view_menu = QScrollableGridWidget()
        self.critical_path_view_menu.setMinimumWidth(450)
        self.critical_path_view_menu.setMinimumHeight(200)
        self.critical_path_view_menu.setFrameShape(QFrame.Shape.NoFrame)
        self.critical_path_view_menu.scroll_widget.setProperty('QDockWidget', True)
        
        self.critical_path_view_menu_dock_widget = QDockWidget(self.save_data.language_data['QDockWidget']['criticalPathView']['title'])
        self.critical_path_view_menu_dock_widget.setWidget(self.critical_path_view_menu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.critical_path_view_menu_dock_widget)

        self.create_critical_path_view_menu()


        self.window.tabifyDockWidget(self.connection_view_menu_dock_widget, self.critical_path_view_menu_dock_widget)
        self.connection_view_menu_dock_widget.raise_()


        self.generation_menu = QScrollableGridWidget()
        self.generation_menu.setMinimumWidth(450)
        self.generation_menu.setMinimumHeight(200)
        self.generation_menu.setFrameShape(QFrame.Shape.NoFrame)
        self.generation_menu.scroll_widget.setProperty('QDockWidget', True)
        
        self.generation_menuDockWidget = QDockWidget(self.save_data.language_data['QDockWidget']['generation']['title'])
        self.generation_menuDockWidget.setWidget(self.generation_menu)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.generation_menuDockWidget)

        self.create_generation_menu()


        self.window.setCentralWidget(self.root)


        self.canvas.installEventFilter(self)
        self.canvas.setMouseTracking(True)
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.window.keyPressEvent = self.key_press_event
        self.window.keyReleaseEvent = self.key_release_event

        self.create_menu_bar()

        self.canvas.update()

    def create_menu_bar(self):
        menuBar = self.window.menuBar()

        def create_file_menu():
            lang = self.save_data.language_data['QMainWindow']['QMenuBar']['fileMenu']['QAction']

            file_menu: QMenu = menuBar.addMenu(self.save_data.language_data['QMainWindow']['QMenuBar']['fileMenu']['title'])

            def create_import_menu():
                lang = self.save_data.language_data['QMainWindow']['QMenuBar']['fileMenu']['QMenu']['importMenu']['QAction']

                import_menu = QMenu(self.save_data.language_data['QMainWindow']['QMenuBar']['fileMenu']['QMenu']['importMenu']['title'], self.window)
                import_menu.setIcon(self.save_data.getIcon('menubar/import.png'))

                table_action = QAction(lang['table'], self.window)
                table_action.triggered.connect(self.file_menu_import_menu_table_action)

                import_menu.addAction(table_action)

                return import_menu

            def create_export_menu():
                lang = self.save_data.language_data['QMainWindow']['QMenuBar']['fileMenu']['QMenu']['exportMenu']['QAction']

                export_menu = QMenu(self.save_data.language_data['QMainWindow']['QMenuBar']['fileMenu']['QMenu']['exportMenu']['title'], self.window)
                export_menu.setIcon(self.save_data.getIcon('menubar/export.png'))

                table_action = QAction(lang['table'], self.window)
                table_action.triggered.connect(self.file_menu_export_menu_table_action)

                image_action = QAction(lang['image'], self.window)
                image_action.triggered.connect(self.file_menu_export_menu_image_action)

                export_menu.addAction(table_action)
                export_menu.addAction(image_action)

                return export_menu

            new_action = QAction(self.save_data.getIcon('menubar/new.png'), lang['new'], self.window)
            new_action.setShortcut('Ctrl+N')
            new_action.triggered.connect(self.file_menu_new_action)

            open_action = QAction(self.save_data.getIcon('menubar/open.png'), lang['open'], self.window)
            open_action.setShortcut('Ctrl+O')
            open_action.triggered.connect(self.file_menu_open_action)

            import_menu = create_import_menu()
            export_menu = create_export_menu()

            save_action = QAction(self.save_data.getIcon('menubar/save.png'), lang['save'], self.window)
            save_action.setShortcut('Ctrl+S')
            save_action.triggered.connect(self.file_menu_save_action)

            save_as_action = QAction(self.save_data.getIcon('menubar/saveAs.png'), lang['saveAs'], self.window)
            save_as_action.setShortcut('Ctrl+Shift+S')
            save_as_action.triggered.connect(self.file_menu_save_as_action)

            settings_action = QAction(self.save_data.getIcon('menubar/settings.png'), lang['settings'], self.window)
            settings_action.setShortcut('Ctrl+Alt+S')
            settings_action.triggered.connect(self.file_menu_settings_action)

            exitAction = QAction(self.save_data.getIcon('menubar/exit.png'), lang['exit'], self.window)
            exitAction.setShortcut('Alt+F4')
            exitAction.triggered.connect(self.window.close)


            file_menu.addAction(new_action)
            file_menu.addAction(open_action)
            file_menu.addSeparator()
            file_menu.addMenu(import_menu)
            file_menu.addMenu(export_menu)
            file_menu.addSeparator()
            file_menu.addAction(save_action)
            file_menu.addAction(save_as_action)
            file_menu.addSeparator()
            file_menu.addAction(settings_action)
            file_menu.addSeparator()
            file_menu.addAction(exitAction)

        def create_view_menu():
            lang = self.save_data.language_data['QMainWindow']['QMenuBar']['viewMenu']['QAction']

            view_menu: QMenu = menuBar.addMenu(self.save_data.language_data['QMainWindow']['QMenuBar']['viewMenu']['title'])

            grid_switch_action = QAction(self.save_data.getIcon('menubar/grid.png'), lang['gridSwitch'], self.window)
            grid_switch_action.triggered.connect(self.view_menu_grid_switch_action)

            grid_align_action = QAction(self.save_data.getIcon('menubar/gridAlign.png'), lang['gridAlign'], self.window)
            grid_align_action.triggered.connect(self.view_menu_grid_align_action)


            view_menu.addAction(grid_switch_action)
            view_menu.addAction(grid_align_action)

        def create_help_menu():
            lang = self.save_data.language_data['QMainWindow']['QMenuBar']['helpMenu']['QAction']

            help_menu: QMenu = menuBar.addMenu(self.save_data.language_data['QMainWindow']['QMenuBar']['helpMenu']['title'])

            about_action = QAction(QIcon('./data/themes/logo.ico'), lang['about'], self.window)
            about_action.triggered.connect(self.help_menu_about_action)

            about_qt_action = QAction(self.save_data.getIcon('menubar/qt.png', mode = QSaveData.IconMode.Global), lang['aboutPySide'], self.window)
            about_qt_action.triggered.connect(self.help_menu_about_pyside_action)

            tips_action = QAction(self.save_data.getIcon('menubar/tips.png'), lang['tips'], self.window)
            tips_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/Synell/PERT-Maker/blob/main/README.md#usage')))

            def create_donate_menu():
                donate_menu = QMenu(self.save_data.language_data['QMainWindow']['QMenuBar']['helpMenu']['QMenu']['donate']['title'], self.window)
                donate_menu.setIcon(self.save_data.getIcon('menubar/donate.png'))

                buymeacoffee_action = QAction(self.save_data.getIcon('menubar/buyMeACoffee.png'), 'Buy Me a Coffee', self.window)
                buymeacoffee_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.buymeacoffee.com/Synell')))

                donate_menu.addAction(buymeacoffee_action)

                return donate_menu


            help_menu.addAction(about_action)
            help_menu.addAction(about_qt_action)
            help_menu.addSeparator()
            help_menu.addAction(tips_action)
            help_menu.addSeparator()
            help_menu.addMenu(create_donate_menu())


        create_file_menu()
        create_view_menu()
        create_help_menu()

    def refresh_connection_view(self):
        self.connectionTable.clear()
        paths = {}
        nodes = []
        beginNodes = []
        errors = []

        if self.use_node_names: self.graph.set_path_names_as_node_names()

        for node in self.graph.nodes:
            if len(list(self.graph.node(node).next.keys())) > 0:
                if len(list(self.graph.node(node).previous.keys())) > 0: nodes.append(self.graph.node(node))
                else: beginNodes.append(self.graph.node(node))

        for i in range(len(nodes)):
            for x in list(nodes[i].next.keys()):
                if nodes[i].next[x].name:
                    paths[nodes[i].next[x].name] = {'value': nodes[i].next[x].value, 'previous': []}
            for y in list(nodes[i].previous.keys()):
                p = self.graph.find_path(y, nodes[i].name)
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

        if self.use_node_names:
            self.graph.reset_path_names_as_node_names()
            self.canvas.update()


        pathsLst = list(paths.keys())
        pathsLst.sort()

        for n in pathsLst:
            prevLst: list[str] = paths[n]['previous']
            prevLst.sort()

            if n in self.KEY_WORDS: continue
            for kw in self.KEY_WORDS:
                if kw in prevLst: prevLst.remove(kw)

            self.connectionTable.add_item(
                items = [
                    n,
                    ', '.join(prevLst),
                    str(paths[n]['value'])
                ],
                alignmentFlag = Qt.AlignmentFlag.AlignCenter
            )

        if len(errors) > 0 and not self.save_data.live_refresh_connection_view:
            lang = self.save_data.language_data['QMessageBox']['warning']['refreshConnectionView']

            listWidget = QBetterListWidget(headers = [lang['startNode'], lang['endNode']], minimum_section_size = 100, alignment_flag = Qt.AlignmentFlag.AlignCenter)
            listWidget.setMinimumHeight(100)
            for e in errors:
                listWidget.add_item(items = [str(e[0]), str(e[1])], alignmentFlag = Qt.AlignmentFlag.AlignCenter)

            dropDownWidget = QDropDownWidget(text = lang['details'], widget = listWidget)
            msgBox = QMessageBoxWithWidget(
                app = self,
                title = lang['title'],
                text = lang['text'],
                informative_text = lang['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning,
                widget = dropDownWidget
            ).exec()

    def generate_min_max_time(self):
        for k in self.graph.nodes:
            self.graph.node(k).minTime = 0
            self.graph.node(k).maxTime = 0

        max_loops1 = self.save_data.max_loops
        max_loops2 = self.save_data.max_loops

        nodes = []
        for k in self.graph.nodes:
            if (not self.graph.node(k).previous) and self.graph.node(k).next:
                nodes.append(k)
        if not nodes: return

        while nodes and max_loops1 > 0:
            max_loops1 -= 1
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

        while nodes and max_loops2 > 0:
            max_loops2 -= 1

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


        self.set_unsaved()
        self.canvas.update()

        if (max_loops1 == 0 or max_loops2 == 2) and not self.save_data.live_min_max:
            lang = self.save_data.language_data['QMessageBox']['warning']['generate_min_max_time']

            label = QLabel(lang['label'].replace('%s', str(self.save_data.max_loops), 1).replace('%s', str(max_loops1), 1).replace('%s', str(max_loops2), 1))

            dropDownWidget = QDropDownWidget(text = lang['details'], widget = label)
            QMessageBoxWithWidget(
                app = self,
                title = lang['title'],
                text = lang['text'],
                informative_text = lang['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning,
                widget = dropDownWidget
            ).exec()

    def generate_critical_path(self):
        if not self.save_data.live_min_max: self.generate_min_max_time()

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

        max_loops = self.save_data.max_loops
        path = [startNode]
        node = startNode
        while node != endNode and max_loops > 0:
            max_loops -= 1
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
            self.criticalPathTable.add_item(items = [n], alignmentFlag = Qt.AlignmentFlag.AlignCenter)


        if (max_loops == 0) and not self.save_data.live_generate_critical_path:
            lang = self.save_data.language_data['QMessageBox']['warning']['generateCriticalPath']

            label = QLabel(lang['label'].replace('%s', str(self.save_data.max_loops, 1)))

            dropDownWidget = QDropDownWidget(text = lang['details'], widget = label)
            QMessageBoxWithWidget(
                app = self,
                title = lang['title'],
                text = lang['text'],
                informative_text = lang['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning,
                widget = dropDownWidget
            ).exec()


    def create_connection_view_menu(self):
        lang = self.save_data.language_data['QDockWidget']['connectionView']['QBetterListWidget']

        self.connectionTable = QBetterListWidget(headers = [lang['task'], lang['previousTasks'], lang['time']], minimum_section_size = 100, alignment_flag = Qt.AlignmentFlag.AlignCenter)
        self.connection_view_menu.scroll_layout.addWidget(self.connectionTable, 0, 0)

    def create_critical_path_view_menu(self):
        lang = self.save_data.language_data['QDockWidget']['criticalPathView']['QBetterListWidget']

        self.criticalPathTable = QBetterListWidget(headers = [lang['criticalPath']], minimum_section_size = 100, alignment_flag = Qt.AlignmentFlag.AlignCenter)
        self.critical_path_view_menu.scroll_layout.addWidget(self.criticalPathTable, 0, 0)

    def create_generation_menu(self):
        lang = self.save_data.language_data['QDockWidget']['generation']

        def rcv_value_changed(value: int):
            if value:
                self.save_data.live_refresh_connection_view = True
                self.refresh_connection_view()
            else: self.save_data.live_refresh_connection_view = False

        def mm_value_changed(value: int):
            if value:
                self.save_data.live_min_max = True
                self.generate_min_max_time()
            else: self.save_data.live_min_max = False

        def gcp_value_changed(value: int):
            if value:
                self.save_data.live_generate_critical_path = True
                self.generate_critical_path()
            else: self.save_data.live_generate_critical_path = False

        def unniopn_value_changed(value: int):
            if value: self.use_node_names = True
            else: self.use_node_names = False

            if self.save_data.live_refresh_connection_view: self.refresh_connection_view()
            if self.save_data.live_min_max: self.generate_min_max_time()
            if self.save_data.live_generate_critical_path: self.generate_critical_path()

        live_refresh_connection_view_button = QPushButton(lang['QPushButton']['refreshConnectionView'])
        live_refresh_connection_view_button.setCursor(Qt.CursorShape.PointingHandCursor)
        live_refresh_connection_view_button.setProperty('color', 'main')
        live_refresh_connection_view_button.clicked.connect(self.refresh_connection_view)
        live_refresh_connection_view_checkbox = QToggleButton()
        live_refresh_connection_view_checkbox.setToolTip(lang['QToggleButton']['liveRefreshConnectionView'])
        if self.save_data.live_refresh_connection_view: live_refresh_connection_view_checkbox.setCheckState(Qt.CheckState.Checked)
        live_refresh_connection_view_checkbox.stateChanged.connect(rcv_value_changed)

        generate_min_max_time_button = QPushButton(lang['QPushButton']['generateMinMaxTime'])
        generate_min_max_time_button.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_min_max_time_button.setProperty('color', 'main')
        generate_min_max_time_button.clicked.connect(self.generate_min_max_time)
        generate_min_max_time_checkbox = QToggleButton()
        generate_min_max_time_checkbox.setToolTip(lang['QToggleButton']['liveGenerateMinMax'])
        if self.save_data.live_min_max: generate_min_max_time_checkbox.setCheckState(Qt.CheckState.Checked)
        generate_min_max_time_checkbox.stateChanged.connect(mm_value_changed)

        generate_critical_path_button = QPushButton(lang['QPushButton']['generateCriticalPath'])
        generate_critical_path_button.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_critical_path_button.setProperty('color', 'main')
        generate_critical_path_button.clicked.connect(self.generate_critical_path)
        live_generate_critical_path_checkbox = QToggleButton()
        live_generate_critical_path_checkbox.setToolTip(lang['QToggleButton']['liveGenerateCriticalPath'])
        if self.save_data.live_generate_critical_path: live_generate_critical_path_checkbox.setCheckState(Qt.CheckState.Checked)
        live_generate_critical_path_checkbox.stateChanged.connect(gcp_value_changed)

        self.use_node_names_instead_of_path_names_checkbox = QNamedToggleButton()
        self.use_node_names_instead_of_path_names_checkbox.setText(lang['QToggleButton']['useNodeNamesInsteadOfPathNames'])
        if self.use_node_names: self.use_node_names_instead_of_path_names_checkbox.toggle_button.setCheckState(Qt.CheckState.Checked)
        self.use_node_names_instead_of_path_names_checkbox.toggle_button.stateChanged.connect(unniopn_value_changed)


        self.generation_menu.scroll_layout.addWidget(live_refresh_connection_view_button, 0, 0)
        self.generation_menu.scroll_layout.addWidget(live_refresh_connection_view_checkbox, 0, 1)
        self.generation_menu.scroll_layout.addWidget(generate_min_max_time_button, 1, 0)
        self.generation_menu.scroll_layout.addWidget(generate_min_max_time_checkbox, 1, 1)
        self.generation_menu.scroll_layout.addWidget(generate_critical_path_button, 2, 0)
        self.generation_menu.scroll_layout.addWidget(live_generate_critical_path_checkbox, 2, 1)
        self.generation_menu.scroll_layout.addWidget(self.use_node_names_instead_of_path_names_checkbox, 3, 0, 1, 2)

        rcv_value_changed(self.save_data.live_refresh_connection_view)
        mm_value_changed(self.save_data.live_min_max)
        gcp_value_changed(self.save_data.live_generate_critical_path)
        unniopn_value_changed(self.use_node_names)

    def properties_menu_load(self):
        lang = self.save_data.language_data['QDockWidget']['properties']

        def edit_name(name: str):
            if not name: return
            if name in self.graph.nodes: return
            self.graph.rename(self.selected_item.name, name)
            self.canvas.update()
            self.set_unsaved()

        def edit_min_time(value: float):
            if value.as_integer_ratio()[1] == 1: self.selected_item.minTime = int(value)
            else: self.selected_item.minTime = value
            self.canvas.update()
            self.set_unsaved()

        def edit_max_time(value: float):
            if value.as_integer_ratio()[1] == 1: self.selected_item.maxTime = int(value)
            else: self.selected_item.maxTime = value
            self.canvas.update()
            self.set_unsaved()

        for i in reversed(range(self.properties_menu.scroll_layout.count())):
            self.properties_menu.scroll_layout.itemAt(i).widget().deleteLater()
        if not self.selected_item: return

        min_time_spinbox = QNamedDoubleSpinBox(None, lang['QNamedSpinBox']['QLabel']['minTime'])
        min_time_spinbox.double_spin_box.setValue(self.selected_item.minTime)
        min_time_spinbox.double_spin_box.valueChanged.connect(edit_min_time)

        self.properties_menu.scroll_layout.addWidget(min_time_spinbox, 0, 0)
        self.properties_menu.scroll_layout.setAlignment(min_time_spinbox, Qt.AlignmentFlag.AlignTop)


        max_time_spinbox = QNamedDoubleSpinBox(None, lang['QNamedSpinBox']['QLabel']['maxTime'])
        max_time_spinbox.double_spin_box.setValue(self.selected_item.maxTime)
        max_time_spinbox.double_spin_box.valueChanged.connect(edit_max_time)

        self.properties_menu.scroll_layout.addWidget(max_time_spinbox, 0, 1)
        self.properties_menu.scroll_layout.setAlignment(max_time_spinbox, Qt.AlignmentFlag.AlignTop)


        name_entry = QNamedLineEdit(None, '', lang['QNamedLineEdit']['QLabel']['displayName'])
        name_entry.line_edit.setText(self.selected_item.name)
        name_entry.line_edit.textChanged.connect(edit_name)

        self.properties_menu.scroll_layout.addWidget(name_entry, 1, 0)
        self.properties_menu.scroll_layout.setAlignment(name_entry, Qt.AlignmentFlag.AlignTop)


        lst = list(self.selected_item.next.keys())
        if not lst: return

        node_combobox = QNamedComboBox(None, lang['QNamedComboBox']['QLabel']['node'])

        self.properties_menu.scroll_layout.addWidget(node_combobox, 1, 1)
        self.properties_menu.scroll_layout.setAlignment(node_combobox, Qt.AlignmentFlag.AlignTop)


        node_groupbox = QGridGroupBox()

        node_combobox.combo_box.addItems(lst)
        if lst:
            node_combobox.combo_box.setCurrentIndex(0)
            self.properties_menu_node_groupbox_load(node_groupbox, lst[0])
            self.selected_node = lst[0]

        node_combobox.combo_box.currentIndexChanged.connect(lambda i: self.properties_menu_node_groupbox_load(node_groupbox, lst[i]))

        self.properties_menu.scroll_layout.addWidget(node_groupbox, 2, 0, 1, 2)
        self.properties_menu.scroll_layout.setAlignment(node_groupbox, Qt.AlignmentFlag.AlignTop)
    
    def properties_menu_node_groupbox_load(self, groupbox: QGridGroupBox, key: str):
        lang = self.save_data.language_data['QDockWidget']['properties']
        self.selected_node = key

        def edit_name(name: str):
            self.selected_item.next[key].name = name
            self.canvas.update()
            self.set_unsaved()

        def edit_value(value: float):
            if value.as_integer_ratio()[1] == 1: self.selected_item.next[key].value = int(value)
            else: self.selected_item.next[key].value = value
            self.canvas.update()
            self.set_unsaved()

        def remove_connection(event = None):
            self.graph.remove_connection(self.selected_item.name, key)
            self.canvas.update()
            self.properties_menu_load()
            self.set_unsaved()

        for i in reversed(range(groupbox.grid_layout.count())):
            groupbox.grid_layout.itemAt(i).widget().deleteLater()

        groupbox.setTitle(lang['QGroupBox']['pathToNodeX'].replace('%s', key))

        name_entry = QNamedLineEdit(None, '', lang['QNamedLineEdit']['QLabel']['displayName'])
        name_entry.line_edit.setText(self.selected_item.next[key].name)
        name_entry.line_edit.textChanged.connect(edit_name)
        value_spinbox = QNamedDoubleSpinBox(None, lang['QNamedSpinBox']['QLabel']['time'])
        value_spinbox.double_spin_box.setValue(self.selected_item.next[key].value)
        value_spinbox.double_spin_box.valueChanged.connect(edit_value)

        delete_button = QPushButton(lang['QPushButton']['deleteConnection'])
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setProperty('color', 'main')
        delete_button.clicked.connect(remove_connection)

        groupbox.grid_layout.addWidget(name_entry, 0, 0)
        groupbox.grid_layout.setAlignment(name_entry, Qt.AlignmentFlag.AlignTop)
        groupbox.grid_layout.addWidget(value_spinbox, 0, 1)
        groupbox.grid_layout.setAlignment(value_spinbox, Qt.AlignmentFlag.AlignTop)
        groupbox.grid_layout.addWidget(delete_button, 1, 0, 1, 2)
        groupbox.grid_layout.setAlignment(delete_button, Qt.AlignmentFlag.AlignTop)

        self.canvas.update()

    def load_colors(self) -> None:
        qss = super().load_colors()

        SaveData.COLOR_LINK = self.COLOR_LINK

        self.COLOR_NORMAL = QUtilsColor(
            qss.search(
                QssSelector(widget = 'QPen')
            )['color']
        )

        self.COLOR_FOCUS = QUtilsColor(
            qss.search(
                QssSelector(widget = 'QPen', states = ['focus'])
            )['color']
        )

        self.COLOR_SELECTED = QUtilsColor(
            qss.search(
                QssSelector(widget = 'QPen', states = ['selected'])
            )['color']
        )

        self.COLOR_GRID = QUtilsColor(
            qss.search(
                QssSelector(widget = 'QPen', items = ['grid'])
            )['color']
        )


    def set_unsaved(self):
        self.unsaved = True
        self.update_title()

    def set_saved(self):
        self.unsaved = False
        self.update_title()

    def update_title(self):
        s = ''
        if self.unsaved: s = '*'
        if self.SAVE_PATH: self.window.setWindowTitle(self.save_data.language_data['QMainWindow']['title'] + f' | Version: {self.VERSION} | Build: {self.BUILD} - {self.SAVE_PATH}{s}')
        else: self.window.setWindowTitle(self.save_data.language_data['QMainWindow']['title'] + f' | Version: {self.VERSION} | Build: {self.BUILD} - NewPERT{s}')



    def eventFilter(self, source, event: QMouseEvent|QWheelEvent):
        if source is self.canvas:
            match event.type():
                case QEvent.Type.MouseButtonPress:
                    if event.button() == Qt.MouseButton.LeftButton: self.canvas_LMB_press_event(event)
                    elif event.button() == Qt.MouseButton.RightButton: self.canvas_RMB_press_event(event)
                    elif event.button() == Qt.MouseButton.MiddleButton: self.canvas_MMB_press_event(event)

                case QEvent.Type.MouseMove:
                    if event.buttons() == Qt.MouseButton.LeftButton: self.canvas_LMB_move_event(event)
                    #elif event.buttons() == Qt.MouseButton.RightButton: self.canvas_RMB_move_event(event)
                    elif event.buttons() == Qt.MouseButton.MiddleButton: self.canvas_MMB_move_event(event)
                    elif event.buttons() == Qt.MouseButton.NoButton: self.canvas_no_button_move_event(event)

                case QEvent.Type.MouseButtonRelease:
                    #if event.button() == Qt.MouseButton.LeftButton: self.canvas_LMB_release_event(event)
                    #elif event.button() == Qt.MouseButton.RightButton: self.canvas_RMB_release_event(event)
                    if event.button() == Qt.MouseButton.MiddleButton: self.canvas_MMB_release_event(event)

                case QEvent.Type.Paint: self.canvas_paint_event(event)

                case QEvent.Type.Wheel: self.canvas_wheel_event(event)

        return super(Application, self).eventFilter(source, event)

    def key_press_event(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete:
            if self.selected_item:
                self.graph.remove_node(self.selected_item.name)
                self.selected_item = None
                self.selected_node = None
                self.properties_menu_load()
                self.canvas.update()

        elif event.key() == Qt.Key.Key_Shift:
            self.shift_key = True

        elif event.key() == Qt.Key.Key_Control:
            self.control_key = True

        elif event.key() == Qt.Key.Key_Right:
            self.camera_pos += Vector2(-self.save_data.arrow_move_speed, 0)
            self.canvas.update()
        elif event.key() == Qt.Key.Key_Left:
            self.camera_pos += Vector2(self.save_data.arrow_move_speed, 0)
            self.canvas.update()
        elif event.key() == Qt.Key.Key_Down:
            self.camera_pos += Vector2(0, -self.save_data.arrow_move_speed)
            self.canvas.update()
        elif event.key() == Qt.Key.Key_Up:
            self.camera_pos += Vector2(0, self.save_data.arrow_move_speed)
            self.canvas.update()

    def key_release_event(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Shift:
            self.shift_key = False

        elif event.key() == Qt.Key.Key_Control:
            self.control_key = False



    def Vector2_to_QPoint(self, vect2: Vector2 = Vector2()):
        return QPoint(int(vect2.x), int(vect2.y))

    def canvas_paint_event(self, event: QMouseEvent):
        qp = QPainter()
        qp.begin(self.canvas)
        self.canvas_draw_points(qp)
        qp.end()

    def canvas_draw_points(self, qp: QPainter):
        lineSpace = int(self.save_data.grid_size / 10)

        if self.save_data.grid_mode > 0:
            size = Vector2(self.canvas.size().width(), self.canvas.size().height()) * (1 / self.zoom)
            startPos = self.camera_pos % self.save_data.grid_size
            nb = (size // self.save_data.grid_size) + 1

            if self.save_data.grid_mode == 1:
                offset = self.camera_pos // self.save_data.grid_size
                lineOffset = (self.camera_pos % ((lineSpace * 2) * self.zoom)) - (Vector2(lineSpace, lineSpace) * self.zoom)

                for n in range(int(nb.x)):
                    if (n - offset.x) % 5 == 0:
                        qp.setPen(QPen(self.COLOR_GRID.QColor, 2 * self.zoom))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.SolidLine)
                        qp.setPen(pen)
                        qp.drawLine(
                            self.Vector2_to_QPoint(Vector2((n * self.save_data.grid_size) + startPos.x, size.y) * self.zoom),
                            self.Vector2_to_QPoint(Vector2((n * self.save_data.grid_size) + startPos.x, 0) * self.zoom)
                        )
                    else:
                        qp.setPen(QPen(self.COLOR_GRID.QColor, 1 * self.zoom))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.CustomDashLine)
                        pen.setDashPattern([lineSpace * self.zoom, lineSpace * self.zoom])
                        qp.setPen(pen)
                        qp.drawLine(
                            self.Vector2_to_QPoint(Vector2((n * self.save_data.grid_size) + startPos.x, size.y + lineOffset.y) * self.zoom),
                            self.Vector2_to_QPoint(Vector2((n * self.save_data.grid_size) + startPos.x, 0) * self.zoom),
                        )

                for n in range(int(nb.y)):
                    if (n - offset.y) % 5 == 0:
                        qp.setPen(QPen(self.COLOR_GRID.QColor, 2 * self.zoom))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.SolidLine)
                        qp.setPen(pen)
                        qp.drawLine(
                            self.Vector2_to_QPoint(Vector2(size.x, (n * self.save_data.grid_size) + startPos.y) * self.zoom),
                            self.Vector2_to_QPoint(Vector2(0, (n * self.save_data.grid_size) + startPos.y) * self.zoom)
                        )
                    else:
                        qp.setPen(QPen(self.COLOR_GRID.QColor, 1 * self.zoom))
                        pen = qp.pen()
                        pen.setStyle(Qt.PenStyle.CustomDashLine)
                        pen.setDashPattern([lineSpace * self.zoom, lineSpace * self.zoom])
                        qp.setPen(pen)
                        qp.drawLine(
                            self.Vector2_to_QPoint(Vector2(size.x + lineOffset.x, (n * self.save_data.grid_size) + startPos.y) * self.zoom),
                            self.Vector2_to_QPoint(Vector2(0, (n * self.save_data.grid_size) + startPos.y) * self.zoom)
                        )

            elif self.save_data.grid_mode == 2:
                offset = (self.camera_pos // self.save_data.grid_size) % 2

                qp.setPen(QPen(self.COLOR_GRID.QColor, 1 * self.zoom))
                brush = QBrush(self.COLOR_GRID.QColor)
                brush.setStyle(Qt.BrushStyle.SolidPattern)
                qp.setBrush(brush)
                for x in range(-int(offset.x), int(nb.x) + 1, 2):
                    for y in range(-1, int(nb.y) + 1):
                        rectPos = Vector2((x * self.save_data.grid_size) + startPos.x - self.save_data.grid_size, (y * self.save_data.grid_size) + startPos.y - self.save_data.grid_size)
                        if (y % 2) == 0: rectPos.x += self.save_data.grid_size
                        if offset.y: rectPos.y += self.save_data.grid_size
                        qp.drawRect(int(rectPos.x * self.zoom), int(rectPos.y * self.zoom), int(self.save_data.grid_size * self.zoom), int(self.save_data.grid_size * self.zoom))




        if self.save_data.live_refresh_connection_view: self.refresh_connection_view()
        if self.save_data.live_generate_critical_path: self.generate_critical_path()
        if self.save_data.live_min_max: self.generate_min_max_time()

        f = qp.font()
        f.setPointSizeF(f.pointSizeF() * self.zoom)
        qp.setFont(f)

        for k in self.graph.nodes:
            p = self.graph.node(k)
            if p == self.selected_item: qp.setPen(QPen(self.COLOR_FOCUS.QColor, 3 * self.zoom))
            else: qp.setPen(QPen(self.COLOR_NORMAL.QColor, 2 * self.zoom))
            qp.drawEllipse(int(((self.camera_pos.x + p.pos.x) - (self.DELTA / 2)) * self.zoom), int(((self.camera_pos.y + p.pos.y) - (self.DELTA / 2)) * self.zoom), int(self.DELTA * self.zoom), int(self.DELTA * self.zoom))
            qp.drawLine(self.Vector2_to_QPoint((self.camera_pos + p.pos) * self.zoom), self.Vector2_to_QPoint((self.camera_pos + Vector2(p.pos.x, p.pos.y - (self.DELTA / 2))) * self.zoom))
            qp.drawLine(self.Vector2_to_QPoint((self.camera_pos + Vector2(p.pos.x - (self.DELTA / 2), p.pos.y)) * self.zoom), self.Vector2_to_QPoint((self.camera_pos + Vector2(p.pos.x + (self.DELTA / 2), p.pos.y)) * self.zoom))
            qp.drawText(self.Vector2_to_QPoint((self.camera_pos + Vector2(p.pos.x - (qp.font().pointSize() * (len(p.name) / 3)), p.pos.y + (self.DELTA / 4))) * self.zoom), p.name)
            qp.drawText(self.Vector2_to_QPoint((self.camera_pos + Vector2(p.pos.x - (self.DELTA / 5) - (qp.font().pointSize() * (len(str(p.minTime)) / 3)), p.pos.y - (self.DELTA / 6))) * self.zoom), str(p.minTime))
            qp.drawText(self.Vector2_to_QPoint((self.camera_pos + Vector2(p.pos.x + (self.DELTA / 5) - (qp.font().pointSize() * (len(str(p.maxTime)) / 3)), p.pos.y - (self.DELTA / 6))) * self.zoom), str(p.maxTime))

            for pathKey in list(p.next.keys()):
                if p == self.selected_item:
                    if pathKey == self.selected_node: qp.setPen(QPen(self.COLOR_SELECTED.QColor, 3 * self.zoom))
                    else: qp.setPen(QPen(self.COLOR_FOCUS.QColor, 3 * self.zoom))
                path = p.next[pathKey]
                if (path.value == 0 and path.name == ''):
                    pen = qp.pen()
                    pen.setStyle(Qt.PenStyle.CustomDashLine)
                    pen.setDashPattern([lineSpace * self.zoom, lineSpace * self.zoom])
                    qp.setPen(pen)

                vect2 = (path.node.pos - p.pos).normalized * (self.DELTA // 2)
                qp.drawLine(self.Vector2_to_QPoint((self.camera_pos + p.pos + vect2) * self.zoom), self.Vector2_to_QPoint((self.camera_pos + path.node.pos - vect2) * self.zoom))

                pen = qp.pen()
                pen.setStyle(Qt.PenStyle.SolidLine)
                qp.setPen(pen)

                qp.drawLine(self.Vector2_to_QPoint((self.camera_pos + path.node.pos - vect2) * self.zoom), self.Vector2_to_QPoint((self.camera_pos + path.node.pos - vect2 - (deg2Vector2(absoluteDeg(vect2.normalized.convert2Deg + 25)) * 10)) * self.zoom))
                qp.drawLine(self.Vector2_to_QPoint((self.camera_pos + path.node.pos - vect2) * self.zoom), self.Vector2_to_QPoint((self.camera_pos + path.node.pos - vect2 - (deg2Vector2(absoluteDeg(vect2.normalized.convert2Deg - 25)) * 10)) * self.zoom))
                if not (path.value == 0 and path.name == ''): qp.drawText(self.Vector2_to_QPoint((self.camera_pos + path.node.pos - ((path.node.pos - p.pos) / 2) - (deg2Vector2(absoluteDeg(vect2.normalized.convert2Deg + 90)) * 20)) * self.zoom), f'{path.name} {path.value}')

    def canvas_get_point(self, event: QMouseEvent):
        return Vector2(event.position().x(), event.position().y())

    def canvas_get_node(self, event: QMouseEvent):
        point = (self.canvas_get_point(event) / self.zoom) - self.camera_pos

        nodeLst = self.graph.nodes
        dist = nodeLst[0]
        for p in nodeLst[1:]:
            if (self.graph.node(p).pos - point).magnitude < (self.graph.node(dist).pos - point).magnitude: dist = p

        if (self.graph.node(dist).pos - point).magnitude <= (self.DELTA // 2):
            return self.graph.node(dist)

    def canvas_RMB_press_event(self, event: QMouseEvent):
        if self.selected_item:
            node = self.canvas_get_node(event)
            if node: self.graph.add_connection(self.selected_item.name, node.name)
            else: self.canvas_create_node(event)
        else: self.canvas_create_node(event)
        self.properties_menu_load()
        self.canvas.update()
        self.set_unsaved()

    def canvas_create_node(self, event: QMouseEvent):
        s = '0'
        while s in self.graph.nodes:
            s = str(int(s) + 1)
        self.graph.add_node(name = s, pos = (self.canvas_get_point(event) / self.zoom) - self.camera_pos)
        if self.selected_item: self.graph.add_connection(self.selected_item.name, s)
        self.selected_item = self.graph.node(s)
        if self.save_data.align_to_grid:
            pos = self.selected_item.pos % self.save_data.grid_size
            halfGridSize = self.save_data.grid_size / 2
            self.selected_item.pos -= Vector2(
                pos.x - ((self.save_data.grid_size * self.zoom) * int(not bool(pos.x < halfGridSize))),
                pos.y - ((self.save_data.grid_size * self.zoom) * int(not bool(pos.y < halfGridSize)))
            )

    def canvas_LMB_press_event(self, event: QMouseEvent):
        self.selected_item = None
        self.selected_node = None
        if not self.graph.nodes:
            self.properties_menu_load()
            return self.canvas.update()

        self.selected_item = self.canvas_get_node(event)

        self.properties_menu_load()
        self.canvas.update()

    def canvas_LMB_move_event(self, event: QMouseEvent):
        if not self.selected_item: return
        self.selected_item.pos = (self.canvas_get_point(event) / self.zoom) - self.camera_pos
        if self.save_data.align_to_grid:
            pos = self.selected_item.pos % self.save_data.grid_size
            halfGridSize = self.save_data.grid_size / 2
            self.selected_item.pos -= Vector2(
                pos.x - ((self.save_data.grid_size * self.zoom) * int(not bool(pos.x < halfGridSize))),
                pos.y - ((self.save_data.grid_size * self.zoom) * int(not bool(pos.y < halfGridSize)))
            )

        self.canvas.update()
        self.set_unsaved()

    def canvas_no_button_move_event(self, event: QMouseEvent):
        mousePos = (self.canvas_get_point(event) / self.zoom) - self.camera_pos
        self.status_bar.coordinates_label.setText(f'({floor(mousePos.x / (self.save_data.grid_size))}, {floor(mousePos.y / (self.save_data.grid_size))}) - ({floor(mousePos.x)}, {floor(mousePos.y)})')

    def canvas_MMB_press_event(self, event: QMouseEvent):
        self.canvas.setCursor(Qt.CursorShape.SizeAllCursor)
        self.old_mouse_pos = self.canvas_get_point(event)

    def canvas_MMB_move_event(self, event: QMouseEvent):
        pos = self.canvas_get_point(event)
        self.camera_pos += (pos - self.old_mouse_pos) / self.zoom
        self.old_mouse_pos = pos

        self.canvas.update()

    def canvas_MMB_release_event(self, event: QMouseEvent):
        self.canvas.setCursor(Qt.CursorShape.ArrowCursor)

    def canvas_wheel_event(self, event: QWheelEvent):
        if self.control_key:
            self.edit_zoom(self.zoom + ((event.angleDelta().y() / 120) * self.save_data.zoom_speed))

        else:
            if self.shift_key: self.camera_pos += Vector2(event.angleDelta().y(), event.angleDelta().x())
            else: self.camera_pos += Vector2(event.angleDelta().x(), event.angleDelta().y())

            self.canvas.update()


    def file_menu_new_action(self):
        self.selected_item = None
        self.selected_node = None
        del self.graph
        self.graph = Graph()
        self.SAVE_PATH = None

        self.properties_menu_load()
        self.canvas.update()
        self.set_unsaved()

    def file_menu_open_action(self):
        lang = self.save_data.language_data['QFileDialog']['open']

        path = QFileDialog.getOpenFileName(
            parent = self.window,
            dir = './',
            caption = lang['title'],
            filter = 'Python PERT (*.pypert)'
        )[0]

        if not path: return
        self.SAVE_PATH = path
        self.selected_node = None
        self.selected_item = None

        with open(self.SAVE_PATH, 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)
            if 'data' in list(data.keys()) and 'info' in list(data.keys()):
                self.graph.load_from_dict(data['data'])
                self.use_node_names = bool(data['info']['useNodeNames'])
            else:
                self.graph.load_from_dict(data)
                self.use_node_names = False
            self.use_node_names_instead_of_path_names_checkbox.setChecked(self.use_node_names)

        self.properties_menu_load()
        self.canvas.update()

        self.set_saved()

    def file_menu_save_action(self):
        if not self.SAVE_PATH:
            return self.file_menu_save_as_action()

        with open(self.SAVE_PATH, 'w', encoding = 'utf-8') as outfile:
            json.dump(
                {
                    'info': {
                        'comment': 'Data file generated with PERT Maker.',
                        'useNodeNames': self.use_node_names
                    },
                    'data': self.graph.to_dict()
                },
                outfile,
                sort_keys = True,
                ensure_ascii = False
            )

        self.set_saved()

    def file_menu_save_as_action(self):
        lang = self.save_data.language_data['QFileDialog']['saveAs']

        path = QFileDialog.getSaveFileName(
            parent = self.window,
            dir = './',
            caption = lang['title'],
            filter = 'Python PERT (*.pypert)'
        )[0]

        if not path: return
        self.SAVE_PATH = path
        self.file_menu_save_action()

    def file_menu_settings_action(self):
        self.save_data.settings_menu(self)
        self.load_colors()


    def view_menu_grid_switch_action(self):
        self.save_data.grid_mode += 1
        if self.save_data.grid_mode > 2: self.save_data.grid_mode = 0
        self.save_data.save()

        self.canvas.update()

    def view_menu_grid_align_action(self):
        self.save_data.align_to_grid = not self.save_data.align_to_grid
        self.save_data.save()


    def help_menu_about_action(self):
        lang = self.save_data.language_data['QAbout']['pertMaker']
        QAboutBox(
            app = self,
            title = lang['title'],
            logo = './data/themes/logoNoBg.ico',
            texts = [
                lang['texts'][0],
                lang['texts'][1].replace('%s', f'<a href=\"https://github.com/Synell\" style=\"color: {self.COLOR_LINK.hex};\">Synel</a>'),
                lang['texts'][2].replace('%s', f'<a href=\"https://github.com/Synell/PERT-Maker\" style=\"color: {self.COLOR_LINK.hex};\">PERT Maker Github</a>')
            ]
        ).exec()

    def help_menu_about_pyside_action(self):
        self.aboutQt()


    def file_menu_import_menu_table_action(self):
        data = QImportTableDialog(self.window, self.save_data.language_data['QImportTableDialog'], int(self.use_node_names)).exec()
        if not data: return

        self.status_bar.progress_bar.setHidden(False)
        self.status_bar.progress_bar.setRange(0, 8)
        self.status_bar.progress_bar.setValue(0)
        self.file_menu_new_action()
        node_data = data[0]
        node_order = []
        max_level = 0
        data = bool(data[1])

        self.status_bar.progress_bar.setValue(1)
        node_dct = {}
        for row in range(len(node_data)):
            node_dct[node_data[row][0]] = [0, node_data[row][0], node_data[row][1].replace(', ', ',').split(','), node_data[row][2]]
            if [''] == node_dct[node_data[row][0]][2]: node_dct[node_data[row][0]][2] = []
            node_order.append(node_data[row][0])
            if len(node_dct[node_data[row][0]][2]) > max_level: max_level = len(node_dct[node_data[row][0]][2])

        self.status_bar.progress_bar.setValue(2)
        new_max_lvl = 0
        for lvl in range(max_level + 1):
            for node in list(node_dct.keys()):
                for previous_node in node_dct[node][2]:
                    if node_dct[previous_node][0] >= node_dct[node][0]:
                        node_dct[node][0] = node_dct[previous_node][0] + 1
                        if new_max_lvl < node_dct[node][0]: new_max_lvl = node_dct[node][0]

        self.status_bar.progress_bar.setValue(3)
        new_node_lst = []
        for lvl in range(new_max_lvl + 1):
            new_node_lst.append([])

            for node in list(node_dct.keys()):
                if node_dct[node][0] == lvl:
                    new_node_lst[lvl].append((node_order.index(node_dct[node][1]), node_dct[node][1], node_dct[node][2], node_dct[node][3]))

        self.status_bar.progress_bar.setValue(4)
        node_values_dct = {}
        for x in range(len(new_node_lst)):
            for y in range(len(new_node_lst[x])):
                self.graph.add_node(name = new_node_lst[x][y][1], pos = Vector2((x * (self.save_data.grid_size * 3)) + self.save_data.grid_size, (y * (self.save_data.grid_size * 3)) + self.save_data.grid_size))
                node_values_dct[new_node_lst[x][y][1]] = new_node_lst[x][y][3]

        self.status_bar.progress_bar.setValue(5)
        for x in range(len(new_node_lst)):
            for y in range(len(new_node_lst[x])):
                for prev in new_node_lst[x][y][2]:
                    if data == 0:
                        self.graph.add_connection(from_ = prev, to_ = new_node_lst[x][y][1], name = new_node_lst[x][y][1], value = node_values_dct[new_node_lst[x][y][1]])
                    elif data == 1:
                        self.graph.add_connection(from_ = prev, to_ = new_node_lst[x][y][1], name = '', value = node_values_dct[prev])

        self.status_bar.progress_bar.setValue(6)
        self.graph.add_node(name = '-2', pos = Vector2(((x + 1) * (self.save_data.grid_size * 3)) + self.save_data.grid_size, self.save_data.grid_size))
        for node in self.graph.nodes:
            if self.graph.node(node).next == {} and self.graph.node(node).name != '-2':
                self.graph.add_connection(from_ = self.graph.node(node).name, to_ = '-2', name = '', value = node_values_dct[self.graph.node(node).name])

        self.status_bar.progress_bar.setValue(7)
        if not data:
            for x in range(len(new_node_lst)):
                for y in range(len(new_node_lst[x])):
                    self.graph.rename(new_node_lst[x][y][1], self.graph._TEMP_PATH_NAME + new_node_lst[x][y][1])

            for x in range(len(new_node_lst)):
                for y in range(len(new_node_lst[x])):
                    self.graph.rename(self.graph._TEMP_PATH_NAME + new_node_lst[x][y][1], str(new_node_lst[x][y][0]))

                    for node in list(self.graph.node(str(new_node_lst[x][y][0])).previous.keys()):
                        for next_node in list(self.graph.node(node).next.keys()):
                            if next_node == str(new_node_lst[x][y][0]):
                                self.graph.node(node).next[next_node].name = new_node_lst[x][y][1]

        self.status_bar.progress_bar.setValue(8)
        self.use_node_names = data
        self.use_node_names_instead_of_path_names_checkbox.setChecked(data)

        if '-1' in self.graph.nodes:
            self.graph.rename('-1', 'Start')

        if '-2' in self.graph.nodes:
            self.graph.rename('-2', 'End')

        self.status_bar.progress_bar.setHidden(True)

        self.canvas.update()

    def file_menu_export_menu_table_action(self):
        if not self.connectionTable.get_items():
            self.refresh_connection_view()

        if not self.connectionTable.get_items():
            return QMessageBoxWithWidget(
                app = self,
                title = self.save_data.language_data['QMessageBox']['warning']['exportTable']['title'],
                text = self.save_data.language_data['QMessageBox']['warning']['exportTable']['text'],
                informative_text = self.save_data.language_data['QMessageBox']['warning']['exportTable']['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning
            ).exec()

        lang = self.save_data.language_data['QMainWindow']['QMenuBar']['fileMenu']['QMenu']['exportMenu']

        path = QFileDialog.getSaveFileName(
            parent = self.window,
            dir = './',
            caption = lang['QFileDialog']['table']['title'],
            filter = 'CSV (*.csv)'
        )[0]

        if not path: return

        with open(path, 'w', encoding = 'utf-8') as outfile:
            outfile.write('Task;Previous Tasks;Time\n' + '\n'.join(list(';'.join(item) for item in self.connectionTable.get_items())))

    def file_menu_export_menu_image_action(self):
        if not self.graph.nodes:
            return QMessageBoxWithWidget(
                app = self,
                title = self.save_data.language_data['QMessageBox']['warning']['exportImage']['title'],
                text = self.save_data.language_data['QMessageBox']['warning']['exportImage']['text'],
                informative_text = self.save_data.language_data['QMessageBox']['warning']['exportImage']['informativeText'],
                icon = QMessageBoxWithWidget.Icon.Warning
            ).exec()

        data = self.generate_canvas_pixmap()
        result = QExportImageDialog(self.window, self.save_data.language_data['QExportImageDialog'], self.save_data.export_image_bg_color, self.save_data.export_image_fg_color, data).exec()
        if result:
            path = result['path']
            bg, fg = result['bg'], result['fg']

            if result['format'] == 'svg':
                generator = QSvgGenerator()
                generator.setFileName(path)
                generator.setTitle('.'.join(path.split('/')[-1].split('\\')[-1].split('.')[:-1]))
                generator.setDescription(f'\nGenerated with PERT Maker.\nVersion: {self.VERSION} - Build: {self.BUILD}\nYou can find this app here: https://github.com/Synell/PERT-Maker/releases/latest\n')
                self.generate_canvas_pixmap(generator)

                import xml.etree.ElementTree as ET

                def set_color(tree: ET.Element, lvl: int = 0) -> None:
                    nonlocal x, y

                    for node in tree:
                        if node.tag == f'{xmlns}rect':
                            node.attrib['x'] = str(int(node.attrib['x']) - x)
                            node.attrib['y'] = str(int(node.attrib['y']) - y)

                        elif node.tag in [f'{xmlns}circle', f'{xmlns}ellipse']:
                            node.attrib['cx'] = str(int(node.attrib['cx']) - x)
                            node.attrib['cy'] = str(int(node.attrib['cy']) - y)

                        elif node.tag in [f'{xmlns}polyline', f'{xmlns}polygon']:
                            points = node.attrib['points'].split(' ')
                            node.attrib['points'] = ' '.join(f'{int(point.split(",")[0]) - x},{int(point.split(",")[1]) - y}' for point in points if point)

                        elif node.tag == f'{xmlns}text':
                            node.attrib['x'] = str(int(node.attrib['x']) - x)
                            node.attrib['y'] = str(int(node.attrib['y']) - y)

                        elif node.tag == f'{xmlns}path':
                            node.attrib['d'] = node.attrib['d'].replace('M', f'M{x} {y}').replace('m', f'm{x} {y}')

                        if 'fill' in node.attrib:
                            if node.attrib['fill'] != 'none': node.attrib['fill'] = fg.hexa

                        if 'stroke' in node.attrib:
                            if node.attrib['stroke'] != 'none': node.attrib['stroke'] = fg.hexa

                        set_color(node, lvl + 1)

                t = ET.parse(path)
                xmlns = t.getroot().tag.split('}')[0][1:]
                ET.register_namespace('', xmlns)
                xmlns = '{' + xmlns + '}'

                x, y, w, h = (int(val) for val in t.getroot().attrib['viewBox'].split(' '))
                t.getroot().attrib['viewBox'] = f'0 0 {w} {h}'
                set_color(t.getroot())
                t.find(f'{xmlns}g').insert(0, ET.Element('rect', {'x': '0', 'y': '0', 'width': str(w), 'height': str(h), 'fill': bg.hexa, 'stroke': 'none'}))

                t.write(path, encoding = 'utf-8', xml_declaration = True)

            elif result['format'] == 'img':
                pixmap = result['data']
                pixmap.save(path, path.split('.')[-1].upper())

            self.save_data.export_image_bg_color = bg
            self.save_data.export_image_fg_color = fg
            self.save_data.save()


    def generate_canvas_pixmap(self, obj: QSvgGenerator = None) -> QPixmap|None:
        grid_mode = self.save_data.grid_mode
        self.save_data.grid_mode = 0
        zoom = self.zoom
        self.zoom = self.devicePixelRatio()
        self.selected_item = None
        self.selected_node = None
        self.properties_menu_load()
        self.canvas.update()


        nodes = self.graph.nodes

        min_point = self.graph.node(nodes[0]).pos.copy
        max_point = min_point.copy
        for k in nodes[1:]:
            p = self.graph.node(k)

            if p.pos.x < min_point.x: min_point.x = p.pos.x
            elif p.pos.x > max_point.x: max_point.x = p.pos.x

            if p.pos.y < min_point.y: min_point.y = p.pos.y
            elif p.pos.y > max_point.y: max_point.y = p.pos.y

        min_point -= self.DELTA
        max_point += self.DELTA

        min_point += self.camera_pos
        max_point += self.camera_pos

        min_point *= self.zoom
        max_point *= self.zoom


        result = None
        if type(obj) is QSvgGenerator:
            obj.setViewBox(QRectF(min_point.x, min_point.y, max_point.x - min_point.x, max_point.y - min_point.y))
            self.canvas.render(obj, renderFlags = QWidget.RenderFlag.DrawWindowBackground)

        else: result = self.canvas.grab(QRect(int(min_point.x), int(min_point.y), int(max_point.x - min_point.x), int(max_point.y - min_point.y)))

        self.save_data.grid_mode = grid_mode
        self.zoom = zoom
        self.canvas.update()

        return result



    def edit_zoom(self, zoom):
        if (zoom) >= self.ZOOM_MIN and (zoom) <= self.ZOOM_MAX:
            self.zoom = zoom
            self.update_zoom()

    def zoom_in(self, event = None):
        self.edit_zoom(self.zoom + self.save_data.zoom_speed)

    def zoom_out(self, event = None):
        self.edit_zoom(self.zoom - self.save_data.zoom_speed)

    def zoom_min(self, event = None):
        self.edit_zoom(self.ZOOM_MIN)

    def zoom_max(self, event = None):
        self.edit_zoom(self.ZOOM_MAX)

    def zoom_slider_value_changed(self, event = None):
        self.edit_zoom(self.status_bar.zoom.zoom_slider.value() / 100)

    def update_zoom(self):
        self.status_bar.zoom.zoom_slider.setValue(int(self.zoom * 100))
        self.status_bar.zoom.zoom_level.setText(f' {int(self.zoom * 100)}%\t')
        self.canvas.update()


    def check_updates(self) -> None:
        self.update_request = RequestWorker([self.UPDATE_LINK])
        self.update_request.signals.received.connect(self.check_updates_release)
        self.update_request.signals.failed.connect(self.check_updates_failed)
        self.update_request.start()

    def check_updates_release(self, rel: dict, app: str) -> None:
        self.update_request.exit()
        self.must_update_link = RequestWorker.get_release(rel, None).link
        if rel['tag_name'] > self.BUILD: self.set_update(True)
        else: self.save_data.last_check_for_updates = datetime.now()

    def check_updates_failed(self, error: str) -> None:
        self.update_request.exit()
        print('Failed to check for updates:', error)

    def set_update(self, update: bool) -> None:
        self.update_button.setVisible(update)

    def update_click(self) -> None:
        self.save_data.save()
        self.must_update = self.must_update_link
        self.exit()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    app = Application(QPlatform.Windows)
    app.window.showMaximized()
    sys.exit(app.exec())
#----------------------------------------------------------------------
