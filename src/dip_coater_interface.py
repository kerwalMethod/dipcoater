from tkinter import *
from tkinter.messagebox import showerror
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import sqlite3
from subprocess import call
import time

root = tb.Window(themename = "pulse")
root.title("Dip Coater Gui")
root.attributes("-fullscreen", True)
root.resizable(False, False)

# Connect to the favorite runs database
conn = sqlite3.connect("favoriteruns.db")

# Create a cursor
c = conn.cursor()

# Create a table
'''
c.execute("""CREATE TABLE favoriteruns (
    substrate_length float,
    solution_height float,
    dip_depth float,
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


# Create a list for run parameters
parameters = []

# Create a state variable
state1 = 0

# Create a function to lock and unlock new run frame entry boxes
def new_run_lock_unlock():
    global parameters
    global state1
    
    if state1 == 0:
        
        try:
            parameters.extend([float(entry1.get()), float(entry2.get()), float(entry3.get()), float(entry4.get()), float(entry5.get()), int(entry6.get())])
            new_run_button.config(state = "disabled")
            saved_runs_button.config(state = "disabled")
            shutdown_button.config(state = "disabled")
            exit_button.config(state = "disabled")
            clear_button.config(text = "Save Run", bootstyle = "success", command = save_run)

            conn = sqlite3.connect("favoriteruns.db")
            c = conn.cursor()
            c.execute("SELECT 1 FROM favoriteruns WHERE substrate_length = '" + str(entry1.get()) + "' AND solution_height = '" + str(entry2.get()) + "' AND dip_depth = '" + str(entry3.get()) + 
                        "' AND withdrawal_speed = '" + str(entry4.get()) + "' AND submersion_time = '" + str(entry5.get()) + "' AND dips_number = '" + str(entry6.get()) + "'")

            existing_runs = c.fetchone()

            if existing_runs is None:
                clear_button.config(state = "enabled")

            else:
                clear_button.config(state = "disabled")

            conn.commit()
            conn.close()

            for x in (entry1, entry2, entry3, entry4, entry5, entry6):
                x.config(state = "disabled")
            lock_unlock_button.config(text = "Unlock Parameters", bootstyle = "warning")
            run_button.config(state = "enabled")
            state1 += 1

        except:
            showerror(message = "One of the values you entered isn't a number or doesn't make sense given the situation!")

    elif state1 == 1:
        parameters.clear()
        new_run_button.config(state = "enabled")
        saved_runs_button.config(state = "enabled")
        shutdown_button.config(state = "enabled")
        exit_button.config(state = "enabled")
        clear_button.config(text = "Clear All", bootstyle = "secondary", command = clear_all, state = "enabled")
        for x in (entry1, entry2, entry3, entry4, entry5, entry6):
            x.config(state = "enabled")
        lock_unlock_button.config(text = "Lock Parameters", bootstyle = "success")
        run_button.config(state = "disabled")
        state1 -= 1

# Create a function to clear the new run frame entry boxes
def clear_all():
    for x in (entry1, entry2, entry3, entry4, entry5, entry6):
        x.delete(0, END)

# Create a function to save a run
def save_run():
    conn = sqlite3.connect("favoriteruns.db")
    c = conn.cursor()
    c.execute("INSERT INTO favoriteruns VALUES (:substrate_length, :solution_height, :dip_depth, :withdrawal_speed, :submersion_time, :dips_number)",
            {
                "substrate_length": parameters[0],
                "solution_height": parameters[1],
                "dip_depth": parameters[2],
                "withdrawal_speed": parameters[3],
                "submersion_time": parameters[4],
                "dips_number": parameters[5]
            }
        )
    conn.commit()
    conn.close()
    clear_button.config(state = "disabled")          


###


# Create a function that displays the saved runs
def display_runs():
    delete_button.config(state = "disabled")
    lock_unlock_button3.config(state = "disabled")
    conn = sqlite3.connect("favoriteruns.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM favoriteruns")
    runs = c.fetchall()

    for widget in run_list.winfo_children():
        widget.destroy()

    global option
    option = IntVar()
    option.set(0)

    for run in runs:
        choice = tb.Radiobutton(run_list, text = str(run[0]) + " mm, " + str(run[1]) + " mm, " + str(run[2]) + " mm, " + str(run[3]) + " mm/s, " + str(run[4]) + " s, " + str(run[5]) + " dips",
                                variable = option, value = run[6], command = enable_stuff)
        choice.pack(anchor = "w", pady = 10)
    
    conn.commit()
    conn.close()

# Create a function to turn on the run button
def enable_stuff():
    delete_button.config(state = "enabled")
    lock_unlock_button3.config(state = "enabled")

# Create a delete function
def delete_run():
    conn = sqlite3.connect("favoriteruns.db")
    c = conn.cursor()
    c.execute("DELETE from favoriteruns WHERE oid = " + str(option.get()))
    conn.commit()
    conn.close()
    display_runs()

# Create a state variable
state4 = 0

# Create a function to lock and unlock the saved run selection
def saved_runs_lock_unlock():
    global state4

    if state4 == 0:
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
    
    elif current_mode == 2:
        lock_unlock_button3.config(state = "disabled")

    run_button.config(text = "Cancel", bootstyle = "warning", command = cancel)

# Create a function to cancel a run
def cancel():
    
    if current_mode == 0:
        clear_button.config(state = "enabled")
        lock_unlock_button.config(state = "enabled")
    
    elif current_mode == 2:
        lock_unlock_button3.config(state = "enabled")

    run_button.config(text = "RUN", bootstyle = "info", command = run)


###


# Create the system sleep frame
system_frame = tb.Labelframe(root, text = "System", bootstyle = "primary")
system_frame.grid(row = 0, column = 0, padx = (5, 0), pady = (5, 0))

shutdown_button = tb.Button(system_frame, text = "Shutdown", bootstyle = "secondary", command = shutdown)
shutdown_button.grid(row = 0, column = 0, padx = (9, 5), pady = (7, 10))

exit_button = tb.Button(system_frame, text = "Exit", bootstyle = "secondary", command = exit_program)
exit_button.grid(row = 0, column = 1, padx = (5, 9), pady = (7, 10))


###


# Create the control modes frame
control_frame = tb.Labelframe(root, text = "Control Modes", bootstyle = "primary")
control_frame.grid(row = 0, column = 1, padx = (3, 5), pady = (5, 0))

# Create an new run mode button
new_run_button = tb.Button(control_frame, text = "New Run", bootstyle = "primary, outline", width = 10, command = new_run_switch)
new_run_button.grid(row = 0, column = 0, padx = (9, 5), pady = (7, 10))

# Create a saved runs mode button
saved_runs_button = tb.Button(control_frame, text = "Saved Runs", bootstyle = "primary", width = 10, command = saved_runs_switch)
saved_runs_button.grid(row = 0, column = 2, padx = (5, 9), pady = (7, 10))


###


# Create the new run frame
new_run_frame = tb.Labelframe(root, text = "New Run", bootstyle = "primary")
new_run_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

# Create the first entry box and its labels
label1 = tb.Label(new_run_frame, text = "Enter the substrate length in millimeters:", font = ("Helvetica", 12), bootstyle = "dark")
label1.grid(row = 0, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry1 = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry1.grid(row = 1, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label1 = tb.Label(new_run_frame, text = "mm", font = ("Helvetica", 12), bootstyle = "dark")
unit_label1.grid(row = 1, column = 1, sticky = "w", padx = (0, 70))

# Create the second entry box and its labels
label2 = tb.Label(new_run_frame, text = "Enter the solution height in millimeters:", font = ("Helvetica", 12), bootstyle = "dark")
label2.grid(row = 2, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry2 = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry2.grid(row = 3, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label2 = tb.Label(new_run_frame, text = "mm", font = ("Helvetica", 12), bootstyle = "dark")
unit_label2.grid(row = 3, column = 1, sticky = "w", padx = (0, 70))

# Create the third entry box and its labels
label3 = tb.Label(new_run_frame, text = "Enter the dipping depth in millimeters:", font = ("Helvetica", 12), bootstyle = "dark")
label3.grid(row = 4, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry3 = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry3.grid(row = 5, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label3 = tb.Label(new_run_frame, text = "mm", font = ("Helvetica", 12), bootstyle = "dark")
unit_label3.grid(row = 5, column = 1, sticky = "w", padx = (0, 70))

# Create the fourth entry box and its labels
label4 = tb.Label(new_run_frame, text = "Enter the withdrawal speed in millimeters per second:\n (speeds range from 0.1 mm/s to 50.0 mm/s)", font = ("Helvetica", 12), bootstyle = "dark")
label4.grid(row = 6, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry4 = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry4.grid(row = 7, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label4 = tb.Label(new_run_frame, text = "mm/s", font = ("Helvetica", 12), bootstyle = "dark")
unit_label4.grid(row = 7, column = 1, sticky = "w", padx = (0, 70))

# Create the fifth entry box and its labels
label5 = tb.Label(new_run_frame, text = "Enter the substrate submersion time in seconds:", font = ("Helvetica", 12), bootstyle = "dark")
label5.grid(row = 8, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry5 = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry5.grid(row = 9, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label5 = tb.Label(new_run_frame, text = "s", font = ("Helvetica", 12), bootstyle = "dark")
unit_label5.grid(row = 9, column = 1, sticky = "w", padx = (0, 70))

# Create the sixth entry box and its labels
label6 = tb.Label(new_run_frame, text = "Enter the number of dips:", font = ("Helvetica", 12), bootstyle = "dark")
label6.grid(row = 10, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry6 = tb.Entry(new_run_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry6.grid(row = 11, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label6 = tb.Label(new_run_frame, text = "dips", font = ("Helvetica", 12), bootstyle = "dark")
unit_label6.grid(row = 11, column = 1, sticky = "w", padx = (0, 70))

# Create an edit button
clear_button = tb.Button(new_run_frame, text = "Clear All", bootstyle = "secondary", width = 20, command = clear_all)
clear_button.grid(row = 12, column = 0, padx = (30, 15), pady = (10, 15))

# Create a save button
lock_unlock_button = tb.Button(new_run_frame, text = "Lock Parameters", bootstyle = "success", width = 20, command = new_run_lock_unlock)
lock_unlock_button.grid(row = 12, column = 1, padx = (15, 30), pady = (10, 15), sticky = "w")


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