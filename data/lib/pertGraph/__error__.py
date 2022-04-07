#----------------------------------------------------------------------

    # Libraries
import colorama
#----------------------------------------------------------------------

    # Colorama
colorama.init()

    # Class
class Error(Exception):
    def __init__(self, message = ''):
        super().__init__('\n\n' + colorama.Fore.RED + '[Error] ' + colorama.Fore.RESET + message)
#----------------------------------------------------------------------
