from jrt_green_laser import laser_serial as laser
from time import sleep

port = "/dev/ttyUSB0"
laser = laser.Laser(port, debug=False)

if (laser.ser != None):

    laser.get_status()

    laser.one_shot_distance_measurement()

    