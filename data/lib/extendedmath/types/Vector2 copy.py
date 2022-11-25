#----------------------------------------------------------------------

    # Libraries
from data.lib.extendedmath.Math import Math
from data.lib.utils import classproperty
from typing import overload
#----------------------------------------------------------------------

    # Class
class Vector2:
    '''Representation of 2D vectors and points.'''

    @overload
    def __init__(self) -> None:
        ...
        # self._x = 0.0
        # self._y = 0.0

    @overload
    def __init__(self, x: float, y: float) -> None:
        ...
        # self._x = x
        # self._y = y

    @overload
    def __init__(self, vect: 'Vector2') -> None:
        ...
        # self._x = vect.x
        # self._y = vect.y

    def __init__(self, *args):
        if len(args) == 0:
            self._x = 0.0
            self._y = 0.0

        elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
            self._x = args[0]
            self._y = args[1]

        elif len(args) == 1 and isinstance(args[0], Vector2):
            self._x = args[0].x
            self._y = args[0].y

        else:
            raise TypeError('Vector2 takes 0, 1 or 2 arguments')


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


    def __getitem__(self, index: int) -> float:
        if not isinstance(index, (int)): raise TypeError('Vector2 indices must be integers')
        match index:
            case 0: return self.x
            case 1: return self.y
            case _: raise IndexError('Vector2 index out of range')

    def __setitem__(self, index: int, value: float) -> None:
        if not isinstance(index, (int)): raise TypeError('Vector2 indices must be integers')
        match index:
            case 0: self.x = value
            case 1: self.y = value
            case _: raise IndexError('Vector2 index out of range')


    @classproperty
    def zero(cls) -> 'Vector2':
        '''Shorthand for writing Vector2(0, 0).'''
        return Vector2(0, 0)

    @classproperty
    def one(cls) -> 'Vector2':
        '''Shorthand for writing Vector2(1, 1).'''
        return Vector2(1, 1)

    @classproperty
    def up(cls) -> 'Vector2':
        '''Shorthand for writing Vector2(0, 1).'''
        return Vector2(0, 1)

    @classproperty
    def down(cls) -> 'Vector2':
        '''Shorthand for writing Vector2(0, -1).'''
        return Vector2(0, -1)

    @classproperty
    def left(cls) -> 'Vector2':
        '''Shorthand for writing Vector2(-1, 0).'''
        return Vector2(-1, 0)

    @classproperty
    def right(cls) -> 'Vector2':
        '''Shorthand for writing Vector2(1, 0).'''
        return Vector2(1, 0)


    def normalize(self) -> None:
        '''Makes this vector have a magnitude of 1.'''
        num = self.magnitude
        if num > 1e-05:
            self.x /= num
            self.y /= num
        else:
            self.x = 0
            self.y = 0

    @property
    def normalized(self) -> 'Vector2':
        '''Returns this vector with a magnitude of 1.'''
        return self / self.magnitude


    @property
    def magnitude(self) -> float:
        '''Returns the length of this vector.'''
        return (self.x ** 2 + self.y ** 2) ** 0.5


    @property
    def sqr_magnitude(self) -> float:
        '''Returns the squared length of this vector.'''
        return self.x ** 2 + self.y ** 2


    def set(self, x: float, y: float) -> None:
        ''' Set x and y components of an existing Vector2.'''
        self.x = x
        self.y = y


    def copy(self) -> 'Vector2':
        '''Returns a copy of this vector.'''
        return Vector2(self.x, self.y)


    @staticmethod
    def lerp(a: 'Vector2', b: 'Vector2', t: float) -> 'Vector2':
        '''Linearly interpolates between vectors a and b by t.'''
        return Vector2.lerp_unclamped(a, b, Math.clamp01(t))


    @staticmethod
    def lerp_unclamped(a: 'Vector2', b: 'Vector2', t: float) -> 'Vector2':
        '''Linearly interpolates between vectors a and b by t.'''
        return a + (b - a) * t


    @staticmethod
    def move_towards(current: 'Vector2', target: 'Vector2', max_distance_delta: float) -> 'Vector2':
        '''Moves a point current towards target.'''
        return current + (target - current).normalized * max_distance_delta


    @overload
    def scale(self, scale: 'Vector2') -> None:
        '''Multiplies two vectors component-wise.'''
        ...

    @overload
    def scale(self, scale: int | float) -> None:
        '''Multiplies this vector by a number.'''
        ...

    def scale(self, scale: object) -> None:
        if isinstance(scale, Vector2):
            self.x *= scale.x
            self.y *= scale.y

        elif isinstance(scale, (int, float)):
            self.x *= scale
            self.y *= scale

        else:
            raise TypeError('Vector2.scale() takes a Vector2 or a number')


    @overload
    def scaled(self, d: 'Vector2') -> None:
        '''Multiplies two vectors component-wise.'''
        ...

    @overload
    def scaled(self, scale: int | float) -> None:
        '''Multiplies this vector by a number.'''
        ...

    def scaled(self, scale: object) -> None:
        v = self.copy()

        if isinstance(scale, Vector2):
            v.x *= scale.x
            v.y *= scale.y

        elif isinstance(scale, (int, float)):
            v.x *= scale
            v.y *= scale

        else:
            raise TypeError('Vector2.scale() takes a Vector2 or a number')

        return v


    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y << 2)


    def __str__(self) -> str:
        '''Returns a formatted string for this vector.'''
        return f'Vector2({self.x:.2f}, {self.y:.2f})'


    def __repr__(self) -> str:
        '''Returns a formatted string for this vector.'''
        return f'Vector2({self.x:.2f}, {self.y:.2f})'


    def __eq__(self, other: 'Vector2') -> bool:
        '''Returns true if the given vector is exactly equal to this vector.'''
        if not type(other) is Vector2: return False
        return self.x == other.x and self.y == other.y


    def __ne__(self, other: 'Vector2') -> bool:
        '''Returns true if the given vector is not exactly equal to this vector.'''
        if not type(other) is Vector2: return True
        return self.x != other.x or self.y != other.y


    @overload
    def __add__(self, other: 'Vector2') -> 'Vector2':
        '''Adds two vectors.'''
        ...

    @overload
    def __add__(self, other: int | float) -> 'Vector2':
        '''Adds a scalar to each component of this vector.'''
        ...

    def __add__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)

        else:
            raise TypeError('Vector2.__add__() takes a Vector2 or a number')


    @overload
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        '''Subtracts two vectors.'''
        ...

    @overload
    def __sub__(self, other: int | float) -> 'Vector2':
        '''Subtracts a scalar from each component of this vector.'''
        ...

    def __sub__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)

        else:
            raise TypeError('Vector2.__sub__() takes a Vector2 or a number')


    @overload
    def __mul__(self, other: 'Vector2') -> 'Vector2':
        '''Multiplies two vectors.'''
        ...

    @overload
    def __mul__(self, other: int | float) -> 'Vector2':
        '''Multiplies each component of this vector by a scalar.'''
        ...

    def __mul__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)

        else:
            raise TypeError('Vector2.__mul__() takes a Vector2 or a number')


    @overload
    def __truediv__(self, other: 'Vector2') -> 'Vector2':
        '''Divides two vectors.'''
        ...

    @overload
    def __truediv__(self, other: int | float) -> 'Vector2':
        '''Divides each component of this vector by a scalar.'''
        ...

    def __truediv__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)

        else:
            raise TypeError('Vector2.__truediv__() takes a Vector2 or a number')


    @overload
    def __floordiv__(self, other: 'Vector2') -> 'Vector2':
        '''Divides two vectors.'''
        ...

    @overload
    def __floordiv__(self, other: int | float) -> 'Vector2':
        '''Divides each component of this vector by a scalar.'''
        ...

    def __floordiv__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)

        else:
            raise TypeError('Vector2.__floordiv__() takes a Vector2 or a number')


    @overload
    def __mod__(self, other: 'Vector2') -> 'Vector2':
        '''Returns the component-wise modulo of two vectors.'''
        ...

    @overload
    def __mod__(self, other: int | float) -> 'Vector2':
        '''Returns the component-wise modulo of this vector by a scalar.'''
        ...

    def __mod__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x % other.x, self.y % other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x % other, self.y % other)

        else:
            raise TypeError('Vector2.__mod__() takes a Vector2 or a number')


    @overload
    def __pow__(self, other: 'Vector2') -> 'Vector2':
        '''Returns the component-wise power of two vectors.'''
        return Vector2(self.x ** other.x, self.y ** other.y)

    @overload
    def __pow__(self, other: int | float) -> 'Vector2':
        '''Returns the component-wise power of this vector by a scalar.'''
        return Vector2(self.x ** other, self.y ** other)

    def __pow__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x ** other.x, self.y ** other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x ** other, self.y ** other)

        else:
            raise TypeError('Vector2.__pow__() takes a Vector2 or a number')


    def __abs__(self) -> 'Vector2':
        '''Returns the component-wise absolute value of two vectors.'''
        return Vector2(abs(self.x), abs(self.y))

    def __neg__(self) -> 'Vector2':
        '''Returns the component-wise negation of this vector.'''
        return Vector2(-self.x, -self.y)

    def __pos__(self) -> 'Vector2':
        '''Returns the component-wise negation of this vector.'''
        return Vector2(+self.x, +self.y)


    @overload
    def __and__(self, other: 'Vector2') -> 'Vector2':
        '''Returns the component-wise bitwise and of two vectors.'''
        ...

    @overload
    def __and__(self, other: int) -> 'Vector2':
        '''Returns the component-wise bitwise and of this vector by a scalar.'''
        ...

    def __and__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x & other.x, self.y & other.y)

        elif isinstance(other, int):
            return Vector2(self.x & other, self.y & other)

        else:
            raise TypeError('Vector2.__and__() takes a Vector2 or an int')


    @overload
    def __or__(self, other: 'Vector2') -> 'Vector2':
        '''Returns the component-wise bitwise or of two vectors.'''
        ...

    @overload
    def __or__(self, other: int) -> 'Vector2':
        '''Returns the component-wise bitwise or of this vector by a scalar.'''
        ...

    def __or__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x | other.x, self.y | other.y)

        elif isinstance(other, int):
            return Vector2(self.x | other, self.y | other)

        else:
            raise TypeError('Vector2.__or__() takes a Vector2 or an int')


    @overload
    def __xor__(self, other: 'Vector2') -> 'Vector2':
        '''Returns the component-wise bitwise xor of two vectors.'''
        ...

    @overload
    def __xor__(self, other: int) -> 'Vector2':
        '''Returns the component-wise bitwise xor of this vector by a scalar.'''
        ...

    def __xor__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x ^ other.x, self.y ^ other.y)

        elif isinstance(other, int):
            return Vector2(self.x ^ other, self.y ^ other)

        else:
            raise TypeError('Vector2.__xor__() takes a Vector2 or an int')


    @overload
    def __lshift__(self, other: 'Vector2') -> 'Vector2':
        '''Returns the component-wise bitwise left shift of two vectors.'''
        ...

    @overload
    def __lshift__(self, other: int) -> 'Vector2':
        '''Returns the component-wise bitwise left shift of this vector by a scalar.'''
        ...

    def __lshift__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x << other.x, self.y << other.y)

        elif isinstance(other, int):
            return Vector2(self.x << other, self.y << other)

        else:
            raise TypeError('Vector2.__lshift__() takes a Vector2 or an int')


    @overload
    def __rshift__(self, other: 'Vector2') -> 'Vector2':
        '''Returns the component-wise bitwise right shift of two vectors.'''
        ...

    @overload
    def __rshift__(self, other: int) -> 'Vector2':
        '''Returns the component-wise bitwise right shift of this vector by a scalar.'''
        ...

    def __rshift__(self, other: object) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x >> other.x, self.y >> other.y)

        elif isinstance(other, int):
            return Vector2(self.x >> other, self.y >> other)

        else:
            raise TypeError('Vector2.__rshift__() takes a Vector2 or an int')


    def __invert__(self) -> 'Vector2':
        '''Returns the component-wise bitwise inversion of this vector.'''
        return Vector2(~self.x, ~self.y)


    def __bool__(self) -> bool:
        '''Returns True if any component of this vector is non-zero.'''
        return self.x != 0 or self.y != 0


    @staticmethod
    def reflect(in_direction: 'Vector2', in_normal: 'Vector2') -> 'Vector2':
        '''Reflects a vector off the vector defined by a normal.'''
        num = -2 * Vector2.dot(in_normal, in_direction)
        return Vector2(num * in_normal.x + in_direction.x, num * in_normal.y + in_direction.y)


    @staticmethod
    def perpendicular(in_direction: 'Vector2') -> 'Vector2':
        '''Returns the 2D vector perpendicular to this 2D vector. The result is always rotated 90-degrees in a counter-clockwise direction for a 2D coordinate system where the positive Y axis goes up.'''
        return Vector2(-in_direction.y, in_direction.x)


    @staticmethod
    def dot(a: 'Vector2', b: 'Vector2') -> float:
        '''Dot Product of two vectors.'''
        return a.x * b.x + a.y * b.y


    @staticmethod
    def angle(from_: 'Vector2', to_: 'Vector2') -> float:
        '''Gets the unsigned angle in degrees between from_ and to_.'''
        num = float(Math.sqrt(from_.sqr_magnitude * to_.sqr_magnitude))
        if (num < 1E-15):
            return 0.0

        num2 = Math.clamp(Vector2.dot(from_, to_) / num, -1.0, 1.0)
        return float(Math.acos(num2) * Math.Rad2Deg)

    @staticmethod
    def signed_angle(from_: 'Vector2', to_: 'Vector2') -> float:
        '''Gets the signed angle in degrees between from_ and to_.'''
        num = Vector2.angle(from_, to_)
        num2 = Math.sign(from_.x * to_.y - from_.y * to_.x)
        return num * num2


    @staticmethod
    def distance(a: 'Vector2', b: 'Vector2') -> float:
        '''Returns the distance between a and b.'''
        return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


    @staticmethod
    def clamp_magnitude(vector: 'Vector2', max_length: float) -> 'Vector2':
        '''Returns a copy of vector with its magnitude clamped to maxLength.'''
        num = vector.sqr_magnitude
        if (num > max_length * max_length):
            num2 = float(Math.sqrt(num))
            num3 = vector.x / num2
            num4 = vector.y / num2
            return Vector2(num3 * max_length, num4 * max_length)

        return vector


    @staticmethod
    def min(a: 'Vector2', b: 'Vector2') -> 'Vector2':
        '''Returns a vector that is made from the smallest components of two vectors.'''
        return Vector2(min(a.x, b.x), min(a.y, b.y))

    @staticmethod
    def max(a: 'Vector2', b: 'Vector2') -> 'Vector2':
        '''Returns a vector that is made from the largest components of two vectors.'''
        return Vector2(max(a.x, b.x), max(a.y, b.y))


    @staticmethod
    @overload
    def smooth_damp(current: 'Vector2', target: 'Vector2', current_velocity: 'Vector2', smooth_time: float, delta_time: float, max_speed: float = Math.PositiveInfinity) -> 'Vector2':
        '''Returns the current velocity + (target - current) * smooth_time * speed, clamped to the given max_speed.'''
        smooth_time = max(0.0001, smooth_time)
        num = 2.0 / smooth_time
        num2 = num * delta_time
        num3 = 1.0 / (1.0 + num2 + 0.48 * num2 * num2 + 0.235 * num2 * num2 * num2)
        num4 = current.x - target.x
        num5 = current.y - target.y
        vector = target
        num6 = max_speed * smooth_time
        num7 = num6 * num6
        num8 = num4 * num4 + num5 * num5
        if (num8 > num7):
            num9 = float(Math.sqrt(num8))
            num4 = num4 / num9 * num6
            num5 = num5 / num9 * num6

        target.x = current.x - num4
        target.y = current.y - num5
        num10 = (current_velocity.x + num * num4) * delta_time
        num11 = (current_velocity.y + num * num5) * delta_time
        current_velocity.x = (current_velocity.x - num * num10) * num3
        current_velocity.y = (current_velocity.y - num * num11) * num3
        num12 = target.x + (num4 + num10) * num3
        num13 = target.y + (num5 + num11) * num3
        num14 = vector.x - current.x
        num15 = vector.y - current.y
        num16 = num12 - vector.x
        num17 = num13 - vector.y
        if (num14 * num16 + num15 * num17 > 0.0):
            num12 = vector.x
            num13 = vector.y
            current_velocity.x = (num12 - vector.x) / delta_time
            current_velocity.y = (num13 - vector.y) / delta_time

        return Vector2(num12, num13)
#----------------------------------------------------------------------
