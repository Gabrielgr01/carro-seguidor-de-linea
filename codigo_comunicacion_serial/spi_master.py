import spidev
import time

# Inicializar SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Abrir bus SPI 0, dispositivo (CS) 0
spi.max_speed_hz = 100000  # Configurar velocidad de SPI
spi.mode = 0  # Configurar CPOL y CPHA (polarity = 0, phase = 0)

def send_data(data):
    spi.xfer2(data)

def read_data(length):
    # Leer 'length' bytes del esclavo
    return spi.readbytes(length)

try:
    while True:
        # Mensaje a enviar como lista de bytes
        #message = [0x01, 0x02, 0x03]
        message = b'\x01\x02\x03'
        #message = bytearray([0x01, 0x02, 0x03])
        print(f"Enviando: {message}")
        send_data(message)

        time.sleep(0.01)
        response = read_data(3)
        print(f"Respuesta del esclavo: {response}")

        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
    print("SPI cerrado")
