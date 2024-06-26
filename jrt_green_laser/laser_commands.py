commands = {
    "READ_MODULE_LATEST_STATUS": {
        "description": "Read out the module's status after the previous command executed",
        "head": b'\xaa',
        "address": b'\x80',
        "register": b'\x00\x00',
        "count": b'',
        "payload": b'',
        "checksum": b'\x80'
    },
    "READ_HARDWARE_VERSION_NUMBER": {
        "description": "Read out the module's hardware version number",
        "head": b'\xaa',
        "address": b'\x80',
        "register": b'\x00\x0a',
        "count": b'\x00',
        "payload": b'',
        "checksum": b'\x8a'
    },
    "READ_SOFTWARE_VERSION_NUMBER": {
        "description": "Read out the module's software version number",
        "head": b'\xaa',
        "address": b'\x80',
        "register": b'\x00\x0c',
        "count": b'',
        "payload": b'',
        "checksum": b'\x8c'
    },
    "READ_MODULE_SERIAL_NUMBER": {
        "description": "Read out the module's serial number",
        "head": b'\xaa',
        "address": b'\x80',
        "register": b'\x00\x0e',
        "count": b'',
        "payload": b'',
        "checksum": b'\x8e'
    },
    "READ_INPUT_VOLTAGE": {
        "description": "Read out the module's input voltage in mV with BCD encode",
        "head": b'\xaa',
        "address": b'\x80',
        "register": b'\x00\x06',
        "count": b'',
        "payload": b'',
        "checksum": b'\x86'
    },
    "READ_MEASURE_RESULT": {
        "description": "Read out the distance measure result",
        "head": b'\xaa',
        "address": b'\x80',
        "register": b'\x00\x22',
        "count": b'',
        "payload": b'',
        "checksum": b'\xa2'
    },
    "SET_MODULE_ADDRESS": {
        "description": "Set the slave's address, this address will not be lost after module power off",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x10',
        "count": b'\x00\x01',
        "payload": b'\PAYLOAD',
        "checksum": b'\SUM'
    },
    "SET_MODULE_MEASURE_OFFSET": {
        "description": "Set the slave's measure offset",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x12',
        "count": b'\x00\x01',
        "payload": b'\PAYLOAD',
        "checksum": b'\SUM'
    },
    "TURN_ON_LASER": {
        "description": "Turn on the laser",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x01\xbe',
        "count": b'\00\x01',
        "payload": b'\x00\x01',
        "checksum": b'\xc1'
    },
    "TURN_OFF_LASER": {
        "description": "Turn off the laser",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x01\xbe',
        "count": b'\x00\x01',
        "payload": b'\x00\x00',
        "checksum": b'\xc0'
    },
    "START_1_SHOT_AUTO_DISTANCE_MEASURE": {
        "description": "Initiate a 1-shot automatic distance measurement",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x20',
        "count": b'\x00\x01',
        "payload": b'\x00\x00',
        "checksum": b'\x21'
    },
    "START_1_SHOT_SLOW_DISTANCE_MEASURE": {
        "description": "Initiate a 1-shot slow distance measurement",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x20',
        "count": b'\x00\x01',
        "payload": b'\x00\x01',
        "checksum": b'\x22'
    },
    "START_1_SHOT_FAST_DISTANCE_MEASURE": {
        "description": "Initiate a 1-shot fast distance measurement",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x20',
        "count": b'\x00\x01',
        "payload": b'\x00\x02',
        "checksum": b'\x23'
    },
    "START_CONTINUOUS_AUTO_DISTANCE_MEASURE": {
        "description": "Initiate continuous automatic distance measurement",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x20',
        "count": b'\x00\x01',
        "payload": b'\x00\x04',
        "checksum": b'\x25'
    },
    "START_CONTINUOUS_SLOW_DISTANCE_MEASURE": {
        "description": "Initiate continuous slow distance measurement",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x20',
        "count": b'\x00\x01',
        "payload": b'\x00\x05',
        "checksum": b'\x26'
    },
    "START_CONTINUOUS_FAST_DISTANCE_MEASURE": {
        "description": "Initiate continuous fast distance measurement",
        "head": b'\xaa',
        "address": b'\x00',
        "register": b'\x00\x20',
        "count": b'\x00\x01',
        "payload": b'\x00\x06',
        "checksum": b'\x27'
    },
}
