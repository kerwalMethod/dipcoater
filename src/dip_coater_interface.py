from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter.messagebox import showerror
import sqlite3

root = tb.Window(themename = "pulse")
root.title("Dip Coater Gui")
# root.geometry("400x800")
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


# Create a function to shutdown the system
def shutdown():
    return


###


# Create a mode variable
current_mode = 0

# Create a function for the auto button
def auto_switch():
    global current_mode

    if current_mode == 1:
        manual_frame.grid_forget()
        auto_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        auto_frame.focus_set()
        auto_button.config(bootstyle = "primary, outline")
        manual_button.config(bootstyle = "primary")
        current_mode -= 1

    elif current_mode == 2:
        history_frame.grid_forget()
        auto_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        auto_frame.focus_set()
        auto_button.config(bootstyle = "primary, outline")
        favorites_button.config(bootstyle = "primary")
        current_mode -= 2

    else:
        pass

# Create a function for the manual button
def manual_switch():
    global current_mode

    if current_mode == 0:
        auto_frame.grid_forget()
        manual_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        manual_frame.focus_set()
        manual_button.config(bootstyle = "primary, outline")
        auto_button.config(bootstyle = "primary")
        current_mode += 1

    elif current_mode == 2:
        history_frame.grid_forget()
        manual_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        manual_frame.focus_set()
        manual_button.config(bootstyle = "primary, outline")
        favorites_button.config(bootstyle = "primary")
        current_mode -= 1

    else:
        pass

# Create a function for the favorites button
def favorites_switch():
    global current_mode

    if current_mode == 0:
        auto_frame.grid_forget()
        history_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        run_list.focus_set()
        display_runs()
        favorites_button.config(bootstyle = "primary, outline")
        auto_button.config(bootstyle = "primary")
        current_mode += 2

    elif current_mode == 1:
        manual_frame.grid_forget()
        history_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)
        run_list.focus_set()
        display_runs()
        favorites_button.config(bootstyle = "primary, outline")
        manual_button.config(bootstyle = "primary")
        current_mode += 1

    else:
        pass


###


# Create a list for run parameters
parameters = []

# Create a state variable
state1 = 0

# Create a function to lock and unlock automated control frame entry boxes
def auto_lock_unlock():
    global parameters
    global state1
    
    try:
        parameters.clear()
        parameters.extend([float(entry1.get()), float(entry2.get()), float(entry3.get()), float(entry4.get()), float(entry5.get()), int(entry6.get())])

        if state1 == 0:
            auto_button.config(state = "disabled")
            manual_button.config(state = "disabled")
            favorites_button.config(state = "disabled")
            clear_button.config(text = "Save as Favorite", bootstyle = "success", command = favorite_run)

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

        elif state1 == 1:
            auto_button.config(state = "enabled")
            manual_button.config(state = "enabled")
            favorites_button.config(state = "enabled")
            clear_button.config(text = "Clear All", bootstyle = "secondary", command = clear_all, state = "enabled")
            for x in (entry1, entry2, entry3, entry4, entry5, entry6):
                x.config(state = "enabled")
            lock_unlock_button.config(text = "Lock Parameters", bootstyle = "success")
            run_button.config(state = "disabled")
            state1 -= 1
    
    except:
        showerror(message = "One of the values you entered isn't a number or doesn't make sense given the situation!")

# Create a function to clear the automated control frame entry boxes
def clear_all():
    for x in (entry1, entry2, entry3, entry4, entry5, entry6):
        x.delete(0, END)

# Create a function to save a favorite run
def favorite_run():
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


# Create two state variables
state2 = 0
state3 = 0

# Create a function to lock and unlock the manual control frame entry boxes
def manual_lock_unlock(x):
    global state2
    global state3

    if x == "UP":

        try:
            float(entry7.get())

            if state2 == 0:
                up_button.config(state = "enabled")
                entry7.config(state = "disabled")
                lock_unlock_button1.config(text = "Unlock Speed", bootstyle = "warning")
                state2 += 1

            elif state2 == 1:
                up_button.config(state = "disabled")
                entry7.config(state = "enabled")
                lock_unlock_button1.config(text = "Lock Speed", bootstyle = "success")
                state2 -= 1
            
        except:
            showerror(message = "The speed you entered is invalid!")

    elif x == "DOWN":

        try:
            float(entry8.get())

            if state3 == 0:
                down_button.config(state = "enabled")
                entry8.config(state = "disabled")
                lock_unlock_button2.config(text = "Unlock Speed", bootstyle = "warning")
                state3 += 1

            elif state3 == 1:
                down_button.config(state = "disabled")
                entry8.config(state = "enabled")
                lock_unlock_button2.config(text = "Lock Speed", bootstyle = "success")
                state3 -= 1

        except:
            showerror(message = "The speed you entered is invalid!")

# Create two state variables
state5 = 0
state6 = 0

# Create a function for the up button
def up():
    global state5

    if state5 == 0:
        lock_unlock_button1.config(state = "disabled")
        up_button.config(text = "STOP UP")
        lock_unlock_button2.config(state = "disabled")
        down_button.config(state = "disabled")
        auto_button.config(state = "disabled")
        manual_button.config(state = "disabled")
        favorites_button.config(state = "disabled")
        state5 += 1

    elif state5 == 1:
        lock_unlock_button1.config(state = "enabled")
        up_button.config(text = "START UP")
        lock_unlock_button2.config(state = "enabled")
        if state3 == 1:
            down_button.config(state = "enabled")
        auto_button.config(state = "enabled")
        manual_button.config(state = "enabled")
        favorites_button.config(state = "enabled")
        state5 -= 1

# Create a function for the down button
def down():
    global state6

    if state6 == 0:
        lock_unlock_button2.config(state = "disabled")
        down_button.config(text = "STOP DOWN")
        lock_unlock_button1.config(state = "disabled")
        up_button.config(state = "disabled")
        auto_button.config(state = "disabled")
        manual_button.config(state = "disabled")
        favorites_button.config(state = "disabled")
        state6 += 1

    elif state6 == 1:
        lock_unlock_button2.config(state = "enabled")
        down_button.config(text = "START DOWN")
        lock_unlock_button1.config(state = "enabled")
        if state2 == 1:
            up_button.config(state = "enabled")
        auto_button.config(state = "enabled")
        manual_button.config(state = "enabled")
        favorites_button.config(state = "enabled")
        state6 -= 1


###


# Create a function that displays the favorite runs
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
        choice = tb.Radiobutton(run_list, text = str(run[0]) + " cm, " + str(run[1]) + " cm, " + str(run[2]) + " cm, " + str(run[3]) + " m/s, " + str(run[4]) + " s, " + str(run[5]) + " dips",
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

# Create a function to lock and unlock the favorite run selection
def favorite_lock_unlock():
    global state4

    if state4 == 0:
        auto_button.config(state = "disabled")
        manual_button.config(state = "disabled")
        favorites_button.config(state = "disabled")
        delete_button.config(state = "disabled")
        lock_unlock_button3.config(text = "Unlock Parameters", bootstyle = "warning")

        for widget in run_list.winfo_children():
            widget.config(state = "disabled")

        run_button.config(state = "enabled")
        state4 += 1
    
    elif state4 == 1:
        auto_button.config(state = "enabled")
        manual_button.config(state = "enabled")
        favorites_button.config(state = "enabled")
        delete_button.config(state = "enabled")
        lock_unlock_button3.config(text = "Lock Parameters", bootstyle = "success")

        for widget in run_list.winfo_children():
            widget.config(state = "enabled")

        run_button.config(state = "disabled")
        state4 -= 1


###


# Create the system sleep frame
sleep_frame = tb.Labelframe(root, text = "System", bootstyle = "primary")
sleep_frame.grid(row = 0, column = 0, padx = 5, pady = (5, 0))

shutdown_button = tb.Button(sleep_frame, text = "Shutdown", bootstyle = "secondary", command = shutdown)
shutdown_button.pack(padx = 13, pady = (7, 10))


###


# Create the control modes frame
control_frame = tb.Labelframe(root, text = "Control Modes", bootstyle = "primary")
control_frame.grid(row = 0, column = 1, padx = 5, pady = (5, 0))

# Create a manual mode button
auto_button = tb.Button(control_frame, text = "Auto", bootstyle = "primary, outline", width = 9, command = auto_switch)
auto_button.grid(row = 0, column = 0, padx = (13, 6), pady = (7, 10))

# Create a manual mode button
manual_button = tb.Button(control_frame, text = "Manual", bootstyle = "primary", width = 9, command = manual_switch)
manual_button.grid(row = 0, column = 1, padx = 6, pady = (7, 10))

# Create a manual mode button
favorites_button = tb.Button(control_frame, text = "Favorites", bootstyle = "primary", width = 9, command = favorites_switch)
favorites_button.grid(row = 0, column = 2, padx = (6, 13), pady = (7, 10))



###


# Create the automated control frame
auto_frame = tb.Labelframe(root, text = "Auto Control Mode", bootstyle = "primary")
auto_frame.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

# Create the first entry box and its labels
label1 = tb.Label(auto_frame, text = "Enter the substrate length in centimeters:", font = ("Helvetica", 12), bootstyle = "dark")
label1.grid(row = 0, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry1 = tb.Entry(auto_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry1.grid(row = 1, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label1 = tb.Label(auto_frame, text = "cm", font = ("Helvetica", 12), bootstyle = "dark")
unit_label1.grid(row = 1, column = 1, sticky = "w", padx = (0, 70))

# Create the second entry box and its labels
label2 = tb.Label(auto_frame, text = "Enter the solution height in centimeters:", font = ("Helvetica", 12), bootstyle = "dark")
label2.grid(row = 2, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry2 = tb.Entry(auto_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry2.grid(row = 3, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label2 = tb.Label(auto_frame, text = "cm", font = ("Helvetica", 12), bootstyle = "dark")
unit_label2.grid(row = 3, column = 1, sticky = "w", padx = (0, 70))

# Create the third entry box and its labels
label3 = tb.Label(auto_frame, text = "Enter the dipping depth in centimeters:", font = ("Helvetica", 12), bootstyle = "dark")
label3.grid(row = 4, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry3 = tb.Entry(auto_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry3.grid(row = 5, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label3 = tb.Label(auto_frame, text = "cm", font = ("Helvetica", 12), bootstyle = "dark")
unit_label3.grid(row = 5, column = 1, sticky = "w", padx = (0, 70))

# Create the fourth entry box and its labels
label4 = tb.Label(auto_frame, text = "Enter the withdrawal speed in centimeters per second:\n (speeds range from x to y)", font = ("Helvetica", 12), bootstyle = "dark")
label4.grid(row = 6, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry4 = tb.Entry(auto_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry4.grid(row = 7, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label4 = tb.Label(auto_frame, text = "cm/s", font = ("Helvetica", 12), bootstyle = "dark")
unit_label4.grid(row = 7, column = 1, sticky = "w", padx = (0, 70))

# Create the fifth entry box and its labels
label5 = tb.Label(auto_frame, text = "Enter the substrate submersion time in seconds:", font = ("Helvetica", 12), bootstyle = "dark")
label5.grid(row = 8, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry5 = tb.Entry(auto_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry5.grid(row = 9, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label5 = tb.Label(auto_frame, text = "s", font = ("Helvetica", 12), bootstyle = "dark")
unit_label5.grid(row = 9, column = 1, sticky = "w", padx = (0, 70))

# Create the sixth entry box and its labels
label6 = tb.Label(auto_frame, text = "Enter the number of dips:", font = ("Helvetica", 12), bootstyle = "dark")
label6.grid(row = 10, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry6 = tb.Entry(auto_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry6.grid(row = 11, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label6 = tb.Label(auto_frame, text = "dips", font = ("Helvetica", 12), bootstyle = "dark")
unit_label6.grid(row = 11, column = 1, sticky = "w", padx = (0, 70))

# Create an edit button
clear_button = tb.Button(auto_frame, text = "Clear All", bootstyle = "secondary", width = 20, command = clear_all)
clear_button.grid(row = 12, column = 0, padx = (30, 15), pady = (10, 15))

# Create a save button
lock_unlock_button = tb.Button(auto_frame, text = "Lock Parameters", bootstyle = "success", width = 20, command = auto_lock_unlock)
lock_unlock_button.grid(row = 12, column = 1, padx = (15, 30), pady = (10, 15), sticky = "w")


###


# Create the manual control mode frame
manual_frame = tb.Labelframe(root, text = "Manual Control Mode", bootstyle = "primary")

# Create the first entry box and its labels
label7 = tb.Label(manual_frame, text = "Enter the upward speed in centimeters per second:\n (speeds range from x to y)", font = ("Helvetica", 12), bootstyle = "dark")
label7.grid(row = 0, column = 0, columnspan = 2, padx = 15, pady = (13, 5), sticky = "w")
entry7 = tb.Entry(manual_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry7.grid(row = 1, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label7 = tb.Label(manual_frame, text = "cm/s", font = ("Helvetica", 12), bootstyle = "dark")
unit_label7.grid(row = 1, column = 1, sticky = "w", padx = (0, 60))

# Create the first lock/unlock button
lock_unlock_button1 = tb.Button(manual_frame, text = "Lock Speed", bootstyle = "success", width = 30, command = lambda: manual_lock_unlock("UP"))
lock_unlock_button1.grid(row = 2, column = 0, columnspan = 2, padx = 15, pady = (10, 15))

# Create the up button
up_button = tb.Button(manual_frame, text = "START UP", bootstyle = "info", width = 43, state = "disabled", command = up)
up_button.grid(row = 3, column = 0, columnspan = 2, padx = 45, pady = (10, 15), ipady = 40, sticky = "ew")

# Create the second entry box and its labels
label8 = tb.Label(manual_frame, text = "Enter the downward speed in centimeters per second:\n (speeds range from x to y)", font = ("Helvetica", 12), bootstyle = "dark")
label8.grid(row = 4, column = 0, columnspan = 2, padx = 15, pady = (10, 5), sticky = "w")
entry8 = tb.Entry(manual_frame, font = ("Helvetica", 12), bootstyle = "secondary", width = 10)
entry8.grid(row = 5, column = 0, padx = (0, 5), pady = 10, sticky = "e")
unit_label8 = tb.Label(manual_frame, text = "cm/s", font = ("Helvetica", 12), bootstyle = "dark")
unit_label8.grid(row = 5, column = 1, sticky = "w", padx = (0, 60))

# Create the second lock/unlock button
lock_unlock_button2 = tb.Button(manual_frame, text = "Lock Speed", bootstyle = "success", width = 30, command = lambda: manual_lock_unlock("DOWN"))
lock_unlock_button2.grid(row = 6, column = 0, columnspan = 2, padx = 15, pady = (10, 15))

# Create the down button
down_button = tb.Button(manual_frame, text = "START DOWN", bootstyle = "info", width = 43, state = "disabled", command = down)
down_button.grid(row = 7, column = 0, columnspan = 2, padx = 45, pady = (10, 15), ipady = 40, sticky = "ew")


###


# Create a favorite runs frame
history_frame = tb.Labelframe(root, text = "Favorite Runs", bootstyle = "primary")

# Create a scrolled frame
run_list = ScrolledFrame(history_frame, bootstyle = "light", width = 410, height = 510)
run_list.grid(row = 1, column = 0, columnspan = 2, padx = 24, pady = 15)

# Create an edit button
delete_button = tb.Button(history_frame, text = "Delete", bootstyle = "danger", width = 20, command = delete_run, state = "disabled")
delete_button.grid(row = 0, column = 0, padx = 15, pady = (17, 7))

# Create a delete button
lock_unlock_button3 = tb.Button(history_frame, text = "Lock Parameters", bootstyle = "success", width = 17, command = favorite_lock_unlock, state = "disabled")
lock_unlock_button3.grid(row = 0, column = 1, padx = (10, 15), pady = (17, 7), sticky = "w")


###


# Create the run frame
run_frame = tb.Labelframe(root, text = "Run Dip Coater", bootstyle = "primary")
run_frame.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = (0, 5))

run_button = tb.Button(run_frame, text = "RUN", bootstyle = "info", width = 43, state = "disabled")
run_button.grid(row = 0, column = 0, padx = 45, pady = (10, 15), ipady = 10)


###


# Commit any changes
conn.commit()

# Close the connection
conn.close()

root.mainloop()