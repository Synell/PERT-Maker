#----------------------------------------------------------------------

    # Libraries
from .deg2Rad import deg2Rad
from math import cos, sin

from data.lib.dimensionalEnv.vectors.vector2 import Vector2
#----------------------------------------------------------------------

    # Function
def deg2Vector2(deg: float = 0, direction: str = 'right'):
    '''
    deg2Vector2(float degrees, string direction)
        Returns:
            Vector2 vect2
    '''
    if direction == 'right': return Vector2(cos(deg2Rad(deg)), sin(deg2Rad(deg)))
    elif direction == 'left': return Vector2(-cos(deg2Rad(deg)), -sin(deg2Rad(deg)))
    elif direction == 'up': return Vector2(sin(deg2Rad(deg)), cos(deg2Rad(deg)))
    elif direction == 'down': return Vector2(-sin(deg2Rad(deg)), -cos(deg2Rad(deg)))
    raise ValueError
#----------------------------------------------------------------------
