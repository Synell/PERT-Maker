#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtGui import QColor
from .byte import Byte
#----------------------------------------------------------------------

    # Class
class Color:
    def __init__(self, *color: int|str) -> None:
        self.__red__ = Byte()
        self.__green__ = Byte()
        self.__blue__ = Byte()
        self.__alpha__ = Byte()

        self.set(*color)


    @property
    def red(self): return self.__red__

    @red.setter
    def red(self, value: int = 0): self.__red__.value = value


    @property
    def green(self): return self.__green__

    @green.setter
    def green(self, value: int = 0): self.__green__.value = value


    @property
    def blue(self): return self.__blue__

    @blue.setter
    def blue(self, value: int = 0): self.__blue__.value = value


    @property
    def alpha(self): return self.__alpha__

    @alpha.setter
    def alpha(self, value: int = 0): self.__alpha__.value = value


    def set(self, *color: int|str):
        if len(color) == 0: color: str = '#000000'
        if len(color) == 1: color = color[0]

        match color:
            case (red, green, blue):
                self.red = red
                self.green = green
                self.blue = blue

            case (red, green, blue, alpha):
                self.red = red
                self.green = green
                self.blue = blue
                self.alpha = alpha

            case str(color):
                if not color.startswith('#'): return
                color = color[1:]

                if len(color) == 6:
                    red, green, blue = Byte(color[0:2]), Byte(color[2:4]), Byte(color[4:6])
                elif len(color) == 8:
                    red, green, blue, alpha = Byte(color[0:2]), Byte(color[2:4]), Byte(color[4:6]), Byte(color[6:])
                    self.alpha = alpha
                else: return

                self.red = red
                self.green = green
                self.blue = blue



    def toRGB(self):
        return (self.red.value, self.green.value, self.blue.value)

    def toRGBA(self):
        return (self.red.value, self.green.value, self.blue.value, self.alpha.value)


    def toHex(self):
        return f'#{self.red.toHex(False)}{self.green.toHex(False)}{self.blue.toHex(False)}'

    def toHexa(self):
        return f'#{self.red.toHex(False)}{self.green.toHex(False)}{self.blue.toHex(False)}{self.alpha.toHex(False)}'

    def toAhex(self):
        return f'#{self.alpha.toHex(False)}{self.red.toHex(False)}{self.green.toHex(False)}{self.blue.toHex(False)}'


    def toQColor(self):
        return QColor(self.red.value, self.green.value, self.blue.value, 255)

    def toQColorAlpha(self):
        return QColor(self.red.value, self.green.value, self.blue.value, self.alpha.value)
#----------------------------------------------------------------------
