#----------------------------------------------------------------------

    # Libraries
from sys import argv
from PyQt6.QtWidgets import QApplication, QMainWindow
import os
import colorama
#----------------------------------------------------------------------

    # Colorama
colorama.init()

    # Class
class QBaseApplication(QApplication):
    def __init__(self, qss = None, mode = 'default'):
        super().__init__(argv)
        self.window = QMainWindow()
        self.window.setWindowTitle('Base Qt Window')

        if qss != None:
            self.setStyleSheet(self.getStyleSheet(qss, mode))
    
    def getStyleSheet(self, qss = None, mode = 'default'):
        if qss != None:
            if os.path.exists(f'{os.path.dirname(__file__)}/themes/{qss}/{mode}/main.qss'):
                with open(f'{os.path.dirname(__file__)}/themes/{qss}/{mode}/main.qss') as infile:
                    return infile.read()
            else: print(colorama.Fore.YELLOW + '[Warning]' + colorama.Style.RESET_ALL + f' The \'{qss}/{mode}\' Stylesheet doesn\'t exist!')
        return ''
#----------------------------------------------------------------------
