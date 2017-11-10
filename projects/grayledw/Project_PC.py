import mqtt_remote_method_calls as com
import tkinter
from tkinter import  ttk


def main():

    root = tkinter.Tk()
    root.title = "User Input"

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3("mosquitto.csse.rose-hulman.edu", 3)

    color_to_drive_and_pickup_label = ttk.Label(main_frame, text="Color to drive to and pickup: Enter Red, Blue, Green"
                                                                 " or Yellow")
    color_to_drive_and_pickup_label.grid(row=0, column=0)
    color_to_drive_and_pickup_entry = ttk.Entry(main_frame, width=8)
    color_to_drive_and_pickup_entry.grid(row=1, column=0)

    submit_button = ttk.Button(main_frame, text="Submit your color to drive to and pickup")
    submit_button.grid(row=2, column=0)
    submit_button['command'] = lambda: button_callbacks_for_ev3(mqtt_client, color_to_drive_and_pickup_entry)

    root.mainloop()


def button_callbacks_for_ev3(mqtt_client, color_to_drive_and_pickup_entry):
    print("In callback", color_to_drive_and_pickup_entry.get())
    if color_to_drive_and_pickup_entry.get() == "Red":
        print("You can also press the Up Button on the eV3 Robot to drive to Red")
        mqtt_client.send_message("drive_to_lego_color_pickup", [color_to_drive_and_pickup_entry.get()])
    if color_to_drive_and_pickup_entry.get() == "Blue":
        print("You can also press the Left Button on the eV3 Robot to drive to Blue")
        mqtt_client.send_message("drive_to_lego_color_pickup", [color_to_drive_and_pickup_entry.get()])
    if color_to_drive_and_pickup_entry.get() == "Green":
        print("You can also press the Down Button on the eV3 Robot to drive to Green")
        mqtt_client.send_message("drive_to_lego_color_pickup", [color_to_drive_and_pickup_entry.get()])
    if color_to_drive_and_pickup_entry.get() == "Yellow":
        print("You can also press the Right Button on the eV3 Robot to drive to Yellow")
        mqtt_client.send_message("drive_to_lego_color_pickup", [color_to_drive_and_pickup_entry.get()])


main()

