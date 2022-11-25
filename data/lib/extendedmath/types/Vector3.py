#----------------------------------------------------------------------

    # Libraries
from data.lib.extendedmath.Math import Math
from data.lib.utils import deprecated, classproperty
from data.lib.extendedmath.types import Vector2
from typing import overload
#----------------------------------------------------------------------

    # Class
class Vector3:
    '''Representation of 3D vectors and points.'''

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        ...

    @overload
    def __init__(self, x: int | float, y: int | float) -> None:
        ...

    @overload
    def __init__(self, vect: 'Vector3') -> None:
        ...

    @overload
    def __init__(self, vect: Vector2) -> None:
        ...

    @overload
    def __init__(self, xyz: int | float) -> None:
        ...

    def __init__(self, *args):
        if len(args) == 3 and all(isinstance(arg, (int, float)) for arg in args):
            self._x = args[0]
            self._y = args[1]
            self._z = args[2]

        elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
            self._x = args[0]
            self._y = args[1]
            self._z = 0.0

        elif len(args) == 1 and isinstance(args[0], Vector3):
            if isinstance(args[0], Vector3):
                self._x = args[0].x
                self._y = args[0].y
                self._z = args[0].z

            elif isinstance(args[0], Vector2):
                self._x = args[0].x
                self._y = args[0].y
                self._z = 0.0

            elif isinstance(args[0], (int, float)):
                self._x = args[0]
                self._y = args[0]
                self._z = args[0]

            else:
                raise TypeError("Invalid arguments")

        elif len(args) == 0:
            self._x = 0.0
            self._y = 0.0
            self._z = 0.0

        else:
            raise TypeError("Invalid arguments")


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


    def __getitem__(self, index: int) -> float:
        if not isinstance(index, (int)): raise TypeError("Vector3 indices must be integers")
        match index:
            case 0: return self.x
            case 1: return self.y
            case 2: return self.z
            case _: raise IndexError("Vector3 index out of range")

    def __setitem__(self, index: int, value: float) -> None:
        if not isinstance(index, (int)): raise TypeError("Vector3 indices must be integers")
        match index:
            case 0: self.x = value
            case 1: self.y = value
            case 2: self.z = value
            case _: raise IndexError("Vector3 index out of range")


    def __str__(self) -> str:
        '''Returns a formatted string for this vector.'''
        return f'Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})'
    
    def __repr__(self) -> str:
        '''Returns a formatted string for this vector.'''
        return f'Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})'


    @classproperty
    def zero(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(0, 0, 0).'''
        return Vector3(0, 0, 0)

    @classproperty
    def one(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(1, 1, 1).'''
        return Vector3(1, 1, 1)

    @classproperty
    def up(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(0, 1, 0).'''
        return Vector3(0, 1, 0)

    @classproperty
    def down(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(0, -1, 0).'''
        return Vector3(0, -1, 0)

    @classproperty
    def left(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(-1, 0, 0).'''
        return Vector3(-1, 0, 0)

    @classproperty
    def right(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(1, 0, 0).'''
        return Vector3(1, 0, 0)

    @classproperty
    def forward(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(0, 0, 1).'''
        return Vector3(0, 0, 1)

    @classproperty
    def backward(cls) -> 'Vector3':
        '''Shorthand for writing Vector3(0, 0, -1).'''
        return Vector3(0, 0, -1)


    def normalize(self) -> None:
        '''Makes this vector have a magnitude of 1.'''
        num = self.magnitude
        if (num > 1E-05): self /= num
        else: self = Vector3.zero

    @property
    def normalized(self) -> 'Vector3':
        '''Returns this vector with a magnitude of 1.'''
        return self / self.magnitude


    @property
    def magnitude(self) -> float:
        '''Returns the length of this vector.'''
        return Math.sqrt(self.sqr_magnitude)

    @property
    def sqr_magnitude(self) -> float:
        '''Returns the squared length of this vector.'''
        return self.x * self.x + self.y * self.y + self.z * self.z


    @staticmethod
    def slerp(a: 'Vector3', b: 'Vector3', t: float) -> 'Vector3':
        '''Spherically interpolates between two vectors.'''
        return Vector3.slerp_unclamped(a, b, Math.clamp(t, 0.0, 1.0))

    @staticmethod
    def slerp_unclamped(a: 'Vector3', b: 'Vector3', t: float) -> 'Vector3':
        '''Spherically interpolates between two vectors.'''
        dot = Vector3.dot(a, b)
        dot = Math.clamp(dot, -1.0, 1.0)

        theta = Math.acos(dot) * t
        relative_vec = b - a * dot
        relative_vec.normalize()

        return ((a * Math.cos(theta)) + (relative_vec * Math.sin(theta)))


    @staticmethod
    def rotate_towards(current: 'Vector3', target: 'Vector3', max_delta: float) -> 'Vector3':
        '''Rotates a vector towards a target vector.'''
        if current.sqr_magnitude == 0.0: return target

        angle = Math.acos(Math.clamp(Vector3.dot(current.normalized, target.normalized), -1.0, 1.0))
        if angle == 0.0: return current

        if angle > max_delta: angle = max_delta
        return Vector3.slerp(current.normalized, target.normalized, 1.0 - angle / max_delta).normalized * current.magnitude

    @staticmethod
    def lerp(a: 'Vector3', b: 'Vector3', t: float) -> 'Vector3':
        '''Linearly interpolates between two vectors.'''
        return a + (b - a) * Math.clamp01(t)

    @staticmethod
    def lerp_unclamped(a: 'Vector3', b: 'Vector3', t: float) -> 'Vector3':
        '''Linearly interpolates between two vectors.'''
        return a + (b - a) * t


    @staticmethod
    def move_towards(current: 'Vector3', target: 'Vector3', max_distance_delta: float) -> 'Vector3':
        '''Moves a vector towards a target vector.'''
        return current + (target - current).normalized * max_distance_delta


    @staticmethod
    def smooth_damp(current: 'Vector3', target: 'Vector3', current_velocity: 'Vector3', smooth_time: float, delta_time: float, max_speed: float = Math.PositiveInfinity) -> 'Vector3':
        '''Smoothly interpolates between current and target.'''
        num = 0.0
        num2 = 0.0
        num3 = 0.0
        smooth_time = Math.max(0.0001, smooth_time)
        num4 = 2.0 / smooth_time
        num5 = num4 * delta_time
        num6 = 1.0 / (1.0 + num5 + 0.48 * num5 * num5 + 0.235 * num5 * num5 * num5)
        num7 = current.x - target.x
        num8 = current.y - target.y
        num9 = current.z - target.z
        vector = Vector3(target)
        num10 = max_speed * smooth_time
        num11 = num10 * num10
        num12 = num7 * num7 + num8 * num8 + num9 * num9
        if (num12 > num11):
            num13 = float(Math.sqrt(num12))
            num7 = num7 / num13 * num10
            num8 = num8 / num13 * num10
            num9 = num9 / num13 * num10

        target.x = current.x - num7
        target.y = current.y - num8
        target.z = current.z - num9
        num14 = (current_velocity.x + num4 * num7) * delta_time
        num15 = (current_velocity.y + num4 * num8) * delta_time
        num16 = (current_velocity.z + num4 * num9) * delta_time
        current_velocity.x = (current_velocity.x - num4 * num14) * num6
        current_velocity.y = (current_velocity.y - num4 * num15) * num6
        current_velocity.z = (current_velocity.z - num4 * num16) * num6
        num = target.x + (num7 + num14) * num6
        num2 = target.y + (num8 + num15) * num6
        num3 = target.z + (num9 + num16) * num6
        num17 = vector.x - current.x
        num18 = vector.y - current.y
        num19 = vector.z - current.z
        num20 = num - vector.x
        num21 = num2 - vector.y
        num22 = num3 - vector.z
        if (num17 * num20 + num18 * num21 + num19 * num22 > 0.0):
            num = vector.x
            num2 = vector.y
            num3 = vector.z
            current_velocity.x = (num - vector.x) / delta_time
            current_velocity.y = (num2 - vector.y) / delta_time
            current_velocity.z = (num3 - vector.z) / delta_time

        return Vector3(num, num2, num3)


    def set(self, x: float, y: float, z: float) -> None:
        '''Set x, y and z components of an existing Vector3.'''
        self.x = x
        self.y = y
        self.z = z


    def copy(self) -> 'Vector3':
        '''Returns a copy of the vector.'''
        return Vector3(self.x, self.y, self.z)


    @overload
    def scale(self, scale: 'Vector3') -> None:
        '''Multiplies two vectors component-wise.'''
        ...

    @overload
    def scale(self, scale: int | float) -> None:
        '''Multiplies this vector by a number.'''
        ...

    def scale(self, scale: object) -> None:
        '''Multiplies this vector by a number or another vector.'''
        if isinstance(scale, Vector3):
            self.x *= scale.x
            self.y *= scale.y
            self.z *= scale.z

        elif isinstance(scale, (int, float)):
            self.x *= scale
            self.y *= scale
            self.z *= scale

        else:
            raise TypeError(f'Unsupported type {type(scale)} for scale')


    @overload
    def scaled(self, scale: 'Vector3') -> 'Vector3':
        '''Multiplies two vectors component-wise.'''
        ...

    @overload
    def scaled(self, scale: int | float) -> 'Vector3':
        '''Multiplies this vector by a number.'''
        ...

    def scaled(self, scale: object) -> 'Vector3':
        '''Multiplies this vector by a number or another vector.'''
        if isinstance(scale, Vector3):
            return Vector3(self.x * scale.x, self.y * scale.y, self.z * scale.z)

        elif isinstance(scale, (int, float)):
            return Vector3(self.x * scale, self.y * scale, self.z * scale)

        else:
            raise TypeError(f'Unsupported type {type(scale)} for scale')


    @staticmethod
    def cross(lhs: 'Vector3', rhs: 'Vector3') -> 'Vector3':
        '''Cross Product of two vectors.'''
        return Vector3(lhs.y * rhs.z - lhs.z * rhs.y, lhs.z * rhs.x - lhs.x * rhs.z, lhs.x * rhs.y - lhs.y * rhs.x)


    @staticmethod
    def reflect(in_direction: 'Vector3', in_normal: 'Vector3') -> 'Vector3':
        '''Reflects a vector off the plane defined by a normal.'''
        num = -2.0 * Vector3.dot(in_normal, in_direction)
        return in_direction + in_normal * num


    @staticmethod
    def dot(lhs: 'Vector3', rhs: 'Vector3') -> float:
        '''Dot Product of two vectors.'''
        return lhs.x * rhs.x + lhs.y * rhs.y + lhs.z * rhs.z


    @staticmethod
    def project(vector: 'Vector3', on_normal: 'Vector3') -> 'Vector3':
        '''Projects a vector onto another vector.'''
        num = Vector3.dot(on_normal, on_normal)
        if (num < Math.Epsilon): return Vector3.zero

        num2 = Vector3.dot(vector, on_normal)
        return Vector3(on_normal.x * num2 / num, on_normal.y * num2 / num, on_normal.z * num2 / num)


    @staticmethod
    def project_on_plane(vector: 'Vector3', plane_normal: 'Vector3') -> 'Vector3':
        '''Projects a vector onto a plane defined by a normal orthogonal to the plane.'''
        num = Vector3.dot(plane_normal, plane_normal)
        if (num < Math.Epsilon): return vector

        num2 = Vector3.dot(vector, plane_normal)
        return Vector3(vector.x - plane_normal.x * num2 / num, vector.y - plane_normal.y * num2 / num, vector.z - plane_normal.z * num2 / num)


    @staticmethod
    def angle(from_: 'Vector3', to_: 'Vector3') -> float:
        '''Calculates the angle between vectors from_ and to_.'''
        num = float(Math.sqrt(from_.sqr_magnitude * to_.sqr_magnitude))
        if (num < 1E-15): return 0.0

        num2 = Math.clamp(Vector3.dot(from_, to_) / num, -1.0, 1.0)
        return float(Math.acos(num2)) * Math.Rad2Deg

    @staticmethod
    def signed_angle(from_: 'Vector3', to_: 'Vector3', axis: 'Vector3') -> float:
        '''Calculates the signed angle between vectors from and to in relation to axis.'''
        num = Vector3.angle(from_, to_)
        num2 = from_.y * to_.z - from_.z * to_.y
        num3 = from_.z * to_.x - from_.x * to_.z
        num4 = from_.x * to_.y - from_.y * to_.x
        num5 = Math.sign(axis.x * num2 + axis.y * num3 + axis.z * num4)
        return -num * num5


    @staticmethod
    def distance(a: 'Vector3', b: 'Vector3') -> float:
        '''Returns the distance between a and b.'''
        vect = a - b
        return float(Math.sqrt(vect.x ** 2 + vect.y ** 2 + vect.z ** 2))

    @staticmethod
    def clamp_magnitude(vector: 'Vector3', max_length: float) -> 'Vector3':
        '''Returns a copy of vector with its magnitude clamped to max_length.'''
        num = vector.magnitude
        if (num > max_length): return vector.normalized * max_length
        return vector


    @staticmethod
    def min(lhs: 'Vector3', rhs: 'Vector3') -> 'Vector3':
        '''Returns a vector that is made from the smallest components of two vectors.'''
        return Vector3(min(lhs.x, rhs.x), min(lhs.y, rhs.y), min(lhs.z, rhs.z))

    @staticmethod
    def max(lhs: 'Vector3', rhs: 'Vector3') -> 'Vector3':
        '''Returns a vector that is made from the largest components of two vectors.'''
        return Vector3(max(lhs.x, rhs.x), max(lhs.y, rhs.y), max(lhs.z, rhs.z))


    @overload
    def __add__(self, other: 'Vector3') -> 'Vector3':
        '''Adds two vectors.'''
        ...

    @overload
    def __add__(self, other: int | float) -> 'Vector3':
        '''Adds a scalar to each component of a vector.'''
        ...

    def __add__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x + other, self.y + other, self.z + other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for addition')


    @overload
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        '''Subtracts two vectors.'''
        ...

    @overload
    def __sub__(self, other: int | float) -> 'Vector3':
        '''Subtracts a scalar from each component of a vector.'''
        ...

    def __sub__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x - other, self.y - other, self.z - other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for subtraction')


    @overload
    def __mul__(self, other: 'Vector3') -> 'Vector3':
        '''Multiplies two vectors.'''
        ...

    @overload
    def __mul__(self, other: int | float) -> 'Vector3':
        '''Multiplies a vector by a scalar.'''
        ...

    def __mul__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for multiplication')


    @overload
    def __truediv__(self, other: 'Vector3') -> 'Vector3':
        '''Divides two vectors.'''
        ...

    @overload
    def __truediv__(self, other: int | float) -> 'Vector3':
        '''Divides a vector by a scalar.'''
        ...

    def __truediv__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x / other, self.y / other, self.z / other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for division')


    @overload
    def __floordiv__(self, other: 'Vector3') -> 'Vector3':
        '''Divides two vectors.'''
        ...

    @overload
    def __floordiv__(self, other: int | float) -> 'Vector3':
        '''Divides a vector by a scalar.'''
        ...

    def __floordiv__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x // other.x, self.y // other.y, self.z // other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x // other, self.y // other, self.z // other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for division')


    @overload
    def __mod__(self, other: 'Vector3') -> 'Vector3':
        '''Returns the component-wise modulo of two vectors.'''
        ...

    @overload
    def __mod__(self, other: int | float) -> 'Vector3':
        '''Returns the component-wise modulo of a vector by a scalar.'''
        ...

    def __mod__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x % other.x, self.y % other.y, self.z % other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x % other, self.y % other, self.z % other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for modulo')


    @overload
    def __pow__(self, other: 'Vector3') -> 'Vector3':
        '''Returns the component-wise power of two vectors.'''
        ...

    @overload
    def __pow__(self, other: int | float) -> 'Vector3':
        '''Returns the component-wise power of a vector by a scalar.'''
        ...

    def __pow__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x ** other.x, self.y ** other.y, self.z ** other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x ** other, self.y ** other, self.z ** other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for power')


    def __abs__(self) -> 'Vector3':
        '''Returns the absolute value of a vector.'''
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __neg__(self) -> 'Vector3':
        '''Returns the negative of a vector.'''
        return Vector3(-self.x, -self.y, -self.z)

    def __pos__(self) -> 'Vector3':
        '''Returns the positive of a vector.'''
        return Vector3(+self.x, +self.y, +self.z)


    @overload
    def __and__(self, other: 'Vector3') -> 'Vector3':
        '''Returns the component-wise bitwise AND of two vectors.'''
        ...

    @overload
    def __and__(self, other: int | float) -> 'Vector3':
        '''Returns the component-wise bitwise AND of a vector by a scalar.'''
        ...

    def __and__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x & other.x, self.y & other.y, self.z & other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x & other, self.y & other, self.z & other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for bitwise AND')


    @overload
    def __or__(self, other: 'Vector3') -> 'Vector3':
        '''Returns the component-wise bitwise OR of two vectors.'''
        ...

    @overload
    def __or__(self, other: int) -> 'Vector3':
        '''Returns the component-wise bitwise OR of a vector by a scalar.'''
        ...

    def __or__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x | other.x, self.y | other.y, self.z | other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x | other, self.y | other, self.z | other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for bitwise OR')


    @overload
    def __xor__(self, other: 'Vector3') -> 'Vector3':
        '''Returns the component-wise bitwise XOR of two vectors.'''
        ...

    @overload
    def __xor__(self, other: int) -> 'Vector3':
        '''Returns the component-wise bitwise XOR of a vector by a scalar.'''
        ...

    def __xor__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x ^ other.x, self.y ^ other.y, self.z ^ other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x ^ other, self.y ^ other, self.z ^ other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for bitwise XOR')


    @overload
    def __lshift__(self, other: 'Vector3') -> 'Vector3':
        '''Returns the component-wise bitwise left shift of two vectors.'''
        ...

    @overload
    def __lshift__(self, other: int) -> 'Vector3':
        '''Returns the component-wise bitwise left shift of a vector by a scalar.'''
        ...

    def __lshift__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x << other.x, self.y << other.y, self.z << other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x << other, self.y << other, self.z << other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for bitwise left shift')


    @overload
    def __rshift__(self, other: 'Vector3') -> 'Vector3':
        '''Returns the component-wise bitwise right shift of two vectors.'''
        ...

    @overload
    def __rshift__(self, other: int) -> 'Vector3':
        '''Returns the component-wise bitwise right shift of a vector by a scalar.'''
        ...

    def __rshift__(self, other: object) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x >> other.x, self.y >> other.y, self.z >> other.z)

        elif isinstance(other, (int, float)):
            return Vector3(self.x >> other, self.y >> other, self.z >> other)

        else:
            raise TypeError(f'Unsupported type {type(other)} for bitwise right shift')


    def __invert__(self) -> 'Vector3':
        '''Returns the component-wise bitwise inverse of a vector.'''
        return Vector3(~self.x, ~self.y, ~self.z)


    def __bool__(self) -> bool:
        '''Returns True if all components are non-zero.'''
        return self.x != 0 and self.y != 0 and self.z != 0


    def __hash__(self) -> int:
        '''Returns the hash of the vector.'''
        return hash(self.x) ^ hash(self.y << 2) ^ hash(self.z >> 2)


    def __eq__(self, other: 'Vector3') -> bool:
        '''Returns whether two vectors are equal.'''
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: 'Vector3') -> bool:
        '''Returns whether two vectors are not equal.'''
        return self.x != other.x or self.y != other.y or self.z != other.z


    @staticmethod
    @deprecated('Use Vector3.angle instead. angle_between uses radians instead of degrees and was deprecated for this reason.')
    def angle_between(from_: 'Vector3', to_: 'Vector3') -> float:
        '''[Obsolete] Use Vector3.angle instead. angle_between uses radians instead of degrees and was deprecated for this reason.'''
        return Math.acos(Math.clamp(Vector3.dot(from_.normalized, to_.normalized), -1.0, 1.0))

    @staticmethod
    @deprecated('Use Vector3.project_on_plane instead.')
    def exclude(exclude_this: 'Vector3', from_that: 'Vector3') -> 'Vector3':
        '''[Obsolete] Use Vector3.project_on_plane instead.'''
        return Vector3.project_on_plane(from_that, exclude_this)
#----------------------------------------------------------------------
