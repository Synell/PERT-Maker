#----------------------------------------------------------------------

    # Libraries
from typing import overload
from data.lib.extendedmath.Math import Math
from data.lib.extendedmath.types import Vector2, Vector3
from data.lib.utils import classproperty
#----------------------------------------------------------------------

    # Class
class Vector4:
    '''Representation of 4D vectors and points.'''

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        ...

    @overload
    def __init__(self, x: float, y: float, z: float) -> None:
        ...

    @overload
    def __init__(self, x: float, y: float) -> None:
        ...

    @overload
    def __init__(self, vect: 'Vector4') -> None:
        ...

    @overload
    def __init__(self, vect: Vector3) -> None:
        ...

    @overload
    def __init__(self, vect: Vector2) -> None:
        ...

    @overload
    def __init__(self, xyzw: int | float) -> None:
        ...

    def __init__(self, *args) -> None:
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 0

        elif len(args) == 4 and all(isinstance(arg, (int, float)) for arg in args):
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.w = args[3]

        elif len(args) == 3 and all(isinstance(arg, (int, float)) for arg in args):
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.w = 0

        elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
            self.x = args[0]
            self.y = args[1]
            self.z = 0
            self.w = 0

        elif len(args) == 1:
            if isinstance(args[0], Vector4):
                self.x = args[0].x
                self.y = args[0].y
                self.z = args[0].z
                self.w = args[0].w

            elif isinstance(args[0], Vector3):
                self.x = args[0].x
                self.y = args[0].y
                self.z = args[0].z
                self.w = 0

            elif isinstance(args[0], Vector2):
                self.x = args[0].x
                self.y = args[0].y
                self.z = 0
                self.w = 0

            elif isinstance(args[0], (int, float)):
                self.x = args[0]
                self.y = args[0]
                self.z = args[0]
                self.w = args[0]

            else:
                raise TypeError('Invalid argument type')

        else:
            raise TypeError('Invalid argument count')


    @property
    def x(self) -> float:
        '''X component of the vector.'''
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value


    @property
    def y(self) -> float:
        '''Y component of the vector.'''
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value


    @property
    def z(self) -> float:
        '''Z component of the vector.'''
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        self._z = value


    @property
    def w(self) -> float:
        '''W component of the vector.'''
        return self._w

    @w.setter
    def w(self, value: float) -> None:
        self._w = value


    def __getitem__(self, index: int) -> float:
        if not isinstance(index, (int)): raise TypeError('Vector4 indices must be integers')
        match index:
            case 0: return self.x
            case 1: return self.y
            case 2: return self.z
            case 3: return self.w
            case _: raise IndexError('Vector4 index out of range')

    def __setitem__(self, index: int, value: float) -> None:
        if not isinstance(index, (int)): raise TypeError('Vector4 indices must be integers')
        match index:
            case 0: self.x = value
            case 1: self.y = value
            case 2: self.z = value
            case 3: self.w = value
            case _: raise IndexError('Vector4 index out of range')


    def __str__(self) -> str:
        '''Returns a formatted string for this vector.'''
        return f'Vector4({self.x:.2f}, {self.y:.2f}, {self.z:.2f}, {self.w:.2f})'

    def __repr__(self) -> str:
        '''Returns a formatted string for this vector.'''
        return f'Vector4({self.x:.2f}, {self.y:.2f}, {self.z:.2f}, {self.w:.2f})'


    @classproperty
    def zero(cls) -> None:
        '''Shorthand for writing Vector4(0, 0, 0, 0).'''
        return Vector4(0, 0, 0, 0)

    @classproperty
    def one(cls) -> None:
        '''Shorthand for writing Vector4(1, 1, 1, 1).'''
        return Vector4(1, 1, 1, 1)


    def normalize(self) -> None:
        '''Normalizes this vector.'''
        num = self.magnitude
        if (num > 1E-05): self /= num
        else: self = Vector4.zero

    @property
    def normalized(self) -> 'Vector4':
        '''Returns this vector with a magnitude of 1.'''
        return self / self.magnitude


    @property
    def magnitude(self) -> float:
        '''Returns the length of this vector.'''
        return Math.sqrt(Vector4.dot(self, self))

    @property
    def sqr_magnitude(self) -> float:
        '''Returns the squared length of this vector.'''
        return Vector4.dot(self, self)


    def set(self, x: float, y: float, z: float, w: float) -> None:
        '''Set x, y, z and w components of an existing Vector4.'''
        self.x = x
        self.y = y
        self.z = z
        self.w = w


    def copy(self) -> 'Vector4':
        '''Returns a copy of this vector.'''
        return Vector4(self.x, self.y, self.z, self.w)


    @staticmethod
    def lerp(a: 'Vector4', b: 'Vector4', t: float) -> 'Vector4':
        '''Linearly interpolates between two vectors.'''
        return a + (b - a) * Math.clamp01(t)

    @staticmethod
    def lerp_unclamped(a: 'Vector4', b: 'Vector4', t: float) -> 'Vector4':
        '''Linearly interpolates between two vectors.'''
        return a + (b - a) * t


    @staticmethod
    def move_towards(current: 'Vector4', target: 'Vector4', max_distance_delta: float) -> 'Vector4':
        '''Moves a point current towards target.'''
        return current + (target - current).normalized * max_distance_delta


    @overload
    def scale(self, scale: 'Vector4') -> None:
        '''Multiplies two vectors component-wise.'''
        ...

    @overload
    def scale(self, scale: int | float) -> None:
        '''Multiplies this vector by a number.'''
        ...

    def scale(self, scale: object) -> None:
        '''Multiplies this vector by a number or another vector.'''
        if isinstance(scale, Vector4):
            self.x *= scale.x
            self.y *= scale.y
            self.z *= scale.z
            self.w *= scale.w

        elif isinstance(scale, (int, float)):
            self.x *= scale
            self.y *= scale
            self.z *= scale
            self.w *= scale

        else:
            raise TypeError('Invalid argument type')


    @overload
    def scaled(self, scale: 'Vector4') -> 'Vector4':
        '''Multiplies two vectors component-wise.'''
        ...

    @overload
    def scaled(self, scale: int | float) -> 'Vector4':
        '''Multiplies this vector by a number.'''
        ...

    def scaled(self, scale: object) -> 'Vector4':
        '''Multiplies this vector by a number or another vector.'''
        if isinstance(scale, Vector4):
            return Vector4(self.x * scale.x, self.y * scale.y, self.z * scale.z, self.w * scale.w)

        elif isinstance(scale, (int, float)):
            return Vector4(self.x * scale, self.y * scale, self.z * scale, self.w * scale)

        else:
            raise TypeError('Invalid argument type')


    @staticmethod
    def dot(a: 'Vector4', b: 'Vector4') -> float:
        '''Dot product of two vectors.'''
        return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w


    @staticmethod
    def project(a: 'Vector4', b: 'Vector4') -> 'Vector4':
        '''Projects a vector onto another vector.'''
        return b * (Vector4.dot(a, b) / Vector4.dot(b, b))


    @staticmethod
    def distance(a: 'Vector4', b: 'Vector4') -> float:
        '''Returns the distance between a and b.'''
        return (a - b).magnitude


    @staticmethod
    def min(a: 'Vector4', b: 'Vector4') -> 'Vector4':
        '''Returns a vector that is made from the smallest components of two vectors.'''
        return Vector4(min(a.x, b.x), min(a.y, b.y), min(a.z, b.z), min(a.w, b.w))


    @staticmethod
    def max(a: 'Vector4', b: 'Vector4') -> 'Vector4':
        '''Returns a vector that is made from the largest components of two vectors.'''
        return Vector4(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z), max(a.w, b.w))


    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y << 2) ^ hash(self.z >> 2) ^ hash(self.w >> 1)


    @overload
    def __add__(self, other: 'Vector4') -> 'Vector4':
        '''Adds two vectors.'''
        ...

    @overload
    def __add__(self, other: int | float) -> 'Vector4':
        '''Adds a scalar to every component of this vector.'''
        ...

    def __add__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

        elif isinstance(other, (int, float)):
            return Vector4(self.x + other, self.y + other, self.z + other, self.w + other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __sub__(self, other: 'Vector4') -> 'Vector4':
        '''Subtracts two vectors.'''
        ...

    @overload
    def __sub__(self, other: int | float) -> 'Vector4':
        '''Subtracts a scalar from every component of this vector.'''
        ...

    def __sub__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

        elif isinstance(other, (int, float)):
            return Vector4(self.x - other, self.y - other, self.z - other, self.w - other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __mul__(self, other: 'Vector4') -> 'Vector4':
        '''Multiplies two vectors.'''
        ...

    @overload
    def __mul__(self, other: int | float) -> 'Vector4':
        '''Multiplies every component of this vector by the same scalar.'''
        ...

    def __mul__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w)

        elif isinstance(other, (int, float)):
            return Vector4(self.x * other, self.y * other, self.z * other, self.w * other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __truediv__(self, other: 'Vector4') -> 'Vector4':
        '''Divides two vectors.'''
        ...

    @overload
    def __truediv__(self, other: int | float) -> 'Vector4':
        '''Divides every component of this vector by the same scalar.'''
        ...

    def __truediv__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w)

        elif isinstance(other, (int, float)):
            return Vector4(self.x / other, self.y / other, self.z / other, self.w / other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __floordiv__(self, other: 'Vector4') -> 'Vector4':
        '''Divides two vectors.'''
        ...

    @overload
    def __floordiv__(self, other: int | float) -> 'Vector4':
        '''Divides every component of this vector by the same scalar.'''
        ...

    def __floordiv__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x // other.x, self.y // other.y, self.z // other.z, self.w // other.w)

        elif isinstance(other, (int, float)):
            return Vector4(self.x // other, self.y // other, self.z // other, self.w // other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __mod__(self, other: 'Vector4') -> 'Vector4':
        '''Returns the component-wise modulo of two vectors.'''
        ...

    @overload
    def __mod__(self, other: int | float) -> 'Vector4':
        '''Returns the component-wise modulo of this vector by the same scalar.'''
        ...

    def __mod__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x % other.x, self.y % other.y, self.z % other.z, self.w % other.w)

        elif isinstance(other, (int, float)):
            return Vector4(self.x % other, self.y % other, self.z % other, self.w % other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __pow__(self, other: 'Vector4') -> 'Vector4':
        '''Returns the component-wise power of two vectors.'''
        ...

    @overload
    def __pow__(self, other: int | float) -> 'Vector4':
        '''Returns the component-wise power of this vector by the same scalar.'''
        ...

    def __pow__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x ** other.x, self.y ** other.y, self.z ** other.z, self.w ** other.w)

        elif isinstance(other, (int, float)):
            return Vector4(self.x ** other, self.y ** other, self.z ** other, self.w ** other)

        else:
            raise TypeError('Invalid argument type')


    def __abs__(self) -> 'Vector4':
        '''Returns the absolute value of this vector.'''
        return Vector4(abs(self.x), abs(self.y), abs(self.z), abs(self.w))

    def __neg__(self) -> 'Vector4':
        '''Returns the negation of this vector.'''
        return Vector4(-self.x, -self.y, -self.z, -self.w)

    def __pos__(self) -> 'Vector4':
        '''Returns the negation of this vector.'''
        return Vector4(self.x, self.y, self.z, self.w)


    @overload
    def __and__(self, other: 'Vector4') -> 'Vector4':
        '''Returns the component-wise bitwise AND of two vectors.'''
        ...

    @overload
    def __and__(self, other: int) -> 'Vector4':
        '''Returns the component-wise bitwise AND of this vector by the same scalar.'''
        ...

    def __and__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x & other.x, self.y & other.y, self.z & other.z, self.w & other.w)

        elif isinstance(other, int):
            return Vector4(self.x & other, self.y & other, self.z & other, self.w & other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __or__(self, other: 'Vector4') -> 'Vector4':
        '''Returns the component-wise bitwise OR of two vectors.'''
        ...

    @overload
    def __or__(self, other: int) -> 'Vector4':
        '''Returns the component-wise bitwise OR of this vector by the same scalar.'''
        ...

    def __or__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x | other.x, self.y | other.y, self.z | other.z, self.w | other.w)

        elif isinstance(other, int):
            return Vector4(self.x | other, self.y | other, self.z | other, self.w | other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __xor__(self, other: 'Vector4') -> 'Vector4':
        '''Returns the component-wise bitwise XOR of two vectors.'''
        ...

    @overload
    def __xor__(self, other: int) -> 'Vector4':
        '''Returns the component-wise bitwise XOR of this vector by the same scalar.'''
        ...

    def __xor__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x ^ other.x, self.y ^ other.y, self.z ^ other.z, self.w ^ other.w)

        elif isinstance(other, int):
            return Vector4(self.x ^ other, self.y ^ other, self.z ^ other, self.w ^ other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __lshift__(self, other: 'Vector4') -> 'Vector4':
        '''Returns the component-wise bitwise left shift of two vectors.'''
        ...

    @overload
    def __lshift__(self, other: int) -> 'Vector4':
        '''Returns the component-wise bitwise left shift of this vector by the same scalar.'''
        ...

    def __lshift__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x << other.x, self.y << other.y, self.z << other.z, self.w << other.w)

        elif isinstance(other, int):
            return Vector4(self.x << other, self.y << other, self.z << other, self.w << other)

        else:
            raise TypeError('Invalid argument type')


    @overload
    def __rshift__(self, other: 'Vector4') -> 'Vector4':
        '''Returns the component-wise bitwise right shift of two vectors.'''
        ...

    @overload
    def __rshift__(self, other: int) -> 'Vector4':
        '''Returns the component-wise bitwise right shift of this vector by the same scalar.'''
        ...

    def __rshift__(self, other: object) -> 'Vector4':
        if isinstance(other, Vector4):
            return Vector4(self.x >> other.x, self.y >> other.y, self.z >> other.z, self.w >> other.w)

        elif isinstance(other, int):
            return Vector4(self.x >> other, self.y >> other, self.z >> other, self.w >> other)

        else:
            raise TypeError('Invalid argument type')


    def __invert__(self) -> 'Vector4':
        '''Returns the component-wise bitwise NOT of this vector.'''
        return Vector4(~self.x, ~self.y, ~self.z, ~self.w)


    def __bool__(self) -> bool:
        '''Returns True if any component of this vector is non-zero.'''
        return self.x != 0 or self.y != 0 or self.z != 0 or self.w != 0


    def __eq__(self, other: 'Vector4') -> bool:
        '''Compares two vectors for equality.'''
        #return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w
        return Vector4.sqr_magnitude(self - other) < 9.99999944E-11

    @overload
    def __ne__(self, other: 'Vector4') -> bool:
        '''Compares two vectors for inequality.'''
        ...

    @overload
    def __ne__(self, other: int | float) -> bool:
        '''Compares every component of this vector to the same scalar.'''
        ...

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Vector4):
            return not self == other

        elif isinstance(other, (int, float)):
            return self.x != other or self.y != other or self.z != other or self.w != other

        else:
            raise TypeError('Invalid argument type')
#----------------------------------------------------------------------
