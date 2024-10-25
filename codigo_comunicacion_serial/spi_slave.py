import machine
import time

# Configuración SPI
spi = machine.SPI(1, baudrate=100000, polarity=0, phase=0, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
cs = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# Configuracion LED
led = machine.Pin(2, machine.Pin.OUT)
led.value(0)

def read_spi():
    cs.value(0)  # Activar esclavo
    data = spi.read(3)  # Leer 3 bytes
    cs.value(1)  # Desactivar esclavo
    return data

def send_response():
    cs.value(0)  # Activar esclavo
    spi.write(b'\x04\x05\x06')  # Enviar respuesta de 3 bytes
    cs.value(1)  # Desactivar esclavo

try:
    while True:
        # Leer datos cuando el maestro envíe un mensaje
        received_data = read_spi()
        print(f"Datos recibidos OUT: {received_data}")
        if (received_data != b'\x00\x00\x00'):
            send_response()
            print("Respuesta enviada")
            print(f"Datos recibidos IN: {received_data}")

            led.value(1)  # Encender el LED          
            time.sleep(1)  # Pausa de 1 segundo
            led.value(0)  # Apagar el LED
        time.sleep(1)  # Pausa de 1 segundo
except KeyboardInterrupt:
    print("Proceso terminado")
