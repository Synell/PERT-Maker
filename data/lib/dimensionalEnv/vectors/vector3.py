#----------------------------------------------------------------------

    # Libraries
from math import sqrt

from data.lib.dimensionalEnv.__lib__.__error__ import DivisionError
#----------------------------------------------------------------------

    # Class
class Vector3:
    '''
    Vector3(float x, float y, float z)
    '''
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        '''
        Args:
            float x
            float y
            float z
        '''

        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float = 0) -> None:
        self._x = float(x)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float = 0) -> None:
        self._y = float(y)

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, z: float = 0) -> None:
        self._z = float(z)

    def __str__(self):
        return f'x: {self.x} - y: {self.y} - z: {self.z}'

    def __add__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(self.x + obj, self.y + obj, self.z + obj)
            case Vector3(x = x, y = y, z = z): return Vector3(self.x + obj.x, self.y + obj.y, self.z + obj.z)
            case _: raise ValueError(f'\'{obj}\' must be an integer, a float or a Vector3!')

    def __sub__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(self.x - obj, self.y - obj, self.z - obj)
            case Vector3(x = x, y = y, z = z): return Vector3(self.x - obj.x, self.y - obj.y, self.z - obj.z)
            case _: raise ValueError(f'\'{obj}\' must be an integer, a float or a Vector3!')

    def __mul__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(self.x * obj, self.y * obj, self.z * obj)
            case Vector3(x = x, y = y, z = z): return self.crossProduct(obj)
            case _: raise ValueError(f'\'{obj}\' must be an integer, a float or a Vector3!')

    def crossProduct(self, obj):
        match obj:
            case Vector3(x = x, y = y, z = z): return Vector3(self.y * obj.z - self.z * obj.y, self.z * obj.x - self.x * obj.z, self.x * obj.y - obj.x * self.y)
            case _: raise ValueError(f'\'{obj}\' must be a Vector3!')
    
    def scalarProduct(self, obj):
        match obj:
            case Vector3(x = x, y = y, z = z): return self.x * obj.x + self.y * obj.y + self.z * obj.z
            case _: raise ValueError(f'\'{obj}\' must be a Vector3!')

    def __truediv__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(self.x / obj, self.y / obj, self.z / obj)
            case Vector3(x = x, y = y, z = z): raise DivisionError('Cannot divide two Vectors!')
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    def __floordiv__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(self.x // obj, self.y // obj, self.z // obj)
            case Vector3(x = x, y = y, z = z): raise DivisionError('Cannot divide two Vectors!')
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    def __mod__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(self.x % obj, self.y % obj, self.z % obj)
            case Vector3(x = x, y = y, z = z): raise DivisionError('Cannot divide two Vectors!')
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    def __pow__(self, obj):
        match obj:
            case int(obj) | float(obj): return Vector3(0, 0, 0)
            case _: raise ValueError(f'\'{obj}\' must be an integer or a float!')

    @property
    def copy(self):
        return Vector3(self.x, self.y, self.z)

    def __eq__(self, obj):
        if type(obj) is Vector3:
            return self.x == obj.x and self.y == obj.y and self.z == obj.z
        return False

    def __ne__(self, obj):
        if type(obj) is Vector3:
            return self.x != obj.x and self.y != obj.y and self.z != obj.z
        return True

    def __lt__(self, obj):
        if type(obj) is Vector3:
            return self.x < obj.x and self.y < obj.y and self.z < obj.z
        return False

    def __gt__(self, obj):
        if type(obj) is Vector3:
            return self.x > obj.x and self.y > obj.y and self.z > obj.z
        return False

    def __le__(self, obj):
        if type(obj) is Vector3:
            return self.x <= obj.x and self.y <= obj.y and self.z <= obj.z
        return False

    def __ge__(self, obj):
        if type(obj) is Vector3:
            return self.x >= obj.x and self.y >= obj.y and self.z >= obj.z
        return False

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __pos__(self):
        return Vector3(self.x, self.y, self.z)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    @property
    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def normalized(self):
        if self.magnitude > 0:
            return self.copy / self.magnitude
        return self.copy
    
    @property
    def get(self):
        return self.x, self.y, self.z

    @property
    def up():
        return Vector3(0, 1, 0)
    
    @property
    def down():
        return Vector3(0, -1, 0)

    @property
    def left():
        return Vector3(-1, 0, 0)

    @property
    def right():
        return Vector3(1, 0, 0)

    @property
    def forward():
        return Vector3(0, 0, 1)

    @property
    def back():
        return Vector3(0, 0, -1)
#----------------------------------------------------------------------
