#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt
from datetime import datetime
import os

from data.lib.qtUtils import QNamedDoubleSpinBox, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QUtilsColor, QNamedComboBox, QNamedSpinBox, QBaseApplication
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()

    def __init__(self, app: QBaseApplication, save_path: str = './data/save.dat', main_color_set: QSaveData.ColorSet = None, neutral_color_set: QSaveData.ColorSet = None) -> None:
        self.max_loops = 5000

        self.align_to_grid = False

        self.grid_mode = 0
        self.grid_size = 50

        self.live_refresh_connection_view = False
        self.live_generate_critical_path = False
        self.live_min_max = False

        self.arrow_move_speed = 20

        self.zoom_speed = 0.25

        self.export_image_bg_color = QUtilsColor.from_hexa('#000000ff')
        self.export_image_fg_color = QUtilsColor.from_hexa('#ffffffff')

        self.check_for_updates = 4
        self.last_check_for_updates = datetime.now()

        self.token = ''
        self.downloads_folder = os.path.abspath('./data/downloads/').replace('\\', '/')

        self.dock_widgets = {}

        super().__init__(app, save_path, main_color_set = main_color_set, neutral_color_set = neutral_color_set)



    def settings_menu_extra(self):
        return {
            self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']: (self.settings_menu_editor(), f'{self.get_icon_dir()}/sidepanel/editor.png'),
            self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']: (self.settings_menu_updates(), f'{self.get_icon_dir()}/sidepanel/updates.png'),
        }, self.get_extra



    def settings_menu_editor(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['editor']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['maxLoops']['title'], lang['QLabel']['maxLoops']['description'])
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.max_loops_spinbox = QNamedSpinBox(None, lang['QNamedSpinBox']['maxLoops'])
        widget.max_loops_spinbox.setRange(255, 65535)
        widget.max_loops_spinbox.setValue(self.max_loops)
        root_frame.grid_layout.addWidget(widget.max_loops_spinbox, 1, 0)
        root_frame.grid_layout.setAlignment(widget.max_loops_spinbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 2, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['gridSize']['title'], lang['QLabel']['gridSize']['description'])
        root_frame.grid_layout.addWidget(label, 3, 0)

        widget.grid_size_spinbox = QNamedSpinBox(None, lang['QNamedSpinBox']['gridSize'])
        widget.grid_size_spinbox.setRange(10, 200)
        widget.grid_size_spinbox.setValue(self.grid_size)
        root_frame.grid_layout.addWidget(widget.grid_size_spinbox, 4, 0)
        root_frame.grid_layout.setAlignment(widget.grid_size_spinbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 5, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['arrowMoveSpeed']['title'], lang['QLabel']['arrowMoveSpeed']['description'])
        root_frame.grid_layout.addWidget(label, 6, 0)

        widget.arrow_move_speed_spinbox = QNamedSpinBox(None, lang['QNamedSpinBox']['arrowMoveSpeed'])
        widget.arrow_move_speed_spinbox.setRange(1, 200)
        widget.arrow_move_speed_spinbox.setValue(self.arrow_move_speed)
        root_frame.grid_layout.addWidget(widget.arrow_move_speed_spinbox, 7, 0)
        root_frame.grid_layout.setAlignment(widget.arrow_move_speed_spinbox, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 8, 0)


        label = QSettingsDialog.textGroup(lang['QLabel']['zoomSpeed']['title'], lang['QLabel']['zoomSpeed']['description'])
        root_frame.grid_layout.addWidget(label, 9, 0)

        widget.zoom_speed_spinbox = QNamedDoubleSpinBox(None, lang['QNamedSpinBox']['zoomSpeed'])
        widget.zoom_speed_spinbox.setRange(0.25, 4.0)
        widget.zoom_speed_spinbox.setValue(self.zoom_speed)
        root_frame.grid_layout.addWidget(widget.zoom_speed_spinbox, 10, 0)
        root_frame.grid_layout.setAlignment(widget.zoom_speed_spinbox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def settings_menu_updates(self):
        lang = self.language_data['QSettingsDialog']['QSidePanel']['updates']
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)


        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = QSettingsDialog.textGroup(lang['QLabel']['checkForUpdates']['title'], lang['QLabel']['checkForUpdates']['description'])
        root_frame.grid_layout.addWidget(label, 0, 0)

        widget.check_for_updates_combobox = QNamedComboBox(None, lang['QNamedComboBox']['checkForUpdates']['title'])
        widget.check_for_updates_combobox.combo_box.addItems([
            lang['QNamedComboBox']['checkForUpdates']['values']['never'],
            lang['QNamedComboBox']['checkForUpdates']['values']['daily'],
            lang['QNamedComboBox']['checkForUpdates']['values']['weekly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['monthly'],
            lang['QNamedComboBox']['checkForUpdates']['values']['atLaunch']
        ])
        widget.check_for_updates_combobox.combo_box.setCurrentIndex(self.check_for_updates)
        root_frame.grid_layout.addWidget(widget.check_for_updates_combobox, 1, 0)
        root_frame.grid_layout.setAlignment(widget.check_for_updates_combobox, Qt.AlignmentFlag.AlignLeft)


        return widget



    def get_extra(self, extra_tabs: dict = {}):
        self.max_loops = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].max_loops_spinbox.value()
        self.grid_size = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].grid_size_spinbox.value()
        self.arrow_move_speed = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].arrow_move_speed_spinbox.value()
        self.zoom_speed = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].zoom_speed_spinbox.value()

        self.check_for_updates = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['updates']['title']].check_for_updates_combobox.combo_box.currentIndex()



    def valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False


    def save_extra_data(self) -> dict:
        return {
            'maxLoops': self.max_loops,
            'gridSize': self.grid_size,
            'arrowMoveSpeed': self.arrow_move_speed,
            'zoomSpeed': self.zoom_speed,

            'liveRefreshConnectionView': self.live_refresh_connection_view,
            'liveMinMax': self.live_min_max,
            'liveGenerateCriticalPath': self.live_generate_critical_path,

            'gridMode': self.grid_mode,
            'gridSize': self.grid_size,
            'alignToGrid': self.align_to_grid,

            'exportImageBgColor': self.export_image_bg_color.hexa,
            'exportImageFgColor': self.export_image_fg_color.hexa,

            'checkForUpdates': self.check_for_updates,
            'lastCheckForUpdates': self.last_check_for_updates.strftime(self.dateformat),

            'dockWidgets': self.dock_widgets
        }

    def load_extra_data(self, extra_data: dict = ..., reload: list = [], reload_all: bool = False) -> bool:
        exc = suppress(Exception)
        res = False

        with exc: self.max_loops = extra_data['maxLoops']
        with exc: self.grid_size = extra_data['gridSize']
        with exc: self.arrow_move_speed = extra_data['arrowMoveSpeed']
        with exc: self.zoom_speed = extra_data['zoomSpeed']

        with exc: self.live_refresh_connection_view = extra_data['liveRefreshConnectionView']
        with exc: self.live_min_max = extra_data['liveMinMax']
        with exc: self.live_generate_critical_path = extra_data['liveGenerateCriticalPath']

        with exc: self.grid_mode = extra_data['gridMode']
        with exc: self.grid_size = extra_data['gridSize']
        with exc: self.align_to_grid = extra_data['alignToGrid']

        with exc: self.export_image_bg_color = QUtilsColor.from_hexa(extra_data['exportImageBgColor'])
        with exc: self.export_image_fg_color = QUtilsColor.from_hexa(extra_data['exportImageFgColor'])

        with exc: self.check_for_updates = extra_data['checkForUpdates']
        with exc: self.last_check_for_updates = datetime.strptime(extra_data['lastCheckForUpdates'], self.dateformat)

        with exc: self.dock_widgets = extra_data['dockWidgets']

        return res
#----------------------------------------------------------------------
