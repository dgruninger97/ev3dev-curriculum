import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time
import math


def main():
    print("--------------------------------------------")
    print("Final Project")
    print("--------------------------------------------")
    robot = robo.Snatch3r()
    ev3.Sound.speak("Beacon Radar").wait()
    global mqtt_client
    mqtt_client = com.MqttClient(Delegate)
    mqtt_client.connect_to_pc("mosquitto.csse.rose-hulman.edu", 3)
    robot.loop_forever()


class Delegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r

    def seek_beacons(self, turn_speed, forward_speed):
        print("seeking...")

        target = 3

        b1_pos = [0, 0]
        b2_pos = [0, 0]

        bc1 = 0
        bc2 = 0

        btn = ev3.Button()

        beacon_1 = ev3.BeaconSeeker(channel=1)
        # beacon_2 = ev3.BeaconSeeker(channel=2)
        robot = robo.Snatch3r()

        robot.arm_calibration()

        while bc1 < 1:
            if beacon_1.distance != -128 and bc1 < 1:
                b1_pos = [beacon_1.heading, beacon_1.distance]
                print("found 1")
                print(beacon_1.heading_and_distance)
                print(btn.backspace)
                # print(beacon_1.distance)
                bc1 += 1
                target = 1
                ev3.Sound.beep().wait()

            # if beacon_2.distance != -128 and bc2 < 1:
            #     b2_pos = [beacon_2.heading, beacon_2.distance]
            #     print("found 2")
            #     print(beacon_2.heading_and_distance)
            #     # print(beacon_1.distance)
            #     bc2 += 1
            #     target = 2
            #     ev3.Sound.beep().wait()
            #     global mqtt_client
            #     mqtt_client.send_message("update_b2", [b2_pos[0], b2_pos[1]])


        beacon = ev3.BeaconSeeker(channel=1)
        while btn.backspace is False and forward_speed > 0 and turn_speed > 0:
            current_heading = beacon.heading  # use the beacon_seeker heading
            current_distance = beacon.distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance == 0:
                        print('You found it')
                        robot.stop()
                        break
                    if current_distance > 0:
                        robot.forward(forward_speed, forward_speed)
                        if current_distance <= 1:
                            robot.stop()
                            robot.drive_inches(3, forward_speed)
                            robot.stop()
                            ev3.Sound.speak('beacon found')
                            time.sleep(3)
                            break
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

        # The touch_sensor
        # was pressed to abort the attempt if this code runs.
        robot.stop()
        mqtt_client.send_message("update_b1", [b1_pos[0], b1_pos[1]])
        return False

    def halt(self):
        robot = robo.Snatch3r()
        robot.stop()
        beacon_1 = ev3.BeaconSeeker(channel=1)
        time.sleep(1)
        print(beacon_1.heading_and_distance)
        global mqtt_client
        mqtt_client.send_message("update_b1", [beacon_1.heading, beacon_1.distance])

    def up(self, forward):
        robot = robo.Snatch3r()
        robot.forward(forward, forward)

    def left(self, turn):
        robot = robo.Snatch3r()
        robot.left_move(-1 * turn, -1 * turn)

    def right(self, turn):
        robot = robo.Snatch3r()
        robot.right_move(-1*turn, -1 * turn)

    def back(self, forward):
        robot = robo.Snatch3r()
        robot.backward(forward, forward)


main()
