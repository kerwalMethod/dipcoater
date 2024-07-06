# Set the file path for writing commands to the stepper motor
file_path = "/tmp/printer"

# Create a function to send commands to the stepper motor
def run_dip_coater(run_parameters):

    down_position = 240 - (run_parameters[0] + run_parameters[1]) + run_parameters[2]
    down_speed = run_parameters[3] * 60
    dwell_time = run_parameters[5] * 1000
    up_position = 240 - (run_parameters[0] + run_parameters[1] + 10)
    up_speed = run_parameters[4] * 60


    down_command = "G0 X" + str(down_position) + " F" + str(down_speed) + "\n"
    dwell_command = "G4 P" + str(stay_time) + "\n"
    up_command = "G0 X" + str(up_position) + " F" + str(up_speed) + "\n"
    upper_pause_command = "G4 P1000\n"
    commands = []

    for dips in run_paremeters[6]:
        commands.append(down_command)
        commands.append(dwell_command)
        commands.append(up_command)
        commands.append(upper_pause_command)
    
    commands.append("G28 X0")
    
    with open (file_path, 'w') as file:
        for command in commands:
            file.write(command)

def get_run_duration(run_parameters):

    down_time = ((240 - (run_parameters[0] + run_parameters[1]) + run_parameters[2]) / run_parameters[3]) * 1000
    down_dwell = run_parameters[5] * 1000
    up_time = ((run_parameters[2] + 10) / run_parameters[4]) * 1000
    up_dwell = 1000

    total_time = (down_time + down_dwell + up_time + up_dwell) * run_parameters[6] + (240 - (run_parameters[0] + run_parameters[1] + 10)) / (5/6)

    return total_time

# Create a function to stop the motor in an emergency and reset it
def stop_and_reset():
    
    with open (file_path, 'w') as file:
        file.write("M112\n")
        file.write("G28 X0")