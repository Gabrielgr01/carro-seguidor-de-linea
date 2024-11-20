import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import serial
import time

######################
# Variables Globales #
######################

mensaje_titulo = "INFO:"
mensaje_texto = "Asigne los colores e inicie el programa."

# Configuración UART en la Raspberry Pi
uart = serial.Serial(
    port="/dev/serial0",  # Revisar en raspberry con "ls -l /dev"
    baudrate=9600,
    timeout=1
)

#############
# Funciones #
#############

def send_message(message):
    uart.write(message.encode())
    print(f"Mensaje enviado: {message}")

def read_message():
    if uart.in_waiting > 0:  # Si hay datos en el búfer de entrada
        message = uart.readline().decode().strip()
        print(f"Mensaje recibido: {message}")
        return message
    return None

# Función para actualizar el mensaje basado en la asignación de color
def actualizar_mensaje(event=None):
    global mensaje
    if (combo_frenar.get() == combo_retroceso.get() or
        combo_frenar.get() == combo_delta_v.get() or
        combo_retroceso.get() == combo_delta_v.get()):
        mensaje_titulo = "ADVERTENCIA:"
        mensaje_texto = "Debe de elegir colores diferentes para la Asignación De Color."
    else:
        mensaje_titulo = "INFO:"
        mensaje_texto = "Asigne los colores e inicie el programa."
    label_mensaje_titulo.config(text=mensaje_titulo)
    label_mensaje_texto.config(text=mensaje_texto)

def enviar_datos():
    datos_a_enviar = "Hola ESP32"  # Configurar para que envíe los datos que necesita el ESP32
    send_message(datos_a_enviar) 
    time.sleep(0.2)
    datos_recibidos = ""
    datos_recibidos = read_message()  # Puede que haga falta hacerle algún procesamiento para interpretarlos datos recibidos
    if datos_recibidos:
        mensaje_titulo = "INFO"
        mensaje_texto = f"Datos enviados correctamente.\nRespuesta: {datos_recibidos}"
    else:
        mensaje_titulo = "ADVERTENCIA"
        mensaje_texto = "Error en el envío de datos. No hubo respuesta.\nProcure que el carrito esté detenido."
    label_mensaje_titulo.config(text=mensaje_titulo)
    label_mensaje_texto.config(text=mensaje_texto.strip())  # Usar .strip() para eliminar espacios
    time.sleep(0.2)
    uart.close()

def fin():
    print("Final")

###########################
# Configuración de la GUI #
###########################

window = tk.Tk()
window.title('Proyecto Final GUI')
height = 475
width = 800
x = window.winfo_screenwidth()//2 - width//2
y = window.winfo_screenheight()//2 - height//2
window.geometry(f'{width}x{height}+{x}+{y}')
# window.resizable(False, False)
window.configure(bg='#191919')

window.columnconfigure(0, weight = 1)
window.columnconfigure(1, weight = 1)
window.rowconfigure(0, weight = 1)
window.rowconfigure(1, weight = 1)

up_color = '#303030'

#Frame for the "Inicio" and "Fin" buttons.
frame_fi = tk.Frame(window, bg='#191919')
frame_fi.grid(row = 1, column = 1, sticky="se", padx = 30, pady = 30)

button_inicio = tk.Button(frame_fi, text = "Enviar Datos", bg = '#30b348', fg = 'white', font = ('Arial', 14, 'bold'), command=enviar_datos)
button_inicio.grid(row = 0, column = 0, padx = 10, sticky = "se")

#button_fin = tk.Button(frame_fi, text = "Fin", bg = '#c23636', fg = 'white', font = ('Arial', 14, 'bold'), command=fin)
#button_fin.grid(row = 0, column = 1, sticky = "se")

#Frame for the color seleciton
combo_values = ['Rojo','Azul','Verde']
frame_selcol = tk.Frame(window, bg = up_color)
frame_selcol.grid(row = 0, column = 0, padx = 30, pady = 30, sticky = 'ew')
frame_selcol.columnconfigure(0, weight = 1)

selcol_label = tk.Label(frame_selcol, text = "Asignación De Color", bg = up_color, fg = 'white', font = ('Arial', 14, 'bold'))
selcol_label.grid(row = 0, column = 0, sticky = 'ew', pady = 20)

label_frenar = tk.Label(frame_selcol, text="Frenar", font=("Arial", 12, 'bold'), fg='white', bg=up_color)
label_frenar.grid(row=1, column=0, padx=10, pady=5, sticky='w')

combo_frenar = ttk.Combobox(frame_selcol, values = combo_values)
combo_frenar.grid(row=2, column=0, padx=10, pady=5, sticky = 'ew')
combo_frenar.current(0)

label_retroceso = tk.Label(frame_selcol, text="Retroceso", font=("Arial", 12, 'bold'), fg='white', bg=up_color)
label_retroceso.grid(row=3, column=0, padx=10, pady=5, sticky='w')

combo_retroceso = ttk.Combobox(frame_selcol, values = combo_values)
combo_retroceso.grid(row=4, column=0, padx=10, pady=5, sticky = 'ew')
combo_retroceso.current(1)

label_delta_v = tk.Label(frame_selcol, text="Δ Velocidad", font=("Arial", 12,'bold'), fg='white', bg=up_color)
label_delta_v.grid(row=5, column=0, padx=10, pady=5, sticky='w')

combo_delta_v = ttk.Combobox(frame_selcol, values = combo_values)
combo_delta_v.grid(row=6, column=0, padx=10, pady=(5,30), sticky = 'ew')
combo_delta_v.current(2)

# Frame for "Conteo de Colores"
frame_colcnt = tk.Frame(window, bg=up_color)
frame_colcnt.grid(row=0, column=1, padx=30, pady=30, sticky = 'ew')
frame_colcnt.columnconfigure(0, weight = 1)

label_conteo = tk.Label(frame_colcnt, text="Conteo de Colores", font=("Arial", 14, 'bold'), fg='white', bg=up_color)
label_conteo.grid(row=0, column=0, padx=10, pady=15)

# Create a pie chart using matplotlib
figure = plt.Figure(figsize=(3, 3), dpi=80)
figure.patch.set_facecolor(up_color)
ax = figure.add_subplot(111)
label_config = {'color': 'white', 'fontsize': 13, 'fontweight': 'bold', 'fontname': 'Arial'}
data = [50, 25, 10]
colors = ['tomato', 'lightgreen', 'skyblue']
labels = ['50', '25', '10']
ax.pie(data, colors = colors, labels = labels, textprops = label_config)
ax.set_aspect('equal')
 
# Add the pie chart to the tkinter window
canvas = FigureCanvasTkAgg(figure, frame_colcnt)
canvas.get_tk_widget().grid(row=1, column=0)

# Frame para mensaje 
frame_mensaje = tk.Frame(window, bg=up_color)
frame_mensaje.grid(row=1, column=0, padx=30, pady=(10, 30), sticky = 'ew')
frame_mensaje.columnconfigure(0, weight = 1)

label_mensaje_titulo = tk.Label(frame_mensaje, text = mensaje_titulo, bg = up_color, fg = 'white', font = ('Arial', 12, 'bold'))
label_mensaje_titulo.grid(row = 0, column = 0, sticky = 'nw', padx = 10, pady=(10, 5))

label_mensaje_texto = tk.Label(frame_mensaje, text = mensaje_texto, bg = up_color, fg = 'white', font = ('Arial', 10))
label_mensaje_texto.grid(row = 1, column = 0, sticky = 'nw', padx = 10, pady=(5, 15))

# Enlaza los comboboxes al evento de cambio de selección
combo_frenar.bind("<<ComboboxSelected>>", actualizar_mensaje)
combo_retroceso.bind("<<ComboboxSelected>>", actualizar_mensaje)
combo_delta_v.bind("<<ComboboxSelected>>", actualizar_mensaje)

###################
# Bucle Principal #
###################
window.mainloop()
