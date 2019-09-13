
from typing import Tuple
import math


__all__ = [
    'Angle',
    'Distance',
    'Speed',
    'Vector3',
    'hex_dump',
    'hex_load',
    'frange',
]


class Angle:
    """
    Angle representation.

    Args:
        radians (float): The number of radians the angle should represent
            (cannot be combined with ``degrees``)
        degrees (float): The number of degress the angle should represent
            (cannot be combined with ``radians``)
    """

    __slots__ = ('_radians', )

    def __init__(self, radians=None, degrees=None):
        if radians is None and degrees is None:
            raise ValueError("Expected either the degrees or radians keyword argument")
        if radians and degrees:
            raise ValueError("Expected either the degrees or radians keyword argument, not both")

        if degrees is not None:
            radians = degrees * math.pi / 180
        self._radians = float(radians)

    def __repr__(self):
        return "<%s %.2f radians (%.2f degrees)>" % (self.__class__.__name__, self.radians, self.degrees)

    def __add__(self, other):
        if not isinstance(other, Angle):
            raise TypeError("Unsupported type for + expected Angle")
        return Angle(radians=self.radians + other.radians)

    def __sub__(self, other):
        if not isinstance(other, Angle):
            raise TypeError("Unsupported type for - expected Angle")
        return Angle(radians=self.radians - other.radians)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported type for * expected number")
        return Angle(radians=self.radians * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported type for / expected number")
        return Angle(radians=self.radians / other)

    def _cmp_int(self, other):
        if not isinstance(other, Angle):
            raise TypeError("Unsupported type for comparison expected Angle")
        return self.radians - other.radians

    def __eq__(self, other):
        return self._cmp_int(other) == 0

    def __ne__(self, other):
        return self._cmp_int(other) != 0

    def __gt__(self, other):
        return self._cmp_int(other) > 0

    def __lt__(self, other):
        return self._cmp_int(other) < 0

    def __ge__(self, other):
        return self._cmp_int(other) >= 0

    def __le__(self, other):
        return self._cmp_int(other) <= 0

    @property
    def radians(self) -> float:
        """ Returns the angle in radians. """
        return self._radians

    @property
    def degrees(self) -> float:
        """ Returns the angle in degrees. """
        return self._radians / math.pi * 180

    @property
    def abs_value(self):
        """:class:`cozmo.util.Angle`: The absolute value of the angle.

        If the Angle is positive then it returns a copy of this Angle, otherwise it returns -Angle.
        """
        return Angle(radians=abs(self._radians))


class Distance:
    """
    Represents a distance.

    The class allows distances to be returned in either millimeters or inches.

    Args:
        mm (float): The number of millimeters the distance should
            represent (cannot be combined with ``distance_inches``).
        inches (float): The number of inches the distance should
            represent (cannot be combined with ``distance_mm``).
    """

    __slots__ = ('_mm', )

    def __init__(self, mm=None, inches=None):
        if mm is None and inches is None:
            raise ValueError("Expected either the mm or inches keyword argument")
        if mm and inches:
            raise ValueError("Expected either the mm or inches keyword argument, not both")

        if inches is not None:
            mm = inches * 25.4
        self._mm = mm

    def __repr__(self):
        return "<%s %.2f mm (%.2f inches)>" % (self.__class__.__name__, self.mm, self.inches)

    def __add__(self, other):
        if not isinstance(other, Distance):
            raise TypeError("Unsupported operand for + expected Distance")
        return Distance(mm=self.mm + other.mm)

    def __sub__(self, other):
        if not isinstance(other, Distance):
            raise TypeError("Unsupported operand for - expected Distance")
        return Distance(mm=self.mm - other.mm)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for * expected number")
        return Distance(mm=self.mm * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for / expected number")
        return Distance(mm=self.mm / other)

    @property
    def mm(self) -> float:
        """ The distance in millimeters. """
        return self._mm

    @property
    def inches(self) -> float:
        """ The distance in inches. """
        return self._mm / 25.4


class Speed:
    """
    Speed representation.

    Args:
        mmps (float): The number of millimeters per second the speed should represent.
    """

    __slots__ = ('_mmps', )

    def __init__(self, mmps: float):
        self._mmps = mmps

    def __repr__(self):
        return "<%s %.2f mmps>" % (self.__class__.__name__, self.mmps)

    def __add__(self, other):
        if not isinstance(other, Speed):
            raise TypeError("Unsupported operand for + expected Speed")
        return Speed(mmps=self.mmps + other.mmps)

    def __sub__(self, other):
        if not isinstance(other, Speed):
            raise TypeError("Unsupported operand for - expected Speed")
        return Speed(mmps=self.mmps - other.mmps)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for * expected number")
        return Speed(mmps=self.mmps * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for / expected number")
        return Speed(mmps=self.mmps / other)

    @property
    def mmps(self) -> float:
        """ Returns the speed in millimeters per second (mmps). """
        return self._mmps


class Vector3:
    """
    Represents a 3D Vector (type/units aren't specified).

    Args:
        x (float): X component
        y (float): Y component
        z (float): Z component
    """

    __slots__ = ('_x', '_y', '_z')

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    def set_to(self, rhs):
        """
        Copy the x, y and z components of the given vector.

        Args:
            rhs (:class:`Vector3`): The right-hand-side of this assignment - the
                source vector to copy into this vector.
        """
        self._x = rhs.x
        self._y = rhs.y
        self._z = rhs.z

    @property
    def x(self) -> float:
        """ The x component. """
        return self._x

    @property
    def y(self) -> float:
        """ The y component. """
        return self._y

    @property
    def z(self) -> float:
        """ The z component. """
        return self._z

    @property
    def x_y_z(self) -> Tuple[float, float, float]:
        """ The X, Y, Z elements of the Vector3 (x,y,z). """
        return self._x, self._y, self._z

    def __repr__(self):
        return "<%s x: %.2f y: %.2f z: %.2f>" % (self.__class__.__name__, self.x, self.y, self.z)

    def __add__(self, other):
        if not isinstance(other, Vector3):
            raise TypeError("Unsupported operand for + expected Vector3")
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Vector3):
            raise TypeError("Unsupported operand for - expected Vector3")
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for * expected number")
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for / expected number")
        return Vector3(self.x / other, self.y / other, self.z / other)


def hex_dump(data: bytes) -> str:
    res = ":".join("{:02x}".format(b) for b in data)
    return res


def hex_load(data: str) -> bytes:
    res = bytearray.fromhex(data.replace(":", ""))
    return res


def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step
