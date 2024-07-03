import glm
import pygame as pg
from model import Eiffel
from collisions import Collisions
from math import sqrt, cos, sin, radians


FOV = 50 #grados
NEAR = 0.1
FAR = 1000
#Velocidad de la cámara
SPEED = 0.02
SENSITIVITY = 0.02

class Camera:
    #Para poder simular una cámara necsitamos determinar la matriz de vista como 
    # la matriz de proyección
    def __init__(self, app, position=(0,10,10), yaw=-90, pitch=0):
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
        self.distance2 = 0  # Inicializar distance2 como variable de instancia

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
            
             # Elementos fuera del museo
            {'position': (0, 0), 'size': (8, 8)},    #Venus de Milo
            {'position': (-4, 62), 'size': (14, 14)},  #Banco 1
            {'position': (-4, -82), 'size': (14, 14)}, #Banco 2
            {'position': (60, 25), 'size': (14, 14)},  #Banco 3
            {'position': (-68, 25), 'size': (14, 14)}, #Banco 4
            
            {'position': (40, 50), 'size': (5, 5)},     #Arbol 1
            {'position': (-40, 50), 'size': (5, 5)},    #Arbol 2
            {'position': (-35, -68), 'size': (5, 5)},   #Arbol 3
            {'position': (27, -68), 'size': (5, 5)},    #Arbol 4
            {'position': (-68, 1), 'size': (5, 5)},     #Arbol 5
            {'position': (68, 1), 'size': (5, 5)},      #Arbol 6 
            
            {'position': (45, -40), 'size': (30, 30)},    #Castillo
            {'position': (-50, -40), 'size': (5, 5)},     #Columpio
            {'position': (8, -8), 'size': (5, 5)},        #Mujer 

        ]
        self.hexagon_radius1 = 25.8  # Radio del segundo hexágono
        self.hexagon_pos1 = glm.vec2(0, 0)  # Posición del segundo hexágono        
                
        self.hexagon_radius2 = 30  # Radio del segundo hexágono
        self.hexagon_pos2 = glm.vec2(0, 0)  # Posición del segundo hexágono
        
        # Límites del área en la que la cámara puede moverse
    
        # Inicializar Collisions con la lista de modelos
        self.collisions = Collisions(self, models)
        self.stateCamera = True # is true camera 1    

    
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
        validate = self.verifyGrande() is not True and self.verifyPequeño() if not self.stateCamera else self.verifyGrande()
        #print(self.verifyGrande() is not True)
        print(self.position)
        
        if keys[pg.K_w]:
            self.z = self.position[2] + self.forward[2] * velocity
            self.x = self.position[0] + self.forward[0] * velocity
            if validate and self.collisions.check_limits():
                self.position[2] = self.z
                self.position[0] = self.x
                
        if keys[pg.K_s]:
            self.z = self.position[2] - self.forward[2] * velocity
            self.x = self.position[0] - self.forward[0] * velocity
            if validate and self.collisions.check_limits():
                self.position[2] = self.z
                self.position[0] = self.x
        
        if keys[pg.K_a]:
            self.x = self.position[0] - self.right[0] * velocity
            self.z = self.position[2] - self.right[2] * velocity
            if validate and self.collisions.check_limits(): 
                self.position[0] = self.x
                self.position[2] = self.z
        
        if keys[pg.K_d]:
            self.x = self.position[0] + self.right[0] * velocity
            self.z = self.position[2] + self.right[2] * velocity
            if validate and self.collisions.check_limits():
                self.position[0] = self.x
                self.position[2] = self.z
        
        if keys[pg.K_1]:
            self.stateCamera = False
            self.position = glm.vec3(-9.65, 10, -128.883)
        if keys[pg.K_2]:
            self.stateCamera = True
            self.position = glm.vec3(0, 10, 10)

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
    
    def verifyGrande(self):
        vertices = ([
            [-43.8833, -76.0611 ],    
            [43.8734, -76.213],        
            
            [88.1478, 0.119104],    
                
            [43.8008, 76.1551],    
            [-44.1507, 76.1202],
            
            [-87.9573, -0.117065]])
        
        # Definir el punto a verificar
        P = ([self.x, self.z])

        # Función para verificar si un punto está dentro de un polígono
        def is_point_in_polygonFuera(point, vertices):
            n = len(vertices)
            inside = False
            x, z = point
            p1x, p1z = vertices[0]
            for i in range(n + 1):
                p2x, p2z = vertices[i % n]
                if z > min(p1z, p2z):
                    if z <= max(p1z, p2z):
                        if x <= max(p1x, p2x):
                            if p1z != p2z:
                                xinters = (z - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1z = p2x, p2z
            return inside

        # Verificar si el punto está dentro del hexágono en el plano 'xz'
        if is_point_in_polygonFuera(P, vertices):
            return True
        else:
            return False

    def verifyPequeño(self):
        verticesDentro = (
            [
                [82.7697, -143.536],
                [166.019, 0.0909767],
                  
                [82.9028, 143.642],
                
                [-82.9764, 143.754],          
                [-165.67, -0.0152953],
                
                [-82.7932, -143.398],
            ])

        P = ([self.x, self.z])
        def is_point_in_polygonDentro(point, vertices):
            n = len(vertices)
            inside = False
            x, z = point
            p1x, p1z = vertices[0]
            for i in range(n + 1):
                p2x, p2z = vertices[i % n]
                if z > min(p1z, p2z):
                    if z <= max(p1z, p2z):
                        if x <= max(p1x, p2x):
                            if p1z != p2z:
                                xinters = (z - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1z = p2x, p2z
            return inside

        # Verificar si el punto está dentro del hexágono en el plano 'xz'
        if is_point_in_polygonDentro(P, verticesDentro):
            return True
        else:
            return False
