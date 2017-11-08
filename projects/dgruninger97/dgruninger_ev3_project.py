import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com
COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
class DataContainer(object):

    def __init__(self):
        self.running = True

def main():
    print("--------------------------------------------")
    print(" Drive to the color")
    print("  Up button goes to Red")
    print("  Down button goes to Blue")
    print("  Left button goes to Black")
    print("  Right button goes to White")
    print("--------------------------------------------")
    ev3.Sound.speak("Drive to the color and then drive in circles").wait()
    print("Press Back to exit this program.")

    robot = robo.Snatch3r()
    dc = DataContainer()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    # For our standard shutdown button.
    btn = ev3.Button()
    # DONE: 2. Uncomment the lines below to setup event handlers for these buttons.
    btn.on_up = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_RED)
    btn.on_down = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_BLUE)
    btn.on_left = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_BLACK)
    btn.on_right = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_WHITE)
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    while dc.running:
        btn.process()
        time.sleep(0.01)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()



# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------
def drive_to_color_and_do_circles(button_state, robot, color_to_seek):
    length = len(str(COLOR_NAMES[color_to_seek]))
    if button_state:
        ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()
        robot.left_motor.run_forever(speed_sp=300)
        robot.right_motor.run_forever(speed_sp=300)
        while True:
            if robot.color_sensor.color == color_to_seek:
                robot.left_motor.stop()
                robot.right_motor.stop()
                break
            time.sleep(.01)
        ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()
        time.sleep(2)
        ev3.Sound.speak("Now I will drive in " + str(length) + "circles")
        time.sleep(3)
        robot.left_motor.run_forever(speed_sp = 700)
        robot.right_motor.run_forever(speed_sp = 200)
        drive_time = 8.25 * length
        time.sleep(drive_time)
        robot.left_motor.stop()
        robot.right_motor.stop()
        ev3.Sound.speak("Wow, I am dizzy")
def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False

main()
