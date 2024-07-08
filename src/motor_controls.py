import serial
import time

# Set the serial port and baud rate for communcating with Klipper
serial_port = "/tmp/printer"
baud_rate = 250000

# Create a function to send commands to the stepper motor
def run_dip_coater(run_parameters):

    down_position = 240 - (run_parameters[0] + run_parameters[1]) + run_parameters[2]
    down_speed = run_parameters[3] * 60
    dwell_time = run_parameters[5] * 1000
    up_position = 240 - (run_parameters[0] + run_parameters[1] + 10)
    up_speed = run_parameters[4] * 60
    pause_time = run_parameters[6] * 1000

    down_command = "G0 X" + str(down_position) + " F" + str(down_speed) + "\n"
    dwell_command = "G4 P" + str(dwell_time) + "\n"
    up_command = "G0 X" + str(up_position) + " F" + str(up_speed) + "\n"
    upper_pause_command = "G4 P" + str(pause_time) + "\n"

    commands = []
    commands.append("G28 X0\n")

    for dip in range(run_parameters[7]):
        commands.append(down_command)
        commands.append(dwell_command)
        commands.append(up_command)
        commands.append(upper_pause_command)

    commands.append("G0 X5 F600\n")
    
    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:

            for command in commands:
                ser.write(command.encode())

            ser.close()

    except serial.SerialException as e:
        print(f"Error opening or communicating with {serial_port}: {e}")

def get_run_duration(run_parameters):

    home_time = 4000
    singular_down_time = ((240 - (run_parameters[0] + run_parameters[1] + 10)) / run_parameters[3]) * 1000
    down_time = ((run_parameters[2] + 10) / run_parameters[3]) * 1000
    down_dwell = run_parameters[5] * 1000
    up_time = ((run_parameters[2] + 10) / run_parameters[4]) * 1000
    up_dwell = run_parameters[6] * 1000
    singular_up_time = (abs(240 - (run_parameters[0] + run_parameters[1] + 10 + 5)) / 10) * 1000

    total_time = home_time + singular_down_time + (down_time + down_dwell + up_time + up_dwell) * run_parameters[7] + singular_up_time

    return int(total_time)

# Create a function to stop the motor in an emergency and reset it
def stop_and_reset():
    
    command1 = "M112\n"
    command2 = "M114\n"
    command3 = "G28 X0\n"
    command4 = "G0 X5 F600\n"

    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:

            ser.write(command1.encode())
            ser.write(command2.encode())
            response = ser.readline().decode().strip()
            ser.write(command3.encode())
            ser.write(command4.encode())

            ser.close()

    except serial.SerialException as e:
        print(f"Error opening or communicating with {serial_port}: {e}")

    wait_time = (response[2:6] / 5) * 1000 + 1000

    return int(wait_time)