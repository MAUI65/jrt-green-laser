from jrt_green_laser import laser_serial as laser
from time import sleep, strftime
import datetime
import os

# Ensure the outputs folder exists
output_dir = "outputs"

# Modify the file name to include the outputs folder
file_name = os.path.join(output_dir, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt")

port = "/dev/ttyUSB0"
laser_device = laser.Laser(port, debug=False)

if laser_device.ser is not None:
    laser_device.get_status()
    laser_device.start_continue_distance_measurement(mode='fast')

    with open(file_name, 'w') as file:
        # Write column headers
        file.write("Iteration,Distance,Quality,Time\n")
        
        iteration = 0
        while True:
            distance, quality = laser_device.read_measurement()
            current_time = strftime("%H:%M:%S")
            log_entry = f"{iteration},{distance},{quality},{current_time}\n"
            file.write(log_entry)
            iteration += 1