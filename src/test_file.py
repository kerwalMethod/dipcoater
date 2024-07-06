# Test writing to stepper motor

file_path = "/tmp/printer"

with open (file_path, 'w') as file:
        file.write("G0 X50 F600")