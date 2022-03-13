#----------------------------------------------------------------------

    # Class
class Byte: pass

class Byte:
    def __init__(self, val: int|str|Byte = 0) -> None:
        self.__value__ = 0
        self.value = val


    @property
    def value(self) -> int:
        return self.__value__

    @value.setter
    def value(self, val: int|str|Byte = 0) -> None:
        match val:
            case int(v):
                if v >= 0 and v <= 255: self.__value__ = v

            case str(v):
                self.__value__ = int(v, 16)

            case Byte():
                self.__value__ = val.value


    def toHex(self, withPrefix = True) -> str:
        value = hex(self.value)[2:]
        if withPrefix: return '0x' + '0' * (2 - len(value)) + value
        return '0' * (2 - len(value)) + value
#----------------------------------------------------------------------
