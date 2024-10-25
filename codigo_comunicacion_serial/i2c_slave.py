from machine import I2C, Pin
import time

# SDA pin 21, SCL pin 22
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

raspberry_pi_address = 0x8 

# Configuración LED
led = Pin(2, Pin.OUT)

while True:
    try:
        data = bytearray([0x42])
        led.value(1)
        i2c.writeto(raspberry_pi_address, data)
        #print("Data sent:", data)
        time.sleep(1)
        led.value(0)
        time.sleep(1) 
    except Exception as e:
        print("Error:", e)
        led.value(0)
        time.sleep(1)
