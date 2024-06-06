import numpy as np
import glm
import moderngl as mgl

class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), radius=1.0):
        self.app = app
        #Posición del objeto
        self.pos = pos
        #convierte una lista de ángulos en grados (rot) a radianes y los almacena como un vector 3D (glm.vec3)
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        self.radius = radius  # Almacenar el radio como un atributo
        
    def update(self):
        ...
    
    def get_model_matrix(self):
        m_model = glm.mat4()
        #En la matriz modelo aplicamos la traslación
        m_model = glm.translate(m_model, self.pos)
        #Rotación
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1,0,0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0,1,0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0,0,1))
        #Escalación
        m_model = glm.scale(m_model, self.scale)
        return m_model    
        
    def render(self):
        self.update()
        # Método para renderizar el triángulo
        self.vao.render()
    

class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), radius=1.0):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, radius)
        self.on_init()
    
    def update(self):
        self.texture.use()
        self.program['m_model'].write(self.m_model)    
        self.program['m_view'].write(self.camera.m_view)
        self.program['camPos'].write(self.camera.position)
        

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        #toma la matriz de proyección (m_proj) de la cámara de la aplicación (self.app.camera)
        # y la escribe en el uniforme m_proj del programa de shaders.
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Eiffel(BaseModel):
    def __init__(self, app, vao_name='eiffel', tex_id='eiffel', pos=(0,0,0), rot=(-90,0,0), scale=(1,1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()
    
    def update(self):
        self.texture.use()
        self.program['m_model'].write(self.m_model)    
        self.program['m_view'].write(self.camera.m_view)
        self.program['camPos'].write(self.camera.position)
        

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        #toma la matriz de proyección (m_proj) de la cámara de la aplicación (self.app.camera)
        # y la escribe en el uniforme m_proj del programa de shaders.
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is) 

        
class Coliseo(BaseModel):
    def __init__(self, app, vao_name='coliseo', tex_id='coliseo', pos=(0,0,0), rot=(-90,0,0), scale=(1,1,1), radius=300.0):
        super().__init__(app, vao_name, tex_id, pos, rot, scale, radius)
        
        self.on_init()
    
    def update(self):
        self.texture.use()
        self.program['m_model'].write(self.m_model)    
        self.program['m_view'].write(self.camera.m_view)
        self.program['camPos'].write(self.camera.position)
        

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        #toma la matriz de proyección (m_proj) de la cámara de la aplicación (self.app.camera)
        # y la escribe en el uniforme m_proj del programa de shaders.
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is) 
        
        
        
class Museo(BaseModel):
    def __init__(self, app, vao_name='museo', tex_id='museo', pos=(0,0,0), rot=(-90,0,0), scale=(1,1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()
    
    def update(self):
        self.texture.use()
        self.program['m_model'].write(self.m_model)    
        self.program['m_view'].write(self.camera.m_view)
        self.program['camPos'].write(self.camera.position)
        

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        #toma la matriz de proyección (m_proj) de la cámara de la aplicación (self.app.camera)
        # y la escribe en el uniforme m_proj del programa de shaders.
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is) 