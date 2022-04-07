#----------------------------------------------------------------------

    # Class
class StringUtils:
    def __new__(cls) -> None:
        return None

    @staticmethod
    def replaceFirst(s: str = '', __old: str = '', __new: str = ''):
        f = s.find(__old)
        if f == -1: return s

        return s[:f] + __new + s[f + len(__old):]
#----------------------------------------------------------------------
