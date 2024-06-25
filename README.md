# JRT Green Laser Python Library
A python package to use the BA9D Green Laser Module from Chengdu JRT:
* BA9D (https://www.jrt-measure.com/2004-2021-new-laser-distance-sensor/62725931.html)

## Installtion
Download jrt-green-laser from github as a pip package in a virtual environment

``` sh
mkdir jrt-green-laser
cd jrt-green-laser
python3 -m venv 'venv'
source ./venv/bin/activate
pip install --upgrade pip
pip install git+https://github.com/MAUI65/jrt-green-laser
```
## Usage
An example of using the library with the sensor connected to /dev/ttyUSB0 (for linux):

### One Shot Distance Measurement
```python
import jrt_green_laser.laser_serial as laser

port = "/dev/ttyUSB0"
laser = laser.Laser(port, debug=False)

laser.one_shot_distance_measurement(mode='auto', display=True)
```
Example Output
```markdown
Setting RTS
Module Bootup: STARTING
Module Bootup: COMPLETE 

Distance: 48.4 cm, Quality: 114
```

### Continuous Shot Distance Measurement
```python
import jrt_green_laser.laser_serial as laser

port = "/dev/ttyUSB0"
laser = laser.Laser(port, debug=False)

laser.start_continue_distance_measurement()

while True:
    laser.read_measurement()
```
Example Output
```markdown
Setting RTS
Module Bootup: STARTING
Module Bootup: COMPLETE 

Distance: 48.5 cm, Quality: 115
Distance: 48.4 cm, Quality: 111
Distance: 48.5 cm, Quality: 84
...
(Note: Output will continue until the loop is interrupted.)
```
