from time import sleep

port = "/dev/ttyUSB0"
laser = Laser(port, debug=False)

if (laser.ser != None):

    laser.get_status()

    laser.start_continue_distance_measurement()


    time = 0
    while time < 10:
        laser.read_measurement()
        sleep(1)
        time += 1

    