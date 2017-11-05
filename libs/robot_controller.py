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
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.running = None
        assert self.right_motor
        assert self.left_motor
        assert self.touch_sensor
        assert self.arm_motor
        assert self.color_sensor
        assert self.ir_sensor

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Drives in a straight line for a given distance"""
        time_s = 1  # Any value other than 0.
        while time_s != 0:
            self.left_motor.run_to_rel_pos(position_sp=(inches_target / .011), speed_sp=speed_deg_per_second)
            self.right_motor.run_to_rel_pos(position_sp=(inches_target / .011), speed_sp=speed_deg_per_second)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
            time_s = 0
        ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed):
        """Turns the robot by a set angle"""
        state = 1  # Any value other than 0.
        while state != 0:
            ang = degrees_to_turn * 0.0174533
            dis = ang * 3
            self.left_motor.run_to_rel_pos(position_sp=(dis/.011) * -1, speed_sp=turn_speed)
            self.right_motor.run_to_rel_pos(position_sp=(dis/.011), speed_sp=turn_speed)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            state = 0
        ev3.Sound.beep().wait()

    def polygon(self, speed_deg_per_second, sides, edge_length):
        """Drives the robot in a polygon given the number of sides and the side length"""
        degrees_to_turn = (180 - ((sides - 2) * 180) / sides)
        time_s = 1
        while time_s != 0:
            for k in range(sides):
                self.drive_inches(edge_length, speed_deg_per_second)
                self.turn_degrees(degrees_to_turn, speed_deg_per_second)
            time_s = 0

    # TO DO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)

    def arm_calibration(self):
        """Calibrates arm"""
        self.arm_motor.run_forever(speed_sp=900)
        while self.touch_sensor.is_pressed == 0:
            print('running motor')
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2
        deg_for_full_range = arm_revolutions_for_full_range * 360
        self.arm_motor.run_to_rel_pos(position_sp=deg_for_full_range * -1)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        print('ready to calibrate')

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

        ev3.Sound.beep().wait()

    def arm_up(self):
        """Moves arm up"""
        max_speed = 900
        self.arm_motor.run_forever(speed_sp=max_speed)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Move arm down"""
        max_speed = 900
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=max_speed)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound().beep().wait()

    def shutdown(self):
        """Shuts down the running program on call"""
        self.running = False

    def move_tread(self, mov_speed, rc1):
        """Moves treads forward on button_state of ir remote"""
        while rc1.red_up & rc1.blue_up:
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            self.left_motor.run_forever(speed_sp=mov_speed)
            self.right_motor.run_forever(speed_sp=mov_speed)
            while rc1.red_up & rc1.blue_up:
                time.sleep(.01)
            self.right_motor.stop()
            self.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

        while rc1.blue_up:
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            self.right_motor.run_forever(speed_sp=mov_speed)
            while rc1.blue_up:
                print(rc1.blue_up)
                time.sleep(.01)
            self.right_motor.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

        while rc1.red_up:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            self.left_motor.run_forever(speed_sp=mov_speed)
            while rc1.red_up:
                print(rc1.blue_up)
                time.sleep(.01)
            self.left_motor.stop()
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def move_tread_back(self, mov_speed, rc1):
        """Moves treads forward on button_state of ir remote"""
        while rc1.red_down & rc1.blue_down:
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
            self.left_motor.run_forever(speed_sp=-mov_speed)
            self.right_motor.run_forever(speed_sp=-mov_speed)
            while rc1.red_down & rc1.blue_down:
                time.sleep(.01)
            self.right_motor.stop()
            self.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

        while rc1.blue_down:
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            self.right_motor.run_forever(speed_sp=-mov_speed)
            while rc1.blue_down:
                print(rc1.blue_down)
                time.sleep(.01)
            self.right_motor.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

        while rc1.red_down:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
            self.left_motor.run_forever(speed_sp=-mov_speed)
            while rc1.red_down:
                print(rc1.blue_down)
                time.sleep(.01)
            self.left_motor.stop()
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def forward(self, left_speed_entry, right_speed_entry):
        #if forward_button.is_pressed:
        self.left_motor.run_forever(speed_sp = left_speed_entry)
        self.right_motor.run_forever(speed_sp = right_speed_entry)

    def backward(self, left_speed_entry, right_speed_entry):
        # if backward_button.is_pressed:
        left_speed_entry = left_speed_entry * -1
        right_speed_entry = right_speed_entry * -1
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def left_move(self, left_speed_entry, right_speed_entry):
        if left_speed_entry==right_speed_entry:
            left_speed_entry = left_speed_entry * -1
            self.left_motor.run_forever(speed_sp=left_speed_entry)
            self.right_motor.run_forever(speed_sp=right_speed_entry)
        else:
            self.left_motor.run_forever(speed_sp = left_speed_entry)
            self.right_motor.run_forever(speed_sp = right_speed_entry)

    def right_move(self, left_speed_entry, right_speed_entry):
        if left_speed_entry == right_speed_entry:
            right_speed_entry = right_speed_entry * -1
            self.left_motor.run_forever(speed_sp = left_speed_entry)
            self.right_motor.run_forever(speed_sp = right_speed_entry)
        else:
            self.left_motor.run_forever(speed_sp = left_speed_entry)
            self.right_motor.run_forever(speed_sp = right_speed_entry)
    def seek_beacon(self, robot):
        forward_speed = 300
        turn_speed = 100
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        while not robot.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                robot.right_move(turn_speed, turn_speed)
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance == 0:
                        print('You found it')
                        robot.stop()
                        return True
                    if current_distance > 0:
                        robot.forward(forward_speed, forward_speed)
                        if current_distance <= 1:
                            robot.drive_inches(2, forward_speed)
                            robot.stop()
                            ev3.Sound.speak('beacon found')
                            time.sleep(3)
                            return True
                if math.fabs(current_heading) > 2 and math.fabs(current_heading) < 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading > 0:
                        robot.left_move(turn_speed, turn_speed)
                        if math.fabs(current_heading) < 2:
                            robot.stop()
                    if current_heading < 0:
                        robot.right_move(turn_speed, turn_speed)
                        if math.fabs(current_heading) < 2:
                            robot.stop()
                if math.fabs(current_heading) > 10:
                    robot.right_move(turn_speed, turn_speed)
            time.sleep(0.2)

            # The touch_sensor was pressed to abort the attempt if this code runs.
            print("Abandon ship!")
            robot.stop()
            return False