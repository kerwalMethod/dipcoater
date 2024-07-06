# Test writing to stepper motor

file_path = "/tmp/printer"

try:

    with open (file_path, 'w') as file:
            file.write("G0 X50 F600")

            print("Success!")

except:

    print("Error")
