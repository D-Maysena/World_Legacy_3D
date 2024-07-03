import moderngl as mgl
import pygame as pg
import pygame
import sys
from model import *
from camera import Camera
from light import Light, AdditionalLight, AdditionalLight2
from mesh import Mesh
from scene import Scene
from button import Button
from info import InfoManager  # Importar InfoManager

class GraphicsEngine:
    def __init__(self, win_size=(1280, 720)):
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

        # Load and play sound
        self.sound = pg.mixer.Sound('Audios/ambiente.mp3')
        self.sound.play(-1)  # Loop the sound

        # Info Manager
        self.info_manager = InfoManager(self.camera)  # Inicializar InfoManager

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.adjust_volume(-0.1)  # Decrease volume
                elif event.key == pg.K_x:
                    self.adjust_volume(0.1)  # Increase volume

    def adjust_volume(self, change):
        volume = self.sound.get_volume() + change
        volume = max(0.0, min(volume, 1.0))  # Limit volume between 0.0 and 1.0
        self.sound.set_volume(volume)
        print(f"Volume set to: {volume}")

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
            self.camera.update()
            self.info_manager.check_proximity()  # Llamar a check_proximity de InfoManager
            self.render()
            self.delta_time = self.clock.tick(60)

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def play():
    app = GraphicsEngine()
    app.run()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        OPTIONS_TEXT = get_font(45).render("INSTRUCCIONES", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        instructions = [
            "1. Presione W para ir enfrente.",
            "2. Presione S para ir atras.",
            "3. Presione A para ir a la derecha",
            "4. Presione D para ir a la izquierda",
            "5. Presione X para subir volumen",
            "6. Presione Z para bajar volumen",
            "7. Presione Esc para salir del juego"
        ]
        for i, line in enumerate(instructions):
            INSTRUCTION_TEXT = get_font(30).render(line, True, "Black")
            INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(640, 200 + i * 40))
            SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 600), 
                            text_input="Regresar", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("WORLD LEGACY", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="ENTRAR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="AYUDA", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="SALIR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Initialize Pygame and set up the main menu
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("WORLD LEGACY 3D")
BG = pygame.transform.scale(pygame.image.load("assets/world5.jpg"), (1280, 720))
main_menu()
