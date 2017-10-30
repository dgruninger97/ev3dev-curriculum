import ev3dev.ev3 as ev3
import time

def main():
    print("--------------------------------------------")
    print("  drive angle")
    print("--------------------------------------------")
    ev3.Sound.speak("drive angle").wait()

    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    state = 1  # Any value other than 0.
    while state != 0:
        ang = int(input("ang (degrees): ")) * 0.0174533
        sp_ang = int(input("dps: "))
        sp_in = sp_ang * 1.3 * 0.0174533 * .5
        dis = ang * 3
        time_s = int((sp_in * (dis**-1)) ** -1)
        dis_ang = sp_ang * time_s
        left_motor.run_to_rel_pos(position_sp=-1 * dis_ang, speed_sp=sp_ang)
        right_motor.run_to_rel_pos(position_sp=dis_ang, speed_sp=sp_ang)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        state = 0
    ev3.Sound.beep().wait()

main()