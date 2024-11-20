from machine import UART, Pin, time_pulse_us
import time

global start_flag
global irq_pin
global dict_colores_funciones

start_flag = 0

uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(16))  # TX=17, RX=16 en el ESP32
led = Pin(2, Pin.OUT)
start_pin = Pin(25, Pin.IN)

# Pines de conexión
S0 = Pin(16, Pin.OUT) 
S1 = Pin(15, Pin.OUT)
S2 = Pin(12, Pin.OUT)
S3 = Pin(14, Pin.OUT)
OUT = Pin(13, Pin.IN)

# Configuración de frecuencia (S0 y S1)
S0.value(0)  # Alta frecuencia
S1.value(1)

# Función para medir la frecuencia
def read_frequency(color_filter):
    # Configuración del filtro de color (S2 y S3)
    S2.value(color_filter[0])
    S3.value(color_filter[1])
    time.sleep(0.1)  # Pequeña pausa para estabilizar
    pulse_time = time_pulse_us(OUT, 1, 1000000)  # Tiempo de pulso en microsegundos
    if pulse_time < 0:
        return 0  # Error de lectura
    return 1000000 // pulse_time  # Convertir a frecuencia en Hz

# Detectar color dominante
def detect_color():
    red = read_frequency((0, 0))
    green = read_frequency((1, 1))
    blue = read_frequency((0, 1))
    
    print(f"R: {red}, G: {green}, B: {blue}")
    
    # Umbrales para distinguir colores
    if red > green and red > blue:
        return "Rojo"
    elif green > red and green > blue:
        return "Verde"
    elif blue > red and blue > green:
        return "Azul"
    elif red < 50 and green < 50 and blue < 50:
        return "Negro"
    else:
        return "Blanco"

def detect_black():
    black = read_frequency((1, 0))
    umbral = 50
    if black < umbral:
        return True
    elif black > umbral:
        return False

def frenar():
    print("Ejecutando Frenar")

def retroceder():
    print("Ejecutando Retroceder")

def cambio_velocidad():
    print("Ejecutando Cambio Velocidad")

def ejecutar_funcion (color):
    global dict_colores_funciones
    funcion = dict_colores_funciones[color] 
    if funcion == "Frenar":
        frenar()
    elif funcion == "Retroceder":
        retroceder()

def handle_start(pin):
    global start_pin
    start_pin = not start_pin
    global irq_pin
    irq_pin = int(str(pin)[4:-1])

# Configuracion de la interrupción
start_pin.irq(trigger=Pin.IRQ_RAISING, handler=handle_start)

# Bucle principal
while True:
    
    if start_flag == 1:
        led.on()
        color = detect_color()
        print(f"Color detectado: {color}")
        ejecutar_funcion(color)
        
        time.sleep(1)
    else:
        # Esto se ejecuta cuando no se ha iniciado el carrito (botón de start del pin 25)
        # Se realiza la configuración inicial con los datos leídos de la interfaz
        
        led.off()

        if uart.any():  # Si hay datos disponibles para leer
            message = uart.readline().decode().strip() # Hay que ver como interpretar este mensaje
            # Hay que definir un diccionario que relacione cada color con su función
            # Ejemplo: Rojo -> Frenar, Azul -> Retroceder
            print(f"Mensaje recibido de la Raspberry Pi: {message}")
        
            response = "Hola Pi"
            uart.write(response)
            print(f"Mensaje enviado: {response}")
        time.sleep(1)
