import glm
import pygame as pg
from model import Eiffel
from collisions import Collisions
from math import sqrt
FOV = 50 #grados
NEAR = 0.1
FAR = 1000
#Velocidad de la cámara
SPEED = 0.02
SENSITIVITY = 0.02

class Camera:
    #Para poder simular una cámara necsitamos determinar la matriz de vista como 
    # la matriz de proyección
    def __init__(self, app, position=(0,0,4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_radio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        
        #Posición de la cámara
        self.position = glm.vec3(position)
        #orientación
        self.up = glm.vec3(0,1,0)
        self.right = glm.vec3(1,0,0)
        self.forward = glm.vec3(0,0,-1)
        
        self.yaw = yaw
        self.pitch = pitch
        
        #matriz de vista
        self.m_view = self.get_view_matrix()
        
        #matriz de proyeccion
        self.m_proj = self.get_projection_matrix() 
        self.Limits = glm.vec2(300, -300)   #Seccion de desplazamiento
        self.x = 0
        self.z = 0
        # Definir la lista de modelos con sus posiciones y tamaños
        models = [
            {'position': (25, -150), 'size': (6, 6)},   #Coliseo
            {'position': (-33, 130), 'size': (5, 5)},   #Eiffel
            {'position': (-126, 60), 'size': (4, 4)},   #PizzaTower
            {'position': (118, -80), 'size': (7, 7)},   #Catedral
            {'position': (-33, -150), 'size': (4, 4)},  #Estatua (Esfinge)
            {'position': (-125, -80), 'size': (5, 5)},  #Estatua2 (Michelangelo)
            {'position': (116, 60), 'size': (4, 4)},    #BigBen
            {'position': (25, 130), 'size': (5, 5)},    #Moai
        ]

        # Inicializar Collisions con la lista de modelos
        self.collisions = Collisions(self, models)
    
    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))
         
      
    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()       

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        print("posicion")
        print(self.position)
        if keys[pg.K_w]:
            
            self.z = self.position[2] + self.forward[2] * velocity
            self.x = self.position[0] + self.forward[0] * velocity
            
            bool_collisions = self.collisions.check_limits()
            if self.Limits[0] > self.z > self.Limits[1] and self.Limits[0] > self.x > self.Limits[1] and bool_collisions:
                self.position[2] = self.z
                self.position[0] = self.x
                
        if keys[pg.K_s]:
            self.z = self.position[2] - self.forward[2] * velocity
            self.x = self.position[0] - self.forward[0] * velocity
            bool_collisions = self.collisions.check_limits()
            
            if self.Limits[1] < self.z < self.Limits[0] and self.Limits[1] < self.x < self.Limits[0] and bool_collisions:
                self.position[2] = self.z
                self.position[0] = self.x
                
        if keys[pg.K_a]:
            self.x = self.position[0] - self.right[0] * velocity
            self.z = self.position[2] - self.right[2] * velocity
            bool_collisions = self.collisions.check_limits()
            
            if self.Limits[1] < self.x < self.Limits[0] and self.Limits[1] < self.z < self.Limits[0] and bool_collisions:
                self.position[0] = self.x
                self.position[2] = self.z
                
        if keys[pg.K_d]:

            self.x = self.position[0] + self.right[0] * velocity
            self.z = self.position[2] + self.right[2] * velocity
            bool_collisions = self.collisions.check_limits()
            
            if self.Limits[0] > self.x > self.Limits[1] and self.Limits[0] > self.z > self.Limits[1] and bool_collisions:
                self.position[0] = self.x
                self.position[2] = self.z
                
        # if keys[pg.K_q]:
        #     self.position += self.up * velocity    
        # if keys[pg.K_e]:
        #     self.position -= self.up * velocity
        # Establece los límites de la coordenada y
        min_y = 5.5  # Altura mínima permitida
        max_y = 6.0  # Altura máxima permitida
        
        # Limitar el movimiento de la camara en Y
        if self.position.y < min_y:
            self.position.y = min_y
        elif self.position.y > max_y:
            self.position.y = max_y
            
    # La matriz de vista se encarga de definir la posición y orientación de la cámara en el espacio 3D
    def get_view_matrix(self):
        #Para encontrar la matriz usamos la función lookat, esta recibe la posición de la cámara
        # hacia donde esta viendo (en este caso ella ve al centro), y la orientación en el eje y a través de up
        #Esto es cuando la cámara apunta a un lugar fijo
        #return glm.lookAt(self.position, glm.vec3(0), self.up)
        #Como la cámara se va a mover no queremos que mire a un punto fijo
        #self.forward es un vector que indica la dirección hacia adelante desde la cámara.
        #AL Sumarlo con la posición de la cámara nos daría como resultado el punto que está en la dirección hacia adelante en el punto actual
        #Osea hacia donde está viendo
        return glm.lookAt(self.position, self.position + self.forward , self.up)
    
    # La matriz de proyección define cómo se proyectan las coordenadas 3D en la pantalla 2D
    #hace que los objetos más lejanos se vean más pequeños. 
    def get_projection_matrix(self):
        #Para determinar la matriz de proyección usamos perspective, 
        #Esta recibe el campo de visión (FOV) en radianes.  
        #La relación de aspecto que determina el campo de visión. Esta se determina diviendo el ancho entre el alto
        #NEAR: distancia desde la cámara al plano de recorte más cercano 
        #FAR: distancia desde la cámara al plano de recorte más lejano
        return glm.perspective(glm.radians(FOV), self.aspect_radio, NEAR, FAR)