#!/usr/bin/env python3
"""
    Name: rover_gui.py
    Author: William A Loring
    Created: 12/18/21
    Purpose: Python tkinter program to 
    control MARS rover
"""

# Purpose: MARS Rover Tkinter remote control program
# ------------------------------------------------
# History
# ------------------------------------------------
# Author     Date           Comments
# Loring


from tkinter import *       # Import tkinter for GUI
from tkinter.ttk import *   # Add ttk themed widgets
import rover                # Import MARS Rover library
# Initialize the rover library without LED's
rover.init(0)


class RoverGUI:
    def __init__(self):
        """ Initialize the program """
        # Set servo physical pin numbers
        self.servo_FL = 9
        self.servo_RL = 11
        self.servo_FR = 15
        self.servo_RR = 13
        self.servo_MA = 0

        # Set initial speed
        self.speed = 60

        # Create window
        self.window = Tk()
        self.window.title("MARS Rover Remote")

        # Set the window size and location
        # 350x250 pixels in size, location at 50x50
        self.window.geometry("300x320+50+50")

        # Bind all key input events to the window
        # This will capture all keystrokes for remote control of robot
        self.window.bind_all('<Key>', self.key_input)

        # Create and layout widgets
        self.create_widgets()
        mainloop()

#--------------------------------- FORWARD --------------------------------#
    def go_forward(self):
        self.reset_servos()
        rover.forward(self.speed)

#--------------------------------- REVERSE --------------------------------#
    def go_reverse(self):
        self.reset_servos()
        rover.reverse(self.speed)

#-------------------------- LEFT ------------------------------------#
    def go_left(self):
        rover.setServo(self.servo_FL, -20)
        rover.setServo(self.servo_FR, -20)
        rover.setServo(self.servo_RL, 20)
        rover.setServo(self.servo_RR, 20)

#-------------------------- RIGHT ------------------------------------#
    def go_right(self):
        rover.setServo(self.servo_FL, 20)
        rover.setServo(self.servo_FR, 20)
        rover.setServo(self.servo_RL, -20)
        rover.setServo(self.servo_RR, -20)

#------------------------- RESET SERVOS ------------------------------------#
    def reset_servos(self):
        """
            Set all wheel steering servos to 0 (straight ahead)
        """
        rover.setServo(self.servo_FL, 0)
        rover.setServo(self.servo_FR, 0)
        rover.setServo(self.servo_RL, 0)
        rover.setServo(self.servo_RR, 0)

#--------------------------------- INCREASE SPEED -------------------------------------#
    def increase_speed(self):
        """ Increase speed """
        self.speed = min(100, self.speed+10)
        self.lbl_speed.config(text="Speed: " + str(self.speed))

#--------------------------------- DECREASE SPEED -------------------------------------#
    def decrease_speed(self):
        """ Decrease speed """
        self.speed = max(0, self.speed-10)
        self.lbl_speed.config(text="Speed: " + str(self.speed))

#----------------------------- EXIT PROGRAM ---------------------------------#
    def exit_program(self):
        print("\nExiting")
        # Cleanup rover resources
        rover.cleanup()
        # Destroy the program object
        self.window.destroy()

#--------------------------------- KEY INPUT -----------------------------------------#
    def key_input(self, event):
        # Get all key preseses as lower case
        key_press = event.keysym.lower()
        # print(key_press)  # For testing

        # Move Forward
        if key_press == 'w':
            self.go_forward()

        # Move Backward
        elif key_press == 's':
            self.go_reverse()

        # Turn Left
        elif key_press == 'a':
            self.go_left()

        # Turn Right
        elif key_press == 'd':
            self.go_right()

        # Increase Speed
        elif key_press == 't':
            self.increase_speed()

        # Decrease Speed
        elif key_press == 'g':
            self.decrease_speed()

        # Stop
        elif key_press == 'space':
            rover.stop()

        # Exit program
        elif key_press == 'z':
            self.exit_program()

#--------------------------------- CREATE WIDGETS -------------------------------------#
    def create_widgets(self):
        """ Create and layout widgets """
        # Reference for GUI display
        """
                    W = Forward
            S = Backward    A = Left
                    D = Right  
            T = Increase Speed  G = Decrease Speed  
            Spacebar = Stop
            Speed: 200
            Z = Exit    Exit button
        """
        # Create frames
        # Create main label frame to hold remote control widgets
        self.main_frame = LabelFrame(
            self.window,
            text="Remote Control",
            relief=GROOVE)
        self.middle_frame = LabelFrame(
            self.window,
            text="Speed",
            relief=GROOVE)
        # Create main frame to hold widgets
        self.bottom_frame = LabelFrame(
            self.window,
            text="Control",
            relief=GROOVE)

        # Fill the frame to the width of the window
        self.main_frame.pack(fill=X, padx=10, pady=(10, 10))
        self.middle_frame.pack(fill=X, padx=10, pady=(0))
        self.bottom_frame.pack(fill=X, padx=10, pady=10)
        # Keep the frame size regardless of the widget sizes
        self.main_frame.pack_propagate(False)
        self.middle_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(False)

        # Create widgets and attach them to the correct frame
        lbl_w_forward = Label(
            self.main_frame, text=" W: Forward", relief=RIDGE)
        lbl_s_reverse = Label(
            self.main_frame, text=" S: Reverse", relief=RIDGE)
        lbl_a_left = Label(self.main_frame, text=" A: Left", relief=RIDGE)
        lbl_d_right = Label(self.main_frame, text=" D: Right", relief=RIDGE)
        # Get and display current speed setting
        self.lbl_speed = Label(
            self.middle_frame, text=f"Speed: {self.speed}")

        lbl_t_increase_speed = Label(
            self.middle_frame, text="T: Increase Speed")
        lbl_g_decrease_speed = Label(
            self.middle_frame, text="G: Decrease Speed")
        lbl_spacebar_stop = Label(self.middle_frame, text="Spacebar: Stop")
        lbl_remote_z = Label(self.bottom_frame, text="Z: Exit")

        btn_exit = Button(
            self.bottom_frame,
            text="Exit",
            command=self.exit_program)

        # Grid the widgets
        lbl_w_forward.grid(row=0, column=1)
        lbl_a_left.grid(row=1, column=0)
        lbl_d_right.grid(row=1, column=2)
        lbl_s_reverse.grid(row=2, column=1)

        self.lbl_speed.grid(row=0, column=0, sticky=W)
        lbl_t_increase_speed.grid(row=1, column=0, sticky=W)
        lbl_g_decrease_speed.grid(row=1, column=1, sticky=W)
        lbl_spacebar_stop.grid(row=0, column=1, sticky=W)

        lbl_remote_z.grid(row=1, column=0, sticky=W)
        btn_exit.grid(row=1, column=1, sticky=E)

        # Set padding for all widgets in frames
        pad = 6
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=3, pady=3, ipadx=2, ipady=2)
        for child in self.middle_frame.winfo_children():
            child.grid_configure(padx=pad, pady=pad)
        for child in self.bottom_frame.winfo_children():
            child.grid_configure(padx=pad, pady=pad)


# Create remote control object
rover_gui = RoverGUI()

