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


    down_command = "G0 X" + str(down_position) + " F" + str(down_speed) + "\n"
    dwell_command = "G4 P" + str(dwell_time) + "\n"
    up_command = "G0 X" + str(up_position) + " F" + str(up_speed) + "\n"
    upper_pause_command = "G4 P1000\n"
    commands = []

    for dips in run_parameters[6]:
        commands.append(down_command)
        commands.append(dwell_command)
        commands.append(up_command)
        commands.append(upper_pause_command)
    
    commands.append("G28 X0\n")
    
    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Opened serial port: {serial_port}")

            for command in commands:
                # Send command
                ser.write(command.encode())
                print(f"Sent command: {command.strip()}")

                # Read response (optional)
                response = ser.readline().decode().strip()
                print(f"Response from Klipper: {response}")

            # Close the serial port
            print("Serial port closed")

    except serial.SerialException as e:
        print(f"Error opening or communicating with {serial_port}: {e}")

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