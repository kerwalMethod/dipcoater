import serial
import time

serial_port = "/tmp/printer"
baud_rate = 250000

commands = [
    "G0 X40 F600\n",
    "G4 P3000\n"
    "G0 X0 F600\n"
]

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Opened serial port: {serial_port}")

    for command in commands:
        # Send command
        ser.write(command.encode())

    # Read response (optional)
    #response = ser.readline().decode().strip()
    #print(f"Response from Klipper: {response}")

    # Close the serial port
    ser.close()
    print("Serial port closed")

except serial.SerialException as e:
    print(f"Error opening or communicating with {serial_port}: {e}")