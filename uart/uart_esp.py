from machine import UART, Pin
import time

# Configuración UART en el ESP32
uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(16))  # TX=17, RX=16 en el ESP32
# Led interno en el ESP32
led = Pin(2, Pin.OUT)

while True:
    if uart.any():  # Si hay datos disponibles para leer
        message = uart.readline().decode().strip()
        print(f"Mensaje recibido de la Raspberry Pi: {message}")
        
        led.on()
        
        response = "Hola Pi"
        uart.write(response)
        print(f"Mensaje enviado: {response}")
        time.sleep(1)
      
        led.off()
    time.sleep(0.1)
