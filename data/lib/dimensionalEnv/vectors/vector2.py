#----------------------------------------------------------------------

    # Libraries
from math import sqrt, atan2, pi
from .vector3 import *

from data.lib.dimensionalEnv.__lib__.__error__ import DivisionError
#----------------------------------------------------------------------

    # Class
class Vector2:
    '''
    Vector2(float x, float y)
    '''
    def __init__(self, x: float = 0, y: float = 0) -> None:
        '''
        Args:
            float x
            float y
        '''

        self.__x__ = float(x)
        self.__y__ = float(y)

    @property
    def x(self) -> float:
        return self.__x__

    @x.setter
    def x(self, x: float = 0) -> None:
        self.__x__ = float(x)

    @property
    def y(self) -> float:
        return self.__y__

    @y.setter
    def y(self, y: float = 0) -> None:
        self.__y__ = float(y)

    def __str__(self):
        return f'x: {self.x} - y: {self.y}'

    def __add__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector2(self.x + obj, self.y + obj)
            case Vector2(x = x, y = y): return Vector2(self.x + obj.x, self.y + obj.y)
            case _: raise ValueError(f'\'{obj}\' must be an integer, a float or a Vector2!')

    def __sub__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector2(self.x - obj, self.y - obj)
            case Vector2(x = x, y = y): return Vector2(self.x - obj.x, self.y - obj.y)
            case _: raise ValueError(f'\'{obj}\' must be an integer, a float or a Vector2!')

    def __mul__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector2(self.x * obj, self.y * obj)
            case Vector2(x = x, y = y): return self.crossProduct(obj)
            case _: raise ValueError(f'\'{obj}\' must be an integer, a float or a Vector2!')
    
    def crossProduct(self, obj):
        match obj:
            case Vector2(x = x, y = y): return Vector3(0, 0, self.x * obj.y - obj.x * self.y)
            case _: raise ValueError(f'\'{obj}\' must be a Vector2!')
    
    def scalarProduct(self, obj):
        match obj:
            case Vector2(x = x, y = y): return self.x * obj.x + self.y * obj.y
            case _: raise ValueError(f'\'{obj}\' must be a Vector2!')

    def __truediv__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector2(self.x / obj, self.y / obj)
            case Vector2(x = x, y = y): raise DivisionError('Cannot divide two Vectors!')
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    def __floordiv__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector2(self.x // obj, self.y // obj)
            case Vector2(x = x, y = y): raise DivisionError('Cannot divide two Vectors!')
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    def __mod__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector2(self.x % obj, self.y % obj)
            case Vector2(x = x, y = y): raise DivisionError('Cannot divide two Vectors!')
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    def __pow__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(0, 0, 0)
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    @property
    def copy(self):
        return Vector2(self.x, self.y)

    def __eq__(self, obj):
        if type(obj) is Vector2:
            return self.x == obj.x and self.y == obj.y
        return False

    def __ne__(self, obj):
        if type(obj) is Vector2:
            return self.x != obj.x and self.y != obj.y
        return True

    def __lt__(self, obj):
        if type(obj) is Vector2:
            return self.x < obj.x and self.y < obj.y
        return False

    def __gt__(self, obj):
        if type(obj) is Vector2:
            return self.x > obj.x and self.y > obj.y
        return False

    def __le__(self, obj):
        if type(obj) is Vector2:
            return self.x <= obj.x and self.y <= obj.y
        return False

    def __ge__(self, obj):
        if type(obj) is Vector2:
            return self.x >= obj.x and self.y >= obj.y
        return False

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __pos__(self):
        return Vector2(self.x, self.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    @property
    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    @property
    def normalized(self):
        if self.magnitude > 0:
            return self.copy / self.magnitude
        return self.copy
    
    @property
    def get(self):
        return self.x, self.y

    @property
    def convert2Rad(self, direction = 'right'):
        match direction:
            case 'right': return atan2(self.y, self.x)
            case 'left': return atan2(-self.y, -self.x)
            case 'up': return atan2(self.x, self.y)
            case 'down': return atan2(-self.x, -self.y)
            case _: raise ValueError

    @property
    def convert2Deg(self, direction = 'right'):
        match direction:
            case 'right': return atan2(self.y, self.x) * (180 / pi)
            case 'left': return atan2(-self.y, -self.x) * (180 / pi)
            case 'up': return atan2(self.x, self.y) * (180 / pi)
            case 'down': return atan2(-self.x, -self.y) * (180 / pi)
            case _: raise ValueError
    
    @property
    def up():
        return Vector2(0, 1)
    
    @property
    def down():
        return Vector2(0, -1)

    @property
    def left():
        return Vector2(-1, 0)

    @property
    def right():
        return Vector2(1, 0)
#----------------------------------------------------------------------
