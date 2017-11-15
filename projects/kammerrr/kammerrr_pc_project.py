import math as ma
import mqtt_remote_method_calls as com
import tkinter
# import time
from tkinter import ttk


class Delegate(object):
    def __init__(self, canvas):
         self.canvas = canvas

    def update_b1(self, w_ang, dis):
        self.canvas.delete("blip1")
        ang = (-.02737 * w_ang) + 1.5708
        # ang = w_ang * .03546
        rad = (dis * 4)
        a = rad * ma.cos(ang)
        b = rad * ma.sin(ang)

        x = 310 + a
        y = 380 - b
        print(rad)
        x0 = x - 10
        y0 = y - 10
        x1 = x + 10
        y1 = y + 10

        self.canvas.create_rectangle(x0, y0, x1, y1, fill="red", outline=None, tag="blip1")

    def update_b2(self, w_ang, dis):
        self.canvas.delete("blip2")
        ang = (-.02737 * w_ang) + 1.5708
        # ang = w_ang * .03546
        rad = (dis * 4) + 20
        a = rad * ma.cos(ang)
        b = rad * ma.sin(ang)

        x = 310 + a
        y = 380 - b
        print(rad)
        x0 = x - 10
        y0 = y - 10
        x1 = x + 10
        y1 = y + 10
        self.canvas.create_oval(x0, y0, x1, y1, fill="red", outline=None, tag="blip2")

def main():
    global mode
    mode = "short"

    root = tkinter.Tk()
    root.title = "BeaconDar"

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    pic = tkinter.PhotoImage(file="radar.gif")

    canvas = tkinter.Canvas(frame, background="lightgray", width=620, height=400)
    canvas.grid(row=1, column=0, columnspan=4)
    canvas.create_image(310, 200, image=pic)

    # toggle_long = tkinter.Button(frame, text="LONG", width=12, relief="raised", font=("System", 10, "bold"))
    # toggle_short = tkinter.Button(frame, text="SHORT", width=12, relief="sunken", font=("System", 10, "bold"))
    # toggle_long.grid(row=0, column=0)
    # toggle_short.grid(row=0, column=1)
    # toggle_long['command'] = lambda: toggler("long", toggle_long, toggle_short)
    # toggle_short['command'] = lambda: toggler("short", toggle_long, toggle_short)

    stop_btn = tkinter.Button(frame, text="STOP !", width=12, relief="raised", font=("System", 10, "bold"), pady=20)
    stop_btn.grid(row=2,column=3)
    stop_btn['command'] = lambda: stop(mqtt_client)

    my_delegate = Delegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    man_btn = tkinter.Button(frame, text="MANUAL", width=48, relief="raised", font=("System", 10, "bold"))
    man_btn.grid(row=0, column=0, columnspan=2)
    man_btn['command'] = lambda: manned(man_btn, run_btn, drive_slide, turn_slide, mqtt_client)

    run_btn = tkinter.Button(frame, text="SEEK TARGET", width=48, font=("System", 10, "bold"))
    run_btn.grid(row=0, column=2, columnspan=2)
    run_btn['command'] = lambda: send_seek(mqtt_client, turn_slide.get(), drive_slide.get())

    drive_slide = tkinter.Scale(frame, from_=0, to=900, orient="horizontal", label="DRIVE SPEED")
    drive_slide.grid(row=2, column=0)
    turn_slide = tkinter.Scale(frame, from_=0, to=900, orient="horizontal", label="TURN SPEED")
    turn_slide.grid(row=2, column=2)

    root.bind('<w>', lambda event: drive(event, run_btn, turn_slide.get(), drive_slide.get(), mqtt_client))
    root.bind('<a>', lambda event: drive(event, run_btn, turn_slide.get(), drive_slide.get(), mqtt_client))
    root.bind('<s>', lambda event: drive(event, run_btn, turn_slide.get(), drive_slide.get(), mqtt_client))
    root.bind('<d>', lambda event: drive(event, run_btn, turn_slide.get(), drive_slide.get(), mqtt_client))
    root.bind_all('<KeyRelease>', lambda event: halt(event, mqtt_client))

    root.mainloop()


def send_seek(mqtt, turn, drive):
    print(mode)
    mqtt.send_message("seek_beacons", [None, turn, drive])


def manned(btn, run, turn, drive, mqtt):
    if btn.config('relief')[-1] == 'sunken':
        btn.config(relief="raised")
        # long.config(state="normal")
        # short.config(state="normal")
        run.config(state="normal")
    else:
        btn.config(relief='sunken')
        # long.config(state="disabled")
        # short.config(state="disabled")
        run.config(state="disabled")
        #mqtt.send_message("man", [])


def drive(event, run, turn, forward, mqtt):
    if str(run['state']) == "disabled":
        if event.keysym == 'w':
            mqtt.send_message("up", [None, forward])
        if event.keysym == 'a':
            mqtt.send_message("left", [None, turn])
        if event.keysym == 's':
            mqtt.send_message("back", [None, forward])
        if event.keysym == 'd':
            mqtt.send_message("right", [None, turn])

def stop(mqtt):
    mqtt.send_message("halt",[None])

def halt(event, mqtt):
    if event.keysym == "w" or event.keysym == "a" or event.keysym == "s" or event.keysym == "d":
        stop(mqtt)


main()

