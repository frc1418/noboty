from networktables.util import ntproperty
from components import drive

from magicbot import StateMachine, state, timed_state
# TODO: Use this to automate shooting process at the end and things like that
# from automations import
from magicbot import tunable


class Align(StateMachine):
    drive: drive.Drive
    # TODO: define automations too

    # yaw = ntproperty('/vision/target_yaw', 0)
    # TODO: better name
    terminal_angle = 0

    def seek(self):
        """
        Engage automation.
        """
        print('I am running!')
        self.engage()

    @state(first=True, must_finish=True)
    def align(self, initial_call):
        """
        Turn to face tower.
        """
        if initial_call:
            # self.terminal_angle = self.drive.angle + self.yaw
            self.terminal_angle = self.drive.angle + 45
        if self.drive.align(self.terminal_angle):
            self.next_state('advance')

    @timed_state(duration=3)
    def advance(self):
        """
        Drive forward to target.
        """
        self.drive.move(0.3, 0, 0)
