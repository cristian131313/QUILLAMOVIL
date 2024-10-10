import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkintermapview  # Asegúrate de tener esta librería instalada

# Rutas de buses de Transmetro en Barranquilla
bus_routes = {
    "Ruta K54": [
        {"name": "", "coords": (10.97000, -74.78400)},
        {"name": "", "coords": (10.97200, -74.78600)},
        {"name": "", "coords": (10.97600, -74.79000)},
    ],
    "Ruta U30": [
        {"name": "", "coords": (11.018862892176148, -74.86420587457174)},
    ],
}

# Almacena los comentarios por ruta
comments = {route: [] for route in bus_routes.keys()}

# Noticias generales
news = [
    "La próxima semana se aumentará el pasaje en 300 pesos para todas las rutas.",
    "K54: Cambio de ruta de la 43 y 54.",
    "U30: Se espera una mejora en el servicio a partir de la próxima semana.",
]

# Función para mostrar la ruta en el mapa
def show_bus_route(route_name):
    # Elimina los marcadores existentes del mapa
    map_widget.delete_all_marker()
    
    if route_name in bus_routes:
        # Configura el mapa en la posición de la primera parada de la ruta seleccionada
        first_stop = bus_routes[route_name][0]['coords']
        map_widget.set_position(first_stop[0], first_stop[1])  # Posición de la primera parada
        map_widget.set_zoom(14)

        # Dibuja las paradas de la ruta seleccionada
        for stop in bus_routes[route_name]:
            map_widget.set_marker(stop['coords'][0], stop['coords'][1], text=stop['name'])

# Función para abrir la ventana de comentarios (chat)
def open_comments_window():
    comments_window = tk.Toplevel(root)
    comments_window.title("Chat de Comentarios")
    comments_window.geometry("500x500")

    # Seleccionar ruta de bus
    ttk.Label(comments_window, text="Seleccionar Ruta de Bus:").pack(pady=5)
    selected_route = tk.StringVar()
    route_combo = ttk.Combobox(comments_window, textvariable=selected_route, state="readonly")
    route_combo['values'] = list(bus_routes.keys())
    route_combo.pack(pady=5)

    # Crear área de chat (ScrollText) para mostrar los comentarios
    chat_display = scrolledtext.ScrolledText(comments_window, wrap=tk.WORD, height=15, width=50, state="disabled")
    chat_display.pack(pady=10)

    # Crear un campo de entrada para el nuevo comentario
    ttk.Label(comments_window, text="Agregar un comentario:").pack(pady=5)
    comment_entry = ttk.Entry(comments_window, width=50)
    comment_entry.pack(pady=5)

    # Función para actualizar los comentarios en el chat
    def update_chat():
        route_name = selected_route.get()
        if route_name:
            # Limpiar el chat display antes de actualizarlo
            chat_display.config(state="normal")
            chat_display.delete(1.0, tk.END)
            # Mostrar los comentarios de la ruta seleccionada
            for comment in comments[route_name]:
                chat_display.insert(tk.END, f"{comment}\n")
            chat_display.config(state="disabled")

    # Función para enviar el comentario
    def submit_comment():
        route_name = selected_route.get()
        new_comment = comment_entry.get().strip()

        if route_name and new_comment:
            comments[route_name].append(new_comment)  # Añadir comentario a la ruta seleccionada
            comment_entry.delete(0, tk.END)  # Limpiar el campo de entrada
            update_chat()  # Actualizar el chat
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una ruta y escribe un comentario.")

    # Botón para enviar el comentario
    submit_button = ttk.Button(comments_window, text="Enviar", command=submit_comment)
    submit_button.pack(pady=10)

    # Al cambiar la selección de la ruta, actualizar el chat
    route_combo.bind("<<ComboboxSelected>>", lambda e: update_chat())

# Función para mostrar noticias generales
def open_news_window():
    news_window = tk.Toplevel(root)
    news_window.title("Noticias de Rutas")
    news_window.geometry("400x400")

    ttk.Label(news_window, text="Noticias Generales", font=("Helvetica", 14)).pack(pady=10)

    # Mostrar cada noticia
    for item in news:
        ttk.Label(news_window, text=item, wraplength=350).pack(anchor="w", padx=10, pady=5)

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("QuillaMovil - Rutas de Buses")
root.geometry("900x750")

# Crear el Frame para el mapa
my_label = ttk.LabelFrame(root, text="Mapa de Rutas")
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=600, height=400, corner_radius=0)
map_widget.pack()

# Establecer la posición inicial en Colombia (por ejemplo, Barranquilla)
map_widget.set_position(10.97300, -74.79000)  # Coordenadas de Barranquilla
map_widget.set_zoom(12)  # Ajusta el nivel de zoom si es necesario

# Título en la parte superior
label = ttk.Label(root, text="QuillaMovil - Rutas de Buses de Barranquilla", font=("Helvetica", 16))
label.pack(pady=10)

# Frame para seleccionar la ruta de bus
frame_routes = ttk.Frame(root)
frame_routes.pack(pady=10, padx=10, fill='x')

ttk.Label(frame_routes, text="Seleccionar Ruta de Bus", font=("Helvetica", 14)).pack()

# Combobox para seleccionar la ruta
selected_route = tk.StringVar()
route_combo = ttk.Combobox(frame_routes, textvariable=selected_route, state="readonly")
route_combo['values'] = list(bus_routes.keys())
route_combo.pack(pady=10)

# Botón para mostrar la ruta seleccionada en el mapa
btn_show_selected_route = ttk.Button(frame_routes, text="Mostrar Ruta", command=lambda: show_bus_route(selected_route.get()))
btn_show_selected_route.pack(pady=10)

# Botón para abrir la ventana de comentarios (chat)
btn_comments = ttk.Button(root, text="Comentarios (Chat)", command=open_comments_window)
btn_comments.pack(pady=10)

# Botón para mostrar noticias generales
btn_news = ttk.Button(root, text="Noticias Generales", command=open_news_window)
btn_news.pack(pady=10)

# Iniciar la aplicación
root.mainloop()
