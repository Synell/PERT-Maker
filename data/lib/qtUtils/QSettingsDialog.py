#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QFrame, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
from data.lib.qtUtils.QGridFrame import QGridFrame

from data.lib.qtUtils.QGridWidget import QGridWidget

from .QScrollableGridWidget import QScrollableGridWidget
import json

from .QSidePanelWidget import QSidePanelWidget
from .QSidePanel import QSidePanelItem
from .QNamedComboBox import QNamedComboBox
from .QFileExplorer import QFileExplorer
#----------------------------------------------------------------------

    # Class
class __QData__:
    class __QLang__:
        def __init__(self, lang_folder = '', lang_path = ''):
            with open(f'{lang_folder}/{lang_path}', encoding = 'utf-8') as infile:
                data = json.load(infile)
                self.display_name = data['info']['name']
                self.version = data['info']['version']
                self.desc = data['info']['description']
                self.filename = '.'.join(lang_path.split('.')[:-1])


    class __QTheme__:
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
            self.lang.append(self.__QLang__(lang_folder, file))

        self.themes = []
        for file in QFileExplorer.get_files(themes_folder, ['json'], False, True):
            self.themes.append(self.__QTheme__(themes_folder, file))


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

        self.root = QSidePanelWidget(widget = QGridWidget(), width = 220)
        self.root.widget.layout().setSpacing(0)
        self.root.widget.layout().setContentsMargins(16, 16, 16, 16)

        self.__data__ = __QData__(lang_folder, themes_folder)
        def clear_root_widget(widget: QWidget):
            for i in reversed(range(self.root.widget.layout().count())):
                self.root.widget.layout().itemAt(i).widget().setHidden(True)
            widget.setHidden(False)

        def show_appearance_tab():
            clear_root_widget(self.appearanceTab)
            self.root.sidepanel.set_current_index(0)

        def show_extra_tab(widget, index):
            clear_root_widget(widget)
            self.root.sidepanel.set_current_index(index)

        self.appearanceTab = self.__appearance_tab_widget__(settings_data['QSidePanel']['appearance'], current_lang, current_theme, current_theme_variant)
        self.root.widget.layout().addWidget(self.appearanceTab)
        self.root.sidepanel.add_item(QSidePanelItem(settings_data['QSidePanel']['appearance']['title'], f'./data/lib/qtUtils/themes/{current_theme}/{current_theme_variant}/icons/sidepanel/appearance.png', show_appearance_tab))

        self.extra_tabs = extra_tabs

        kLst = list(extra_tabs.keys())
        send_param = lambda w, i: lambda: show_extra_tab(w, i)
        for k in range(len(kLst)):
            self.root.widget.layout().addWidget(self.extra_tabs[kLst[k]])
            self.root.sidepanel.add_item(QSidePanelItem(kLst[k], extra_icons[kLst[k]], send_param(self.extra_tabs[kLst[k]], k + 1)))

        show_appearance_tab()

        self.get_function = get_function

        self._layout.addWidget(self.root, 0, 0)
        self._layout.addWidget(self.frame, 1, 0)

        self.setLayout(self._layout)

        self.setMinimumSize(int(parent.window().size().width() * (205 / 256)), int(parent.window().size().height() * (13 / 15)))

    def __appearance_tab_widget__(self, lang_data = {}, current_lang = '', current_theme = '', current_theme_variant = ''):
        widget = QScrollableGridWidget()
        widget.scroll_layout.setSpacing(0)
        widget.scroll_layout.setContentsMargins(0, 0, 0, 0)

        root_frame = QGridFrame()
        root_frame.grid_layout.setSpacing(16)
        root_frame.grid_layout.setContentsMargins(0, 0, 16, 0)
        widget.scroll_layout.addWidget(root_frame, 0, 0)
        widget.scroll_layout.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)

        label = QSettingsDialog.textGroup(lang_data['QLabel']['language']['title'], lang_data['QLabel']['language']['description'])
        root_frame.grid_layout.addWidget(label, 0, 0)

        self.lang_dropdown = QNamedComboBox(None, lang_data['QNamedComboBox']['language'])
        self.lang_dropdown.combo_box.addItems(list(lang.display_name for lang in self.__data__.lang))
        i = 0
        for langId in range(len(self.__data__.lang)):
            if self.__data__.lang[langId].filename == current_lang: i = langId
        self.lang_dropdown.combo_box.setCurrentIndex(i)
        root_frame.grid_layout.addWidget(self.lang_dropdown, 1, 0)
        root_frame.grid_layout.setAlignment(self.lang_dropdown, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.grid_layout.addWidget(frame, 2, 0)


        label = QSettingsDialog.textGroup(lang_data['QLabel']['theme']['title'], lang_data['QLabel']['theme']['description'])
        root_frame.grid_layout.addWidget(label, 3, 0)

        self.themes_dropdown = QNamedComboBox(None, lang_data['QNamedComboBox']['theme'])
        self.themes_dropdown.combo_box.addItems(list(theme.display_name for theme in self.__data__.themes))
        i = 0
        for themeId in range(len(self.__data__.themes)):
            if self.__data__.themes[themeId].filename == current_theme: i = themeId
        self.themes_dropdown.combo_box.setCurrentIndex(i)
        self.themes_dropdown.combo_box.currentIndexChanged.connect(self.__loadThemeVariants__)
        root_frame.grid_layout.addWidget(self.themes_dropdown, 4, 0)
        root_frame.grid_layout.setAlignment(self.themes_dropdown, Qt.AlignmentFlag.AlignLeft)

        self.theme_variants_dropdown = QNamedComboBox(None, lang_data['QNamedComboBox']['themeVariant'])
        self.__loadThemeVariants__(i)
        self.theme_variants_dropdown.combo_box.setCurrentIndex(list(self.__data__.themes[i].variants.keys()).index(current_theme_variant))
        root_frame.grid_layout.addWidget(self.theme_variants_dropdown, 5, 0)
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

    def __loadThemeVariants__(self, index):
        self.theme_variants_dropdown.combo_box.clear()
        self.theme_variants_dropdown.combo_box.addItems(list(self.__data__.themes[index].variants[variant]['displayName'] for variant in self.__data__.themes[index].variants.keys()))
        self.theme_variants_dropdown.combo_box.setCurrentIndex(0)

    def exec(self):
        if super().exec():
            try: self.get_function(self.extra_tabs)
            except Exception as e: print(e)
            return (
                self.__data__.lang[self.lang_dropdown.combo_box.currentIndex()].filename,
                self.__data__.themes[self.themes_dropdown.combo_box.currentIndex()].filename,
                list(self.__data__.themes[self.themes_dropdown.combo_box.currentIndex()].variants.keys())[self.theme_variants_dropdown.combo_box.currentIndex()]
            )
        return None
#----------------------------------------------------------------------
