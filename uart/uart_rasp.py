import serial
import time

# Configuración UART en la Raspberry Pi
uart = serial.Serial(
    port="/dev/serial0",  # Revisar en raspberry con "ls -l /dev"
    baudrate=9600,
    timeout=1
)

def send_message(message):
    uart.write(message.encode())
    print(f"Mensaje enviado: {message}")

def read_message():
    if uart.in_waiting > 0:  # Si hay datos en el búfer de entrada
        message = uart.readline().decode().strip()
        print(f"Mensaje recibido: {message}")
        return message
    return None

try:
    while True:
        send_message("Hola ESP32")
        time.sleep(1)
        received = read_message()
        #if received:
        #    print(f"ESP32 dijo: {received}")
        time.sleep(1)
except KeyboardInterrupt:
    uart.close()
    print("Comunicación UART cerrada")
