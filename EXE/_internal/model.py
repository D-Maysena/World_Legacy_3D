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

class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
    

class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=6, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), radius=1.0):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
    
    

class Eiffel(ExtendedBaseModel):
    def __init__(self, app, vao_name='eiffel', tex_id='eiffel', pos=(0,0,0), rot=(-90,0,0), scale=(1,1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

       

        
class Coliseo(ExtendedBaseModel):
    def __init__(self, app, vao_name='coliseo', tex_id='coliseo', pos=(0,0,0), rot=(-90,0,0), scale=(1,1,1), radius=300.0):
                super().__init__(app, vao_name, tex_id, pos, rot, scale)

       
        
class Museo(ExtendedBaseModel):
    def __init__(self, app, vao_name='museo', tex_id='museo', pos=(0,0,0), rot=(-90,0,0), scale=(1,1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
       
class PisaTower(ExtendedBaseModel):
    def __init__(self, app, vao_name='pisatower', tex_id='pisatower',
                 pos=(1, 1, 1), rot=(-85, 0, 0), scale=(0.002, 0.002, 0.002)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
       
class Catedral(ExtendedBaseModel):
    def __init__(self, app, vao_name='catedral', tex_id='catedral',
                 pos=(1, 1, 1), rot=(-90, 0, 0), scale=(0.00015, 0.00015, 0.00015)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
       

class Estatua(ExtendedBaseModel):
    def __init__(self, app, vao_name='estatua', tex_id='estatua', 
                 pos=(0, 0, 0), rot=(-90,0,0), scale=(0.0015,0.0015,0.0015)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
       
            
            
class Estatua2(ExtendedBaseModel):
    def __init__(self, app, vao_name='estatua2', tex_id='estatua2', 
                 pos=(0, 0, 0), rot=(-90,0,0), scale=(0.025,0.025,0.025)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
        
class Bigben(ExtendedBaseModel):
    def __init__(self, app, vao_name='bigben', tex_id='bigben',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(0.0015, 0.0015, 0.0015)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
       
class moai(ExtendedBaseModel):
    def __init__(self, app, vao_name='moai', tex_id='moai',
                 pos=(0, 0, 0), rot=(-90, 0, 180), scale=(0.018, 0.018, 0.018)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
#############################################################################################
        
class Pedestal_bigben(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_bigben', tex_id='pedestal_bigben',
                 pos=(0, 0, 0), rot=(-90,0, 180), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Pedestal_eiffel(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_eiffel', tex_id='pedestal_eiffel',
                 pos=(0, 0, 0), rot=(-90,0, 90), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Pedestal_coliseo(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_coliseo', tex_id='pedestal_coliseo',
                 pos=(0, 0, 0), rot=(-90,0, 90), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Pedestal_pisatower(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_pisatower', tex_id='pedestal_pisatower',
                 pos=(0, 0, 0), rot=(-90,0, 90), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Pedestal_catedral(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_catedral', tex_id='pedestal_catedral',
                 pos=(0, 0, 0), rot=(-90,0, 90), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Pedestal_estatua(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_estatua', tex_id='pedestal_estatua',
                 pos=(0, 0, 0), rot=(-90,0, 90), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
        
class Pedestal_estatua2(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_estatua2', tex_id='pedestal_estatua2',
                 pos=(0, 0, 0), rot=(-90,0, 90), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
        
class Pedestal_moai(ExtendedBaseModel):
    def __init__(self, app, vao_name='pedestal_moai', tex_id='pedestal_moai',
                 pos=(0, 0, 0), rot=(-90,0, 90), scale=(0.06, 0.06, 0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
############################################################################################

class Estatua3(ExtendedBaseModel):
    def __init__(self, app, vao_name='estatua3', tex_id='estatua3', 
                 pos=(0, 0, 0), rot=(-90,0,0), scale=(0.1,0.1,0.1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Banco1(ExtendedBaseModel):
    def __init__(self, app, vao_name='banco1', tex_id='banco1', 
                 pos=(0, 0, 0), rot=(-90,0,180), scale=(0.08,0.08,0.08)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Banco2(ExtendedBaseModel):
    def __init__(self, app, vao_name='banco2', tex_id='banco2', 
                 pos=(0, 0, 0), rot=(-90,0,0), scale=(0.08,0.08,0.08)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
        
class Banco3(ExtendedBaseModel):
    def __init__(self, app, vao_name='banco3', tex_id='banco3', 
                 pos=(0, 0, 0), rot=(-90,0,-120), scale=(0.08,0.08,0.08)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
        
class Banco4(ExtendedBaseModel):
    def __init__(self, app, vao_name='banco4', tex_id='banco4', 
                 pos=(0, 0, 0), rot=(-90,0,-240), scale=(0.08,0.08,0.08)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Arbol1(ExtendedBaseModel):
    def __init__(self, app, vao_name='arbol1', tex_id='arbol1', 
                 pos=(0, 0, 0), rot=(-90,0,-240), scale=(0.03,0.03,0.03)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Arbol2(ExtendedBaseModel):
    def __init__(self, app, vao_name='arbol2', tex_id='arbol2', 
                 pos=(0, 0, 0), rot=(-90,0,-240), scale=(0.03,0.03,0.03)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Arbol3(ExtendedBaseModel):
    def __init__(self, app, vao_name='arbol3', tex_id='arbol3', 
                 pos=(0, 0, 0), rot=(-90,0,-240), scale=(0.03,0.03,0.03)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Arbol4(ExtendedBaseModel):
    def __init__(self, app, vao_name='arbol4', tex_id='arbol4', 
                 pos=(0, 0, 0), rot=(-90,0,-240), scale=(0.03,0.03,0.03)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Arbol5(ExtendedBaseModel):
    def __init__(self, app, vao_name='arbol5', tex_id='arbol5', 
                 pos=(0, 0, 0), rot=(-90,0,-240), scale=(0.03,0.03,0.03)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
class Arbol6(ExtendedBaseModel):
    def __init__(self, app, vao_name='arbol6', tex_id='arbol6', 
                 pos=(0, 0, 0), rot=(-90,0,-240), scale=(0.03,0.03,0.03)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Castillo(ExtendedBaseModel):
    def __init__(self, app, vao_name='castillo', tex_id='castillo', 
                 pos=(0, 0, 0), rot=(-90,0,-50), scale=(2,2,2)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
        
class Columpio(ExtendedBaseModel):
    def __init__(self, app, vao_name='columpio', tex_id='columpio', 
                 pos=(0, 0, 0), rot=(-90,0,-25), scale=(0.06,0.06,0.06)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)  
        
        
class Mujer(ExtendedBaseModel):
    def __init__(self, app, vao_name='mujer', tex_id='mujer', 
                 pos=(0, 0, 0), rot=(-90,0,-120), scale=(0.067,0.067,0.067)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)      


###########################################################################################
        
class cubo(ExtendedBaseModel):
    def __init__(self, app, vao_name='cubo', tex_id='cubo',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(0.01, 0.01, 0.01)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        
class museo4(BaseModel):
    def __init__(self, app, vao_name='museo4', tex_id='museo4',
                 pos=(0, 0, 0), rot=(0,0,0), scale=(0.01, 0.01, 0.01)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)