#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils.QGridFrame import QGridFrame

from data.lib.qtUtils.QGridWidget import QGridWidget

from .QScrollableGridWidget import QScrollableGridWidget
import json

from .QSidePanelWidget import QSidePanelWidget
from .QNamedComboBox import QNamedComboBox
from .QFileExplorer import QFileExplorer
from .QSlidingStackedWidget import QSlidingStackedWidget
#----------------------------------------------------------------------

    # Class
class _QData:
    class _QLang:
        def __init__(self, lang_folder = '', lang_path = ''):
            with open(f'{lang_folder}/{lang_path}', encoding = 'utf-8') as infile:
                data = json.load(infile)
                self.display_name = data['info']['name']
                self.version = data['info']['version']
                self.desc = data['info']['description']
                self.filename = '.'.join(lang_path.split('.')[:-1])


    class _QTheme:
        def __init__(self, themes_folder = '', themePath = ''):
            with open(f'{themes_folder}/{themePath}', encoding = 'utf-8') as infile:
                data = json.load(infile)
                self.display_name = data['info']['name']
                self.version = data['info']['version']
                self.desc = data['info']['description']
                self.filename = '.'.join(themePath.split('.')[:-1])
                self.variants = data['qss']


    def __init__(self, lang_folder = '', themes_folder = ''):
        self.lang = []
        for file in QFileExplorer.get_files(lang_folder, ['json'], False, True):
            self.lang.append(self._QLang(lang_folder, file))

        self.themes = []
        for file in QFileExplorer.get_files(themes_folder, ['json'], False, True):
            self.themes.append(self._QTheme(themes_folder, file))


class QSettingsDialog(QDialog):
    def __init__(self, parent = None, settings_data = {}, lang_folder = '', themes_folder = '', current_lang = '', current_theme = '', current_theme_variant = '', extra_tabs: dict[str: QWidget] = {}, get_function = None):
        super().__init__(parent)

        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        extra_icons = {k: extra_tabs[k][1] for k in list(extra_tabs.keys())}
        extra_tabs = {k: extra_tabs[k][0] for k in list(extra_tabs.keys())}

        right_buttons = QGridWidget()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(settings_data['QPushButton']['cancel'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(button, 0, 0)

        button = QPushButton(settings_data['QPushButton']['apply'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(button, 0, 1)

        self.setWindowTitle(settings_data['title'])

        self.frame = QGridFrame()
        self.frame.grid_layout.addWidget(right_buttons, 0, 0)
        self.frame.grid_layout.setAlignment(right_buttons, Qt.AlignmentFlag.AlignRight)
        self.frame.grid_layout.setSpacing(0)
        self.frame.grid_layout.setContentsMargins(16, 16, 16, 16)
        self.frame.setProperty('border-top', True)
        self.frame.setProperty('border-bottom', True)
        self.frame.setProperty('border-left', True)
        self.frame.setProperty('border-right', True)

        self.root = QSidePanelWidget(width = 220, direction = QSlidingStackedWidget.Direction.Bottom2Top)
        self.root.setProperty('wider', True)

        self._data = _QData(lang_folder, themes_folder)

        self.appearance_tab = self._appearance_tab_widget(settings_data['QSidePanel']['appearance'], current_lang, current_theme, current_theme_variant)
        self.root.add_widget(self.appearance_tab, settings_data['QSidePanel']['appearance']['title'], f'./data/lib/qtUtils/themes/{current_theme}/{current_theme_variant}/icons/sidepanel/appearance.png')

        self.extra_tabs = extra_tabs

        for k, v in extra_tabs.items():
            self.root.add_widget(v, k, extra_icons[k])

        # todo: add manage data tab

        self.root.set_current_index(0)

        self.get_function = get_function

        self._layout.addWidget(self.root, 0, 0)
        self._layout.addWidget(self.frame, 1, 0)

        self.setLayout(self._layout)

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)), int(parent.window().size().height() * (13 / 15)))

    def _appearance_tab_widget(self, lang_data = {}, current_lang = '', current_theme = '', current_theme_variant = ''):
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)

        label = QSettingsDialog.textGroup(lang_data['QLabel']['language']['title'], lang_data['QLabel']['language']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.lang_dropdown = QNamedComboBox(None, lang_data['QNamedComboBox']['language'])
        self.lang_dropdown.combo_box.addItems(list(lang.display_name for lang in self._data.lang))
        i = 0
        for lang_id in range(len(self._data.lang)):
            if self._data.lang[lang_id].filename == current_lang: i = lang_id

        self.lang_dropdown.combo_box.setCurrentIndex(i)
        root_frame.grid_layout.addWidget(self.lang_dropdown, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.lang_dropdown, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, root_frame.grid_layout.count(), 0)


        label = QSettingsDialog.textGroup(lang_data['QLabel']['theme']['title'], lang_data['QLabel']['theme']['description'])
        root_frame.grid_layout.addWidget(label, root_frame.grid_layout.count(), 0)

        self.themes_dropdown = QNamedComboBox(None, lang_data['QNamedComboBox']['theme'])
        self.themes_dropdown.combo_box.addItems(list(theme.display_name for theme in self._data.themes))
        i = 0
        for themeId in range(len(self._data.themes)):
            if self._data.themes[themeId].filename == current_theme: i = themeId
        self.themes_dropdown.combo_box.setCurrentIndex(i)
        self.themes_dropdown.combo_box.currentIndexChanged.connect(self._load_theme_variants)
        root_frame.grid_layout.addWidget(self.themes_dropdown, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.themes_dropdown, Qt.AlignmentFlag.AlignLeft)

        self.theme_variants_dropdown = QNamedComboBox(None, lang_data['QNamedComboBox']['themeVariant'])
        self._load_theme_variants(i)
        self.theme_variants_dropdown.combo_box.setCurrentIndex(list(self._data.themes[i].variants.keys()).index(current_theme_variant))
        root_frame.grid_layout.addWidget(self.theme_variants_dropdown, root_frame.grid_layout.count(), 0)
        root_frame.grid_layout.setAlignment(self.theme_variants_dropdown, Qt.AlignmentFlag.AlignLeft)

        return widget

    def textGroup(title: str = '', description: str = '') -> QGridWidget:
        widget = QGridWidget()
        widget.grid_layout.setSpacing(0)
        widget.grid_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('bigbrighttitle', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 0, 0)

        label = QLabel(description)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setProperty('brightnormal', True)
        label.setWordWrap(True)
        widget.grid_layout.addWidget(label, 1, 0)
        widget.grid_layout.setRowStretch(2, 1)

        return widget

    def _load_theme_variants(self, index):
        self.theme_variants_dropdown.combo_box.clear()
        self.theme_variants_dropdown.combo_box.addItems(list(self._data.themes[index].variants[variant]['displayName'] for variant in self._data.themes[index].variants.keys()))
        self.theme_variants_dropdown.combo_box.setCurrentIndex(0)

    def exec(self):
        if super().exec():
            try: self.get_function(self.extra_tabs)
            except Exception as e: print(e)
            return (
                self._data.lang[self.lang_dropdown.combo_box.currentIndex()].filename,
                self._data.themes[self.themes_dropdown.combo_box.currentIndex()].filename,
                list(self._data.themes[self.themes_dropdown.combo_box.currentIndex()].variants.keys())[self.theme_variants_dropdown.combo_box.currentIndex()]
            )
        return None
#----------------------------------------------------------------------
