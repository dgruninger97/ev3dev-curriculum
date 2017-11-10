import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com
COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

class DataContainer(object):

    def __init__(self):
        self.running = True


class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(.1)

    def drive_to_color_and_do_circles(self, color_to_seek, LED_color_entry):
        length = len(str(color_to_seek))
        ev3.Sound.speak("Seeking " + color_to_seek)
        time.sleep(2)
        if LED_color_entry == "RED":
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        if LED_color_entry == "ORANGE":
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)
        if LED_color_entry == "AMBER":
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.AMBER)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER)
        if LED_color_entry == "YELLOW":
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
        if LED_color_entry == "BLACK":
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        self.robot.left_motor.run_forever(speed_sp=300)
        self.robot.right_motor.run_forever(speed_sp=300)
        while True:
            if self.robot.color_sensor.color == color_to_seek:
                self.robot.left_motor.stop()
                self.robot.right_motor.stop()
                break
            time.sleep(.01)
        ev3.Sound.speak("Found " + color_to_seek)
        time.sleep(2)
        ev3.Sound.speak("Now I will drive in " + str(length) + "circles")
        time.sleep(3)
        self.robot.left_motor.run_forever(speed_sp=700)
        self.robot.right_motor.run_forever(speed_sp=200)
        drive_time = 8.25 * length
        time.sleep(drive_time)
        self.robot.left_motor.stop()
        self.robot.right_motor.stop()
        ev3.Sound.speak("Wow, I am dizzy")

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
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc("mosquitto.csse.rose-hulman.edu", 3)
    my_delegate.loop_forever()
    robot = robo.Snatch3r()
    dc = DataContainer()

    #
    # # For our standard shutdown button.
    # btn = ev3.Button()
    # # DONE: 2. Uncomment the lines below to setup event handlers for these buttons.
    # btn.on_up = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_RED)
    # btn.on_down = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_BLUE)
    # btn.on_left = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_BLACK)
    # btn.on_right = lambda state: drive_to_color_and_do_circles(state, robot, ev3.ColorSensor.COLOR_WHITE)
    # btn.on_backspace = lambda state: handle_shutdown(state, dc)
    #
    # while dc.running:
    #     btn.process()
    #     time.sleep(0.01)
    #
    # print("Goodbye!")
    # ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------

def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False

main()
