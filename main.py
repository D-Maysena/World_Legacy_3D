import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light, AdditionalLight, AdditionalLight2
from mesh import Mesh
from scene import Scene
from audios import AudioManager

class GraphicsEngine:
    def __init__(self, win_size=(900, 650)):
        pg.init()
        pg.mixer.init()
        self.WIN_SIZE = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # Light
        self.light = Light(position=(50, 50, -10), color=(1, 1, 1))
        self.additional_lights = [
            AdditionalLight(position=(0, -3, -10), color=(1, 1, 1)),
            AdditionalLight2(position=(0, 20, -10), color=(1, 0.5, 0.5))
        ]

        # Camera
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        
        # Audio Manager
        self.audio_manager = AudioManager(self.camera)

        # Cargar y reproducir sonido
        self.sound = pg.mixer.Sound('Audios/ambiente.mp3')
        self.sound.play(-1)  # Reproducir en bucle

    def check_events(self):
        # Procesar eventos de Pygame
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.audio_manager.adjust_volume(-0.1)  # Disminuir el volumen
                elif event.key == pg.K_x:
                    self.audio_manager.adjust_volume(0.1) # Aumentar el volumen


    def adjust_volume(self, change):
        # Ajustar el volumen del sonido
        volume = self.sound.get_volume() + change
        volume = max(0.0, min(volume, 1.0))  # Limitar el volumen entre 0.0 y 1.0
        self.sound.set_volume(volume) # Establecer el nuevo volumen
        print(f"Volume set to: {volume}") # Imprime el volumen actual en la consola

    def render(self):
        self.ctx.clear(color=(0.1, 0.3, 0.2))
        self.scene.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.audio_manager.check_proximity()  # Añadir la verificación de proximidad
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()

