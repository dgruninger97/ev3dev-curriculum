import math as ma
import mqtt_remote_method_calls as com
import robot_controller as robo
import tkinter
import ev3dev.ev3 as ev3
import time
from tkinter import ttk


def main():
    print("--------------------------------------------")
    print("Final Project")
    print("--------------------------------------------")
    ev3.Sound.speak("Final Project").wait()
    robot = robo.Snatch3r()

class MyDelegate(object):
    def __init__(self, canvas, rectangle_tag):



main():
