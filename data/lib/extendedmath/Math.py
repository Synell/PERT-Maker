#----------------------------------------------------------------------

    # Libraries
import math
from typing import overload
#----------------------------------------------------------------------

    # Class
class Math:
    '''A collection of common math functions.'''

    Infinity = float('inf')
    PositiveInfinity = float('inf')
    NegativeInfinity = float('-inf')

    PI = math.pi
    Deg2Rad = PI / 180.0
    Rad2Deg = 180.0 / PI # 57.29578

    Epsilon = 1.0e-06


    def __new__(cls) -> None: return None


    @staticmethod
    def closest_power_of_two(value: int) -> int:
        '''Returns the closest power of two value.'''
        n = Math.previous_power_of_two(value)
        return n if value <= n + (n / 2) else n << 1


    @staticmethod
    def is_power_of_two(value: int) -> bool:
        '''Returns true if the value is a power of two.'''
        return (value & (value - 1)) == 0


    @staticmethod
    def previous_power_of_two(value: int) -> int:
        '''Returns the previous power of two value.'''
        n = Math.next_power_of_two(value)
        return n if n <= value else n >> 1

    @staticmethod
    def next_power_of_two(value: int) -> int:
        '''Returns the next power of two value.'''
        return 1 << (value - 1).bit_length()


    @staticmethod
    def gamma_to_linear_space(value: float) -> float:
        '''Converts the given value from gamma (sRGB) to linear color space.'''
        return value / 2.2

    @staticmethod
    def linear_to_gamma_space(value: float) -> float:
        '''Converts the given value from linear to gamma (sRGB) color space.'''
        return value * 2.2


    @staticmethod
    def sin(value: int | float) -> int | float:
        '''Returns the sine of the given value.'''
        return math.sin(value)

    @staticmethod
    def cos(value: int | float) -> int | float:
        '''Returns the cosine of the given value.'''
        return math.cos(value)

    @staticmethod
    def tan(value: int | float) -> int | float:
        '''Returns the tangent of the given value.'''
        return math.tan(value)


    @staticmethod
    def asin(value: int | float) -> int | float:
        '''Returns the arc sine of the given value.'''
        return math.asin(value)

    @staticmethod
    def acos(value: int | float) -> int | float:
        '''Returns the arc cosine of the given value.'''
        return math.acos(value)

    @staticmethod
    def atan(value: int | float) -> int | float:
        '''Returns the arc tangent of the given value.'''
        return math.atan(value)

    @staticmethod
    def atan2(y: int | float, x: int | float) -> int | float:
        '''Returns the arc tangent of the given value.'''
        return math.atan2(y, x)


    @staticmethod
    def sqrt(value: int | float) -> int | float:
        '''Returns the square root of the given value.'''
        return math.sqrt(value)


    @staticmethod
    def abs(value: int | float) -> int | float:
        '''Returns the absolute value of the given value.'''
        return math.fabs(value)


    @staticmethod
    def min(*values: int | float) -> int | float:
        '''Returns the minimum value of the given values.'''
        return min(values)

    @staticmethod
    def max(*values: int | float) -> int | float:
        '''Returns the maximum value of the given values.'''
        return max(values)


    @staticmethod
    def pow(value: int | float, power: int | float) -> int | float:
        '''Returns the value of the given value to the given power.'''
        return math.pow(value, power)

    @staticmethod
    def exp(value: int | float) -> int | float:
        '''Returns e raised to the specified power.'''
        return math.exp(value)


    @staticmethod
    @overload
    def log(value: int | float) -> int | float:
        '''Returns the natural (base e) logarithm of a specified number.'''
        ...

    @staticmethod
    @overload
    def log(value: int | float, p: int | float) -> int | float:
        '''Returns the logarithm of a specified number to the given base.'''
        ...

    @staticmethod
    def log(**args) -> int | float:
        '''Returns the logarithm of a specified number to the given base.'''
        return math.log(**args)


    @staticmethod
    def log10(value: int | float) -> int | float:
        '''Returns the base 10 logarithm of a specified number.'''
        return math.log10(value)


    @staticmethod
    def floor(value: int | float) -> int | float:
        '''Returns the largest integer less than or equal to the given value.'''
        return math.floor(value)

    @staticmethod
    def ceil(value: int | float) -> int | float:
        '''Returns the smallest integer greater than or equal to the given value.'''
        return math.ceil(value)


    @staticmethod
    def round(value: int | float) -> int | float:
        '''Returns the value rounded to the nearest integer.'''
        return round(value)


    @staticmethod
    def floor_to_int(value: int | float) -> int:
        '''Returns the largest integer less than or equal to the given value.'''
        return int(Math.floor(value))

    @staticmethod
    def ceil_to_int(value: int | float) -> int:
        '''Returns the smallest integer greater than or equal to the given value.'''
        return int(Math.ceil(value))


    @staticmethod
    @overload
    def sign(value: int) -> int:
        '''Returns the sign of value.'''
        ...

    @staticmethod
    @overload
    def sign(value: float) -> float:
        '''Returns the sign of value.'''
        ...

    @staticmethod
    def sign(*args) -> int | float:
        '''Returns the sign of value.'''
        if len(args) == 1 and isinstance(args[0], int):
            return 1 if (args[0] >= 0) else -1
        
        elif len(args) == 1 and isinstance(args[0], float):
            return 1.0 if (args[0] >= 0) else -1.0
        
        else:
            raise TypeError('Invalid type for value.')


    @staticmethod
    @overload
    def clamp(value: int, min: int, max: int) -> int:
        '''Clamps the given value between the given minimum and maximum values. Returns the given value if it is within the minimum and maximum range.'''
        ...

    @staticmethod
    @overload
    def clamp(value: float, min: float, max: float) -> float:
        '''Clamps the given value between the given minimum and maximum values. Returns the given value if it is within the minimum and maximum range.'''
        ...

    @staticmethod
    def clamp(*args) -> int | float:
        '''Clamps the given value between the given minimum and maximum values. Returns the given value if it is within the minimum and maximum range.'''
        if len(args) == 3 and all(isinstance(arg, int) for arg in args):
            return args[2] if (args[0] > args[2]) else args[1] if (args[0] < args[1]) else args[0]
        
        elif len(args) == 3 and all(isinstance(arg, float) for arg in args):
            return args[2] if (args[0] > args[2]) else args[1] if (args[0] < args[1]) else args[0]
        
        else:
            raise TypeError('Invalid type for value.')


    @staticmethod
    def clamp01(value: float) -> float:
        '''Clamps the given value between 0 and 1.'''
        return Math.clamp(value, 0.0, 1.0)


    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        '''Linearly interpolates between a and b by t.'''
        return a + (b - a) * Math.clamp01(t)

    @staticmethod
    def lerp_unclamped(a: float, b: float, t: float) -> float:
        '''Linearly interpolates between a and b by t with no limit to t.'''
        return a + (b - a) * t

    @staticmethod
    def lerp_angle(a: float, b: float, t: float) -> float:
        '''Same as Lerp but makes sure the values interpolate correctly when they wrap around 360 degrees.'''
        num = Math.repeat(b - a, 360.0)
        if (num > 180.0): num -= 360.0

        return a + num * Math.clamp01(t)


    @staticmethod
    def move_towards(current: float, target: float, max_delta: float) -> float:
        '''Moves a value current towards target.'''
        if (abs(target - current) <= max_delta): return target
        return current + Math.sign(target - current) * max_delta

    @staticmethod
    def move_towards_angle(current: float, target: float, max_delta: float) -> float:
        '''Same as MoveTowards but makes sure the values interpolate correctly when they wrap around 360 degrees.'''
        num = Math.delta_angle(current, target)
        if (-max_delta < num and num < max_delta): return target

        target = current + num
        return Math.move_towards(current, target, max_delta)


    @staticmethod
    def smooth_step(from_: float, to_: float, t: float) -> float:
        '''Interpolates between from_ and to_ with smoothing at the limits.'''
        t = Math.clamp01(t)
        t = -2.0 * t * t * t + 3.0 * t * t
        return to_ * t + from_ * (1.0 - t)


    @staticmethod
    def gamma(value: float, absmax: float, gamma: float) -> float:
        '''Applies a gamma curve to a value. The default value is 2.0.'''
        flag = value < 0
        num = abs(value)
        if (num > absmax): return (-num) if flag else num

        num2 = pow(num / absmax, gamma) * absmax
        return (-num2) if flag else num2


    @staticmethod
    def approximately(a: float, b: float) -> bool:
        '''Compares two floating point values and returns true if they are similar.'''
        return abs(b - a) < max(1E-06 * max(abs(a), abs(b)), Math.Epsilon * 8.0)


    @staticmethod
    def smooth_damp(current: float, target: float, current_velocity: float, smooth_time: float, delta_time: float, max_speed: float = PositiveInfinity) -> float:
        smooth_time = max(0.0001, smooth_time)
        num = 2.0 / smooth_time
        num2 = num * delta_time
        num3 = 1.0 / (1.0 + num2 + 0.48 * num2 * num2 + 0.235 * num2 * num2 * num2)
        value = current - target
        num4 = target
        num5 = max_speed * smooth_time
        value = Math.clamp(value, 0.0 - num5, num5)
        target = current - value
        num6 = (current_velocity + num * value) * delta_time
        current_velocity = (current_velocity - num * num6) * num3
        num7 = target + (value + num6) * num3
        if (num4 - current > 0.0 == num7 > num4):
            num7 = num4
            current_velocity = (num7 - num4) / delta_time

        return num7


    @staticmethod
    def smooth_damp_angle(current: float, target: float, current_velocity: float, smooth_time: float, delta_time: float, max_speed: float = PositiveInfinity) -> float:
        target = current + Math.delta_angle(current, target)
        return Math.smooth_damp(current, target, current_velocity, smooth_time, max_speed, delta_time)


    @staticmethod
    def repeat(t: float, length: float) -> float:
        '''Loops the value t, so that it is never larger than length and never smaller than 0.'''
        return Math.clamp(t - math.floor(t / length) * length, 0.0, length)


    @staticmethod
    def ping_pong(t: float, length: float) -> float:
        '''ping_pong returns a value that will increment and decrement between the value 0 and length.'''
        t = Math.repeat(t, length * 2.0)
        return length - abs(t - length)


    @staticmethod
    def inverse_lerp(a: float, b: float, value: float) -> float:
        '''Determines where a value lies between two points.'''
        if (a != b): return (value - a) / (b - a)
        return 0.0


    @staticmethod
    def delta_angle(current: float, target: float) -> float:
        '''Calculates the shortest difference between two given angles given in degrees.'''
        num = Math.repeat(target - current, 360.0)
        if (num > 180.0): num -= 360.0
        return num
#----------------------------------------------------------------------
