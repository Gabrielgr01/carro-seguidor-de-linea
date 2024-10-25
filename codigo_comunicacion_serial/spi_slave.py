import machine
import time

# Configuración SPI
spi = machine.SPI(1, baudrate=100000, polarity=0, phase=0, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
cs = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# Configuracion LED
led = machine.Pin(2, machine.Pin.OUT)
led.value(0)

def read_spi():
    cs.value(0)
    data = spi.read(3)
    cs.value(1)
    return data

def send_response():
    cs.value(0)
    spi.write(b'\x04\x05\x06')
    cs.value(1)

try:
    while True:
        received_data = read_spi()
        print(f"Datos recibidos OUT: {received_data}")
        if (received_data != b'\x00\x00\x00'):
            send_response()
            print("Respuesta enviada")
            print(f"Datos recibidos IN: {received_data}")

            led.value(1)        
            time.sleep(1)
            led.value(0) 
        time.sleep(1) 
except KeyboardInterrupt:
    print("Proceso terminado")
