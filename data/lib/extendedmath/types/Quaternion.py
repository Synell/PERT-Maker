#----------------------------------------------------------------------

    # Libraries
from data.lib.extendedmath.Math import Math
from data.lib.extendedmath.types import Vector3, Matrix4x4
from typing import overload
from data.lib.utils import classproperty
#----------------------------------------------------------------------

    # Class
class Quaternion:
    '''Quaternions are used to represent rotations.'''

    @overload
    def __init__(self) -> None:
        '''Creates a new Quaternion with a magnitude of 1.'''
        ...

    @overload
    def __init__(self, x: int | float, y: int | float, z: int | float, w: int | float) -> None:
        '''Creates a new Quaternion with the given values.'''
        ...

    @overload
    def __init__(self, other: 'Quaternion') -> None:
        '''Creates a new Quaternion with the given values.'''
        ...

    def __init__(self, *args: object) -> None:
        if (len(args) == 0):
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            self.w = 1.0

        elif (len(args) == 4) and all(isinstance(arg, (int, float)) for arg in args):
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.w = args[3]

        elif (len(args) == 1) and isinstance(args[0], Quaternion):
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
            self.w = args[0].w

        else:
            raise TypeError('Invalid arguments!')


    @property
    def x(self) -> float:
        '''The x component of the Quaternion. Don't modify this directly unless you know quaternions inside out.'''
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value


    @property
    def y(self) -> float:
        '''The y component of the Quaternion. Don't modify this directly unless you know quaternions inside out.'''
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value


    @property
    def z(self) -> float:
        '''The z component of the Quaternion. Don't modify this directly unless you know quaternions inside out.'''
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        self._z = value


    @property
    def w(self) -> float:
        '''The w component of the Quaternion. Don't modify this directly unless you know quaternions inside out.'''
        return self._w

    @w.setter
    def w(self, value: float) -> None:
        self._w = value


    @overload
    def set(self, x: int | float, y: int | float, z: int | float, w: int | float) -> None:
        '''Sets the Quaternion to the given values.'''
        ...

    @overload
    def set(self, other: 'Quaternion') -> None:
        '''Sets this quaternion to the values of the other quaternion.'''
        ...

    def set(self, *args: object) -> None:
        if (len(args) == 4) and all(isinstance(arg, (int, float)) for arg in args):
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.w = args[3]

        elif (len(args) == 1) and isinstance(args[0], Quaternion):
            self.x, self.y, self.z, self.w = args[0].x, args[0].y, args[0].z, args[0].w

        else:
            raise TypeError('Invalid arguments!')


    def __str__(self) -> str:
        return f'Quaternion({self.x}, {self.y}, {self.z}, {self.w})'

    def __repr__(self) -> str:
        return f'Quaternion({self.x}, {self.y}, {self.z}, {self.w})'


    @classproperty
    def identity(cls) -> 'Quaternion':
        '''The identity Quaternion.'''
        return Quaternion(0.0, 0.0, 0.0, 1.0)


    def __getitem__(self, index: int) -> float:
        match index:
            case 0: return self.x
            case 1: return self.y
            case 2: return self.z
            case 3: return self.w
            case _: raise IndexError('Invalid Quaternion index!')


    def __setitem__(self, index: int, value: float) -> None:
        match index:
            case 0: self.x = value
            case 1: self.y = value
            case 2: self.z = value
            case 3: self.w = value
            case _: raise IndexError('Invalid Quaternion index!')


    @property
    def euler_angles_rad(self) -> Vector3:
        '''Returns the Euler angles (in radians) of this Quaternion.'''
        angles = Vector3.zero
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x * self.x + self.y * self.y)
        angles.x = Math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (self.w * self.y - self.z * self.x)
        if (abs(sinp) >= 1):
            angles.y = Math.sign(Math.min(Math.PI / 2, sinp)) # Use 90 degrees if out of range
        else:
            angles.y = Math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y * self.y + self.z * self.z)
        angles.z = Math.atan2(siny_cosp, cosy_cosp)

        return angles

    @euler_angles_rad.setter
    def euler_angles_rad(self, value: Vector3) -> None:
        cy = Math.cos(value.z * 0.5)
        sy = Math.sin(value.z * 0.5)
        cp = Math.cos(value.y * 0.5)
        sp = Math.sin(value.y * 0.5)
        cr = Math.cos(value.x * 0.5)
        sr = Math.sin(value.x * 0.5)
        self.x = sr * cp * cy - cr * sp * sy
        self.y = cr * sp * cy + sr * cp * sy
        self.z = cr * cp * sy - sr * sp * cy
        self.w = cr * cp * cy + sr * sp * sy


    @property
    def euler_angles(self) -> Vector3:
        '''Returns the Euler angles (in degrees) of this Quaternion.'''
        angles = self.euler_angles_rad
        return Vector3(angles.x * Math.Rad2Deg, angles.y * Math.Rad2Deg, angles.z * Math.Rad2Deg)

    @euler_angles.setter
    def euler_angles(self, value: Vector3) -> None:
        self.euler_angles_rad = Vector3(value.x * Math.Deg2Rad, value.y * Math.Deg2Rad, value.z * Math.Deg2Rad)


    def normalize(self) -> 'Quaternion':
        '''Normalizes this quaternion.'''
        num = Math.sqrt(Quaternion.dot(self, self))
        if (num < Math.Epsilon): return Quaternion.identity
        self = Quaternion(self.x / num, self.y / num, self.z / num, self.w / num)

    @property
    def normalized(self) -> 'Quaternion':
        '''Returns this quaternion with a magnitude of 1.'''
        num = Math.sqrt(Quaternion.dot(self, self))
        if (num < Math.Epsilon): return Quaternion.identity
        return Quaternion(self.x / num, self.y / num, self.z / num, self.w / num)


    @staticmethod
    def from_to_rotation(from_: Vector3, to_: Vector3) -> 'Quaternion':
        '''Creates a rotation which rotates from from_direction to to_direction.'''
        from_ = from_.normalized
        to_ = to_.normalized
        dot = Vector3.dot(from_, to_)
        if (dot < -1):
            dot = -1
        if (dot > 1):
            dot = 1
        angle = Math.acos(dot)
        axis = Vector3.cross(from_, to_)
        return Quaternion(axis.x, axis.y, axis.z, angle)


    @staticmethod
    def inverse(rotation: 'Quaternion') -> 'Quaternion':
        '''Returns the Inverse of rotation.'''
        return Quaternion(-rotation.x, -rotation.y, -rotation.z, rotation.w)


    @staticmethod
    def slerp(a: 'Quaternion', b: 'Quaternion', t: float) -> 'Quaternion':
        '''A quaternion spherically interpolated between quaternions a and b.'''
        if (t <= 0.0):
            return a
        if (t >= 1.0):
            return b
        return Quaternion.slerp_unclamped(a, b, t)

    @staticmethod
    def slerp_unclamped(a: 'Quaternion', b: 'Quaternion', t: float) -> 'Quaternion':
        '''Spherically interpolates between a and b by t. The parameter t is not clamped.'''
        cosom = a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w
        if (abs(cosom) >= 1.0):
            return a
        omega = Math.acos(cosom)
        sinom = Math.sin(omega)
        sclp = Math.sin((1.0 - t) * omega) / sinom
        sclq = Math.sin(t * omega) / sinom
        return Quaternion(
            a.x * sclp + b.x * sclq,
            a.y * sclp + b.y * sclq,
            a.z * sclp + b.z * sclq,
            a.w * sclp + b.w * sclq
        )


    @staticmethod
    def lerp(a: 'Quaternion', b: 'Quaternion', t: float) -> 'Quaternion':
        ''' Interpolates between a and b by t and normalizes the result afterwards. The parameter t is clamped to the range [0, 1].'''
        t = Math.clamp(t, 0.0, 1.0)
        return Quaternion.lerp_unclamped(a, b, t)

    @staticmethod
    def lerp_unclamped(a: 'Quaternion', b: 'Quaternion', t: float) -> 'Quaternion':
        '''Interpolates between a and b by t and normalizes the result afterwards. The parameter t is not clamped.'''
        return Quaternion(
            a.x + t * (b.x - a.x),
            a.y + t * (b.y - a.y),
            a.z + t * (b.z - a.z),
            a.w + t * (b.w - a.w)
        )


    @staticmethod
    def angle_axis(angle: float, axis: Vector3) -> 'Quaternion':
        '''Creates a rotation which rotates angle degrees around axis.'''
        axis = axis.normalized
        sin = Math.sin(angle * 0.5)
        return Quaternion(axis.x * sin, axis.y * sin, axis.z * sin, Math.cos(angle * 0.5))


    @staticmethod
    def look_rotation(forward: Vector3, upwards: Vector3 = Vector3.up) -> 'Quaternion':
        '''Creates a rotation which looks in the direction of forward, using upwards as up.'''
        forward = forward.normalized
        upwards = upwards.normalized
        if (forward.x == 0 and forward.y == 0 and forward.z == 0):
            return Quaternion.identity
        right = Vector3.cross(upwards, forward)
        right = right.normalized
        up = Vector3.cross(forward, right)
        up = up.normalized
        m = Matrix4x4()
        m.m00 = right.x
        m.m01 = right.y
        m.m02 = right.z
        m.m10 = up.x
        m.m11 = up.y
        m.m12 = up.z
        m.m20 = forward.x
        m.m21 = forward.y
        m.m22 = forward.z
        return Quaternion(m)


    @overload
    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        '''Multiplies two quaternions.'''
        ...

    @overload
    def __mul__(self, other: Vector3) -> Vector3:
        '''Multiplies a quaternion by a vector.'''
        ...

    def __mul__(self, other: object) -> object:
        if isinstance(other, Quaternion):
            return Quaternion(
                self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
                self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z,
                self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x,
                self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            )

        elif isinstance(other, Vector3):
            num = self.x * 2.0
            num2 = self.y * 2.0
            num3 = self.z * 2.0
            num4 = self.x * num
            num5 = self.y * num2
            num6 = self.z * num3
            num7 = self.x * num2
            num8 = self.x * num3
            num9 = self.y * num3
            num10 = self.w * num
            num11 = self.w * num2
            num12 = self.w * num3
            result = Vector3.zero
            result.x = (1.0 - (num5 + num6)) * other.x + (num7 - num12) * other.y + (num8 + num11) * other.z
            result.y = (num7 + num12) * other.x + (1.0 - (num4 + num6)) * other.y + (num9 - num10) * other.z
            result.z = (num8 - num11) * other.x + (num9 + num10) * other.y + (1.0 - (num4 + num5)) * other.z
            return result

        else:
            raise TypeError('unsupported operand type(s) for *: \'Quaternion\' and \'{}\''.format(type(other).__name__))


    def _is_equal_using_dot(dot: float) -> bool:
        '''Determines whether two quaternions are equal.'''
        return dot > 0.999999


    def __eq__(self, other: object) -> bool:
        '''Determines whether this quaternion is equal to another quaternion, within a tolerance.'''
        if (isinstance(other, Quaternion)):
            return Quaternion._is_equal_using_dot(Quaternion.dot(self, other))
        return False

    def __ne__(self, other: object) -> bool:
        '''Determines whether this quaternion is not equal to another quaternion, within a tolerance.'''
        return not self == other


    @staticmethod
    def dot(a: 'Quaternion', b: 'Quaternion') -> float:
        '''The dot product between two rotations.'''
        return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w


    def set_look_rotation(self, view: Vector3, up: Vector3 = Vector3.up) -> None:
        '''Sets this quaternion to a rotation which looks in the direction of view, using up as up.'''
        self = self.look_rotation(view, up)


    @staticmethod
    def angle(a: 'Quaternion', b: 'Quaternion') -> float:
        '''The angle between two rotations.'''
        # return Math.acos(Math.clamp(Quaternion.dot(a, b), -1.0, 1.0)) * 2.0
        num = Math.min(Math.abs(Quaternion.dot(a, b)), 1.0)
        return 0.0 if Quaternion._is_equal_using_dot(num) else (Math.acos(num) * 2.0 * Math.Rad2Deg)

    def to_angle_axis(self) -> tuple[float, Vector3]:
        '''Converts this quaternion to an angle and axis.'''
        angle = 2.0 * Math.acos(self.w)
        s = Math.sqrt(1.0 - self.w * self.w)
        if (s < 0.001):
            return angle, Vector3(1.0, 0.0, 0.0)
        return angle, Vector3(self.x / s, self.y / s, self.z / s)


    @staticmethod
    def euler(x: int | float, y: int | float, z: int | float) -> 'Quaternion':
        '''Creates a quaternion from Euler angles in degrees.'''
        return Quaternion.euler_rad(Math.radians(x) * Math.Deg2Rad, y * Math.Deg2Rad, z * Math.Deg2Rad)

    @staticmethod
    def euler_rad(x: int | float, y: int | float, z: int | float) -> 'Quaternion':
        '''Creates a quaternion from Euler angles in radians.'''
        q = Quaternion()
        q.euler_angles_rad = Vector3(x, y, z)
        return q


    def set_from_to_rotation(self, from_direction: Vector3, to_direction: Vector3) -> None:
        '''Sets this quaternion to a rotation which rotates from one direction to another.'''
        self = self.from_to_rotation(from_direction, to_direction)


    @staticmethod
    def rotate_towards(from_: 'Quaternion', to_: 'Quaternion', max_degrees_delta: float) -> 'Quaternion':
        '''Rotates a direction from one direction to another.'''
        num = Quaternion.angle(from_, to_)
        if (num == 0.0): return to_
        return Quaternion.slerp_unclamped(from_, to_, Math.min(1.0, max_degrees_delta / num))


    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y << 2) ^ hash(self.z >> 2) ^ hash(self.w >> 1)
#----------------------------------------------------------------------
