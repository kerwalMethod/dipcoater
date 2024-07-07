import serial
import time

# Set the serial port and baud rate for communcating with Klipper
serial_port = "/tmp/printer"
baud_rate = 250000

command = "M114\n"

try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:

            ser.write(command.encode())
            response = ser.readline().decode().strip()
            print(response)

            ser.close()

except serial.SerialException as e:
        print(f"Error opening or communicating with {serial_port}: {e}")

