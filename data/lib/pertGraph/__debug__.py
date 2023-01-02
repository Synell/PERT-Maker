#----------------------------------------------------------------------

    # Class
class Debug:
    def __new__(cls) -> None:
        return None

    def log(message: str = ''):
        print('[Log] ' + message)

    def warning(message: str = ''):
        print('[Warning] ' + message)


    def error(message: str = ''):
        print('[Error] ' + message)
#----------------------------------------------------------------------
