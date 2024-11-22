from machine import UART, Pin, time_pulse_us, PWM, ADC # type: ignore
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
    "Negro":"Seguir Linea",
    "Blanco":"Corregir Linea",
    "Rojo":"Frenar",
    "Verde":"Retroceder",
    "Azul":"Delta_v"
}


###########################
# Inicialización de Pines #
###########################
### Pines Inicio (interrupción) ###
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
in1 = Pin(19, Pin.OUT)  # Pin para IN1 del Motor A (usando el L298)
in2 = Pin(18, Pin.OUT)  # Pin para IN2 del Motor A (usando el L298)
ena = PWM(Pin(5), freq=2000)  # Pin para ENA del Motor A (PWM)
in3 = Pin(22, Pin.OUT)  # Pin para IN3 del Motor B
in4 = Pin(23, Pin.OUT)  # Pin para IN4 del Motor B
enb = PWM(Pin(21), freq=2000)  # Pin para ENB del Motor B (PWM)
### Pines Sensores infrarrojos ANALÓGICOS ###
IR_derecha = ADC(Pin(32))  
IR_izquierda = ADC(Pin(35)) 
IR_derecha.atten(ADC.ATTN_11DB)   # Rango completo de 0 a 3.3V
IR_izquierda.atten(ADC.ATTN_11DB) # Rango completo de 0 a 3.3V
### Variables de control ###
threshold = 900  # Menos de 900 es blanco, más de 900 es negro
velocidad_base = 550  # Velocidad base de los motores
velocidad_inicial = 550 # Velocidad inicial para el arranque

#############
# Funciones #
#############

### Función para controlar la dirección y velocidad del Motor A ###
# El motor A es el izquierdo
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
# El motor B es el derecho
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
def seguir_linea(dir):
    sensorR = IR_derecha.read()
    sensorL = IR_izquierda.read()

    #print(f"Sensor Derecho: {sensorR}, Izquierdo: {sensorL}")

    # Si ambos sensores están en blanco, avanzar en línea recta
    if sensorL < threshold and sensorR < threshold:
        motor_a(dir , velocidad_base)
        motor_b(dir , velocidad_base)
    
    # Si el sensor izquierdo detecta negro, corregir hacia la izquierda
    elif (sensorL > threshold) and (sensorR < threshold):
        motor_a(dir , 0)  # Detener motor izquierdo
        motor_b(dir , velocidad_base)
    
    # Si el sensor derecho detecta negro, corregir hacia la derecha
    elif (sensorR > threshold) and (sensorL < threshold):
        motor_a(dir , velocidad_base)
        motor_b(dir , 0)  # Detener motor derecho

    # Manejo de la bifurcación
    # Si ambos sensores detectan negro se gira en una dirección seleccionada 
    # con la variable global bifur_sel
    elif (sensorR > threshold) and (sensorL > threshold):
        
        if (bifur_sel == 0):
            motor_a(dir , velocidad_base)
            motor_b(dir , 0) 

        elif (bifur_sel == 1):
            motor_a(dir , 0)
            motor_b(dir , velocidad_base)

def arranque():
    motor_a("adelante", velocidad_inicial)
    motor_b("adelante", velocidad_inicial)
    time.sleep(0.2)

def retroceso():
    seguir_linea("atras")
    time.sleep(3)

def cambiar_velocidad():
    print("Ejecutando Cambio Velocidad")

### Función para medir la frecuencia ###
def read_frequency(color_filter):
    # Configuración del filtro de color (S2 y S3)
    S2.value(color_filter[0])
    S3.value(color_filter[1])
    time.sleep(0.05)  # Pequeña pausa para estabilizar 0.05 mejor valor hasta ahora
    pulse_time = time_pulse_us(OUT, 1, 10000)  # Tiempo de pulso en microsegundos
    if pulse_time <= 0:
        return 0  # Error de lectura
    return 10000 // pulse_time  # Convertir a frecuencia en Hz

### Función para detectar color dominante ###
def detect_single_color():
    red = read_frequency((0, 0))
    green = read_frequency((1, 1))
    blue = read_frequency((0, 1))
    print(f"R: {red}, G: {green}, B: {blue}")
    
    # Criterios para detectar colores
    if red < 40 and green < 40 and blue < 40:
        return "Negro"
    elif red > 50 and green > 50 and blue > 50:
        return "Blanco"
    elif red > green and red > blue:
        return "Rojo"
    elif green > red and green > blue:
        return "Verde"
    elif blue > red and blue > green:
        return "Azul"
    else:
        return "Desconocido"

### Detectar color dominante en 10 mediciones ###
def detect_color():
    counts = {"Blanco": 0, "Rojo": 0, "Verde": 0, "Azul": 0, "Negro": 0}

    for _ in range(10):  # Realizar 10 mediciones
        color = detect_single_color()
        if color in counts:
            counts[color] += 1
        #time.sleep(0.1)  # Breve pausa entre mediciones

    # Determinar el color con más ocurrencias
    detected_color = max(counts, key=counts.get)
    print(f"Conteo de colores: {counts}")
    return detected_color

#def detect_black():
#    black = read_frequency((1, 0))
#    umbral = 50
#    if black < umbral:
#        return True
#    elif black > umbral:
#        return False
    
### Función para ejecutar la maniobra del carrito ###
def ejecutar_maniobra (color):
    global dict_colores_funciones
    funcion = dict_colores_funciones[color]
    if funcion == "Seguir linea":
        seguir_linea()
    elif funcion == "Frenar":
        detener_motores()
    elif funcion == "Retroceder":
        retroceso()
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
    global start_flag
    msg = ""

    lista_datos = message.split(" ")
    size_list = len(lista_datos)
    if size_list == 1:
        if lista_datos[0] == "Inicio":
            if start_flag == 0:
                msg = "-I- Ejecutando inicio"
                start_flag = 1

                print("encender motores") #ejecutar funcion inicio
        elif lista_datos[0] == "Fin":
            if start_flag == 1:
                msg = "-I- Ejecutando fin"
                start_flag = 0

                print("apagar motores") #ejecutar funcion de fin
    elif size_list > 1:
        if start_flag == 0:
            maniobra_rojo = lista_datos[0]
            maniobra_verde = lista_datos[1]
            maniobra_azul = lista_datos[2]
            dict_colores_funciones = {
                "Negro":"Seguir Linea",
                "Blanco":"Corregir Linea",
                "Rojo":maniobra_rojo,
                "Verde":maniobra_verde,
                "Azul":maniobra_azul
            }
            msg = "-I- Datos guardados correctamente"
        else:
            msg = "-E- El carrito está iniciado"
    return msg

####################################
# Configuracion de la interrupción #
####################################
start_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_start)

###################
# Bucle principal #
###################
while True:
    if uart.any():  # Si hay datos disponibles para leer
        mensaje = uart.readline().decode().strip()
        print(f"Mensaje recibido de la Raspberry Pi: {mensaje}")
        respuesta = interpretar_mensaje_UART(mensaje)
        uart.write(respuesta)
        print(f"Mensaje enviado al ESP32: {respuesta}")
         
        print(dict_colores_funciones)

    if start_flag == 1:
        led.on()
        print("-I- Carrito iniciado")
        
        arranque("adelante")
        time.sleep(0.08)  # Delay entre las actualizaciones
        detener_motores()
        time.sleep(0.1) # Delay entre las actualizaciones

        color = detect_color()
        print(f"Color detectado: {color}")
        #ejecutar_maniobra(color)
    else:
        detener_motores()

        led.off()

    time.sleep(0.5) # Sleep necesario para que le de tiempo al buffer de datos de recibir todos los bits     
