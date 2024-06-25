import serial
from time import sleep
from laser_commands import commands

def calculate_checksum(command):
    # Exclude the start byte from the checksum calculation if necessary
    # Assuming the start byte is the first byte and should not be included
    relevant_parts = command[1:]  # Adjust this slice as per your command structure
    print(f"Relevant parts: {relevant_parts}")
    checksum = sum(relevant_parts) % 256
    print(f"Check sum is: {checksum:02X}")  # Print checksum in 2-digit hexadecimal
    return checksum

def append_checksum(command):
    checksum = calculate_checksum(command)
    # Ensure the checksum is appended as a byte
    updated_command = command + bytes([checksum])
    print(f"Command updated to: {updated_command}")
    return updated_command

def check_device(device):
    try:
        ser = serial.Serial(device)
        ser.close()
        return True
    except serial.SerialException:
        return False

def write_read_command(command_key, ser, read_length=15):
    command_info = commands.get(command_key)
    if command_info:
        description = command_info["description"]
        command = command_info["command"]
        
        if b'SUM' in command:  # Changed from b'\xsum' to b'SUM'
            command = command.replace(b'\SUM', b'')
            command = append_checksum(command)
        
        print(f"Executing command: {description}")
        ser.write(command)
        response = ser.read(15)
        return response
    else:
        print(f"Command {command_key} not found.")
        return None
    
def decode_distance_measurement(response_hex):
    # Extract the distance (4 bytes) and signal quality (2 bytes) from the response
    distance_hex = response_hex[12:20]
    quality_hex = response_hex[20:24] 

    # Convert hex to integers
    distance = int(distance_hex, 16)
    quality = int(quality_hex, 16)

    # print(f"Hex Distance: {distance_hex}, Converted Distance: {distance}")
    # print(f"Hex Quality: {quality_hex}, Converted Quality: {quality}")

    return distance, quality

# Main function
def main():
    device = '/dev/ttyUSB0'
    if check_device(device):
        ser = serial.Serial(device, 19200, timeout=1)

        # Enable M88's PWREN pin by deasserting RTS pin
        ser.rts = True
        sleep(0.1)
        ser.rts = False

        # Wait for the module to boot up
        sleep(3)

        # Turn on laser
        response = write_read_command("TURN_ON_LASER", ser)
        print(f"Get reply: {response.hex()}")
        print("\n")

        sleep(1.)

        response = write_read_command("START_1_SHOT_SLOW_DISTANCE_MEASURE", ser)
        print(f"Get reply: {response.hex()}")

        distance, quality = decode_distance_measurement(response.hex())
        print(f"Distance: {distance} mm, Signal Quality: {quality}")
        print("\n")

        sleep(1.)

        response = write_read_command("TURN_OFF_LASER", ser)
        print("Get reply: ", response.hex(), "\n")
        
        

        ser.close()
    else:
        print(f"Device {device} not found.")

if __name__ == "__main__":
    main()
