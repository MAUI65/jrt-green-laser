import serial
from .laser_commands import commands
import time
import sys


class Laser:
    def __init__(self, port, debug=False):
        self.port = port
        self.debug = debug

        self.distance = None
        self.quality = None

        self.ser = self._init_serial()

    def _init_serial(self):
        try:
            ser = serial.Serial(self.port, baudrate=19200, timeout=1)

            self._debug_print("Module Bootup:")
            self._debug_print(" - SETTING RTS:")
            ser.rts = True
            time.sleep(0.5)
            ser.rts = False

            self._debug_print(" - BOOTINGS:")

            # Wait for the module to boot up
            time.sleep(3)

            # Overwrite the starting message with the complete message, ensuring the line is cleared
            self._debug_print(" - COMPLETE:")

            return ser
        except serial.SerialException as e:
            print(f"\rFailed to open serial port {self.port}: {e}")
            exit(1)
            return None
    
    def calculate_checksum(self, command_parts):
        relevant_parts = command_parts["address"] + command_parts["register"] + command_parts["count"] + command_parts["payload"]
        checksum = sum(relevant_parts) % 256
        return bytes([checksum])

    
    def write_command(self, cmd_info, payload=b''):
        if self.ser:
            try:
                # Check for placeholder payload and replace if necessary
                if cmd_info["payload"] == b'/PAYLOAD':
                    cmd_info["payload"] = payload

                    self._debug_print(f"    Updated Payload to: {payload.hex()}")

                # Check for placeholder checksum and calculate if necessary
                if cmd_info["checksum"] == b'/SUM':
                    cmd_info["checksum"] = self.calculate_checksum(cmd_info)
                    self._debug_print(f"    Updated Checksum to: {cmd_info['checksum'].hex()}")

                # Construct the full command from the individual components
                command = (cmd_info["head"] + cmd_info["address"] + cmd_info["register"] + 
                        cmd_info["count"] + cmd_info["payload"] + cmd_info["checksum"])
                
                if self.debug:
                    print("Command:", command.hex())
                    # print("    Head:", cmd_info['head'].hex())
                    # print("    Address:", cmd_info['address'].hex())
                    # print("    Register:", cmd_info['register'].hex())
                    # print("    Count:", cmd_info['count'].hex())
                    # print("    Payload:", cmd_info['payload'].hex())
                    # print("    Checksum:", cmd_info['checksum'].hex())
                

                self.ser.write(command)

                self._debug_print(f"    Wrote Command Hex: {command.hex()}")
                return True
            
            except serial.SerialException as e:
                print(f"Error communicating with laser: {e}")
        else:
            print("Serial connection not established.")
        return False



    def read_command(self):
        if self.ser:
            header = self.ser.read(1)
            in_message = False

            if header != b'\xaa' or header != b'\xee':
                while header != b'\xaa' and header != b'\xee':
                    header = self.ser.read(1)
                    self._debug_print(f"New Header: {header.hex()}")
                self._debug_print(f"Header Corrected to: {header.hex()}")

            # Read address
            address = self.ser.read(1)
            register = self.ser.read(2)
            count = self.ser.read(2)
            payload = self.ser.read(int(count.hex(), 16) + 1)

            if register == b'\x00\x22':
                self._debug_print("  Quality present in response")
                quality = self.ser.read(2)
                payload += quality

                self.quality =  int(quality.hex(), 16)
                
            

            checksum = self.ser.read(1)

            message = header + address + register + count + payload + checksum

            self._debug_print(f"    Response Hex: {message.hex()}")

            if checksum != self.calculate_checksum({
                "address": address,
                "register": register,
                "count": count,
                "payload": payload
            }):
                print("Checksum error")
                raise Exception('Invalid checksum')

            if header == b'\xee':
                print(f"Status Code: {self.read_status(message)}")
            
            return message
        else:
            print("Serial connection not established.")
        return None
    
    def set_laser(self, enable=True):
        command_key = "TURN_ON_LASER" if enable else "TURN_OFF_LASER"
        write_state = self.write_command(commands[command_key])
        
        if write_state:
            time.sleep(2.0)
            print(f"Laser State = {enable}")

    def get_status(self):
        print("Checking Status")
        command = commands["READ_MODULE_LATEST_STATUS"]
        self.write_command(command)

        response = self.read_command()
        print(f"Status Code: {self.read_status(response)}")

    def read_status(self, response):
        status_code = response[7:8]
        return self.status_code_to_description(status_code)

    def status_code_to_description(self, code):
        self._debug_print(f"Code number: {code}")
        status_descriptions = {
            b'\x00': "No error",
            b'\x01': "Power input too low, power voltage should >= 2.2V",
            b'\x02': "Internal error, don't care",
            b'\x03': "Module temperature is too low(< -20℃)",
            b'\x04': "Module temperature is too high(> +40℃)",
            b'\x05': "Target out of range",
            b'\x06': "Invalid measure result",
            b'\x07': "Background light too strong",
            b'\x08': "Laser signal too weak",
            b'\x09': "Laser signal too strong",
            b'\x0A': "Hardware fault 1",
            b'\x0B': "Hardware fault 2",
            b'\x0C': "Hardware fault 3",
            b'\x0D': "Hardware fault 4",
            b'\x0E': "Hardware fault 5",
            b'\x0F': "Laser signal not stable",
            b'\x10': "Hardware fault 6",
            b'\x11': "Hardware fault 7",
            b'\x81': "Invalid Frame"
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

    def one_shot_distance_measurement(self, mode='auto'):
        if mode == 'slow':
            cmd_info = commands["START_1_SHOT_SLOW_DISTANCE_MEASURE"]
        elif mode == 'fast':
            cmd_info = commands["START_1_SHOT_FAST_DISTANCE_MEASURE"]
        else:
            cmd_info = commands["START_1_SHOT_AUTO_DISTANCE_MEASURE"]

        self.write_command(cmd_info)
        distance, quality = self.read_measurement()

        return distance, quality
    
    def start_continue_distance_measurement(self, mode='auto'):
        if mode == 'slow':
            command = commands["START_CONTINUOUS_SLOW_DISTANCE_MEASURE"]
        elif mode == 'fast':
            command = commands["START_CONTINUOUS_FAST_DISTANCE_MEASURE"]
        else:
            command = commands["START_CONTINUOUS_AUTO_DISTANCE_MEASURE"]
        
        self.write_command(command)

    
    def stop_continue_distance_measurement(self):
        self.ser.write(b'X')

    def read_measurement(self):
        response = self.read_command()
        if response[0:1] == b'\xee':
            return -1, -1
        else:
            distance, quality = self.decode_distance_measurement(response.hex())
            distance_cm = distance / 10  # Convert distance from mm to cm
            print(f"Distance: {distance_cm:.1f} cm, Quality: {quality}")
            return distance, quality

    def _debug_print(self, message):
        if self.debug:
            print(message)

    def close(self):
        if self.ser:
            self.ser.close()