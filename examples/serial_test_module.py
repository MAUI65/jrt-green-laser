from laser_serial import Laser
from time import sleep

port = "/dev/ttyUSB0"
laser = Laser(port, debug=True)
laser.set_laser(False)

laser.get_status()

laser.start_continue_distance_measurement()

x = 0
while x < 10:
    print(f"({x})")
    laser.read_measurement()
    sleep(0.1)
    x += 1

# laser.set_laser(False)