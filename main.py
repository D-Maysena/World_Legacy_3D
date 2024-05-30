import pygame as pg
import moderngl as mgl
import sys

class GraphicsEngine:
    #El método __init__(self, win_size=(800, 600)) en la clase GraphicsEngine es el 
    # constructor que inicializa una nueva instancia de la clase, configurando Pygame y estableciendo el tamaño de la ventana con un valor por defecto de (800, 600)
    def __init__(self, win_size=(800, 600)):
        # Inicializa el módulo Pygame
        pg.init()
    
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
    
        #Crea un contexto de OpenGL utilizando ModernGL, proporcionando un entorno para 
        #realizar operaciones gráficas con OpenGL en la aplicación, como renderizado de objetos, 
        # configuración de shaders y manipulación de texturas.
        self.ctx = mgl.create_context()
    
       #crea un objeto de reloj pygame, permitiendo controlar el tiempo dentro del juego, 
       # como limitar la velocidad de fotogramas o calcular el tiempo transcurrido entre 
       # fotogramas para mantener una animación suave y consistente
        self.clock = pg.time.Clock()
        
    def check_events(self):
        # Gestiona los eventos de entrada del usuario, permitiendo que 
        # la aplicación responda a acciones como cerrar la ventana.
        #Los eventos son almacenados en una cola
        for event in pg.event.get():
            print(event.type)
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
        
    #a función render se encarga de limpiar la pantalla con un color específico y 
    # luego actualizarla para mostrar los cambios realizados en la escena gráfica    
    def render(self):
        #limpiamos la ventana y le damos un color nuevo a traves del contexto de opengl
        self.ctx.clear(color=(0.8, 0.6, 0.18))
        #Luego actualizamos la ventana de pygame con flip
        pg.display.flip()
            
    # bucle principal de la aplicación. Similiar a una función main
    def run(self):
        #Bcule infinito
        while True:
            #Se llama al metodo check events
            self.check_events()
            #Al render para cambiar el color
            self.render()
            #A traves de clock que nos permite controlar el tiempo de nuestro juego
            #Limitamos los fps con tick
            self.clock.tick(60)
                
if __name__ == '__main__':
    # crea una instancia de la clase GraphicsEngine
    app = GraphicsEngine()
    #llama al método run() en esa instancia, lo que inicia el bucle principal de la aplicación.
    app.run()
        
        