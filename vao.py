from vbo import VBO
from shader_program import ShaderProgram

class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}        
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])
        
        self.vaos['eiffel'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['eiffel'])
        
        self.vaos['coliseo'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['coliseo'])
        
        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])

        # Pisa Tower vao
        self.vaos['pisatower'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pisatower'])
        
        # Catedral vao
        self.vaos['catedral'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['catedral'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()