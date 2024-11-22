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
    if (combo_rojo.get() == combo_verde.get() or
        combo_rojo.get() == combo_azul.get() or
        combo_verde.get() == combo_azul.get()):
        mensaje_titulo = "ADVERTENCIA:"
        mensaje_texto = "-W- Asignación De Color: Debe de elegir valores distintos"
        button_guardar.config(state=tk.DISABLED)
    else:
        mensaje_titulo = "INFO:"
        mensaje_texto = "-I- Asigne los colores e inicie el programa."
        button_guardar.config(state=tk.NORMAL)
    label_mensaje_titulo.config(text=mensaje_titulo)
    label_mensaje_texto.config(text=mensaje_texto)

def inicio():
    print("INICIO")
    datos_a_enviar = "Inicio\n"
    enviar_datos(datos_a_enviar)

def fin():
    print("FIN")
    datos_a_enviar = "Fin\n"
    enviar_datos(datos_a_enviar)

def guardar():
    print("GUARDAR")
    maniobra_rojo = combo_rojo.get()
    maniobra_verde = combo_verde.get()
    maniobra_azul = combo_azul.get()
    datos_a_enviar = f"{maniobra_rojo} {maniobra_verde} {maniobra_azul}\n"
    enviar_datos(datos_a_enviar)

def enviar_datos(datos_a_enviar):
    try:
        send_message(datos_a_enviar)
        time.sleep(1)
        datos_recibidos = ""
        datos_recibidos = read_message()  # Puede que haga falta hacerle algún procesamiento para interpretarlos datos recibidos

        if datos_recibidos:
            mensaje_titulo = "INFO"
            mensaje_texto = f"-I- Datos enviados correctamente. Respuesta:\n{datos_recibidos}"
        else:
            mensaje_titulo = "ERROR"
            mensaje_texto = "-E- Error en el envío de datos. No hubo respuesta."
        label_mensaje_titulo.config(text=mensaje_titulo)
        label_mensaje_texto.config(text=mensaje_texto.strip())  # Usar .strip() para eliminar espacios
        time.sleep(1)
    except KeyboardInterrupt:
        uart.close()
        print("Comunicacion UART cerrada")

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

button_guardar = tk.Button(frame_fi, text = "Guardar", bg = '#30b348', fg = 'white', font = ('Arial', 14, 'bold'), command=guardar)
button_guardar.grid(row = 0, column = 0, padx = 10, sticky = "se")

button_inicio = tk.Button(frame_fi, text = "Inicio", bg = 'green', fg = 'white', font = ('Arial', 14, 'bold'), command=inicio)
button_inicio.grid(row = 0, column = 1, sticky = "se")

button_fin = tk.Button(frame_fi, text = "Fin", bg = '#c23636', fg = 'white', font = ('Arial', 14, 'bold'), command=fin)
button_fin.grid(row = 0, column = 2, sticky = "se")

#Frame for the color seleciton
#Δ_Velocidad
combo_values = ['Frenar','Retroceder','Cambiar Velocidad']
frame_selcol = tk.Frame(window, bg = up_color)
frame_selcol.grid(row = 0, column = 0, padx = 30, pady = 30, sticky = 'ew')
frame_selcol.columnconfigure(0, weight = 1)

selcol_label = tk.Label(frame_selcol, text = "Asignación De Color", bg = up_color, fg = 'white', font = ('Arial', 14, 'bold'))
selcol_label.grid(row = 0, column = 0, sticky = 'ew', pady = 20)

label_rojo = tk.Label(frame_selcol, text="Rojo", font=("Arial", 12, 'bold'), fg='white', bg=up_color)
label_rojo.grid(row=1, column=0, padx=10, pady=5, sticky='w')

combo_rojo = ttk.Combobox(frame_selcol, values = combo_values)
combo_rojo.grid(row=2, column=0, padx=10, pady=5, sticky = 'ew')
combo_rojo.current(0)

label_verde = tk.Label(frame_selcol, text="Verde", font=("Arial", 12, 'bold'), fg='white', bg=up_color)
label_verde.grid(row=3, column=0, padx=10, pady=5, sticky='w')

combo_verde = ttk.Combobox(frame_selcol, values = combo_values)
combo_verde.grid(row=4, column=0, padx=10, pady=5, sticky = 'ew')
combo_verde.current(1)

label_azul = tk.Label(frame_selcol, text="Azul", font=("Arial", 12,'bold'), fg='white', bg=up_color)
label_azul.grid(row=5, column=0, padx=10, pady=5, sticky='w')

combo_azul = ttk.Combobox(frame_selcol, values = combo_values)
combo_azul.grid(row=6, column=0, padx=10, pady=(5,30), sticky = 'ew')
combo_azul.current(2)

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
combo_rojo.bind("<<ComboboxSelected>>", actualizar_mensaje)
combo_verde.bind("<<ComboboxSelected>>", actualizar_mensaje)
combo_azul.bind("<<ComboboxSelected>>", actualizar_mensaje)

###################
# Bucle Principal #
###################
window.mainloop()
