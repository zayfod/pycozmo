"""

Utility classes and functions.

"""

from typing import Optional, Tuple
import os
import pathlib
import math
import time

from . import exception


__all__ = [
    'Angle',
    'Distance',
    'Speed',
    'Vector2',
    'Vector3',
    'angle_z_to_quaternion',
    'Matrix44',
    'Quaternion',
    'Pose',
    'FPSTimer',

    'hex_dump',
    'hex_load',
    'frange',
    'get_pycozmo_dir',
    'get_cozmo_asset_dir',
    'check_assets',
    'get_cozmo_anim_dir',
]


class Angle:
    """
    Angle representation.

    Args:
        radians (float): The number of radians the angle should represent
            (cannot be combined with ``degrees``)
        degrees (float): The number of degrees the angle should represent
            (cannot be combined with ``radians``)
    """

    __slots__ = '_radians'

    def __init__(self, radians: Optional[float] = None, degrees: Optional[float] = None):
        if radians is None and degrees is None:
            raise ValueError("Expected either the degrees or radians keyword argument")
        if radians and degrees:
            raise ValueError("Expected either the degrees or radians keyword argument, not both")

        if degrees is not None:
            radians = degrees * math.pi / 180
        self._radians = float(radians)  # type: ignore

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

    __slots__ = '_mm'

    def __init__(self, mm: Optional[float] = None, inches: Optional[float] = None):
        if mm is None and inches is None:
            raise ValueError("Expected either the mm or inches keyword argument")
        if mm and inches:
            raise ValueError("Expected either the mm or inches keyword argument, not both")

        if inches is not None:
            mm = inches * 25.4
        self._mm = mm   # type: float   # type: ignore

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

    __slots__ = '_mmps'

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


class Vector2:
    """
    Represents a 2D Vector (type/units aren't specified)

    Args:
        x (float): X component
        y (float): Y component
    """

    __slots__ = ('_x', '_y')

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def set_to(self, rhs) -> None:
        """
        Copy the x and y components of the given vector.

        Args:
            rhs (:class:`Vector2`): The right-hand-side of this assignment - the
                source vector to copy into this vector.
        """
        self._x = rhs.x
        self._y = rhs.y

    @property
    def x(self) -> float:
        """ The x component. """
        return self._x

    @property
    def y(self) -> float:
        """ The y component. """
        return self._y

    @property
    def x_y(self) -> Tuple[float, float]:
        """ The X, Y elements of the Vector2 (x,y). """
        return self._x, self._y

    def __repr__(self):
        return "<%s x: %.2f y: %.2f>" % (self.__class__.__name__, self.x, self.y)

    def __add__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError("Unsupported operand for + expected Vector2")
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError("Unsupported operand for - expected Vector2")
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for * expected number")
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for / expected number")
        return Vector2(self.x / other, self.y / other)


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


def angle_z_to_quaternion(angle_z: Angle) -> Tuple[float, float, float, float]:
    """
    Converts an angle in the z axis (Euler angle z component) to a quaternion.
    """
    # Define the quaternion to be converted from a Euler angle (x,y,z) of 0,0,angle_z
    # These equations have their original equations above, and simplified implemented
    # q0 = cos(x/2)*cos(y/2)*cos(z/2) + sin(x/2)*sin(y/2)*sin(z/2)
    q0 = math.cos(angle_z.radians / 2)
    # q1 = sin(x/2)*cos(y/2)*cos(z/2) - cos(x/2)*sin(y/2)*sin(z/2)
    q1 = 0
    # q2 = cos(x/2)*sin(y/2)*cos(z/2) + sin(x/2)*cos(y/2)*sin(z/2)
    q2 = 0
    # q3 = cos(x/2)*cos(y/2)*sin(z/2) - sin(x/2)*sin(y/2)*cos(z/2)
    q3 = math.sin(angle_z.radians / 2)
    return q0, q1, q2, q3


class Matrix44:
    """
    A 4x4 Matrix for representing the rotation and/or position of an object in the world.

    Can be generated from a Quaternion for a pure rotation matrix, or
    combined with a position for a full translation matrix, as done by Pose.to_matrix().
    """
    __slots__ = ('m00', 'm10', 'm20', 'm30',
                 'm01', 'm11', 'm21', 'm31',
                 'm02', 'm12', 'm22', 'm32',
                 'm03', 'm13', 'm23', 'm33')

    def __init__(self,
                 m00, m10, m20, m30,
                 m01, m11, m21, m31,
                 m02, m12, m22, m32,
                 m03, m13, m23, m33):
        self.m00 = m00
        self.m10 = m10
        self.m20 = m20
        self.m30 = m30

        self.m01 = m01
        self.m11 = m11
        self.m21 = m21
        self.m31 = m31

        self.m02 = m02
        self.m12 = m12
        self.m22 = m22
        self.m32 = m32

        self.m03 = m03
        self.m13 = m13
        self.m23 = m23
        self.m33 = m33

    def __repr__(self):
        return ("<%s: "
                "%.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f "
                "%.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f>" % (self.__class__.__name__, *self.in_row_order))

    @property
    def tabulated_string(self):
        """str: A multi-line string formatted with tabs to show the matrix contents."""
        return ("%.1f\t%.1f\t%.1f\t%.1f\n"
                "%.1f\t%.1f\t%.1f\t%.1f\n"
                "%.1f\t%.1f\t%.1f\t%.1f\n"
                "%.1f\t%.1f\t%.1f\t%.1f" % self.in_row_order)

    @property
    def in_row_order(self) -> Tuple[float, float, float, float,
                                    float, float, float, float,
                                    float, float, float, float,
                                    float, float, float, float]:
        """
        Returns the contents of the matrix in row order.
        """
        return self.m00, self.m01, self.m02, self.m03, \
            self.m10, self.m11, self.m12, self.m13, \
            self.m20, self.m21, self.m22, self.m23, \
            self.m30, self.m31, self.m32, self.m33

    @property
    def in_column_order(self) -> Tuple[float, float, float, float,
                                       float, float, float, float,
                                       float, float, float, float,
                                       float, float, float, float]:
        """
        Returns the contents of the matrix in column order.
        """
        return self.m00, self.m10, self.m20, self.m30, \
            self.m01, self.m11, self.m21, self.m31, \
            self.m02, self.m12, self.m22, self.m32, \
            self.m03, self.m13, self.m23, self.m33

    @property
    def forward_xyz(self) -> Tuple[float, float, float]:
        """
        Returns the x,y,z components representing the matrix's forward vector.
        """
        return self.m00, self.m01, self.m02

    @property
    def left_xyz(self) -> Tuple[float, float, float]:
        """
        Returns the x,y,z components representing the matrix's left vector.
        """
        return self.m10, self.m11, self.m12

    @property
    def up_xyz(self) -> Tuple[float, float, float]:
        """
        Returns the x,y,z components representing the matrix's up vector.
        """
        return self.m20, self.m21, self.m22

    @property
    def pos_xyz(self) -> Tuple[float, float, float]:
        """
        Returns the x,y,z components representing the matrix's position vector.
        """
        return self.m30, self.m31, self.m32

    def set_forward(self, x: float, y: float, z: float) -> None:
        """
        Set the x,y,z components representing the matrix's forward vector.
        """
        self.m00 = x
        self.m01 = y
        self.m02 = z

    def set_left(self, x: float, y: float, z: float) -> None:
        """
        Set the x,y,z components representing the matrix's left vector.
        """
        self.m10 = x
        self.m11 = y
        self.m12 = z

    def set_up(self, x: float, y: float, z: float) -> None:
        """
        Set the x,y,z components representing the matrix's up vector.
        """
        self.m20 = x
        self.m21 = y
        self.m22 = z

    def set_pos(self, x: float, y: float, z: float) -> None:
        """
        Set the x,y,z components representing the matrix's position vector.
        """
        self.m30 = x
        self.m31 = y
        self.m32 = z


class Quaternion:
    """
    Represents rotation.
    """

    __slots__ = ('_q0', '_q1', '_q2', '_q3')

    def __init__(self,
                 q0: Optional[float] = None,
                 q1: Optional[float] = None,
                 q2: Optional[float] = None,
                 q3: Optional[float] = None,
                 angle_z: Optional[Angle] = None):

        is_quaternion = (q0 is not None) and (q1 is not None) and (q2 is not None) and (q3 is not None)

        if not is_quaternion and angle_z is None:
            raise ValueError("Expected either the q0 q1 q2 and q3 or angle_z keyword arguments")
        if is_quaternion and angle_z:
            raise ValueError("Expected either the q0 q1 q2 and q3 or angle_z keyword argument, not both")
        if angle_z is not None:
            if not isinstance(angle_z, Angle):
                raise TypeError("Unsupported type for angle_z expected Angle")
            q0, q1, q2, q3 = angle_z_to_quaternion(angle_z)

        self._q0 = q0   # type: float   # type: ignore
        self._q1 = q1   # type: float   # type: ignore
        self._q2 = q2   # type: float   # type: ignore
        self._q3 = q3   # type: float   # type: ignore

    def __repr__(self):
        return ("<%s q0: %.2f q1: %.2f q2: %.2f q3: %.2f (angle_z: %s)>" %
                (self.__class__.__name__, self.q0, self.q1, self.q2, self.q3, self.angle_z))

    def to_matrix(self, pos_x: float = 0.0, pos_y: float = 0.0, pos_z: float = 0.0) -> Matrix44:
        """
        Convert the Quaternion to a 4x4 matrix representing this rotation.

        A position can also be provided to generate a full translation matrix.
        """

        # See https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
        q0q0 = self.q0 * self.q0
        q1q1 = self.q1 * self.q1
        q2q2 = self.q2 * self.q2
        q3q3 = self.q3 * self.q3

        q0x2 = self.q0 * 2.0  # saves 2 multiplies
        q0q1x2 = q0x2 * self.q1
        q0q2x2 = q0x2 * self.q2
        q0q3x2 = q0x2 * self.q3
        q1x2 = self.q1 * 2.0  # saves 1 multiply
        q1q2x2 = q1x2 * self.q2
        q1q3x2 = q1x2 * self.q3
        q2q3x2 = 2.0 * self.q2 * self.q3

        m00 = (q0q0 + q1q1 - q2q2 - q3q3)
        m01 = (q1q2x2 + q0q3x2)
        m02 = (q1q3x2 - q0q2x2)

        m10 = (q1q2x2 - q0q3x2)
        m11 = (q0q0 - q1q1 + q2q2 - q3q3)
        m12 = (q0q1x2 + q2q3x2)

        m20 = (q0q2x2 + q1q3x2)
        m21 = (q2q3x2 - q0q1x2)
        m22 = (q0q0 - q1q1 - q2q2 + q3q3)

        return Matrix44(m00, m10, m20, pos_x,
                        m01, m11, m21, pos_y,
                        m02, m12, m22, pos_z,
                        0.0, 0.0, 0.0, 1.0)

    # These are only for angle_z because quaternion addition/subtraction is not relevant here
    def __add__(self, other):
        if not isinstance(other, Quaternion):
            raise TypeError("Unsupported operand for + expected Quaternion")
        angle_z = self.angle_z + other.angle_z
        return Quaternion(angle_z=angle_z)

    def __sub__(self, other):
        if not isinstance(other, Quaternion):
            raise TypeError("Unsupported operand for - expected Quaternion")
        angle_z = self.angle_z - other.angle_z
        return Quaternion(angle_z=angle_z)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for * expected number")
        angle_z = self.angle_z * other
        return Quaternion(angle_z=angle_z)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for / expected number")
        angle_z = self.angle_z / other
        return Quaternion(angle_z=angle_z)

    @property
    def q0(self) -> float:
        return self._q0

    @property
    def q1(self) -> float:
        return self._q1

    @property
    def q2(self) -> float:
        return self._q2

    @property
    def q3(self) -> float:
        return self._q3

    @property
    def q0_q1_q2_q3(self) -> Tuple[float, float, float, float]:
        return self._q0, self._q1, self._q2, self._q3

    @property
    def angle_z(self) -> Angle:
        radians = math.atan2(2 * (self.q1 * self.q2 + self.q0 * self.q3),
                             1 - 2 * (self.q2 ** 2 + self.q3 ** 2))
        return Angle(radians=radians)

    @property
    def euler_angles(self) -> Tuple[float, float, float]:
        """
        Returns the pitch, yaw, roll Euler components of the object's
        rotation defined as rotations in the x, y, and z axis respectively.

        :return:
        """

        # convert to matrix
        matrix = self.to_matrix()

        # normalize the magnitudes of cos(roll)*sin(pitch) (i.e. m12) and
        #   cos(roll)*cos(pitch) (ie. m22), to isolate cos(roll) to be compared
        #   against -sin(roll) (m02).  Unfortunately, this omits results with an
        #   absolute angle larger than 90 degrees on roll.
        absolute_cos_roll = math.sqrt(matrix.m12 * matrix.m12 + matrix.m22 * matrix.m22)
        near_gimbal_lock = absolute_cos_roll < 1e-6
        if not near_gimbal_lock:
            # general case euler decomposition
            pitch = math.atan2(matrix.m22, matrix.m12)
            yaw = math.atan2(matrix.m00, matrix.m01)
            roll = math.atan2(absolute_cos_roll, -matrix.m02)
        else:
            # special case euler angle decomposition near gimbal lock
            pitch = math.atan2(matrix.m11, -matrix.m21)
            yaw = 0
            roll = math.atan2(absolute_cos_roll, -matrix.m02)

        # adjust roll to be consistent with how the device is oriented
        roll = math.pi * 0.5 - roll
        if roll > math.pi:
            roll -= math.pi * 2

        return pitch, yaw, roll


class Pose:
    """
    A combination of position (vector) and rotation (quaternion).
    """

    __slots__ = ('_position', '_rotation', '_origin_id', '_is_accurate')

    def __init__(self,
                 x: float, y: float, z: float,
                 q0: Optional[float] = None, q1: Optional[float] = None,
                 q2: Optional[float] = None, q3: Optional[float] = None,
                 angle_z: Optional[Angle] = None, origin_id: int = -1, is_accurate: bool = True):
        self._position = Vector3(x, y, z)
        self._rotation = Quaternion(q0, q1, q2, q3, angle_z)
        self._origin_id = origin_id
        self._is_accurate = is_accurate

    @classmethod
    def _create_from_clad(cls, pose):
        return cls(pose.x, pose.y, pose.z,
                   q0=pose.q0, q1=pose.q1, q2=pose.q2, q3=pose.q3,
                   origin_id=pose.originID)

    @classmethod
    def _create_default(cls):
        return cls(0.0, 0.0, 0.0,
                   q0=1.0, q1=0.0, q2=0.0, q3=0.0,
                   origin_id=-1)

    def __repr__(self):
        return "<%s %s %s origin_id=%d>" % (self.__class__.__name__, self.position, self.rotation, self.origin_id)

    def __add__(self, other):
        if not isinstance(other, Pose):
            raise TypeError("Unsupported operand for + expected Pose")
        pos = self.position + other.position
        rot = self.rotation + other.rotation
        return Pose(pos.x, pos.y, pos.z, rot.q0, rot.q1, rot.q2, rot.q3)

    def __sub__(self, other):
        if not isinstance(other, Pose):
            raise TypeError("Unsupported operand for - expected Pose")
        pos = self.position - other.position
        rot = self.rotation - other.rotation
        return Pose(pos.x, pos.y, pos.z, rot.q0, rot.q1, rot.q2, rot.q3)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for * expected number")
        pos = self.position * other
        rot = self.rotation * other
        return Pose(pos.x, pos.y, pos.z, rot.q0, rot.q1, rot.q2, rot.q3)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Unsupported operand for / expected number")
        pos = self.position / other
        rot = self.rotation / other
        return Pose(pos.x, pos.y, pos.z, rot.q0, rot.q1, rot.q2, rot.q3)

    def define_pose_relative_this(self, new_pose):
        """
        Creates a new pose such that new_pose's origin is now at the location of this pose.
        """

        if not isinstance(new_pose, Pose):
            raise TypeError("Unsupported type for new_origin, must be of type Pose")
        x, y, z = self.position.x_y_z
        angle_z = self.rotation.angle_z
        new_x, new_y, new_z = new_pose.position.x_y_z
        new_angle_z = new_pose.rotation.angle_z

        cos_angle = math.cos(angle_z.radians)
        sin_angle = math.sin(angle_z.radians)
        res_x = x + (cos_angle * new_x) - (sin_angle * new_y)
        res_y = y + (sin_angle * new_x) + (cos_angle * new_y)
        res_z = z + new_z
        res_angle = angle_z + new_angle_z
        return Pose(res_x, res_y, res_z, angle_z=res_angle, origin_id=self._origin_id)

    def invalidate(self) -> None:
        """
        Mark this pose as being invalid (unusable).
        """
        self._origin_id = -1

    def is_comparable(self, other_pose: "Pose") -> bool:
        """
        Are these two poses comparable.

        Poses are comparable if they're valid and having matching origin IDs.
        """
        return (self.is_valid and other_pose.is_valid and
                (self.origin_id == other_pose.origin_id))

    @property
    def is_valid(self) -> bool:
        """
        Checks whether a pose is valid (usable).
        """
        return self.origin_id >= 0

    @property
    def position(self) -> Vector3:
        """
        Returns the position component of this pose.
        """
        return self._position

    @property
    def rotation(self) -> Quaternion:
        """
        Returns the rotation component of this pose.
        """
        return self._rotation

    def to_matrix(self):
        """
        Convert the Pose to a Matrix44.
        """
        return self.rotation.to_matrix(*self.position.x_y_z)

    @property
    def origin_id(self) -> int:
        """
        Returns an ID maintained by the robot (engine) which represents which coordinate frame this pose is in.
        """
        return self._origin_id

    @origin_id.setter
    def origin_id(self, value: int) -> None:
        """
        Change the ID of a pose.
        """
        if not isinstance(value, int):
            raise TypeError("The type of origin_id must be int")
        self._origin_id = value

    @property
    def is_accurate(self) -> bool:
        """
        Returns True if this pose is valid and accurate.

        Poses are marked as inaccurate if we detect movement via accelerometer,
        or if they were observed from far enough away that we're less certain
        of the exact pose.
        """
        return self.is_valid and self._is_accurate


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


def get_pycozmo_dir() -> pathlib.Path:
    """ Get PyCozmo directory. """
    pycozmo_dir = ".pycozmo" if os.name != "nt" else "pycozmo"
    default_dir = pathlib.Path.home() / pycozmo_dir
    path = pathlib.Path(os.environ.get('PYCOZMO_DIR', str(default_dir)))
    return path


def get_cozmo_asset_dir() -> pathlib.Path:
    """ Get Cozmo asset directory. """
    path = get_pycozmo_dir() / "assets"
    return path


def check_assets() -> None:
    """ Check whether Cozmo assets are available. """
    asset_dir = get_cozmo_asset_dir()
    if not os.path.exists(asset_dir / "resources.txt"):
        raise exception.ResourcesNotFound(
            f"Resources not found in {asset_dir} . Try running 'pycozmo_resources.py download'.")


def get_cozmo_anim_dir() -> pathlib.Path:
    """ Get Cozmo animation asset directory. """
    path = get_cozmo_asset_dir() / "cozmo_resources" / "assets" / "animations"
    return path


class FPSTimer:
    """ A timer that maintains frame rate by sleeping for a variable amount of time. """

    def __init__(self, fps: int) -> None:
        if fps <= 0:
            raise ValueError("Frame rate must be a positive integer.")
        # Timer period in seconds.
        self._period = 1.0 / int(fps)
        # Start time of the last successfully maintained frame sequence.
        self._start = None
        # Number of successfully maintained frames.
        self._frames = 1

    def sleep(self):
        """ Sleep to maintain the framerate. Should be called at the end of a frame. """
        now = time.perf_counter()
        if not self._start:
            # First call.
            self._start = now
        delay = self._start + (self._frames * self._period) - now
        if delay < 0:
            # Too long since the last call. Don't sleep at all and reset the frame sequence.
            self._start = now
            self._frames = 1
        else:
            time.sleep(delay)
            self._frames += 1
