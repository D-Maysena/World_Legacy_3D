import glm
import pygame as pg
from model import Eiffel
from collisions import Collisions
from math import sqrt, cos, sin, radians


FOV = 50 #grados
NEAR = 0.1
FAR = 1000
#Velocidad de la cámara
SPEED = 0.05
SENSITIVITY = 0.02

class Camera:
    #Para poder simular una cámara necsitamos determinar la matriz de vista como 
    # la matriz de proyección
    def __init__(self, app, position=(0,10,0), yaw=-90, pitch=0):
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
        self.Limits = glm.vec2(100, -300)
        self.x = 0
        self.z = 0
        # Definir la lista de modelos con sus posiciones y tamaños
        models = [
            {'position': (20, -10), 'size': (8, 8)},
            {'position': (0, -5), 'size': (2, 2)},
            
        ]
                
        self.hexagon_radius1 = 25.8  # Radio del segundo hexágono
        self.hexagon_pos1 = glm.vec2(0, 0)  # Posición del segundo hexágono        
                
        self.hexagon_radius2 = 30  # Radio del segundo hexágono
        self.hexagon_pos2 = glm.vec2(0, 0)  # Posición del segundo hexágono
        
            # Límites del área en la que la cámara puede moverse
      
        # Inicializar Collisions con la lista de modelos
        self.collisions = Collisions(self, models)
        self.dentro = True
        self.fuera = True
    
    def verifyGrande(self):
        vertices = ([
            [44.1048, 76.7512],
            
            [-44.4962, 76.6076],
            
            [-88.6649, -0.123909],
            
            [-44.2154, -76.8449],
            
            [44.4397, -76.5908],
            
            [88.6445, 0.0905567],
            
            #AFUERA
            #1
            #[82.4833, -143.217],
            #2
            #[165.335, 0.0486343],
            #3
            #[82.5721, 143.146],
            #4
            #[-82.5137, 143.115],
            #5
            #[-165.287, 0.147995],
            #6
            #[-82.7653, -143.053],
            
            
        ])

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
            return False
        else:
            return True
        
    def verifyPequeño(self):
        verticesDentro = (
            [            
            #AFUERA
            #1
            [82.4833, -143.217],
            #2
            [165.335, 0.0486343],
            #3
            [82.5721, 143.146],
            #4
            [-82.5137, 143.115],
            #5
            [-165.287, 0.147995],
            #6
            [-82.7653, -143.053],
        ])

        # Definir el punto a verificar
        P = ([self.x, self.z])

        # Función para verificar si un punto está dentro de un polígono
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
            return False
        else:
            return True  
        
    
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
    
    def is_within_hexagon(self, x, z, radius, hexagon_pos):
        # Determinar si el punto (x, z) está dentro del hexágono de radio `radius` en la posición `hexagon_pos`
        hex_x, hex_z = hexagon_pos.x, hexagon_pos.y
        for i in range(6):
            angle1 = radians(60 * i)
            angle2 = radians(60 * (i + 1))
            x1, z1 = radius * cos(angle1), radius * sin(angle1)
            x2, z2 = radius * cos(angle2), radius * sin(angle2)
            if (x - x1 + hex_x) * (z2 - z1 + hex_z) - (z - z1 + hex_z) * (x2 - x1 + hex_x) > 0:
                print("negra")
                return False
        print("presidente")
        return True

    def distance_to_hexagon(self, hexagon_pos, hexagon_radius):
        # Calcular la distancia euclidiana entre la cámara y el hexágono en hexagon_pos con radio hexagon_radius
        dist_x = self.position.x - hexagon_pos.x
        dist_z = self.position.z - hexagon_pos.y
        distance = sqrt(dist_x * dist_x + dist_z * dist_z)
        return distance


    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
    
        if keys[pg.K_w]:
            self.z = self.position.z + self.forward.z * velocity
            self.x = self.position.x + self.forward.x * velocity
            if self.collisions.check_limits():
                get = self.verifyPequeño()
                get2 = self.verifyGrande()
                print(get2)
                print("primero")
                print(get)
                if (self.verifyGrande() and not self.verifyPequeño()) and (self.verifyGrande() or self.verifyPequeño()):
                    self.position.z = self.z
                    self.position.x = self.x
                    # Imprimir distancia y radio del hexágono más cercano
                    distance2 = self.distance_to_hexagon(self.hexagon_pos2, self.hexagon_radius2)
                    print(f"Distancia al segundo hexágono: {distance2}, Radio: {self.hexagon_radius2}")
                if (not self.verifyGrande() and not self.verifyPequeño()) and ( self.verifyGrande() or self.verifyPequeño()):
                        self.position.z = self.z
                        self.position.x = self.x
            # if self.collisions.check_limits():
            #     te= self.verifyPequeño()
            #     te2=self.verifyGrande()
            #     print(te)
            #     print("yeyp")
            #     print(te2)
                
            #     if not (self.verifyPequeño() or self.verifyGrande()):
            #         print("aquyi")
            #         get = self.verifyPequeño()
            #         self.position.z = self.z
            #         self.position.x = self.x
            #         # Imprimir distancia y radio del hexágono más cercano
            #         distance2 = self.distance_to_hexagon(self.hexagon_pos2, self.hexagon_radius2)
            #         print(f"Distancia al segundo hexágono: {distance2}, Radio: {self.hexagon_radius2}")          
                
        elif keys[pg.K_s]:
            self.z = self.position.z - self.forward.z * velocity
            self.x = self.position.x - self.forward.x * velocity
            if self.collisions.check_limits():
                get = self.verifyPequeño()
                get2 = self.verifyGrande()
                print(get2)
                print("primero")
                print(get)
                if (self.verifyGrande() and not self.verifyPequeño()) and (self.verifyGrande() or self.verifyPequeño()):
                    self.dentro = False
                    self.position.z = self.z
                    self.position.x = self.x
                    # Imprimir distancia y radio del hexágono más cercano
                    distance2 = self.distance_to_hexagon(self.hexagon_pos2, self.hexagon_radius2)
                    print(f"Distancia al segundo hexágono: {distance2}, Radio: {self.hexagon_radius2}")
                if (not self.verifyGrande() and not self.verifyPequeño()) and self.dentro:
                        self.afuera = False
                        
                        self.position.z = self.z
                        self.position.x = self.x
                           
        elif keys[pg.K_a]:
            self.x = self.position.x - self.right.x * velocity
            self.z = self.position.z - self.right.z * velocity
            if self.collisions.check_limits():
                get = self.verifyPequeño()
                get2 = self.verifyGrande()
                print(get2)
                print("primero")
                print(get)
                if (self.verifyGrande() and not self.verifyPequeño()) and (self.verifyGrande() or self.verifyPequeño()):
                    self.dentro = False
                    self.position.z = self.z
                    self.position.x = self.x
                    # Imprimir distancia y radio del hexágono más cercano
                    distance2 = self.distance_to_hexagon(self.hexagon_pos2, self.hexagon_radius2)
                    print(f"Distancia al segundo hexágono: {distance2}, Radio: {self.hexagon_radius2}")
                if (not self.verifyGrande() and not self.verifyPequeño()) and self.dentro:
                        self.afuera = False
                        
                        self.position.z = self.z
                        self.position.x = self.x
                
        elif keys[pg.K_d]:
            self.x = self.position.x + self.right.x * velocity
            self.z = self.position.z + self.right.z * velocity
            if self.collisions.check_limits():
                get = self.verifyPequeño()
                get2 = self.verifyGrande()
                print(get2)
                print("primero")
                print(get)
                if (self.verifyGrande() and not self.verifyPequeño()) and (self.verifyGrande() or self.verifyPequeño()):
                    self.dentro = False
                    self.position.z = self.z
                    self.position.x = self.x
                    # Imprimir distancia y radio del hexágono más cercano
                    distance2 = self.distance_to_hexagon(self.hexagon_pos2, self.hexagon_radius2)
                    print(f"Distancia al segundo hexágono: {distance2}, Radio: {self.hexagon_radius2}")
                if (not self.verifyGrande() and not self.verifyPequeño()) and self.dentro:
                        self.afuera = False
                        
                        self.position.z = self.z
                        self.position.x = self.x
                
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