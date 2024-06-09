from vbo import VBO
from shader_program import ShaderProgram

class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)   
        self.vaos = {}        
        
         # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])

        self.vaos['eiffel'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['eiffel'])
        
        self.vaos['coliseo'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['coliseo'])
        

        # Pisa Tower vao
        self.vaos['pisatower'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pisatower'])
        
        # Catedral vao
        self.vaos['catedral'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['catedral'])
        
         # torre vao
        self.vaos['estatua'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['estatua'])
        
        # Estatua 2
        self.vaos['estatua2'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['estatua2'])

        # bigben vao
        self.vaos['bigben'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['bigben'])
        # moai vao
        self.vaos['moai'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['moai'])
        
        # Cubo
        self.vaos['cubo'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cubo'])
        
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # advanced_skybox vao
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao
    
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()