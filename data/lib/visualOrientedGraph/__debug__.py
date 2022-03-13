#----------------------------------------------------------------------

    # Libraries
import colorama
#----------------------------------------------------------------------

    # Colorama
colorama.init()

    # Class
class Debug:
    def __new__(cls) -> None:
        return None

    def log(message: str = ''):
        print(colorama.Fore.WHITE + '[Log] ' + colorama.Fore.RESET + message)

    def warning(message: str = ''):
        print(colorama.Fore.YELLOW + '[Warning] ' + colorama.Fore.RESET + message)


    def error(message: str = ''):
        print(colorama.Fore.RED + '[Error] ' + colorama.Fore.RESET + message)
#----------------------------------------------------------------------
