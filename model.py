import moderngl as mgl
import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vao_name, text_id, pos=(0,0,0)):
        self.app = app
        self.pos = pos
        self.m_model = self.get_model_matrix()
        self.tex_id = text_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        
    def update(self): ...
    
    def get_model_matrix(self):
        m_model = glm.mat4()
        # traslacion
        m_model = glm.translate(m_model, self.pos)
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()
        
class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0)):
        super().__init__(app, vao_name, tex_id, pos)
        self.on_init()
        
        
    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        
    def on_init(self):
        # textura
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # luz
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
            
            
