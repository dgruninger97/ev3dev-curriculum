import tkinter
from tkinter import ttk

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
from PIL import Image
import traceback

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3("mosquitto.csse.rose-hulman.edu", 3)

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=50, relief='raised')
    main_frame.grid()

    drive_color = ttk.Label(main_frame, text="Please enter a color to drive to")
    drive_color.grid(row=0, column=0)
    drive_color = ttk.Entry(main_frame, width=8)
    drive_color.insert(0, "Blue")
    drive_color.grid(row=1, column=0)

    LED_color = ttk.Label(main_frame, text="Please enter an LED to shine on robot")
    LED_color.grid(row=0, column=2)
    LED_color_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    LED_color_entry.insert(0, "Red")
    LED_color_entry.grid(row=1, column=2)
    mid_button = ttk.Button(main_frame, text="Enter both")
    mid_button.grid(row=2, column=1)
    mid_button['command'] = lambda: buttons(mqtt_client, drive_color, LED_color_entry)

    root.mainloop()

def buttons(mqtt_client, left_speed_entry, LED_color_entry):
    mqtt_client.send_message("drive_to_color_and_do_circles", [left_speed_entry.get(), LED_color_entry.get()])
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
