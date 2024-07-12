from tkinter import *
from tkinter.messagebox import showerror
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import sqlite3
from subprocess import call
import motor_controls
import time

root = tb.Window(themename = "pulse")
root.title("Dip Coater Gui")
root.attributes("-fullscreen", True)
root.resizable(False, False)

# Connect to the saved runs database
conn = sqlite3.connect("savedruns.db")

# Create a cursor
c = conn.cursor()
'''
# Create a table
c.execute("""CREATE TABLE savedruns (
    substrate_length float,
    solution_height float,
    dip_depth float,
    immersion_speed float,
    withdrawal_speed float,
    submersion_time float,
    pause_time float,
    dips_number integer
    )""")
'''
###


# Create a power state variable
power_state = 0

# Create a function to power off the backlight
def power_off_backlight():
    global power_state

    if power_state == 0:
        call("echo 1 | sudo tee /sys/class/backlight/10-0045/bl_power", shell = True)
        power_state += 1

        if current_mode == 0:
            if state1 == 0:
                for x in (new_run_button, saved_runs_button, shutdown_button, exit_button, depth_toggle, immersion_toggle, clear_button, lock_unlock_button, substrate_entry, solution_entry, depth_entry, immersion_entry, withdrawal_entry, submersion_entry, pause_entry, dips_entry):
                    x.config(state = "disabled")

            elif state1 == 1:
                for x in (clear_button, lock_unlock_button, run_button):
                    x.config(state = "disabled")

        elif current_mode == 1:
            if state2 == 0:
                for x in (new_run_button, saved_runs_button, shutdown_button, exit_button):
                    x.config(state = "disabled")

                for widget in run_list.winfo_children():
                    widget.config(state = "disabled")

            elif state2 == 1:
                for x in (delete_button, lock_unlock_button2, run_button):
                    x.config(state = "disabled")
    
    elif power_state == 1:
        pass

# Create a function to power on the backlight
def power_on_backlight(event=None):
    global power_state
    global backlight_poweroff

    if power_state == 1:
        call("echo 0 | sudo tee /sys/class/backlight/10-0045/bl_power", shell = True)
        power_state -= 1

        if current_mode == 0:
            if state1 == 0:
                for x in (new_run_button, saved_runs_button, shutdown_button, exit_button, depth_toggle, immersion_toggle, clear_button, lock_unlock_button, substrate_entry, solution_entry, depth_entry, immersion_entry, withdrawal_entry, submersion_entry, pause_entry, dips_entry):
                    x.config(state = "enabled")

            elif state1 == 1:
                for x in (clear_button, lock_unlock_button, run_button):
                    x.config(state = "enabled")

        elif current_mode == 1:
            if state2 == 0:
                for x in (new_run_button, saved_runs_button, shutdown_button, exit_button):
                    x.config(state = "enabled")

                for widget in run_list.winfo_children():
                    widget.config(state = "enabled")

            elif state2 == 1:
                for x in (delete_button, lock_unlock_button2, run_button):
                    x.config(state = "enabled")

        backlight_poweroff = root.after(600000, power_off_backlight)
    
    elif power_state == 0:
        pass

# Create a function to reset the power off timeout
def reset_poweroff(event=None):
    global backlight_poweroff

    if power_state == 0:
        root.after_cancel(backlight_poweroff)
        backlight_poweroff = root.after(600000, power_off_backlight)
    
    elif power_state == 1:
        pass


###


# Create a function that displays a confirmation message box for shutting down the system
def shutdown():
    mb = Messagebox.yesno("Are you sure you want to shutdown the system?", "System Shutdown")

    if mb == "Yes":
        root.after_cancel(backlight_poweroff)
        call("sudo nohup shutdown -h now", shell = True)

    else:
        pass

# Create a function to exit the dip coater software
def exit_program():

    # Create a function to check the password
    def check_password():

        if password_entry.get() == "176371092":
            root.after_cancel(backlight_poweroff)
            call("sudo systemctl stop autolaunch.service", shell = True)
            root.destroy()

        else:
            feedback_label = tb.Label(authentication_popup, text = "That's not the correct password.", bootstyle = "danger")
            feedback_label.grid(row = 3, column = 0, columnspan = 4, pady = (0, 15))

    # Set up the popup window
    authentication_popup = tb.Toplevel()
    authentication_popup.title("Authentication to Exit")
    authentication_popup.geometry("300x210")
    authentication_popup.resizable(False, False)

    # Create a label to prompt the user
    prompt_label = tb.Label(authentication_popup, text = "Enter the password to exit the program. \n(This will stop the systemd service!)", bootstyle = "dark")
    prompt_label.grid(row = 0, column = 0, columnspan = 4, padx = 18, pady = (25, 15))

    # Create an entry box for the password
    password_entry = tb.Entry(authentication_popup, textvariable = "password", bootstyle = "secondary", show = "*")
    password_entry.grid(row = 1, column = 0, columnspan = 4, padx = 18, pady = (0, 15), sticky = "EW")

    # Create a cancel button
    cancel_button = tb.Button(authentication_popup, text = "Cancel", bootstyle = "secondary", width = 9, command = lambda: authentication_popup.destroy())
    cancel_button.grid(row = 2, column = 2, padx = (18, 0), pady = (0, 15), sticky = "E")

    # Create a submit button
    submit_button = tb.Button(authentication_popup, text = "Enter", bootstyle = "primary", width = 9, command = check_password)
    submit_button.grid(row = 2, column = 3, padx = (0, 18), pady = (0, 15), sticky = "E")

    # Set the focus to the entry box
    password_entry.focus_set()


###


# Create a mode variable
current_mode = 0

# Create a function for the new run button
def new_run_switch():
    global current_mode
    global next_entry

    if current_mode == 1:
        saved_runs_frame.grid_forget()
        new_run_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        new_run_frame.focus_set()
        new_run_button.config(bootstyle = "primary, outline")
        saved_runs_button.config(bootstyle = "primary")
        next_entry = 1
        current_mode -= 1
        reset_poweroff()

    else:
        pass

# Create a function for the saved runs button
def saved_runs_switch():
    global current_mode

    if current_mode == 0:
        new_run_frame.grid_forget()
        saved_runs_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        run_list.focus_set()
        display_runs()
        saved_runs_button.config(bootstyle = "primary, outline")
        new_run_button.config(bootstyle = "primary")
        current_mode += 1
        reset_poweroff()

    else:
        pass


###


# Create a variable to keep track of the entry box to focus on when none are selected
next_entry = 1

# Create a function to switch to the next entry box
def go_to_next_entry(x):
    global next_entry
    
    if x == 1:
        substrate_entry.focus_set()
        next_entry = 2
    elif x == 2:
        solution_entry.focus_set()
        next_entry = 3
    elif x == 3:
        depth_entry.focus_set()
        next_entry = 4
    elif x == 4:
        immersion_entry.focus_set()
        next_entry = 5
    elif x == 5:
        withdrawal_entry.focus_set()
        next_entry = 6
    elif x == 6:
        submersion_entry.focus_set()
        next_entry = 7
    elif x == 7:
        pause_entry.focus_set()
        next_entry = 8
    elif x == 8:
        dips_entry.focus_set()
        next_entry = 1

# Create a function to call the toggler function when either of the first two entry boxes changes
def call_back(var, index, mode):
    toggler("d")

# Create a function for the two toggles
def toggler(x):

    if x == "d":
        if depth_var.get() == 1:  
            try:
                depth_entry.config(state = "enabled")
                depth_entry.delete(0, END)
                if float(solution_entry.get()) >= float(substrate_entry.get()):
                    depth_entry.insert(0, float(substrate_entry.get()) - 15)
                else:
                    depth_entry.insert(0, float(solution_entry.get()) - 15)
                depth_entry.config(state = "disabled")
            except:
                depth_entry.config(state = "enabled")
                depth_entry.insert(0, "")
                depth_entry.config(state = "disabled")

        elif depth_var.get() == 0:
            depth_entry.config(state = "enabled")

    elif x == "i":
        if immersion_var.get() == 1:
            immersion_entry.delete(0, END)
            immersion_entry.insert(0, 20)
            immersion_entry.config(state = "disabled")

        elif immersion_var.get() == 0:
            immersion_entry.config(state = "enabled")

# Define the maximums for run parameters
min_len = 60
max_len = 95
min_sol = 85
max_sol = 135
min_speed = 0.5
max_speed = 35
min_time = 0
max_time = 90
min_pause = 0
max_pause = 300
min_dip = 1
max_dip = 50

# Create a list for run parameters
parameters = []

# Create a state variable
state1 = 0

# Create a variable to track the save button
saved = False

# Create a function to lock and unlock new run frame entry boxes
def new_run_lock_unlock():
    global parameters
    global state1
    global saved
    global next_entry

    reset_poweroff()

    try:

        if (float(substrate_entry.get()) < min_len or float(substrate_entry.get()) > max_len or float(solution_entry.get()) < min_sol or float(solution_entry.get()) > max_sol 
            or float(depth_entry.get()) > (float(substrate_entry.get()) - 15) or float(depth_entry.get()) > (float(solution_entry.get()) - 15)
            or float(immersion_entry.get()) < min_speed or float(immersion_entry.get()) > max_speed or float(withdrawal_entry.get()) < min_speed 
            or float(withdrawal_entry.get()) > max_speed or float(submersion_entry.get()) < min_time or float(submersion_entry.get()) > max_time 
            or float(pause_entry.get()) < min_pause or float(pause_entry.get()) > max_pause or int(dips_entry.get()) < min_dip or int(dips_entry.get()) > max_dip):

            showerror(message = "One of the values you entered lies outside the allowable range!")

        else:

            if state1 == 0:
                    parameters.extend([float(substrate_entry.get()), float(solution_entry.get()), float(depth_entry.get()), float(immersion_entry.get()), float(withdrawal_entry.get()), float(submersion_entry.get()), float(pause_entry.get()), int(dips_entry.get())])
                    new_run_button.config(state = "disabled")
                    saved_runs_button.config(state = "disabled")
                    shutdown_button.config(state = "disabled")
                    exit_button.config(state = "disabled")
                    depth_toggle.config(state = "disabled")
                    immersion_toggle.config(state = "disabled")
                    clear_button.config(text = "Save Run", bootstyle = "success", command = save_run)

                    conn = sqlite3.connect("savedruns.db")
                    c = conn.cursor()
                    c.execute("SELECT 1 FROM savedruns WHERE substrate_length = '" + str(substrate_entry.get()) + "' AND solution_height = '" + str(solution_entry.get()) + "' AND dip_depth = '" + str(depth_entry.get()) + "' AND immersion_speed = '" + str(immersion_entry.get()) + 
                                "' AND withdrawal_speed = '" + str(withdrawal_entry.get()) + "' AND submersion_time = '" + str(submersion_entry.get()) + "' AND pause_time = '" + str(pause_entry.get()) + "' AND dips_number = '" + str(dips_entry.get()) + "'")

                    existing_runs = c.fetchone()

                    if existing_runs is None:
                        clear_button.config(state = "enabled")

                    else:
                        clear_button.config(state = "disabled")
                        saved = True

                    conn.commit()
                    conn.close()

                    for x in (substrate_entry, solution_entry, depth_entry, immersion_entry, withdrawal_entry, submersion_entry, pause_entry, dips_entry):
                        x.config(state = "disabled")

                    lock_unlock_button.config(text = "Unlock Parameters", bootstyle = "warning")
                    run_button.config(state = "enabled")
                    state1 += 1

            elif state1 == 1:
                parameters.clear()
                saved = False
                new_run_button.config(state = "enabled")
                saved_runs_button.config(state = "enabled")
                shutdown_button.config(state = "enabled")
                exit_button.config(state = "enabled")
                depth_toggle.config(state = "enabled")
                immersion_toggle.config(state = "enabled")
                clear_button.config(text = "Clear All", bootstyle = "secondary", command = clear_all, state = "enabled")
                substrate_entry.config(state = "enabled")
                solution_entry.config(state = "enabled")

                if depth_var.get() == 0:
                    depth_entry.config(state = "enabled")
                
                if immersion_var.get() == 0:
                    immersion_entry.config(state = "enabled")

                withdrawal_entry.config(state = "enabled")
                submersion_entry.config(state = "enabled")
                pause_entry.config(state = "enabled")
                dips_entry.config(state = "enabled")
                lock_unlock_button.config(text = "Lock Parameters", bootstyle = "success")
                run_button.config(state = "disabled")
                new_run_frame.focus_set()
                next_entry = 1
                state1 -= 1

    except:
        showerror(message = "One of the values you entered isn't a number or doesn't make sense given the situation!")

# Create a function to clear the new run frame entry boxes
def clear_all():
    global next_entry

    reset_poweroff()
    
    depth_var.set(0)
    toggler("d")
    immersion_var.set(0)
    toggler("i")

    for x in (substrate_entry, solution_entry, depth_entry, immersion_entry, withdrawal_entry, submersion_entry, pause_entry, dips_entry):
        x.delete(0, END)

    new_run_frame.focus_set()
    next_entry = 1

# Create a function to save a run
def save_run():
    global saved
    global parameters

    reset_poweroff()

    conn = sqlite3.connect("savedruns.db")
    c = conn.cursor()
    c.execute("INSERT INTO savedruns VALUES (:substrate_length, :solution_height, :dip_depth, :immersion_speed, :withdrawal_speed, :submersion_time, :pause_time, :dips_number)",
            {
                "substrate_length": parameters[0],
                "solution_height": parameters[1],
                "dip_depth": parameters[2],
                "immersion_speed": parameters[3],
                "withdrawal_speed": parameters[4],
                "submersion_time": parameters[5],
                "pause_time": parameters[6],
                "dips_number": parameters[7]
            }
        )
    conn.commit()
    conn.close()
    clear_button.config(state = "disabled")
    saved = True          


###


# Create a function that displays the saved runs
def display_runs():
    delete_button.config(state = "disabled")
    lock_unlock_button2.config(state = "disabled")
    conn = sqlite3.connect("savedruns.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM savedruns")
    runs = c.fetchall()

    for widget in run_list.winfo_children():
        widget.destroy()

    global option
    option = IntVar()
    option.set(0)

    for run in runs:
        choice = tb.Radiobutton(run_list, text = "Run " + str(run[8]) + ": \nsubstrate length: " + str(run[0]) + " mm, solution height: " + str(run[1]) + " mm, \ndipping depth: " + str(run[2]) + " mm, immersion speed: " + str(run[3]) + " mm/s, \nwithdrawal speed: " + str(run[4]) + " mm/s, submersion time: " + str(run[5]) + " s, \npause time: " + str(run[6]) + " s, number of dips: " + str(run[7]) + " dips",
                                variable = option, value = run[8], command = enable_stuff)
        choice.pack(anchor = "w", pady = 10)
    
    conn.commit()
    conn.close()

# Create a function to turn on the run button
def enable_stuff():
    delete_button.config(state = "enabled")
    lock_unlock_button2.config(state = "enabled")
    reset_poweroff()

# Create a delete function
def delete_run():
    conn = sqlite3.connect("savedruns.db")
    c = conn.cursor()
    c.execute("DELETE from savedruns WHERE oid = " + str(option.get()))
    conn.commit()
    conn.close()
    display_runs()
    reset_poweroff()

# Create a state variable
state2 = 0

# Create a function to lock and unlock the saved run selection
def saved_runs_lock_unlock():
    global state2
    global parameters

    reset_poweroff()

    if state2 == 0:
        conn = sqlite3.connect("savedruns.db")
        c = conn.cursor()
        c.execute("SELECT * FROM savedruns WHERE oid = " + str(option.get()))
        run = c.fetchall()
        for par in run:
            parameters.extend([par[0], par[1], par[2], par[3], par[4], par[5], par[6], par[7]])
        conn.commit()
        conn.close()

        new_run_button.config(state = "disabled")
        saved_runs_button.config(state = "disabled")
        shutdown_button.config(state = "disabled")
        exit_button.config(state = "disabled")
        delete_button.config(state = "disabled")
        lock_unlock_button2.config(text = "Unlock Parameters", bootstyle = "warning")

        for widget in run_list.winfo_children():
            widget.config(state = "disabled")

        run_button.config(state = "enabled")
        state2 += 1
    
    elif state2 == 1:
        parameters.clear()
        new_run_button.config(state = "enabled")
        saved_runs_button.config(state = "enabled")
        shutdown_button.config(state = "enabled")
        exit_button.config(state = "enabled")
        delete_button.config(state = "enabled")
        lock_unlock_button2.config(text = "Lock Parameters", bootstyle = "success")

        for widget in run_list.winfo_children():
            widget.config(state = "enabled")

        run_button.config(state = "disabled")
        state2 -= 1


###


# Create a function to reenable buttons after a run
def reenabling():
    global backlight_poweroff

    if current_mode == 0:
        if not saved:
            clear_button.config(state = "enabled")
        lock_unlock_button.config(state = "enabled")
        run_button.config(text = "RUN", bootstyle = "info", state = "enabled", command = run)

    elif current_mode == 1:
        lock_unlock_button2.config(state = "enabled")
        run_button.config(text = "RUN", bootstyle = "info", state = "enabled", command = run)

    call("echo 255 | sudo tee /sys/class/backlight/10-0045/brightness", shell = True)
    backlight_poweroff = root.after(600000, power_off_backlight)

# Create a function to run the dip coater
def run():
    global run_wait
    global backlight_poweroff
    global parameters

    if current_mode == 0:
        clear_button.config(state = "disabled")
        lock_unlock_button.config(state = "disabled")
        run_button.config(text = "EMERGENCY STOP", bootstyle = "danger", command = cancel)
        call("echo 100 | sudo tee /sys/class/backlight/10-0045/brightness", shell = True)
        root.after_cancel(backlight_poweroff)
    
    elif current_mode == 1:
        lock_unlock_button2.config(state = "disabled")
        run_button.config(text = "EMERGENCY STOP", bootstyle = "danger", command = cancel)
        call("echo 100 | sudo tee /sys/class/backlight/10-0045/brightness", shell = True)
        root.after_cancel(backlight_poweroff)
    
    motor_controls.run_dip_coater(parameters)
    wait_time = motor_controls.get_run_duration(parameters)
    run_wait = root.after(wait_time, reenabling)

# Create a function to cancel a run
def cancel():
    global run_wait

    run_button.config(text = "Waiting for homing...", state = "disabled")
    root.after_cancel(run_wait)
    motor_controls.stop_and_reset()
    wait_time = 35 * 1000
    stop_wait = root.after(wait_time, reenabling)


###


# Create the system sleep frame
system_frame = tb.Labelframe(root, text = "System", bootstyle = "primary")
system_frame.grid(row = 0, column = 0, padx = (5, 0), pady = (5, 0))

shutdown_button = tb.Button(system_frame, text = "Shutdown", bootstyle = "secondary", width = 9, command = shutdown)
shutdown_button.grid(row = 0, column = 0, padx = (9, 5), pady = (7, 10))

exit_button = tb.Button(system_frame, text = "Exit", bootstyle = "secondary", width = 6, command = exit_program)
exit_button.grid(row = 0, column = 1, padx = (3, 9), pady = (7, 10))


###


# Create the control modes frame
control_frame = tb.Labelframe(root, text = "Control Modes", bootstyle = "primary")
control_frame.grid(row = 0, column = 1, padx = (2, 5), pady = (5, 0))

# Create an new run mode button
new_run_button = tb.Button(control_frame, text = "New Run", bootstyle = "primary, outline", width = 11, command = new_run_switch)
new_run_button.grid(row = 0, column = 0, padx = (9, 5), pady = (7, 10))

# Create a saved runs mode button
saved_runs_button = tb.Button(control_frame, text = "Saved Runs", bootstyle = "primary", width = 11, command = saved_runs_switch)
saved_runs_button.grid(row = 0, column = 2, padx = (3, 9), pady = (7, 10))


###


# Create the new run frame
new_run_frame = tb.Labelframe(root, text = "New Run", bootstyle = "primary")
new_run_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

# Create two variables for autofilling the depth entry box when the maximum depth toggle is on
substrate_var = DoubleVar()
solution_var = DoubleVar()
substrate_var.trace_add("write", call_back)
solution_var.trace_add("write", call_back)

# Create the descriptor for substrate length, solution height, and dip depth
measurements_descriptor = tb.Label(new_run_frame, text = "Place the top edge of the substrate flush with the top of the \nrubber clamp ends (should be 235 mm above the table).", font = ("Helvetica", 12), bootstyle = "dark")
measurements_descriptor.grid(row = 0, column = 0, columnspan = 4, padx = 15, pady = (10, 2), sticky = "w")

# Create the substrate length entry box and its labels
substrate_label = tb.Label(new_run_frame, text = "Substrate length (" + str(min_len) + " - " + str(max_len) + " mm):", font = ("Helvetica", 12), bootstyle = "dark")
substrate_label.grid(row = 1, column = 0, columnspan = 2, padx = (15, 5), pady = (17, 5), sticky = "w")
substrate_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10, textvariable = substrate_var)
substrate_entry.grid(row = 1, column = 2, padx = (0, 5), pady = (17, 5), sticky = "e")
substrate_units = tb.Label(new_run_frame, text = "mm", font = ("Helvetica", 12), bootstyle = "dark")
substrate_units.grid(row = 1, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create the solution height entry box and its labels
solution_label = tb.Label(new_run_frame, text = "Solution height (" + str(min_sol) + " - " + str(max_sol) + " mm):", font = ("Helvetica", 12), bootstyle = "dark")
solution_label.grid(row = 2, column = 0, columnspan = 2, padx = (15, 5), pady = (17, 5), sticky = "w")
solution_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10, textvariable = solution_var)
solution_entry.grid(row = 2, column = 2, padx = (0, 5), pady = (17, 5), sticky = "e")
solution_units = tb.Label(new_run_frame, text = "mm", font = ("Helvetica", 12), bootstyle = "dark")
solution_units.grid(row = 2, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create the dipping depth entry box and its labels
depth_label = tb.Label(new_run_frame, text = "Substrate dipping depth:", font = ("Helvetica", 12), bootstyle = "dark")
depth_label.grid(row = 3, column = 0, padx = (15, 5), pady = (17, 5), sticky = "w")
depth_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
depth_entry.grid(row = 3, column = 2, padx = (0, 5), pady = (15, 5), sticky = "e")
depth_units = tb.Label(new_run_frame, text = "mm", font = ("Helvetica", 12), bootstyle = "dark")
depth_units.grid(row = 3, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create a toggle to autofill the maximum dipping depth
depth_var = IntVar()
depth_toggle = tb.Checkbutton(new_run_frame, text = "Toggle for automatic maximum dipping depth.", bootstyle = "info, square-toggle", variable = depth_var, onvalue = 1, offvalue = 0, command = lambda: toggler("d"))
depth_toggle.grid(row = 4, column = 0, columnspan = 3, padx = 15, pady = (7, 8), sticky = "w")

# Create the immersion speed entry box and labels
immersion_label = tb.Label(new_run_frame, text = "Immersion speed (" + str(min_speed) + " - " + str(max_speed) + " mm/s):", font = ("Helvetica", 12), bootstyle = "dark")
immersion_label.grid(row = 5, column = 0, columnspan = 2, padx = (15, 5), pady = (15, 5), sticky = "w")
immersion_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
immersion_entry.grid(row = 5, column = 2, padx = (0, 5), pady = (16, 5), sticky = "e")
immersion_units = tb.Label(new_run_frame, text = "mm/s", font = ("Helvetica", 12), bootstyle = "dark")
immersion_units.grid(row = 5, column = 3, sticky = "w", padx = (0, 15), pady = (16, 5))

# Create a toggle to autofill a standard immersion speed
immersion_var = IntVar()
immersion_toggle = tb.Checkbutton(new_run_frame, text = "Toggle for standard immersion speed.", bootstyle = "info, square-toggle", variable = immersion_var, onvalue = 1, offvalue = 0, command = lambda: toggler("i"))
immersion_toggle.grid(row = 6, column = 0, columnspan = 3, padx = 15, pady = (7, 8), sticky = "w")

# Create the withdrawal speed entry box and its labels
withdrawal_label = tb.Label(new_run_frame, text = "Withdrawal speed (" + str(min_speed) + " - " + str(max_speed) + " mm/s):", font = ("Helvetica", 12), bootstyle = "dark")
withdrawal_label.grid(row = 7, column = 0, columnspan = 2, padx = (15, 5), pady = (15, 5), sticky = "w")
withdrawal_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
withdrawal_entry.grid(row = 7, column = 2, padx = (0, 5), pady = (16, 5), sticky = "e")
withdrawal_units = tb.Label(new_run_frame, text = "mm/s", font = ("Helvetica", 12), bootstyle = "dark")
withdrawal_units.grid(row = 7, column = 3, sticky = "w", padx = (0, 15), pady = (16, 5))

# Create the submersion time entry box and its labels
submersion_label = tb.Label(new_run_frame, text = "Submersion time (max. " + str(max_time) + " s):", font = ("Helvetica", 12), bootstyle = "dark")
submersion_label.grid(row = 8, column = 0, columnspan = 2, padx = (15, 5), pady = (17, 5), sticky = "w")
submersion_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
submersion_entry.grid(row = 8, column = 2, padx = (0, 5), pady = (17, 5), sticky = "e")
submersion_units = tb.Label(new_run_frame, text = "s", font = ("Helvetica", 12), bootstyle = "dark")
submersion_units.grid(row = 8, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create the upper pause entry box and its labels
pause_label = tb.Label(new_run_frame, text = "Upper pause time (max. " + str(max_pause) + " s):", font = ("Helvetica", 12), bootstyle = "dark")
pause_label.grid(row = 9, column = 0, columnspan = 2, padx = (15, 5), pady = (17, 5), sticky = "w")
pause_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
pause_entry.grid(row = 9, column = 2, padx = (0, 5), pady = (17, 5), sticky = "e")
pause_units = tb.Label(new_run_frame, text = "s", font = ("Helvetica", 12), bootstyle = "dark")
pause_units.grid(row = 9, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create the dips number entry box and its labels
dips_label = tb.Label(new_run_frame, text = "Number of dips (" + str(min_dip) + " - " + str(max_dip) + "):", font = ("Helvetica", 12), bootstyle = "dark")
dips_label.grid(row = 10, column = 0, padx = (15, 5), pady = (17, 5), sticky = "w")
dips_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
dips_entry.grid(row = 10, column = 2, padx = (0, 5), pady = (17, 5), sticky = "e")
dips_units = tb.Label(new_run_frame, text = "dips", font = ("Helvetica", 12), bootstyle = "dark")
dips_units.grid(row = 10, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create an edit button
clear_button = tb.Button(new_run_frame, text = "Clear All", bootstyle = "secondary", width = 20, command = clear_all)
clear_button.grid(row = 11, column = 0, padx = (30, 15), pady = 15)

# Create a lock/unlock button
lock_unlock_button = tb.Button(new_run_frame, text = "Lock Parameters", bootstyle = "success", width = 20, command = new_run_lock_unlock)
lock_unlock_button.grid(row = 11, column = 1, columnspan = 3, padx = (15, 30), pady = 15, sticky = "w")

# Bind the new run frame, entry boxes, clear all button, and lock/unlock button to the return key
new_run_frame.bind('<KP_Enter>', lambda event: go_to_next_entry(next_entry))
substrate_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(2))
solution_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(3))
depth_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(4))
immersion_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(5))
withdrawal_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(6))
submersion_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(7))
pause_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(8))
dips_entry.bind('<KP_Enter>', lambda event: go_to_next_entry(1))
depth_toggle.bind('<KP_Enter>', lambda event: go_to_next_entry(next_entry))
immersion_toggle.bind('<KP_Enter>', lambda event: go_to_next_entry(next_entry))

# Clear the automatically entered zeros from the frist two entry boxes and set the focus on the entire labelframe
substrate_entry.delete(0, END)
solution_entry.delete(0, END)
new_run_frame.focus_set()


###


# Create a saved runs frame
saved_runs_frame = tb.Labelframe(root, text = "Saved Runs", bootstyle = "primary")

# Create a scrolled frame
run_list = ScrolledFrame(saved_runs_frame, bootstyle = "light", width = 410, height = 510)
run_list.grid(row = 1, column = 0, columnspan = 2, padx = 24, pady = 15)

# Create a delete button
delete_button = tb.Button(saved_runs_frame, text = "Delete", bootstyle = "danger", width = 20, command = delete_run, state = "disabled")
delete_button.grid(row = 0, column = 0, padx = 15, pady = (17, 7))

# Create a lock/unlock button
lock_unlock_button2 = tb.Button(saved_runs_frame, text = "Lock Parameters", bootstyle = "success", width = 17, command = saved_runs_lock_unlock, state = "disabled")
lock_unlock_button2.grid(row = 0, column = 1, padx = (10, 15), pady = (17, 7), sticky = "w")


###


# Create the run frame
run_frame = tb.Labelframe(root, text = "Run Dip Coater", bootstyle = "primary")
run_frame.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = (0, 5))

run_button = tb.Button(run_frame, text = "RUN", bootstyle = "info", width = 43, state = "disabled", command = run)
run_button.grid(row = 0, column = 0, padx = 45, pady = (10, 15), ipady = 10)


###


# Commit any changes
conn.commit()

# Close the connection
conn.close()

# Create a timeout to power off the backlight and add keybindings to turn backlight on and reset timeout
root.bind('<KP_Add>', power_on_backlight)
root.bind('<KP_0>', reset_poweroff)
root.bind('<KP_1>', reset_poweroff)
root.bind('<KP_2>', reset_poweroff)
root.bind('<KP_3>', reset_poweroff)
root.bind('<KP_4>', reset_poweroff)
root.bind('<KP_5>', reset_poweroff)
root.bind('<KP_6>', reset_poweroff)
root.bind('<KP_7>', reset_poweroff)
root.bind('<KP_8>', reset_poweroff)
root.bind('<KP_9>', reset_poweroff)
backlight_poweroff = root.after(600000, power_off_backlight)

reset_poweroff()

root.mainloop()