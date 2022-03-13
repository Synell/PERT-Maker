#----------------------------------------------------------------------

    # Libraries
from math import cos, sin

from data.lib.dimensionalEnv.vectors.vector2 import Vector2
#----------------------------------------------------------------------

    # Function

def rad2Vector2(rad):
    """
    rad2Vector2(float radians)
        Returns:
            Vector2 vect2
    """
    return Vector2(cos(rad), sin(rad))
#----------------------------------------------------------------------
