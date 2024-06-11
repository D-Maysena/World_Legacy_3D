import glm
import pygame as pg

FOV = 50 #grados
NEAR = 0.1
FAR = 1000
#Velocidad de la cámara
SPEED = 0.04
SENSITIVITY  = 0.03

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
    
    #Cambiaremos la posición de la cámara usando las teclas
    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity    
        if keys[pg.K_e]:
            self.position -= self.up * velocity
    
    #La matriz de vista se encarga de definir la posición y orientación de la cámara en el espacio 3D
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