import smbus
import time

# Initialize the I2C bus (bus 1 for Raspberry Pi 3 B+)
bus = smbus.SMBus(1)

# I2C address of the Raspberry Pi (must match what is set on the ESP32)
# The Raspberry Pi does not have a fixed I2C slave address, it must act as a master reader
esp32_address = 0x08

def read_data():
    while True:
        try:
            # Attempt to read one byte from the ESP32
            data = bus.read_byte(esp32_address)
            print(f"Data received: {data}")
        except Exception as e:
            print(f"Error reading from I2C device: {e}")
        time.sleep(1)  # Read every second

read_data()
