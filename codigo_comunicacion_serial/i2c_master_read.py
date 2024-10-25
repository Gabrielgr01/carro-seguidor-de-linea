import smbus
import time

bus = smbus.SMBus(1)
esp32_address = 0x08

def read_data():
    while True:
        try:
            data = bus.read_byte(esp32_address)
            print(f"Data received: {data}")
        except Exception as e:
            print(f"Error reading from I2C device: {e}")
        time.sleep(1)

read_data()
