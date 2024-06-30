from tkinter import *
from tkinter.messagebox import showerror
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import sqlite3
from subprocess import call
import math

root = tb.Window(themename = "pulse")
root.title("Dip Coater Gui")
root.attributes("-fullscreen", True)
root.resizable(False, False)

# Connect to the saved runs database
conn = sqlite3.connect("savedruns.db")

# Create a cursor
c = conn.cursor()

# Create a table
'''
c.execute("""CREATE TABLE savedruns (
    substrate_length float,
    solution_height float,
    dip_depth float,
    immersion_speed float,
    withdrawal_speed float,
    submersion_time float,
    dips_number integer
    )""")
'''

###


# Create a function that displays a confirmation message box for shutting down the system
def shutdown():
    mb = Messagebox.yesno("Are you sure you want to shutdown the system?", "System Shutdown")

    if mb == "Yes":
        call("sudo nohup shutdown -h now", shell = True)

    else:
        pass

# Create a function to exit the dip coater software
def exit_program():

    # Create a function to check the password
    def check_password():

        if password_entry.get() == "176371092":
            root.destroy()

        else:
            feedback_label = tb.Label(authentication_popup, text = "That's not the correct password.", bootstyle = "danger")
            feedback_label.grid(row = 3, column = 0, columnspan = 4, pady = (0, 15))

    # Set up the popup window
    authentication_popup = tb.Toplevel()
    authentication_popup.title("Authentication to Exit")
    authentication_popup.geometry("300x200")
    authentication_popup.resizable(False, False)

    # Create a label to prompt the user
    prompt_label = tb.Label(authentication_popup, text = "Enter the password to exit the program.", bootstyle = "dark")
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

    if current_mode == 1:
        saved_runs_frame.grid_forget()
        new_run_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        new_run_frame.focus_set()
        new_run_button.config(bootstyle = "primary, outline")
        saved_runs_button.config(bootstyle = "primary")
        current_mode -= 1

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

    else:
        pass


###


# Define the maximums for run parameters
min_len = 40
max_len = 140
min_sol = 40
max_sol = 140
min_speed = 0.1
max_speed = 35
max_time = 120
min_dip = 1
max_dip = 10

# Create a function for the two toggles
def toggler(x):

    if x == "d":
        if depth_var.get() == 1:
            
            try:
                depth_entry.delete(0, END)
                depth_entry.insert(0, (float(solution_entry.get()) - 13) - math.remainder((float(solution_entry.get()) - 13), (float(substrate_entry.get()) - 13)))
                substrate_entry.config(state = "disabled")
                solution_entry.config(state = "disabled")
                depth_entry.config(state = "disabled")
            except:
                depth_entry.insert(0, "")
                substrate_entry.config(state = "disabled")
                solution_entry.config(state = "disabled")
                depth_entry.config(state = "disabled")

        elif depth_var.get() == 0:
            substrate_entry.config(state = "enabled")
            solution_entry.config(state = "enabled")
            depth_entry.config(state = "enabled")
            depth_entry.delete(0, END)

    elif x == "i":
        if immersion_var.get() == 1:
            immersion_entry.delete(0, END)
            immersion_entry.insert(0, 20)
            immersion_entry.config(state = "disabled")

        elif immersion_var.get() == 0:
            immersion_entry.config(state = "enabled")
            immersion_entry.delete(0, END)

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

    try:

        if (float(substrate_entry.get()) < min_len or float(substrate_entry.get()) > max_len or float(solution_entry.get()) < min_sol or float(solution_entry.get()) > max_sol 
            or float(depth_entry.get()) > (float(solution_entry.get()) - 13) - math.remainder((float(solution_entry.get()) - 13), (float(substrate_entry.get()) - 13)) 
            or float(immersion_entry.get()) < min_speed or float(immersion_entry.get()) > max_speed or float(withdrawal_entry.get()) < min_speed or float(withdrawal_entry.get()) > max_speed 
            or float(submersion_entry.get()) > max_time or int(dips_entry.get()) < min_dip or int(dips_entry.get()) > max_dip):

            showerror(message = "One of the values you entered lies outside the allowable range!")

        else:

            if state1 == 0:
                    parameters.extend([float(substrate_entry.get()), float(solution_entry.get()), float(depth_entry.get()), float(immersion_entry.get()), float(withdrawal_entry.get()), float(submersion_entry.get()), int(dips_entry.get())])
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
                                "' AND withdrawal_speed = '" + str(withdrawal_entry.get()) + "' AND submersion_time = '" + str(submersion_entry.get()) + "' AND dips_number = '" + str(dips_entry.get()) + "'")

                    existing_runs = c.fetchone()

                    if existing_runs is None:
                        clear_button.config(state = "enabled")

                    else:
                        clear_button.config(state = "disabled")
                        saved = True

                    conn.commit()
                    conn.close()

                    for x in (substrate_entry, solution_entry, depth_entry, immersion_entry, withdrawal_entry, submersion_entry, dips_entry):
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

                if depth_var.get() == 0:
                    substrate_entry.config(state = "enabled")
                    solution_entry.config(state = "enabled")
                    depth_entry.config(state = "enabled")
                
                if immersion_var.get() == 0:
                    immersion_entry.config(state = "enabled")

                withdrawal_entry.config(state = "enabled")
                submersion_entry.config(state = "enabled")
                dips_entry.config(state = "enabled")
                lock_unlock_button.config(text = "Lock Parameters", bootstyle = "success")
                run_button.config(state = "disabled")
                state1 -= 1

    except:
        showerror(message = "One of the values you entered isn't a number or doesn't make sense given the situation!")

# Create a function to clear the new run frame entry boxes
def clear_all():
    for x in (substrate_entry, solution_entry, depth_entry, immersion_entry, withdrawal_entry, submersion_entry, dips_entry):
        x.delete(0, END)

# Create a function to save a run
def save_run():
    global saved

    conn = sqlite3.connect("savedruns.db")
    c = conn.cursor()
    c.execute("INSERT INTO savedruns VALUES (:substrate_length, :solution_height, :dip_depth, :immersion_speed, :withdrawal_speed, :submersion_time, :dips_number)",
            {
                "substrate_length": parameters[0],
                "solution_height": parameters[1],
                "dip_depth": parameters[2],
                "immersion_speed": parameters[3],
                "withdrawal_speed": parameters[4],
                "submersion_time": parameters[5],
                "dips_number": parameters[6]
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
    lock_unlock_button3.config(state = "disabled")
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
        choice = tb.Radiobutton(run_list, text = "Run " + str(run[7]) + ": \nsubstrate length: " + str(run[0]) + " mm, solution height: " + str(run[1]) + " mm, \ndipping depth: " + str(run[2]) + " mm, immersion speed: " + str(run[3]) + " mm/s, \nwithdrawal speed: " + str(run[4]) + " mm/s, submersion time: " + str(run[5]) + " s, \nnumber of dips: " + str(run[6]) + " dips",
                                variable = option, value = run[7], command = enable_stuff)
        choice.pack(anchor = "w", pady = 10)
    
    conn.commit()
    conn.close()

# Create a function to turn on the run button
def enable_stuff():
    delete_button.config(state = "enabled")
    lock_unlock_button3.config(state = "enabled")

# Create a delete function
def delete_run():
    conn = sqlite3.connect("savedruns.db")
    c = conn.cursor()
    c.execute("DELETE from savedruns WHERE oid = " + str(option.get()))
    conn.commit()
    conn.close()
    display_runs()

# Create a state variable
state4 = 0

# Create a function to lock and unlock the saved run selection
def saved_runs_lock_unlock():
    global state4

    if state4 == 0:
        conn = sqlite3.connect("savedruns.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM savedruns WHERE oid = " + str(option.get()))
        runs = c.fetchone()
        for run in runs:
            parameters.extend([run[0], run[1], run[2], run[3], run[4], run[5], run[6]])
        conn.commit()
        conn.close()

        new_run_button.config(state = "disabled")
        saved_runs_button.config(state = "disabled")
        shutdown_button.config(state = "disabled")
        exit_button.config(state = "disabled")
        delete_button.config(state = "disabled")
        lock_unlock_button3.config(text = "Unlock Parameters", bootstyle = "warning")

        for widget in run_list.winfo_children():
            widget.config(state = "disabled")

        run_button.config(state = "enabled")
        state4 += 1
    
    elif state4 == 1:
        parameters.clear()
        new_run_button.config(state = "enabled")
        saved_runs_button.config(state = "enabled")
        shutdown_button.config(state = "enabled")
        exit_button.config(state = "enabled")
        delete_button.config(state = "enabled")
        lock_unlock_button3.config(text = "Lock Parameters", bootstyle = "success")

        for widget in run_list.winfo_children():
            widget.config(state = "enabled")

        run_button.config(state = "disabled")
        state4 -= 1


###


# Create a function to run the dip coater
def run():    
    
    if current_mode == 0:
        clear_button.config(state = "disabled")
        lock_unlock_button.config(state = "disabled")
    
    elif current_mode == 1:
        lock_unlock_button3.config(state = "disabled")

    run_button.config(text = "Cancel", bootstyle = "warning", command = cancel)

    print(parameters)

# Create a function to cancel a run
def cancel():
    
    if current_mode == 0:
        if not saved:
            clear_button.config(state = "enabled")
        lock_unlock_button.config(state = "enabled")
    
    elif current_mode == 1:
        lock_unlock_button3.config(state = "enabled")

    run_button.config(text = "RUN", bootstyle = "info", command = run)


###


# Create the system sleep frame
system_frame = tb.Labelframe(root, text = "System", bootstyle = "primary")
system_frame.grid(row = 0, column = 0, padx = (5, 0), pady = (5, 0))

shutdown_button = tb.Button(system_frame, text = "Shutdown", bootstyle = "secondary", width = 9, command = shutdown)
shutdown_button.grid(row = 0, column = 0, padx = (9, 5), pady = (7, 10))

exit_button = tb.Button(system_frame, text = "Exit", bootstyle = "secondary", width = 6, command = exit_program)
exit_button.grid(row = 0, column = 1, padx = (4, 9), pady = (7, 10))


###


# Create the control modes frame
control_frame = tb.Labelframe(root, text = "Control Modes", bootstyle = "primary")
control_frame.grid(row = 0, column = 1, padx = (1, 5), pady = (5, 0))

# Create an new run mode button
new_run_button = tb.Button(control_frame, text = "New Run", bootstyle = "primary, outline", width = 11, command = new_run_switch)
new_run_button.grid(row = 0, column = 0, padx = (9, 5), pady = (7, 10))

# Create a saved runs mode button
saved_runs_button = tb.Button(control_frame, text = "Saved Runs", bootstyle = "primary", width = 11, command = saved_runs_switch)
saved_runs_button.grid(row = 0, column = 2, padx = (4, 9), pady = (7, 10))


###


# Create the new run frame
new_run_frame = tb.Labelframe(root, text = "New Run", bootstyle = "primary")
new_run_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

# Create the descriptor for substrate length, solution height, and dip depth
measurements_descriptor = tb.Label(new_run_frame, text = "Enter all physical dimensions in millimeters, all speeds in \nmillimeters per second, and all times in seconds. Note that \nthe maximum dipping depth depends on the first two \nparameters and is always less than the substrate length \nby at least 13 mm.", font = ("Helvetica", 12), bootstyle = "dark")
measurements_descriptor.grid(row = 0, column = 0, columnspan = 4, padx = 15, pady = (10, 4), sticky = "w")

# Create the substrate length entry box and its labels
substrate_label = tb.Label(new_run_frame, text = "Substrate length (" + str(min_len) + " - " + str(max_len) + " mm):", font = ("Helvetica", 12), bootstyle = "dark")
substrate_label.grid(row = 1, column = 0, columnspan = 2, padx = (15, 5), pady = (17, 5), sticky = "w")
substrate_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
substrate_entry.grid(row = 1, column = 2, padx = (0, 5), pady = (17, 5), sticky = "e")
substrate_units = tb.Label(new_run_frame, text = "mm", font = ("Helvetica", 12), bootstyle = "dark")
substrate_units.grid(row = 1, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create the solution height entry box and its labels
solution_label = tb.Label(new_run_frame, text = "Solution height (" + str(min_sol) + " - " + str(max_sol) + " mm):", font = ("Helvetica", 12), bootstyle = "dark")
solution_label.grid(row = 2, column = 0, columnspan = 2, padx = (15, 5), pady = (17, 5), sticky = "w")
solution_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
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
depth_toggle = tb.Checkbutton(new_run_frame, text = "Check box for automatic maximum dipping depth.", bootstyle = "info", variable = depth_var, onvalue = 1, offvalue = 0, command = lambda: toggler("d"))
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
immersion_toggle = tb.Checkbutton(new_run_frame, text = "Check box for standard immersion speed.", bootstyle = "info", variable = immersion_var, onvalue = 1, offvalue = 0, command = lambda: toggler("i"))
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

# Create the dips number entry box and its labels
dips_label = tb.Label(new_run_frame, text = "Number of dips (" + str(min_dip) + " - " + str(max_dip) + "):", font = ("Helvetica", 12), bootstyle = "dark")
dips_label.grid(row = 9, column = 0, padx = (15, 5), pady = (17, 5), sticky = "w")
dips_entry = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
dips_entry.grid(row = 9, column = 2, padx = (0, 5), pady = (17, 5), sticky = "e")
dips_units = tb.Label(new_run_frame, text = "dips", font = ("Helvetica", 12), bootstyle = "dark")
dips_units.grid(row = 9, column = 3, sticky = "w", padx = (0, 15), pady = (17, 5))

# Create an edit button
clear_button = tb.Button(new_run_frame, text = "Clear All", bootstyle = "secondary", width = 20, command = clear_all)
clear_button.grid(row = 10, column = 0, padx = (30, 15), pady = 15)

# Create a save button
lock_unlock_button = tb.Button(new_run_frame, text = "Lock Parameters", bootstyle = "success", width = 20, command = new_run_lock_unlock)
lock_unlock_button.grid(row = 10, column = 1, columnspan = 3, padx = (15, 30), pady = 15, sticky = "w")


###


# Create a saved runs frame
saved_runs_frame = tb.Labelframe(root, text = "Saved Runs", bootstyle = "primary")

# Create a scrolled frame
run_list = ScrolledFrame(saved_runs_frame, bootstyle = "light", width = 410, height = 510)
run_list.grid(row = 1, column = 0, columnspan = 2, padx = 24, pady = 15)

# Create an edit button
delete_button = tb.Button(saved_runs_frame, text = "Delete", bootstyle = "danger", width = 20, command = delete_run, state = "disabled")
delete_button.grid(row = 0, column = 0, padx = 15, pady = (17, 7))

# Create a delete button
lock_unlock_button3 = tb.Button(saved_runs_frame, text = "Lock Parameters", bootstyle = "success", width = 17, command = saved_runs_lock_unlock, state = "disabled")
lock_unlock_button3.grid(row = 0, column = 1, padx = (10, 15), pady = (17, 7), sticky = "w")


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

root.mainloop()