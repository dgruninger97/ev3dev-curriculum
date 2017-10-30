"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    def drive_inches(self, inches_target, speed_deg_per_second):
        time_s = 1  # Any value other than 0.
        while time_s != 0:
            self.left_motor.run_to_rel_pos(position_sp=(inches_target / .011), speed_sp=speed_deg_per_second)
            self.right_motor.run_to_rel_pos(position_sp=(inches_target / .011), speed_sp=speed_deg_per_second)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
            time_s = 0
        ev3.Sound.beep().wait()
     def turn_degrees(self, degrees_to_turn, turn_speed):
         state = 1  # Any value other than 0.
         while state != 0:
             ang = degrees_to_turn * 0.0174533
             sp_ang = turn_speed
             sp_in = sp_ang * 1.3 * 0.0174533 * .5
             dis = ang * 3
             time_s = int((sp_in * (dis ** -1)) ** -1)
             dis_ang = sp_ang * time_s
             self.left_motor.run_to_rel_pos(position_sp=-1 * dis_ang, speed_sp=sp_ang)
             self.right_motor.run_to_rel_pos(position_sp=dis_ang, speed_sp=sp_ang)
             self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
             state = 0
         ev3.Sound.beep().wait()
    #     time_s = 1  # Any value other than 0.
    #     while time_s != 0:
    #         # angle_time = degrees_to_turn / turn_speed
    #         self.left_motor.run_to_rel_pos(position_sp=degrees_to_turn, speed_sp=(turn_speed * -1), stop_action=ev3.Motor.STOP_ACTION_BRAKE)
    #         self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn, speed_sp=(turn_speed), stop_action=ev3.Motor.STOP_ACTION_BRAKE)
    #         # self.left_motor.speed_sp = turn_speed
    #         # self.right_motor.speed_sp = -turn_speed
    #         self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
    #         self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
    #         time_s = 0
    #     ev3.Sound.beep().wait()





    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
