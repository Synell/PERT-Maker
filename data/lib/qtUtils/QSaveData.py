#----------------------------------------------------------------------

    # Libraries
from urllib import response
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QWidget
import json
import os
from enum import Enum

from .QBaseApplication import QBaseApplication
from .QSettingsDialog import QSettingsDialog
#----------------------------------------------------------------------

    # Class
class QSaveData:
    class StyleSheetMode(Enum):
        All = 'all'
        Global = 'global'
        Local = 'local'

    class IconMode(Enum):
        Global = 'global'
        Local = 'local'

    path = './data/save.dat'
    def __init__(self):
        self.language = 'english'
        self.theme = 'neoNeon'
        self.themeVariant = 'dark/green'

        self.load()

    def save(self):
        extraData = self.saveExtraData()
        with open(self.path, 'w', encoding = 'utf-8') as outfile:
            json.dump({'language': self.language, 'theme': self.theme, 'themeVariant': self.themeVariant, 'extraData': extraData}, outfile, indent = 4, sort_keys = True, ensure_ascii = False)

    def saveExtraData(self) -> dict: return {}

    def load(self):
        if not os.path.exists(self.path): self.save()
        with open(self.path, 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)
        self.language = data['language']
        self.theme = data['theme']
        self.themeVariant = data['themeVariant']
        self.loadLanguageData()
        self.loadThemeData()
        self.loadExtraData(data['extraData'])

    def loadLanguageData(self):
        with open(f'./data/lang/{self.language}.json', 'r', encoding = 'utf-8') as infile:
            self.languageData = json.load(infile)['data']

    def loadThemeData(self):
        self.themeData = ''
        with open(f'./data/themes/{self.theme}.json', 'r', encoding = 'utf-8') as infile:
            data = json.load(infile)['qss']
            path = data[self.themeVariant]['filename']
            if 'qUtils' in list(data[self.themeVariant].keys()): loadQUtils = True
            else: loadQUtils = False

        if loadQUtils:
            varPath = data[self.themeVariant]['qUtils']
            with open(f'./data/lib/qtUtils/themes/{varPath}', 'r', encoding = 'utf-8') as infile:
                self.themeData += infile.read() + '\n'

        with open(f'./data/themes/{self.theme}/{path}', 'r', encoding = 'utf-8') as infile:
            self.themeData += infile.read()

    def loadExtraData(self, extraData: dict = {}) -> None: pass

    def setStyleSheet(self, app: QBaseApplication = None):
        if not app: return

        with open(f'./data/themes/{self.theme}/{self.themeVariant}/main.qss') as infile:
            app.setStyleSheet(app.getStyleSheet(self.theme, self.themeVariant) + infile.read())

    def getStyleSheet(self, app: QBaseApplication = None, mode: StyleSheetMode = StyleSheetMode.All) -> str:
        if not app: return ''

        match mode:
            case QSaveData.StyleSheetMode.All:
                with open(f'./data/themes/{self.theme}/{self.themeVariant}/main.qss') as infile:
                    return app.getStyleSheet(self.theme, self.themeVariant) + infile.read()
            case QSaveData.StyleSheetMode.Global:
                return app.getStyleSheet(self.theme, self.themeVariant)
            case QSaveData.StyleSheetMode.Local:
                with open(f'./data/themes/{self.theme}/{self.themeVariant}/main.qss') as infile:
                    return infile.read()
        return ''

    def getIconsDir(self) -> str:
        return f'./data/themes/{self.theme}/{self.themeVariant}/icons/'

    def getIcon(self, path, asQIcon = True, mode: IconMode = IconMode.Local) -> QIcon|str:
        if mode == QSaveData.IconMode.Local:
            if asQIcon: return QIcon(f'./data/themes/{self.theme}/{self.themeVariant}/icons/{path}')
            return f'./data/themes/{self.theme}/{self.themeVariant}/icons/{path}'
        elif mode == QSaveData.IconMode.Global:
            if asQIcon: return QIcon(f'./data/lib/qtUtils/themes/{self.theme}/{self.themeVariant}/icons/{path}')
            return f'./data/lib/qtUtils/themes/{self.theme}/{self.themeVariant}/icons/{path}'

    def settingsMenu(self, app: QBaseApplication = None):
        dat = self.settingsMenuExtra()
        response = QSettingsDialog(
            parent = app.window,
            settingsData = self.languageData['QSettingsDialog'],
            langFolder = './data/lang/',
            themesFolder = './data/themes/',
            currentLang = self.language,
            currentTheme = self.theme,
            currentThemeVariant = self.themeVariant,
            extraTabs = dat[0],
            getFunction = dat[1]
        ).get()
        if response != None:
            self.language = response[0]
            self.theme = response[1]
            self.themeVariant = response[2]

            self.save()
            self.load()
            self.setStyleSheet(app)
            QMessageBox.information(app.window,
                self.languageData['QMessageBox']['information']['settingsReload']['title'],
                self.languageData['QMessageBox']['information']['settingsReload']['text'],
                QMessageBox.StandardButton.Ok
            )

    def settingsMenuExtra(self):
        return {}, None
#----------------------------------------------------------------------
