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

    color_to_drive_and_pickup_label = ttk.Label(main_frame, text="Color to drive to and pickup")
    color_to_drive_and_pickup_label.grid(row=0, column=0)
    color_to_drive_and_pickup_entry = ttk.Entry(main_frame, width=8)
    color_to_drive_and_pickup_entry.insert(0, " ")
    color_to_drive_and_pickup_entry.grid(row=1, column=0)

    submit_button = ttk.Button(main_frame, text="Submit your color to drive to and pickup")
    submit_button.grid(row=0, column=2)
    submit_button['command'] = lambda: button_callbacks_for_ev3(mqtt_client, color_to_drive_and_pickup_entry)

    root.mainloop()


    # left_speed_label = ttk.Label(main_frame, text="Left")
    # left_speed_label.grid(row=0, column=0)
    # left_speed_entry = ttk.Entry(main_frame, width=8)
    # left_speed_entry.insert(0, "600")
    # left_speed_entry.grid(row=1, column=0)
    #
    # right_speed_label = ttk.Label(main_frame, text="Right")
    # right_speed_label.grid(row=0, column=2)
    # right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    # right_speed_entry.insert(0, "600")
    # right_speed_entry.grid(row=1, column=2)
    #
    # color_selection_label = ttk.Label(main_frame,
    #                                   text="What color object would you like to pick up? Enter Blue, Red, or Yellow:")
    # color_selection_label.grid(row=5, column=0)
    # color_selection_entry = ttk.Entry(main_frame, width=10)
    # color_selection_entry.grid(row=5, column=1)
    #
    # root.bind_all('<KeyRelease>', lambda event: release(mqtt_client))
    # root.bind_all('<KeyPress>', lambda event: pressed(event, mqtt_client, left_speed_entry, right_speed_entry))

    root.mainloop()


# def take_control_of_robot(mqtt_client, robot):
#     while True:
# def pressed(event, mqtt_client, left_speed_entry, right_speed_entry):
#     if event.keysym == "Up":
#         print("forward")
#         mqtt_client.send_message("forward", [int(left_speed_entry.get()), int(right_speed_entry.get())])
#
#     elif event.keysym == "Down":
#         print("Back")
#         mqtt_client.send_message("backward", [int(left_speed_entry.get()), int(right_speed_entry.get())])
#
#     elif event.keysym == "Left":
#         print("left")
#         mqtt_client.send_message("left_move", [int(left_speed_entry.get()), int(right_speed_entry.get())])
#
#     elif event.keysym == "Right":
#         print("right")
#         mqtt_client.send_message("right_move", [int(left_speed_entry.get()), int(right_speed_entry.get())])
#
#     elif event.keysym == 'q':
#         mqtt_client.send_message("shutdown")
#         mqtt_client.close()
#         exit()
#
# def release(mqtt_client):
#     mqtt_client.send_message("stop")


# def color_identification(mqtt_client, robot, color_selection_entry):
#
#     mqtt_client.send_message("color_drive_identifier", [robot, color_selection_entry])


def button_callbacks_for_ev3(mqtt_client, color_to_drive_and_pickup_entry):
    if color_to_drive_and_pickup_entry.get() == "Red":
        print("Please press the Up Button on the eV3 Robot to drive to Red1")
        mqtt_client.send_message("drive_to_lego_color_pickup", [color_to_drive_and_pickup_entry.get()])


main()

