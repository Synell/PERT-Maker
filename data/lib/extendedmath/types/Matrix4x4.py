#----------------------------------------------------------------------

    # Libraries
from data.lib.extendedmath.Math import Math
from typing import overload
from data.lib.extendedmath.types import Vector3, Vector4
from data.lib.utils import classproperty
#----------------------------------------------------------------------

    # Class
class Quaternion: pass

class Matrix4x4:

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, column0: Vector4, column1: Vector4, column2: Vector4, column3: Vector4) -> None:
        ...

    @overload
    def __init__(self, m00: int | float, m01: int | float, m02: int | float, m03: int | float, m10: int | float, m11: int | float, m12: int | float, m13: int | float, m20: int | float, m21: int | float, m22: int | float, m23: int | float, m30: int | float, m31: int | float, m32: int | float, m33: int | float) -> None:
        ...

    def __init__(self, *args: object) -> None:
        if len(args) == 0:
            self._m = [[0.0 for x in range(4)] for y in range(4)]

        elif len(args) == 4 and all(isinstance(arg, Vector4) for arg in args):
            self._m = [
                [args[0].x, args[1].x, args[2].x, args[3].x],
                [args[0].y, args[1].y, args[2].y, args[3].y],
                [args[0].z, args[1].z, args[2].z, args[3].z],
                [args[0].w, args[1].w, args[2].w, args[3].w]
            ]

        elif len(args) == 16 and all(isinstance(arg, (int, float)) for arg in args):
            self._m = [
                [args[0], args[1], args[2], args[3]],
                [args[4], args[5], args[6], args[7]],
                [args[8], args[9], args[10], args[11]],
                [args[12], args[13], args[14], args[15]]
            ]

        else:
            raise TypeError(f'Invalid number of arguments: {len(args)}')


    @property
    def m00(self) -> float:
        return self._m[0][0]

    @m00.setter
    def m00(self, value: float) -> None:
        self._m[0][0] = value


    @property
    def m01(self) -> float:
        return self._m[0][1]

    @m01.setter
    def m01(self, value: float) -> None:
        self._m[0][1] = value


    @property
    def m02(self) -> float:
        return self._m[0][2]

    @m02.setter
    def m02(self, value: float) -> None:
        self._m[0][2] = value


    @property
    def m03(self) -> float:
        return self._m[0][3]

    @m03.setter
    def m03(self, value: float) -> None:
        self._m[0][3] = value


    @property
    def m10(self) -> float:
        return self._m[1][0]

    @m10.setter
    def m10(self, value: float) -> None:
        self._m[1][0] = value


    @property
    def m11(self) -> float:
        return self._m[1][1]

    @m11.setter
    def m11(self, value: float) -> None:
        self._m[1][1] = value


    @property
    def m12(self) -> float:
        return self._m[1][2]

    @m12.setter
    def m12(self, value: float) -> None:
        self._m[1][2] = value


    @property
    def m13(self) -> float:
        return self._m[1][3]

    @m13.setter
    def m13(self, value: float) -> None:
        self._m[1][3] = value


    @property
    def m20(self) -> float:
        return self._m[2][0]

    @m20.setter
    def m20(self, value: float) -> None:
        self._m[2][0] = value


    @property
    def m21(self) -> float:
        return self._m[2][1]

    @m21.setter
    def m21(self, value: float) -> None:
        self._m[2][1] = value


    @property
    def m22(self) -> float:
        return self._m[2][2]

    @m22.setter
    def m22(self, value: float) -> None:
        self._m[2][2] = value


    @property
    def m23(self) -> float:
        return self._m[2][3]

    @m23.setter
    def m23(self, value: float) -> None:
        self._m[2][3] = value


    @property
    def m30(self) -> float:
        return self._m[3][0]

    @m30.setter
    def m30(self, value: float) -> None:
        self._m[3][0] = value


    @property
    def m31(self) -> float:
        return self._m[3][1]

    @m31.setter
    def m31(self, value: float) -> None:
        self._m[3][1] = value


    @property
    def m32(self) -> float:
        return self._m[3][2]

    @m32.setter
    def m32(self, value: float) -> None:
        self._m[3][2] = value


    @property
    def m33(self) -> float:
        return self._m[3][3]

    @m33.setter
    def m33(self, value: float) -> None:
        self._m[3][3] = value


    def get_column(self, index: int) -> Vector4:
        '''Gets a column of the matrix.'''
        return Vector4(self._m[0][index], self._m[1][index], self._m[2][index], self._m[3][index])

    def get_row(self, index: int) -> Vector4:
        '''Gets a row of the matrix.'''
        return Vector4(self._m[index][0], self._m[index][1], self._m[index][2], self._m[index][3])


    @classproperty
    def zero_matrix(cls) -> 'Matrix4x4':
        return Matrix4x4(
            Vector4(0.0, 0.0, 0.0, 0.0),
            Vector4(0.0, 0.0, 0.0, 0.0),
            Vector4(0.0, 0.0, 0.0, 0.0),
            Vector4(0.0, 0.0, 0.0, 0.0)
        )

    @classproperty
    def identity_matrix(cls) -> 'Matrix4x4':
        return Matrix4x4(
            Vector4(1.0, 0.0, 0.0, 0.0),
            Vector4(0.0, 1.0, 0.0, 0.0),
            Vector4(0.0, 0.0, 1.0, 0.0),
            Vector4(0.0, 0.0, 0.0, 1.0)
        )


    def is_identity(self) -> bool:
        '''Checks whether this is an identity matrix.'''
        return self == Matrix4x4.identity_matrix()


    def lossy_scale(self) -> Vector3:
        '''Attempts to get a scale value from the matrix.'''
        return Vector3(
            Math.sqrt(self.m00 * self.m00 + self.m01 * self.m01 + self.m02 * self.m02),
            Math.sqrt(self.m10 * self.m10 + self.m11 * self.m11 + self.m12 * self.m12),
            Math.sqrt(self.m20 * self.m20 + self.m21 * self.m21 + self.m22 * self.m22)
        )


    def determinant(self) -> float:
        '''The determinant of the matrix.'''
        return (
            self.m00 * (self.m11 * self.m22 - self.m12 * self.m21) +
            self.m01 * (self.m12 * self.m20 - self.m10 * self.m22) +
            self.m02 * (self.m10 * self.m21 - self.m11 * self.m20)
        )


    def inverse(self) -> 'Matrix4x4':
        '''The inverse of this matrix.'''
        determinant = self.determinant()
        if determinant == 0.0:
            return Matrix4x4.zero_matrix()
        else:
            return Matrix4x4(
                Vector4(
                    (self.m11 * self.m22 - self.m12 * self.m21) / determinant,
                    (self.m12 * self.m20 - self.m10 * self.m22) / determinant,
                    (self.m10 * self.m21 - self.m11 * self.m20) / determinant,
                    0.0
                ),
                Vector4(
                    (self.m02 * self.m21 - self.m01 * self.m22) / determinant,
                    (self.m00 * self.m22 - self.m02 * self.m20) / determinant,
                    (self.m01 * self.m20 - self.m00 * self.m21) / determinant,
                    0.0
                ),
                Vector4(
                    (self.m01 * self.m12 - self.m02 * self.m11) / determinant,
                    (self.m02 * self.m10 - self.m00 * self.m12) / determinant,
                    (self.m00 * self.m11 - self.m01 * self.m10) / determinant,
                    0.0
                ),
                Vector4(
                    (self.m02 * self.m11 - self.m01 * self.m12) / determinant,
                    (self.m00 * self.m12 - self.m02 * self.m10) / determinant,
                    (self.m01 * self.m10 - self.m00 * self.m11) / determinant,
                    1.0
                )
            )


    def transpose(self) -> 'Matrix4x4':
        '''Returns the transpose of this matrix.'''
        return Matrix4x4(
            Vector4(self.m00, self.m10, self.m20, self.m30),
            Vector4(self.m01, self.m11, self.m21, self.m31),
            Vector4(self.m02, self.m12, self.m22, self.m32),
            Vector4(self.m03, self.m13, self.m23, self.m33)
        )


    def __getitem__(self, index: int) -> Vector4:
        return self._m[index % 4][index // 4]

    def __setitem__(self, index: int, value: Vector4) -> None:
        self._m[index % 4][index // 4] = value


    def __str__(self) -> str:
        s = []
        x = 1
        for row in self._m:
            for item in row:
                x = max(x, len(str(item)))
        x += 1
        for row in self._m: s.append(' '.join(str(item).rjust(x) for item in row))

        s[0] = '⎧' + ((x // 2) * ' ') + s[0] + ((x // 2) * ' ') + '⎫'
        for index, row in enumerate(s[1:-1]): s[index + 1] = '⎪' + ((x // 2) * ' ') + row + ((x // 2) * ' ') + '⎪'
        s[-1] = '⎩' + ((x // 2) * ' ') + s[-1] + ((x // 2) * ' ') + '⎭'

        return '\n'.join(s)

    def __repr__(self) -> str:
        return self.__str__()


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix4x4):
            return False
        return self._m == other._m

    def __ne__(self, other: object) -> bool:
        return not self == other


    @staticmethod
    def ortho(left: float, right: float, bottom: float, top: float, z_near: float, z_far: float) -> 'Matrix4x4':
        '''Creates an orthographic projection matrix.'''
        return Matrix4x4(
            Vector4(2.0 / (right - left), 0.0, 0.0, 0.0),
            Vector4(0.0, 2.0 / (top - bottom), 0.0, 0.0),
            Vector4(0.0, 0.0, -2.0 / (z_far - z_near), 0.0),
            Vector4(-(right + left) / (right - left), -(top + bottom) / (top - bottom), -(z_far + z_near) / (z_far - z_near), 1.0)
        )


    @staticmethod
    def perspective(fov: float, aspect: float, z_near: float, z_far: float) -> 'Matrix4x4':
        '''Creates a perspective projection matrix.'''
        tan_half_fov = Math.tan(fov / 2.0)
        return Matrix4x4(
            Vector4(1.0 / (aspect * tan_half_fov), 0.0, 0.0, 0.0),
            Vector4(0.0, 1.0 / tan_half_fov, 0.0, 0.0),
            Vector4(0.0, 0.0, -(z_far + z_near) / (z_far - z_near), -1.0),
            Vector4(0.0, 0.0, -(2.0 * z_far * z_near) / (z_far - z_near), 0.0)
        )


    @staticmethod
    def look_at(from_: Vector3, to_: Vector3, up: Vector3) -> 'Matrix4x4':
        '''Creates a view matrix for the given eye position, target and up vector.'''
        forward = (to_ - from_).normalized
        right = Vector3.cross(forward, up).normalized
        up = Vector3.cross(right, forward).normalized
        return Matrix4x4(
            Vector4(right.x, right.y, right.z, -Vector3.dot(right, from_)),
            Vector4(up.x, up.y, up.z, -Vector3.dot(up, from_)),
            Vector4(forward.x, forward.y, forward.z, -Vector3.dot(forward, from_)),
            Vector4(0.0, 0.0, 0.0, 1.0)
        )


    @staticmethod
    def frustum(left: float, right: float, bottom: float, top: float, z_near: float, z_far: float) -> 'Matrix4x4':
        '''Creates a perspective projection matrix.'''
        a = (right + left) / (right - left)
        b = (top + bottom) / (top - bottom)
        c = -(z_far + z_near) / (z_far - z_near)
        d = -(2.0 * z_far * z_near) / (z_far - z_near)
        return Matrix4x4(
            Vector4(2.0 * z_near / (right - left), 0.0, 0.0, 0.0),
            Vector4(0.0, 2.0 * z_near / (top - bottom), 0.0, 0.0),
            Vector4(a, b, c, -1.0),
            Vector4(0.0, 0.0, d, 0.0)
        )


    def __hash__(self) -> int:
        return hash(self.get_column(0)) ^ hash(self.get_column(1) << 2) ^ hash(self.get_column(2) >> 2) ^ hash(self.get_column(3) >> 1)

    @overload
    def __mul__(self, other: 'Matrix4x4') -> 'Matrix4x4':
        ...

    @overload
    def __mul__(self, other: Vector4) -> Vector4:
        ...

    def __mul__(self, other: object) -> object:
        if isinstance(other, Matrix4x4):
            return Matrix4x4(
                Vector4(
                    self.m00 * other.m00 + self.m01 * other.m10 + self.m02 * other.m20 + self.m03 * other.m30,
                    self.m00 * other.m01 + self.m01 * other.m11 + self.m02 * other.m21 + self.m03 * other.m31,
                    self.m00 * other.m02 + self.m01 * other.m12 + self.m02 * other.m22 + self.m03 * other.m32,
                    self.m00 * other.m03 + self.m01 * other.m13 + self.m02 * other.m23 + self.m03 * other.m33
                ),
                Vector4(
                    self.m10 * other.m00 + self.m11 * other.m10 + self.m12 * other.m20 + self.m13 * other.m30,
                    self.m10 * other.m01 + self.m11 * other.m11 + self.m12 * other.m21 + self.m13 * other.m31,
                    self.m10 * other.m02 + self.m11 * other.m12 + self.m12 * other.m22 + self.m13 * other.m32,
                    self.m10 * other.m03 + self.m11 * other.m13 + self.m12 * other.m23 + self.m13 * other.m33
                ),
                Vector4(
                    self.m20 * other.m00 + self.m21 * other.m10 + self.m22 * other.m20 + self.m23 * other.m30,
                    self.m20 * other.m01 + self.m21 * other.m11 + self.m22 * other.m21 + self.m23 * other.m31,
                    self.m20 * other.m02 + self.m21 * other.m12 + self.m22 * other.m22 + self.m23 * other.m32,
                    self.m20 * other.m03 + self.m21 * other.m13 + self.m22 * other.m23 + self.m23 * other.m33
                ),
                Vector4(
                    self.m30 * other.m00 + self.m31 * other.m10 + self.m32 * other.m20 + self.m33 * other.m30,
                    self.m30 * other.m01 + self.m31 * other.m11 + self.m32 * other.m21 + self.m33 * other.m31,
                    self.m30 * other.m02 + self.m31 * other.m12 + self.m32 * other.m22 + self.m33 * other.m32,
                    self.m30 * other.m03 + self.m31 * other.m13 + self.m32 * other.m23 + self.m33 * other.m33
                )
            )

        elif isinstance(other, Vector4):
            return Vector4(
                self.m00 * other.x + self.m01 * other.y + self.m02 * other.z + self.m03 * other.w,
                self.m10 * other.x + self.m11 * other.y + self.m12 * other.z + self.m13 * other.w,
                self.m20 * other.x + self.m21 * other.y + self.m22 * other.z + self.m23 * other.w,
                self.m30 * other.x + self.m31 * other.y + self.m32 * other.z + self.m33 * other.w
            )

        else:
            raise TypeError(f'Cannot multiply Matrix4x4 with {type(other)}')


    def get_position(self) -> Vector3:
        return Vector3(self.m03, self.m13, self.m23)


    def set_column(self, index: int, value: Vector4):
        self._m[0][index] = value.x
        self._m[1][index] = value.y
        self._m[2][index] = value.z
        self._m[3][index] = value.w

    def set_row(self, index: int, value: Vector4):
        self._m[index][0] = value.x
        self._m[index][1] = value.y
        self._m[index][2] = value.z
        self._m[index][3] = value.w


    def multiply_point(self, point: Vector3) -> Vector3:
        '''Transforms a position by this matrix (generic).'''
        return Vector3(
            self.m00 * point.x + self.m01 * point.y + self.m02 * point.z + self.m03,
            self.m10 * point.x + self.m11 * point.y + self.m12 * point.z + self.m13,
            self.m20 * point.x + self.m21 * point.y + self.m22 * point.z + self.m23
        )


    def multiply_point_3x4(self, point: Vector3) -> Vector3:
        '''Transforms a position by this matrix (fast).'''
        return Vector3(
            self.m00 * point.x + self.m01 * point.y + self.m02 * point.z + self.m03,
            self.m10 * point.x + self.m11 * point.y + self.m12 * point.z + self.m13,
            self.m20 * point.x + self.m21 * point.y + self.m22 * point.z + self.m23
        )

    def multiply_vector(self, vector: Vector3) -> Vector3:
        '''Transforms a direction by this matrix.'''
        return Vector3(
            self.m00 * vector.x + self.m01 * vector.y + self.m02 * vector.z,
            self.m10 * vector.x + self.m11 * vector.y + self.m12 * vector.z,
            self.m20 * vector.x + self.m21 * vector.y + self.m22 * vector.z
        )


    @staticmethod
    def scale(scale: Vector3) -> 'Matrix4x4':
        '''Creates a scale matrix.'''
        return Matrix4x4(
            scale.x, 0, 0, 0,
            0, scale.y, 0, 0,
            0, 0, scale.z, 0,
            0, 0, 0, 1
        )


    @staticmethod
    def translate(translation: Vector3) -> 'Matrix4x4':
        '''Creates a translation matrix.'''
        return Matrix4x4(
            1, 0, 0, translation.x,
            0, 1, 0, translation.y,
            0, 0, 1, translation.z,
            0, 0, 0, 1
        )


    @staticmethod
    def rotate(q: Quaternion):
        '''Creates a rotation matrix.'''
        return Matrix4x4(
            1 - 2 * (q.y * q.y + q.z * q.z), 2 * (q.x * q.y + q.w * q.z), 2 * (q.x * q.z - q.w * q.y), 0,
            2 * (q.x * q.y - q.w * q.z), 1 - 2 * (q.x * q.x + q.z * q.z), 2 * (q.y * q.z + q.w * q.x), 0,
            2 * (q.x * q.z + q.w * q.y), 2 * (q.y * q.z - q.w * q.x), 1 - 2 * (q.x * q.x + q.y * q.y), 0,
            0, 0, 0, 1
        )
#----------------------------------------------------------------------
