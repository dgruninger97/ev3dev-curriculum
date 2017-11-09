import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com


COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


class MyDelegate(object):

    def __init__(self, robot):
        self.running = True
        self.robot = robot

    def drive_to_lego_color_pickup(self, color_to_drive_and_pickup):
        print("Received color", color_to_drive_and_pickup)
        self.robot.arm_calibration()
        self.robot.left_motor.run_forever(speed_sp=300)
        self.robot.right_motor.run_forever(speed_sp=300)
        print(self.robot.color_sensor.color)
        while self.robot.color_sensor.color != COLOR_NAMES[color_to_drive_and_pickup]:
            time.sleep(0.01)
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        ev3.Sound.speak("Found" + COLOR_NAMES[color_to_drive_and_pickup]).wait()
        self.robot.turn_degrees(90, 300)
        while self.robot.ir_sensor.proximity <= 36.3:
            self.robot.left_motor.run_forever(speed_sp=300)
            self.robot.right_motor.run_forever(speed_sp=300)
            time.sleep(0.01)
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        self.robot.drive_inches(20, 300)
        # robot.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        # robot.left_motor.stop()
        # robot.right_motor.stop()
        self.robot.arm_up()
        # robot.drive_inches(26, 300)
        self.robot.left_motor.run_forever(speed_sp=300)
        self.robot.right_motor.run_forever(speed_sp=300)
        while self.robot.color_sensor.color != color_to_drive_and_pickup:
            time.sleep(0.01)
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        ev3.Sound.speak("Found" + COLOR_NAMES[color_to_drive_and_pickup]).wait()

        arm_down_to_drop_in_bucket(self.robot)
        ev3.Sound.speak("You have successfully placed the" + str(
            color_to_drive_and_pickup.get()) + "colored Lego in its bucket")

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
    # btn.on_backspace = lambda state: handle_shutdown(state, my_delegate)

    while my_delegate.running:
        btn.process()
        time.sleep(0.01)

# def color_drive_identifier(robot, color_selection_entry):
#
#     if ev3.ColorSensor.color == color_selection_entry:
#         ev3.Sound.speak("You have found the color of your Lego object:", color_selection_entry)
#         ev3.Sound.speak("Put your arm down to place the Lego object in it's color square!")


def arm_down_to_drop_in_bucket(robot):
    """Move arm down"""
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
        while robot.ir_sensor.proximity <= 36.3:
            robot.left_motor.run_forever(speed_sp=300)
            robot.right_motor.run_forever(speed_sp=300)
            time.sleep(0.01)
        robot.left_motor.stop()
        robot.right_motor.stop()
        robot.drive_inches(20, 300)
        # robot.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        # robot.left_motor.stop()
        # robot.right_motor.stop()
        robot.arm_up()
        # robot.drive_inches(26, 300)
        robot.left_motor.run_forever(speed_sp=300)
        robot.right_motor.run_forever(speed_sp=300)
        while robot.color_sensor.color != color_to_drive_and_pickup:
            time.sleep(0.01)
        robot.left_motor.stop()
        robot.right_motor.stop()
        ev3.Sound.speak("Found" + COLOR_NAMES[color_to_drive_and_pickup]).wait()

        arm_down_to_drop_in_bucket(robot)
        ev3.Sound.speak("You have successfully placed the" + str(color_to_drive_and_pickup.get()) + "colored Lego in its bucket")


main()


