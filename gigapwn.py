import serial
import sys
import time

def initiate_update_sequence(ser):
    # Send AT^SRSR 2 to the device
    ser.write(b'AT^SRSR 2\r\n')
    print("Sent AT^SRSR 2 to the device")

    # Handle the initial responses from the device
    for _ in range(4):
        line = ser.readline().decode().strip()
        print(f"Received line: {line}")
        if line == "AT^SSWS":
            ser.write(b'OK\r\n')
            print("Sent OK in response to AT^SSWS")
        elif line == "AT^SSWR 20":
            ser.write(b'OK\r\n')
            print("Sent OK in response to AT^SSWR 20")

def send_data(ser, file, offset, size):
    file.seek(offset)
    data = file.read(size)
    ser.write(data + b'OK\r\n')
    print(f"Sent data from offset {offset} with size {size}")

def reopen_serial_port(port, baudrate, attempts=5, delay=5):
    """Attempt to reopen the serial port."""
    for attempt in range(attempts):
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            print("Serial port reopened successfully.")
            return ser
        except serial.SerialException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise Exception("Failed to reopen serial port after multiple attempts.")

def main(port, baudrate, file_path):
    with open(file_path, 'rb') as file:
        ser = serial.Serial(port, baudrate, timeout=1)
        initiate_update_sequence(ser)

        while True:
            try:
                line = ser.readline().decode().strip()
                if line.startswith("AT^SGBD"):
                    _, hex_offset, hex_size = line.split()
                    offset = int(hex_offset[:-1], 16)  # Remove the trailing comma and convert
                    size = int(hex_size, 16)
                    send_data(ser, file, offset, size)
            except serial.SerialException as e:
                print(f"Serial exception: {e}. Attempting to reopen port.")
                ser.close()
                ser = reopen_serial_port(port, baudrate)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

        if ser.is_open:
            ser.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: script.py <COM port> <baud rate> <firmware file path>")
        sys.exit(1)

    port = sys.argv[1]
    baudrate = int(sys.argv[2])
    file_path = sys.argv[3]

    main(port, baudrate, file_path)
