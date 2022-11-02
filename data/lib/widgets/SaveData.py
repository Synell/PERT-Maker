#----------------------------------------------------------------------

    # Libraries
from urllib.parse import urlparse
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt

from data.lib.qtUtils import QNamedDoubleSpinBox, QSaveData, QGridFrame, QScrollableGridWidget, QSettingsDialog, QUtilsColor, QDragList, QNamedSpinBox
#----------------------------------------------------------------------

    # Class
class SaveData(QSaveData):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    COLOR_LINK = QUtilsColor()

    def __init__(self, save_path: str = './data/save.dat') -> None:
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

        super().__init__(save_path)



    def settings_menu_extra(self):
        return {
            self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']: (self.settings_menu_editor(), f'{self.getIconsDir()}/sidepanel/editor.png')
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



    def get_extra(self, extra_tabs: dict = {}):
        self.max_loops = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].max_loops_spinbox.value()
        self.grid_size = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].grid_size_spinbox.value()
        self.arrow_move_speed = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].arrow_move_speed_spinbox.value()
        self.zoom_speed = extra_tabs[self.language_data['QSettingsDialog']['QSidePanel']['editor']['title']].zoom_speed_spinbox.value()



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
            'exportImageFgColor': self.export_image_fg_color.hexa
        }

    def load_extra_data(self, extra_data: dict = ...) -> None:
        try:
            self.max_loops = extra_data['maxLoops']
            self.grid_size = extra_data['gridSize']
            self.arrow_move_speed = extra_data['arrowMoveSpeed']
            self.zoom_speed = extra_data['zoomSpeed']

            self.live_refresh_connection_view = extra_data['liveRefreshConnectionView']
            self.live_min_max = extra_data['liveMinMax']
            self.live_generate_critical_path = extra_data['liveGenerateCriticalPath']

            self.grid_mode = extra_data['gridMode']
            self.grid_size = extra_data['gridSize']
            self.align_to_grid = extra_data['alignToGrid']

            self.export_image_bg_color = QUtilsColor.from_hexa(extra_data['exportImageBgColor'])
            self.export_image_fg_color = QUtilsColor.from_hexa(extra_data['exportImageFgColor'])

        except: self.save()
#----------------------------------------------------------------------
