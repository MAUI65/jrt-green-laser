import serial
from time import sleep
from .laser_commands import commands

class Laser:
    def __init__(self, port, debug=False):
        self.port = port
        self.ser = self._init_serial()
        self.debug = debug

    def _init_serial(self):
        try:
            ser = serial.Serial(self.port, baudrate=19200, timeout=1)

            print("Setting RTS")
            ser.rts = True
            sleep(0.1)
            ser.rts = False

            print("Module Bootup: STARTING")
            # Wait for the module to boot up
            sleep(3)
            print("Module Bootup: COMPLETE \n")
            return ser
        except serial.SerialException as e:
            print(f"Failed to open serial port {self.port}: {e}")
            return None
    
    def calculate_checksum(self, command):
        relevant_parts = command[1:]  # ignore \xaa
        checksum = sum(relevant_parts) % 256
        return checksum

    def append_checksum(self, command):
        checksum = self.calculate_checksum(command)
        updated_command = command + bytes([checksum])
        return updated_command
    
    def write_command(self,command):
        if self.ser:
            try:
                self.ser.write(command)
                if self.debug:
                    print(f"Wrote Command Ascii: {command}")
                    print(f"Wrote Command Hex: {command.hex()}")
                return True
            except serial.SerialException as e:
                print(f"Error communicating with laser: {e}")
        else:
            print("Serial connection not established.")
        return False

    def read_command(self):
        if self.ser:
            message = bytearray()
            in_message = False

            while True:
                byte = self.ser.read(1)
                if byte == b'\xaa':
                    # If we're already in a message, and we encounter another start byte,
                    # it could indicate the start of a new message. Break or handle accordingly.
                    if in_message:
                        # Here, you might want to check if the message before this was complete
                        # based on your protocol. If it was, break, else keep reading.
                        break
                    else:
                        in_message = True
                if in_message:
                    message += byte

                # Implement logic to determine if the message is complete.
                # This could be based on length, checksum, or specific end markers.
                # If complete, break.

            if self.debug:
                print(f"Response Ascii: {message}")
                print(f"Response Hex: {message.hex()}")

            return message
        else:
            print("Serial connection not established.")
        return None
    
    def set_laser(self, enable=True):
        command_key = "TURN_ON_LASER" if enable else "TURN_OFF_LASER"
        write_state = self.write_command(commands[command_key]["command"])
        
        if write_state:
            sleep(2.0)
            print(f"Laser State = {enable}")

    def get_status(self):
        print("Checking Status")
        command = commands["READ_MODULE_LATEST_STATUS"]["command"]
        self.write_command(command)

        response = self.read_command()

        print(f"Status Code: {self.read_status(response.hex())} \n")

    def read_status(self, response):
        code_hex = response[14:16]
        return self.status_code_to_description(code_hex)

    def status_code_to_description(self, code):
        status_descriptions = {
            "00": "No error",
            "01": "Power input too low, power voltage should >= 2.2V",
            "02": "Internal error, don't care",
            "03": "Module temperature is too low(< -20℃)",
            "04": "Module temperature is too high(> +40℃)",
            "05": "Target out of range",
            "06": "Invalid measure result",
            "07": "Background light too strong",
            "08": "Laser signal too weak",
            "09": "Laser signal too strong",
            "0A": "Hardware fault 1",
            "0B": "Hardware fault 2",
            "0C": "Hardware fault 3",
            "0D": "Hardware fault 4",
            "0E": "Hardware fault 5",
            "0F": "Laser signal not stable",
            "10": "Hardware fault 6",
            "11": "Hardware fault 7",
            "81": "Invalid Frame"
        }
        return status_descriptions.get(code, "Unknown status code")

    def decode_distance_measurement(self, response_hex):
        # Extract the distance (4 bytes) and signal quality (2 bytes) from the response
        distance_hex = response_hex[12:20]
        quality_hex = response_hex[20:24] 

        # Convert hex to integers
        distance = int(distance_hex, 16)
        quality = int(quality_hex, 16)

        return distance, quality

    def one_shot_distance_measurement(self, mode='auto', display=True):
        if mode == 'slow':
            command = commands["START_1_SHOT_SLOW_DISTANCE_MEASURE"]["command"]
        elif mode == 'fast':
            command = commands["START_1_SHOT_FAST_DISTANCE_MEASURE"]["command"]
        else:
            command = commands["START_1_SHOT_AUTO_DISTANCE_MEASURE"]["command"]

        self.write_command(command)
        response = self.read_command()

        distance, quality = self.decode_distance_measurement(response.hex())

        if display:
            distance_cm = distance / 10  # Convert distance from mm to cm
            print(f"Distance: {distance_cm:.1f} cm, Quality: {quality}")

        return distance, quality
    
    def start_continue_distance_measurement(self, mode='auto'):
        if mode == 'slow':
            command = commands["START_CONTINUOUS_SLOW_DISTANCE_MEASURE"]["command"]
        elif mode == 'fast':
            command = commands["START_CONTINUOUS_FAST_DISTANCE_MEASURE"]["command"]
        else:
            command = commands["START_CONTINUOUS_AUTO_DISTANCE_MEASURE"]["command"]
        
        self.write_command(command)

    
    def stop_continue_distance_measurement(self):
        self.ser.write(b'X')

    def read_measurement(self):
        response = self.read_command()
        distance, quality = self.decode_distance_measurement(response.hex())
        distance_cm = distance / 10  # Convert distance from mm to cm
        print(f"Distance: {distance_cm:.1f} cm, Quality: {quality}")



    def close(self):
        if self.ser:
            self.ser.close()