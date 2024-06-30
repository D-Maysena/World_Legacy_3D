import moderngl as mgl
import pygame as pg
import pygame
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene

from button import Button

class GraphicsEngine:
    def __init__(self, win_size=(1280, 720)):

        pg.init()
      # Inicializa el mixer de Pygame
        pg.mixer.init()
        # Establece el tamaño de la ventana
        self.WIN_SIZE = win_size
    
        # Configura los atributos de OpenGL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        #pg.GL_CONTEXT_PROFILE_MASK: Especifica que se está configurando el tipo de perfil del contexto OpenGL.
        #pg.GL_CONTEXT_PROFILE_CORE: Indica que se utilizará el perfil core de OpenGL, que incluye solo funciones modernas y excluye las obsoletas.
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    
        # Crea una ventana de visualización con OpenGL
        #Flags controla qué tipo de pantalla deseas
        #OPENGL indica que se utilizará OpenGL para renderizar en la ventana, mientras que DOUBLEBUF habilita el doble búfer, lo que reduce el parpadeo al renderizar.
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        #Ajustes del mouse
        # captura (o "agarra") el cursor del ratón dentro de la ventana de Pygame. Esto significa que el cursor no podrá salir de la ventana mientras esta esté activa
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
    
    

        #Crea un contexto de OpenGL utilizando ModernGL, proporcionando un entorno para 
        #realizar operaciones gráficas con OpenGL en la aplicación, como renderizado de objetos, 
        # configuración de shaders y manipulación de texturas.
        self.ctx = mgl.create_context()

        #Prueba de Profundidad, asegurando el ordenamiento correcto de los objetos en la escena 3D, y el Descarte de Caras, optimizando el renderizado al evitar dibujar caras no visibles.
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
       #crea un objeto de reloj pygame, permitiendo controlar el tiempo dentro del juego, 
       # como limitar la velocidad de fotogramas o calcular el tiempo transcurrido entre 
       # fotogramas para mantener una animación suave y consistente
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        #Light
        self.light = Light()
        #Camara
        self.camera = Camera(self)
        
        self.mesh = Mesh(self)
        #Escene
        #crea una instancia de la clase Triangle y la asigna a la variable self.scene
        self.scene = Scene(self)


        # Load and play sound
        self.sound = pg.mixer.Sound('Audios/ambiente.mp3')
        self.sound.play(-1)  # Loop the sound


        
    def check_events(self):


        for event in pg.event.get():
            #print(event.type)
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                #Cuando cerramos el programa liberamos memroai
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
        #limpiamos la ventana y le damos un color nuevo a traves del contexto de opengl
        self.ctx.clear(color=(0.1, 0.3, 0.2))
        #Una vez que se cargo la ventana con el color, renderizamos el objeto

        self.scene.render()
        #Luego actualizamos la ventana de pygame con flip
        pg.display.flip()
        
            
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.0005     
            
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
        
    # bucle principal de la aplicación. Similiar a una función main
    def run(self):
        #Bcule infinito 
        while True:
            self.get_time()
            #Se llama al metodo check events
            self.check_events()
            self.camera.update()
            #Al render para cambiar el color
            self.render()


            self.delta_time = self.clock.tick(60)

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def play():

    app = GraphicsEngine()
    #llama al método run() en esa instancia, lo que inicia el bucle principal de la aplicación.
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

