import tkinter as tk
from PIL import Image, ImageTk
import random
import winsound  # Para el sonido en Windows
from datetime import datetime

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

        # Encontrar el valor más alto y su clave
        mayor_key, mayor_valor = max(nuevas_prob.items(), key=lambda x: x[1])

        # Suma de los otros
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
                img = Image.open(ruta).resize((150, 150))
                return ImageTk.PhotoImage(img)
            except:
                pass
    return None


def mostrar_historial():
    top = tk.Toplevel()
    top.title("Historial de Sorteos")
    top.geometry("400x300")
    
    scrollbar = tk.Scrollbar(top)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    historial_text = tk.Text(top, yscrollcommand=scrollbar.set)
    historial_text.pack(fill=tk.BOTH, expand=True)
    
    for item in reversed(historial):
        historial_text.insert(tk.END, f"{item}\n\n")
    
    scrollbar.config(command=historial_text.yview)


def ejecutar_sorteo():
    try:
        puntos = int(entry_puntos.get())
        prob_actuales = ajustar_probabilidades(puntos)
        caja = elegir_caja(prob_actuales)
        item_extra = evaluar_item_extra(puntos)

        resultado_caja.set(f"Caja: {caja}")
        resultado_extra.set(f"Item Extra: {item_extra}")

        imagen = cargar_imagen_de_caja(caja)
        if imagen:
            label_imagen.config(image=imagen)
            label_imagen.image = imagen  # evitar recolección de basura
        else:
            label_imagen.config(image="", text="Sin imagen")

        # Agregar al historial
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historial.append(f"{timestamp}\nPuntos: {puntos}\nCaja: {caja}\nItem Extra: {item_extra}")

    except ValueError:
        resultado_caja.set("Error: Ingresa un número válido")
        resultado_extra.set("")
        label_imagen.config(image="", text="Error")


# GUI
ventana = tk.Tk()
ventana.title("Sorteo de Caja CS2")

# Frame principal para mejor organización
main_frame = tk.Frame(ventana)
main_frame.pack(padx=10, pady=10)

# Entrada de puntos
tk.Label(main_frame, text="Ingresa tus puntos:").pack()
entry_puntos = tk.Entry(main_frame)
entry_puntos.pack()

# Botones
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Sortear", command=ejecutar_sorteo).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Ver Historial", command=mostrar_historial).pack(side=tk.LEFT, padx=5)

# Resultados
resultado_caja = tk.StringVar()
resultado_extra = tk.StringVar()

tk.Label(main_frame, textvariable=resultado_caja, font=("Arial", 12)).pack(pady=5)
tk.Label(main_frame, textvariable=resultado_extra, font=("Arial", 12)).pack(pady=5)

# Imagen
label_imagen = tk.Label(main_frame)
label_imagen.pack(pady=10)

ventana.mainloop()