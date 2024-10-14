import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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

button_inicio = tk.Button(frame_fi, text = "Inicio", bg = '#30b348', fg = 'white', font = ('Arial', 14, 'bold'))
button_inicio.grid(row = 0, column = 0, padx = 10, sticky = "se")

button_fin = tk.Button(frame_fi, text = "Fin", bg = '#c23636', fg = 'white', font = ('Arial', 14, 'bold'))
button_fin.grid(row = 0, column = 1, sticky = "se")

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

window.mainloop()