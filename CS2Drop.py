import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import winsound
from datetime import datetime

# Configuración de estilo
BG_COLOR = "#2c3e50"
FG_COLOR = "#ecf0f1"
BUTTON_COLOR = "#3498db"
HOVER_COLOR = "#2980b9"
FONT = ("Arial", 10)

# Diccionario de probabilidades base
base_probabilidades = {
    "Recoil Case (cs3)": 33.0,
    "Fracture Case (cs5)": 26.4,
    "Revolution Case (cs2)": 19.8,
    "Kilowatt Case (cs1)": 13.2,
    "Dreams & Nightmares Case (cs4)": 6.6,
    "Otras (27 cajas)": 1.0,
}

otras_cajas = [
    "Snakebite Case (cs6)",
    "Prisma 2 Case (cs7)",
    "CS20 Case (cs8)",
    "Prisma Case (cs9)",
    "Danger Zone Case (cs10)",
    "Horizon Case (cs11)",
    "Clutch Case (cs12)",
    "Spectrum 2 Case (cs13)",
    "Operation Hydra Case (cs14)",
    "Spectrum Case (cs15)",
    "Glove Case (cs16)",
    "Gamma 2 Case (cs17)",
    "Gamma Case (cs18)",
    "Chroma 3 Case (cs19)",
    "Operation Wildfire Case (cs20)",
    "Revolver Case (cs21)",
    "Shadow Case (cs22)",
    "Falchion Case (cs23)",
    "Chroma 2 Case (cs24)",
    "Chroma Case (cs25)",
    "Operation Vanguard Weapon Case (cs26)",
    "Operation Breakout Weapon Case (cs27)",
    "Huntsman Weapon Case (cs28)",
    "Operation Phoenix Weapon Case (cs29)",
    "CS:GO Weapon Case 3 (cs30)",
    "Winter Offensive Weapon Case (cs31)",
    "CS:GO Weapon Case 2 (cs32)",
    "Operation Bravo Case (cs33)",
    "CS:GO Weapon Case (cs34)"
]

caja_imagenes = {f"cs{i}": f"cs{i}.png" for i in range(1, 35)}

# Variables globales para el historial
historial = []

def ajustar_probabilidades(puntos):
    if puntos < 4000:
        return {
            "Recoil Case (cs3)": 19.8,
            "Fracture Case (cs5)": 19.8,
            "Revolution Case (cs2)": 19.8,
            "Kilowatt Case (cs1)": 19.8,
            "Dreams & Nightmares Case (cs4)": 19.8,
            "Otras (27 cajas)": 1.0,
        }

    factor = puntos / 4000
    nuevas_prob = {k: v * factor for k, v in base_probabilidades.items()}

    while True:
        suma_total = sum(nuevas_prob.values())
        if suma_total <= 100:
            break

        mayor_key, mayor_valor = max(nuevas_prob.items(), key=lambda x: x[1])
        suma_otros = suma_total - mayor_valor
        espacio_disponible = 100 - suma_otros

        if espacio_disponible <= 1:
            nuevas_prob[mayor_key] = 0.0
        else:
            nuevas_prob[mayor_key] = espacio_disponible

    return nuevas_prob

def elegir_caja(probabilidades):
    items = []
    pesos = []
    for caja, prob in probabilidades.items():
        if caja == "Otras (27 cajas)":
            for otra in otras_cajas:
                items.append(otra)
                pesos.append(prob / 27.0)
        else:
            items.append(caja)
            pesos.append(prob)

    return random.choices(items, weights=pesos, k=1)[0]

def evaluar_item_extra(puntos):
    prob = (puntos / 4000) * 2.0
    prob = min(prob, 100.0)
    resultado = random.uniform(0, 100) < prob
    if resultado:
        try:
            winsound.Beep(1000, 300)  # Sonido al ganar item extra
        except:
            pass
    return "Sí" if resultado else "No"

def cargar_imagen_de_caja(caja_nombre):
    if "(" in caja_nombre and ")" in caja_nombre:
        codigo = caja_nombre.split("(")[-1].strip(")")
        if codigo in caja_imagenes:
            ruta = caja_imagenes[codigo]
            try:
                img = Image.open(ruta).resize((200, 200))
                return ImageTk.PhotoImage(img)
            except:
                pass
    return None

def mostrar_historial():
    top = tk.Toplevel()
    top.title("Historial de Sorteos")
    top.geometry("500x400")
    top.configure(bg=BG_COLOR)
    
    # Frame para el historial
    hist_frame = tk.Frame(top, bg=BG_COLOR)
    hist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(hist_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Texto del historial con estilo
    historial_text = tk.Text(
        hist_frame, 
        yscrollcommand=scrollbar.set,
        bg="#34495e",
        fg=FG_COLOR,
        font=FONT,
        padx=10,
        pady=10,
        wrap=tk.WORD
    )
    historial_text.pack(fill=tk.BOTH, expand=True)
    
    # Insertar historial
    if not historial:
        historial_text.insert(tk.END, "No hay registros en el historial")
    else:
        for item in reversed(historial):
            historial_text.insert(tk.END, f"{item}\n{'='*50}\n")
    
    scrollbar.config(command=historial_text.yview)
    
    # Botón para cerrar
    close_btn = ttk.Button(
        top, 
        text="Cerrar", 
        command=top.destroy,
        style="TButton"
    )
    close_btn.pack(pady=5)

def ejecutar_sorteo():
    try:
        puntos = int(entry_puntos.get())
        if puntos <= 0:
            raise ValueError
        
        prob_actuales = ajustar_probabilidades(puntos)
        caja = elegir_caja(prob_actuales)
        item_extra = evaluar_item_extra(puntos)

        resultado_caja.set(f"Caja obtenida: {caja}")
        resultado_extra.set(f"Item Extra: {item_extra}")
        
        # Cambiar color según si hay item extra
        label_extra.config(fg="#2ecc71" if item_extra == "Sí" else "#e74c3c")

        imagen = cargar_imagen_de_caja(caja)
        if imagen:
            label_imagen.config(image=imagen)
            label_imagen.image = imagen
        else:
            label_imagen.config(image="", text="Imagen no disponible")

        # Agregar al historial
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historial.append(f"{timestamp}\nPuntos usados: {puntos}\nCaja: {caja}\nItem Extra: {item_extra}")

    except ValueError:
        resultado_caja.set("Error: Ingresa un número válido (mayor que 0)")
        resultado_extra.set("")
        label_imagen.config(image="", text="Error")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("CS2 Case Simulator")
ventana.geometry("500x600")
ventana.configure(bg=BG_COLOR)
ventana.resizable(False, False)

# Estilo para los botones
style = ttk.Style()
style.configure("TButton", 
                font=FONT,
                background=BUTTON_COLOR,
                foreground=FG_COLOR)
style.map("TButton",
          background=[('active', HOVER_COLOR)])

# Frame principal
main_frame = tk.Frame(ventana, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Título
title_label = tk.Label(
    main_frame,
    text="CS2 Case Simulator",
    font=("Arial", 18, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
)
title_label.pack(pady=(0, 20))

# Frame de entrada
input_frame = tk.Frame(main_frame, bg=BG_COLOR)
input_frame.pack(fill=tk.X, pady=10)

tk.Label(
    input_frame,
    text="Puntos disponibles:",
    font=FONT,
    bg=BG_COLOR,
    fg=FG_COLOR
).pack(side=tk.LEFT)

entry_puntos = ttk.Entry(input_frame, font=FONT, width=10)
entry_puntos.pack(side=tk.LEFT, padx=10)

# Frame de botones
button_frame = tk.Frame(main_frame, bg=BG_COLOR)
button_frame.pack(pady=15)

ttk.Button(
    button_frame,
    text="Realizar Sorteo",
    command=ejecutar_sorteo,
    style="TButton"
).pack(side=tk.LEFT, padx=5)

ttk.Button(
    button_frame,
    text="Ver Historial",
    command=mostrar_historial,
    style="TButton"
).pack(side=tk.LEFT, padx=5)

# Frame de resultados
result_frame = tk.Frame(main_frame, bg=BG_COLOR)
result_frame.pack(fill=tk.X, pady=10)

resultado_caja = tk.StringVar()
resultado_extra = tk.StringVar()

label_caja = tk.Label(
    result_frame,
    textvariable=resultado_caja,
    font=("Arial", 12, "bold"),
    bg=BG_COLOR,
    fg="#f39c12",
    wraplength=400
)
label_caja.pack()

label_extra = tk.Label(
    result_frame,
    textvariable=resultado_extra,
    font=("Arial", 12, "bold"),
    bg=BG_COLOR,
    wraplength=400
)
label_extra.pack(pady=5)

# Imagen de la caja
label_imagen = tk.Label(
    main_frame,
    bg=BG_COLOR,
    fg=FG_COLOR,
    text="Esperando sorteo...",
    font=FONT
)
label_imagen.pack(pady=20)

# Footer
footer_label = tk.Label(
    main_frame,
    text="Holaaaaa",
    font=("Arial", 8),
    bg=BG_COLOR,
    fg="#7f8c8d"
)
footer_label.pack(side=tk.BOTTOM, pady=(20, 0))

ventana.mainloop()