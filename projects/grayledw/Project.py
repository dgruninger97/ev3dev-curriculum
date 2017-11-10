import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com


COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

blue_color_number = 2
green_color_number = 3
yellow_color_number = 4
red_color_number = 5


class MyDelegate(object):

    def __init__(self, robot):
        self.running = True
        self.robot = robot

    def drive_to_lego_color_pickup(self, color_to_drive_and_pickup):
        print("Received color", color_to_drive_and_pickup)
        self.robot.arm_calibration()
        self.robot.left_motor.run_forever(speed_sp=300)
        self.robot.right_motor.run_forever(speed_sp=300)
        break_out_variable = 1
        while break_out_variable != 0:
            if self.robot.color_sensor.color == blue_color_number and color_to_drive_and_pickup == "Blue":
                time.sleep(0.01)
                break_out_variable = 0
            if self.robot.color_sensor.color == green_color_number and color_to_drive_and_pickup == "Green":
                time.sleep(0.01)
                break_out_variable = 0
            if self.robot.color_sensor.color == yellow_color_number and color_to_drive_and_pickup == "Yellow":
                time.sleep(0.01)
                break_out_variable = 0
            if self.robot.color_sensor.color == red_color_number and color_to_drive_and_pickup == "Red":
                time.sleep(0.01)
                break_out_variable = 0
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        ev3.Sound.speak("Found" + color_to_drive_and_pickup).wait()
        self.robot.turn_degrees(90, 300)
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        self.robot.drive_inches(5, 300)
        self.robot.arm_up()
        time.sleep(0.1)
        self.robot.left_motor.run_forever(speed_sp=300)
        self.robot.right_motor.run_forever(speed_sp=300)
        break_out_variable_2 = 1
        while break_out_variable_2 != 0:
            if self.robot.color_sensor.color == blue_color_number and color_to_drive_and_pickup == "Blue":
                time.sleep(0.01)
                break_out_variable_2 = 0
            if self.robot.color_sensor.color == green_color_number and color_to_drive_and_pickup == "Green":
                time.sleep(0.01)
                break_out_variable_2 = 0
            if self.robot.color_sensor.color == yellow_color_number and color_to_drive_and_pickup == "Yellow":
                time.sleep(0.01)
                break_out_variable_2 = 0
            if self.robot.color_sensor.color == red_color_number and color_to_drive_and_pickup == "Red":
                time.sleep(0.01)
                break_out_variable_2 = 0
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        ev3.Sound.speak("Found" + color_to_drive_and_pickup).wait()

        arm_down_to_drop_in_bucket(self.robot)
        ev3.Sound.speak("You have successfully place the" + color_to_drive_and_pickup + "colored Lego in its bucket")


def main():
    robot = robo.Snatch3r()
    my_delegate = MyDelegate(robot)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc("mosquitto.csse.rose-hulman.edu", 3)

    btn = ev3.Button()

    btn.on_up = lambda state: drive_to_lego_color_pickup(state, robot, ev3.ColorSensor.COLOR_RED)
    btn.on_down = lambda state: drive_to_lego_color_pickup(state, robot, ev3.ColorSensor.COLOR_GREEN)
    btn.on_left = lambda state: drive_to_lego_color_pickup(state, robot, ev3.ColorSensor.COLOR_BLUE)
    btn.on_right = lambda state: drive_to_lego_color_pickup(state, robot, ev3.ColorSensor.COLOR_YELLOW)

    while my_delegate.running:
        btn.process()
        time.sleep(0.01)


def arm_down_to_drop_in_bucket(robot):
    """Move arm down almost all of the way"""
    max_speed = 900
    arm_revolutions_for_half_range = 7.1
    degrees_for_half_range = arm_revolutions_for_half_range * 360
    robot.arm_motor.run_to_rel_pos(position_sp=degrees_for_half_range * -1, speed_sp=max_speed)
    robot.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
    robot.arm_motor.stop(stop_action='brake')
    ev3.Sound().beep().wait()


def drive_to_lego_color_pickup(button_state, robot, color_to_drive_and_pickup):
    if button_state:
        robot.arm_calibration()
        robot.left_motor.run_forever(speed_sp=300)
        robot.right_motor.run_forever(speed_sp=300)
        while robot.color_sensor.color != color_to_drive_and_pickup:
            time.sleep(0.01)
        robot.left_motor.stop()
        robot.right_motor.stop()
        ev3.Sound.speak("Found" + COLOR_NAMES[color_to_drive_and_pickup]).wait()
        robot.turn_degrees(90, 300)
        robot.left_motor.stop()
        robot.right_motor.stop()
        robot.drive_inches(5, 300)
        robot.arm_up()
        robot.left_motor.run_forever(speed_sp=300)
        robot.right_motor.run_forever(speed_sp=300)
        while robot.color_sensor.color != color_to_drive_and_pickup:
            time.sleep(0.01)
        robot.left_motor.stop()
        robot.right_motor.stop()

        arm_down_to_drop_in_bucket(robot)


main()


