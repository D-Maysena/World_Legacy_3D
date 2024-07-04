import pygame as pg
import os

class AudioManager:
    def __init__(self, camera):
        #Inicializar el mezclador de sonido de pygame
        pg.mixer.init()
        self.camera = camera
        self.current_sound = None
        self.current_key = None
        self.sounds = {}
        self.load_sounds()  #Cargar los sonidos en un diccionario
        self.background_sound = pg.mixer.Sound('Audios/ambiente.mp3')  # Cargar el sonido de fondo
        self.background_volume = 0.3  # Volumen inicial del sonido de fondo
        self.proximity_volume = 1.0   # Volumen inicial del sonido de proximidad
        self.default_background_volume = 0.3
        self.background_sound.set_volume(self.background_volume)
        self.background_sound.play(-1)  # Reproducir en bucle el sonido de fondo

    def load_sounds(self):
        # Cargar los sonidos de los archivos y almacenarlos en un diccionario
        sound_files = {
            "Pedestal_bigben": 'bigben.mp3',
            "Pedestal_eiffel": 'eiffel.mp3',
            "Pedestal_coliseo": 'coliseo.mp3',
            "Pedestal_pisatower": 'pisatower.mp3',
            "Pedestal_catedral": 'catedral.mp3',
            "Pedestal_estatua": 'estatua.mp3',
            "Pedestal_estatua2": 'estatua2.mp3',
            "Pedestal_moai": 'moai.mp3'
        }

        # Recorrer el diccionario de archivos de sonido
        for key, file_name in sound_files.items():
            path = os.path.join('Audios', file_name)
            if os.path.exists(path):
                self.sounds[key] = pg.mixer.Sound(path)  #Cargar el sonido si el archivo existe
                print(f"Loaded sound: {path}")
            else:
                print(f"Sound file not found: {path}")

    def play_sound(self, key):
        # Reproducir un sonido basado en la clave proporcionada
        if self.current_key == key:
            return  # Si ya se está reproduciendo el mismo sonido, no hacer nada

        if self.current_sound is not None:
            self.current_sound.stop()  # Detener el sonido actual si existe
            print(f"Stopped current sound.")
        
        self.current_key = key
        self.current_sound = self.sounds.get(key, None)
        
        if self.current_sound is not None:
            self.background_sound.set_volume(self.background_volume * 0.1)  # Reducir el volumen del sonido de fondo
            self.current_sound.set_volume(self.proximity_volume)  # Ajustar el volumen del sonido de proximidad
            self.current_sound.play(-1)  # Reproducir en bucle el sonido de proximidad
            print(f"Playing sound: {key}")
        else:
            print(f"No sound found for key: {key}")

    def stop_current_sound(self):
        # Detener el sonido actual si existe
        if self.current_sound is not None:
            self.current_sound.stop()
            print("Stopped current sound.")
            self.current_sound = None
            self.current_key = None
            self.background_sound.set_volume(self.background_volume)  # Restaurar el volumen del sonido de fondo

    def check_proximity(self):
        # Verificar la proximidad de la cámara a los pedestales
        positions = {
            "Pedestal_bigben": (120, -1, 63),       #Big Ben
            "Pedestal_eiffel": (-33, -1, 137),      #Torre Eiffel
            "Pedestal_coliseo": (26, -1, -136),     #Coliseo
            "Pedestal_pisatower": (-126, -1, 60),   #Torre de Pisa
            "Pedestal_catedral": (116, -1, -73),    #Catedral de San Basilio
            "Pedestal_estatua": (-39, -1, -136),    #Esfinge
            "Pedestal_estatua2": (-111, -1, -81),   #David de Miguel Ángel
            "Pedestal_moai": (25, -1, 136)          #Moai
        }
        cam_pos = self.camera.position
        threshold = 33.0  # Define un umbral de proximidad en unidades

        # Verificar la distancia de la cámara a cada pedestal
        for key, pos in positions.items():
            distance = ((cam_pos[0] - pos[0]) ** 2 + (cam_pos[1] - pos[1]) ** 2 + (cam_pos[2] - pos[2]) ** 2) ** 0.5
            if distance < threshold:
                print(f"Proximity detected for {key} at distance {distance}")
                self.play_sound(key) 
                return

        self.stop_current_sound()  #Detener el sonido actual si no se detecta proximidad

    def adjust_volume(self, change):
        # Ajustar el volumen tanto del sonido de fondo como del sonido de proximidad
        self.background_volume = max(0.0, min(self.background_volume + change, 1.0))
        self.proximity_volume = max(0.0, min(self.proximity_volume + change, 1.0))

        # Ajustar el volumen del sonido de fondo y de proximidad
        self.background_sound.set_volume(self.background_volume if self.current_sound is None else self.background_volume * 0.1)
        if self.current_sound is not None:
            self.current_sound.set_volume(self.proximity_volume)

        print(f"Adjusted volumes - Background: {self.background_volume}, Proximity: {self.proximity_volume}")
