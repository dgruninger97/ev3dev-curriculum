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
    """Drives in a straight line for a given distance"""

    def turn_degrees(self, degrees_to_turn, turn_speed):
        state = 1  # Any value other than 0.
        while state != 0:
            ang = degrees_to_turn * 0.0174533
            dis = ang * 3
            self.left_motor.run_to_rel_pos(position_sp=(dis/.011) * -1, speed_sp=turn_speed)
            self.right_motor.run_to_rel_pos(position_sp=(dis/.011), speed_sp=turn_speed)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            state = 0
        ev3.Sound.beep().wait()
    """Turns the robot by a set angle"""

    def polygon(self, speed_deg_per_second, sides, edge_length):
        degrees_to_turn = (180 - ((sides - 2) * 180) / sides)
        time_s = 1
        while time_s != 0:
            for k in range(sides):
                self.drive_inches(edge_length, speed_deg_per_second)
                self.turn_degrees(degrees_to_turn, speed_deg_per_second)
            time_s = 0
    """Drives the robot in a polygon given the number of sides and the side length"""



    # TO DO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)

    def arm_calibration(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        touch_sensor = ev3.TouchSensor()
        arm_motor.run_forever(speed_sp=900)
        while touch_sensor.is_pressed == 0:
            print('running motor')
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2
        deg_for_full_range = arm_revolutions_for_full_range * 360
        arm_motor.run_to_rel_pos(position_sp=deg_for_full_range * -1)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        print('ready to calibrate')

        arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

        ev3.Sound.beep().wait()

    def arm_up(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        touch_sensor = ev3.TouchSensor()
        max_speed = 900
        arm_motor.run_forever(speed_sp=max_speed)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        MAX_SPEED = 900
        arm_motor.run_to_abs_pos(position_sp=0, speed_sp = MAX_SPEED)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        arm_motor.stop(stop_action='brake')
        ev3.Sound().beep().wait()


    def shutdown(self, dc):
        dc.running = False

    def move_left_tread(self, mov_speed, rc1):

        self.left_motor.run_forever(speed_sp=mov_speed)
        while rc1.red_up:
            print(rc1.button_state)
            time.sleep(.01)
        self.left_motor.stop()

