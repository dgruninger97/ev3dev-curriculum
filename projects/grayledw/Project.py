import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

class MyDelegate(object):

    def __init__(self):
        self.running = True


def main():
    my_delegate = MyDelegate()
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc("mosquitto.csse.rose-hulman.edu", 3)

    btn = ev3.Button()

    btn.on_up = lambda state: drive_to_lego_color_pickup(state, robot, ev3.ColorSensor.COLOR_RED)
    btn.on_down = lambda state: drive_to_lego_color_pickup(state, robot, ev3.ColorSensor.COLOR_BLUE)
    btn.on_left = lambda state: drive_to_lego_color_pickup(state, robot, ev3.ColorSensor.COLOR_GREEN)
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
    robot.arm_motor.run_to_abs_pos(position_sp=200, speed_sp=max_speed)
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
        robot.drive_inches(20, 300)
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
        ev3.Sound.speak("You have successfully placed the" + color_to_drive_and_pickup + "colored Lego in its bucket")


main()


