from machine import UART, Pin, time_pulse_us, PWM, ADC
import time

######################
# Variables Globales #
######################
global start_flag
global irq_pin
global dict_colores_funciones
global threshold
global velocidad_base
global bifur_sel

start_flag = 0
threshold = 900  # Menos de 900 es blanco, más de 900 es negro
velocidad_base = 500  # Velocidad base de los motores

# Selector de la dirección de viraje cuando se da una bifurcación
# 0 --> derecha
# 1 --> izquierda
bifur_sel = 0

dict_colores_funciones = {
    # Diccionario temporal. Luego tiene que definirse de los datos recibidos de la interfaz
    "Seguir linea":"Negro",
    "":"Blanco",
    "Frenar":"Rojo",
    "Retroceder":"Verde",
    "Delta_v":"Azul"
}


###########################
# Inicialización de Pines #
###########################
### Pines Inicio (interrupción)
start_pin = Pin(25, Pin.IN)
### Pines Comunicacion UART ###
uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(16))  # Tx en pin 17 y Rx en pin 16
led = Pin(2, Pin.OUT)
### Pines sensor de color ###
S0 = Pin(2, Pin.OUT) 
S1 = Pin(15, Pin.OUT)
S2 = Pin(12, Pin.OUT)
S3 = Pin(14, Pin.OUT)
OUT = Pin(13, Pin.IN)
S0.value(0)  # Alta frecuencia
S1.value(1)
### Pines Motores ###
in1 = Pin(19, Pin.OUT)  # Pin para IN1 del Motor A (L298)
in2 = Pin(18, Pin.OUT)  # Pin para IN2 del Motor A (L298)
ena = PWM(Pin(5), freq=2000)  # Pin para ENA del Motor A (PWM)
in3 = Pin(22, Pin.OUT)  # Pin para IN3 del Motor B
in4 = Pin(23, Pin.OUT)  # Pin para IN4 del Motor B
enb = PWM(Pin(21), freq=2000)  # Pin para ENB del Motor B (PWM)
### Pines Sensores infrarrojos ANALÓGICOS ###
IR_derecha = ADC(Pin(32))  
IR_izquierda = ADC(Pin(35))
IR_derecha.atten(ADC.ATTN_11DB)   # Rango completo de 0 a 3.3V
IR_izquierda.atten(ADC.ATTN_11DB) # Rango completo de 0 a 3.3V

#############
# Funciones #
#############

### Función para controlar la dirección y velocidad del Motor A ###
def motor_a(direccion, velocidad):
    if direccion == "adelante":
        in1.off()
        in2.on()
    elif direccion == "atras":
        in1.on()
        in2.off()
    else:
        in1.off()
        in2.off()
    
    ena.duty(velocidad)

### Función para controlar la dirección y velocidad del Motor B ###
def motor_b(direccion, velocidad):
    if direccion == "adelante":
        in3.on()
        in4.off()
    elif direccion == "atras":
        in3.off()
        in4.on()
    else:
        in3.off()
        in4.off()
    
    enb.duty(velocidad)

### Función para detener ambos motores ###
def detener_motores():
    motor_a("detener", 0)
    motor_b("detener", 0)

### Función para seguir la lógica de movimiento ###
def seguir_linea():
    sensorR = IR_derecha.read()
    sensorL = IR_izquierda.read()
    viraje = ""

    print(f"Sensor Derecho: {sensorR}, Izquierdo: {sensorL}")

    # Si ambos sensores están en blanco, avanzar en línea recta
    if sensorL < threshold and sensorR < threshold:
        print("Línea centrada. Avanzando recto.")
        motor_a("adelante", velocidad_base)
        motor_b("adelante", velocidad_base)
    
    # Si el sensor izquierdo detecta negro y el derecho blanco, corregir hacia la izquierda
    elif (sensorL > threshold) and (sensorR < threshold):
        print("Corrigiendo hacia la izquierda.")
        motor_a("adelante", 0)  # Detener motor izquierdo
        motor_b("adelante", velocidad_base)
        time.sleep(0.1)  # Pausa para corrección
    
    # Si el sensor derecho detecta negro y el izquierdo blanco, corregir hacia la derecha
    elif (sensorR > threshold) and (sensorL < threshold):
        print("Corrigiendo hacia la derecha.")
        motor_a("adelante", velocidad_base)
        motor_b("adelante", 0)  # Detener motor derecho
        time.sleep(0.1)  # Pausa para corrección

    # Manejo de la bifurcación
    # Si ambos sensores detectan negro se gira en una dirección seleccionada 
    # con la variable global bifur_sel
    elif (sensorR > threshold) and (sensorL > threshold):
        
        if (bifur_sel == 0):
            viraje = "derecha"
            motor_a("adelante", velocidad_base)
            motor_b("adelante", 0) 

        elif (bifur_sel ==1):
            viraje = "izquierda"
            motor_a("adelante", 0)
            motor_b("adelante", velocidad_base)
        
        print(f"Bifurcación detectada, corrigiendo hacia la {viraje}")

def retroceder():
    print("Ejecutando Retroceder")

def cambiar_velocidad():
    print("Ejecutando Cambio Velocidad")

### Función para medir la frecuencia ###
def read_frequency(color_filter):
    # Configuración del filtro de color (S2 y S3)
    S2.value(color_filter[0])
    S3.value(color_filter[1])
    time.sleep(0.1)  # Pequeña pausa para estabilizar
    pulse_time = time_pulse_us(OUT, 1, 1000000)  # Tiempo de pulso en microsegundos
    if pulse_time < 0:
        return 0  # Error de lectura
    return 1000000 // pulse_time  # Convertir a frecuencia en Hz

### Función para detectar color dominante ###
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
    
### Función para ejecutar la maniobra del carrito ###
def ejecutar_maniobra (color):
    global dict_colores_funciones
    funcion = dict_colores_funciones[color]
    if funcion == "Seguir linea":
        seguir_linea()
    elif funcion == "Frenar":
        detener_motores()
    elif funcion == "Retroceder":
        retroceder()
    elif funcion == "Cambiar velocidad":
        cambiar_velocidad()
        
    # ... agregar maniobra para el color Blanco

### Función para manejar la interrución de start ###
def handle_start(pin):
    global start_flag
    start_flag = not start_flag
    global irq_pin
    irq_pin = int(str(pin)[4:-1])
    

### Función para interpretar el mensaje UART
def interpretar_mensaje_UART(message):
    global dict_colores_funciones
    
    lista_datos = message.split(" ")
    size_list = len(lista_datos)
    print(size_list)
    if size_list == 1:
        if lista_datos[0] == "Inicio":
            #ejecutar funcion inicio
            print("encender motores")
        elif lista_datos[0] == "Fin":
            #ejecutar funcion de apagar motores
            print("apagar motores")
    elif size_list > 1:
        color_frenar = lista_datos[0]
        color_retroceder = lista_datos[1]
        color_delta_v = lista_datos[2]
        print (color_frenar)
        print (color_retroceder)
        print (color_delta_v)
        dict_colores_funciones = {
            "Seguir linea":"Negro",
            "Corregir_linea":"Blanco",
            "Frenar":color_frenar,
            "Retroceder":color_retroceder,
            "Delta_v":color_delta_v
        }

####################################
# Configuracion de la interrupción #
####################################
start_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_start)

###################
# Bucle principal #
###################
while True:
  
    #start_flag = 1 # BORRAR ESTA LINEA PARA HABILITAR INTERRUPCION
    
    if start_flag == 1:
        led.on()
        color = detect_color()
        print(f"Color detectado: {color}")
        ejecutar_maniobra(color)
        
        time.sleep(0.1)
    else:
        led.off()

        if uart.any():  # Si hay datos disponibles para leer
            message = uart.readline().decode().strip() # Hay que ver como interpretar este mensaje
            # Hay que definir un diccionario que relacione cada color con su función
            # Ejemplo: Rojo -> Frenar, Azul -> Retroceder
            print(f"Mensaje recibido de la Raspberry Pi: {message}")
            
            response = "Hola Pi\n"
            uart.write(response)
            print(f"Mensaje enviado: {response}")
            
            interpretar_mensaje_UART(message)
            print(dict_colores_funciones)
            
            time.sleep(1)
        time.sleep(0.5)

