import wpilib
import wpilib.drive
import navx

ENCODER_ROTATION = 1023
WHEEL_DIAMETER = 7.639

SARAH_MULTIPLIER = 0.5


class Drive:
    drivetrain = wpilib.drive.DifferentialDrive

    navx: navx.AHRS

    align_kp = (0.99)
    """
    align_ki = (0.20)
    align_kd = (0.00)
    """
    align_tolerance = (1)
    align_max_rot = (.3)
    previous_error = 0

    def __init__(self):
        self.enabled = False

    def on_enable(self):
        self.y = 0
        self.rotation = 0

    # Verb functions -- these functions do NOT talk to motors directly. This
    # allows multiple callers in the loop to call our functions without
    # conflicts.

    def move(self, y, rotation, sarah=False):
        """
        Causes the robot to move
        :param y: The speed that the robot should drive in the Y direction.
        :param rotation: The rate of rotation for the robot that is completely independent of the translation.
        :param sarah: Is Sarah driving?
        """
        if sarah:
            y *= SARAH_MULTIPLIER
            rotation *= SARAH_MULTIPLIER
        self.y = y
        self.rotation = rotation

    @property
    def angle(self):
        """
        Get current angle of robot.
        """
        return self.navx.getYaw()

    def align(self, target_angle) -> bool:
        """
        Adjusts the robot so that it points at a particular angle.

        :param target_angle: Angle to point at, in degrees
        :returns: Whether robot has reached requested angle
        """
        angle_error = target_angle - self.angle
        print(f"angle_error: {angle_error}, target_angle: {target_angle}, current angle: {self.angle}")
        # Ensure that robot turns the quickest direction to get to the desired angle
        if angle_error > 180:
            angle_error -= 360
        if abs(angle_error) > self.align_tolerance:
            self.i_err += angle_error
            self.rot = self.align_kp * angle_error + self.align_ki * self.i_err + self.align_kd * (self.previous_error - angle_error) / 0.020
            self.rot = max(min(self.align_max_rot, self.rot), -self.align_max_rot)

            self.previous_error = angle_error
            return False
        self.i_err = 0
        return True

    def execute(self):
        """Actually drive."""
        self.drivetrain.arcadeDrive(self.y, self.rotation)

        # Prevent robot from driving by default
        self.y = 0
        self.rotation = 0
