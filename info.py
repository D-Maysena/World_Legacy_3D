import os
import pygame as pg
from tkinter import messagebox, Tk, Toplevel, Label, Button
import tkinter.font as tkFont

class InfoManager:
    def __init__(self, camera):
        self.camera = camera
        self.current_key = None
        self.positions = {
            "Object_bigben": (116, -1, 60),
            "Object_eiffel": (-33, -1, 130),
            "Object_coliseo": (25, -1, -150),
            "Object_pisatower": (-126, -1, 60),
            "Object_catedral": (118, -1, -80),
            "Object_esfinge": (-33, -1, -150),
            "Object_david": (-125, -1, -80),
            "Object_moai": (25, -1, 130)
        }
        self.info = {
            "Object_bigben": (
                "El Big Ben\n\n"
                "Ubicación: Londres, Inglaterra\n\n"
                "Altura: 96,3 metros\n\n"
                "Descripción: El Big Ben, oficialmente conocido como Torre del Reloj del Palacio de Westminster, "
                "es una torre neogótica que alberga el reloj de cuatro caras más grande del mundo. Es uno de los "
                "símbolos más emblemáticos de la ciudad y del Reino Unido."
            ),
            "Object_eiffel": (
                "La Torre Eiffel\n\n"
                "Ubicación: París, Francia\n\n"
                "Altura: 324 metros\n\n"
                "Descripción: La Torre Eiffel es una torre de hierro forjado situada en el Campo de Marte. "
                "Es el monumento más emblemático de la ciudad y uno de los más famosos del mundo."
            ),
            "Object_coliseo": (
                "El Coliseo Romano\n\n"
                "Ubicación: Roma, Italia\n\n"
                "Descripción: El Coliseo, también conocido como Anfiteatro Flavio, es un anfiteatro ovalado de "
                "la época del Imperio romano. Es considerado uno de los monumentos más importantes y reconocidos "
                "del mundo, y fue declarado Patrimonio de la Humanidad por la UNESCO en 1980."
            ),
            "Object_pisatower": (
                "La Torre de Pisa\n\n"
                "Ubicación: Pisa, Italia\n\n"
                "Descripción: La Torre de Pisa, también conocida como Torre Pendente de Pisa, es un campanario "
                "independiente de la catedral de Pisa. Famosa por su singular inclinación hacia el sur, es uno de los "
                "destinos turísticos más renombrados de Italia y está reconocida como uno de los edificios arquitectónicos "
                "más impresionantes de la Europa medieval."
            ),
            "Object_catedral": (
                "La Catedral de San Basilio\n\n"
                "Ubicación: Moscú, Rusia\n\n"
                "Descripción: La Catedral de San Basilio, también conocida como Catedral de la Intercesión de la Santísima "
                "Virgen sobre el Foso, es un templo ortodoxo ubicado en la Plaza Roja de Moscú. Famosa por sus coloridas cúpulas "
                "en forma de bulbo, es considerada uno de los monumentos más emblemáticos de la ciudad y de toda Rusia."
            ),
            "Object_esfinge": (
                "La Esfinge de Egipto\n\n"
                "Ubicación: Egipto\n\n"
                "Descripción: Las esfinges egipcias son esculturas monumentales que representan a una criatura mitológica con cuerpo "
                "de león y cabeza humana, a menudo adornada con la corona real egipcia. Estas figuras eran símbolos de poder, fuerza "
                "y protección en el antiguo Egipto, y se colocaban habitualmente a la entrada de templos, tumbas y otros lugares sagrados."
            ),
            "Object_david": (
                "El David de Miguel Angel\n\n"
                "Ubicación: Florencia, Italia\n\n"
                "Altura: 5,17 metros\n\n"
                "Descripción: El David es una escultura renacentista de mármol blanco realizada por el artista italiano Miguel Ángel entre "
                "1501 y 1504. Representa al héroe bíblico David en el momento previo a su enfrentamiento con el gigante Goliat."
            ),
            "Object_moai": (
                "Los Moai\n\n"
                "Ubicación: Rapa Nui (Isla de Pascua)\n\n"
                "Descripción: Los moai son esculturas monolíticas humanoides típicas de la isla polinésica de Rapa Nui. Talladas en roca volcánica, "
                "estas figuras de gran tamaño, con cabezas desproporcionadamente grandes y expresiones hieráticas, son un ícono de la cultura Rapa Nui "
                "y uno de los principales atractivos turísticos de la isla."
            )
        }

    def check_proximity(self):
        cam_pos = self.camera.position
        threshold = 20.0  # Define un umbral de proximidad

        for key, pos in self.positions.items():
            distance = ((cam_pos[0] - pos[0]) ** 2 + (cam_pos[1] - pos[1]) ** 2 + (cam_pos[2] - pos[2]) ** 2) ** 0.5
            if distance < threshold:
                if self.current_key != key:
                    self.current_key = key
                    self.show_info_dialog(key)
                return

        self.current_key = None

    def show_info_dialog(self, key):
        root = Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        if messagebox.askyesno("Información", "¿Desea ver la información sobre este objeto?"):
            info_window = Toplevel(root)
            info_window.title("Información")
            info_window.geometry("400x400")
            info_window.configure(bg='white')
            info_window.overrideredirect(True)  # Quita la barra de título

            font_body = tkFont.Font(family="Helvetica", size=12)

            info_label = Label(info_window, text=self.info[key], font=font_body, bg='white', fg='blue', wraplength=350, justify="left", anchor="nw", padx=10, pady=10)
            info_label.pack(fill='both', expand=True)

            close_button = Button(info_window, text="Cerrar", command=info_window.destroy, bg='white', fg='blue', font=font_body)
            close_button.pack(pady=10)

            root.wait_window(info_window)
        root.destroy()
