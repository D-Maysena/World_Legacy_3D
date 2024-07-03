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
        
        ######################################################################################################3
        
        self.vaos['pedestal_bigben'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_bigben'])
        
        self.vaos['pedestal_eiffel'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_eiffel'])
        
        self.vaos['pedestal_coliseo'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_coliseo'])
        
        self.vaos['pedestal_pisatower'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_pisatower'])
        
        self.vaos['pedestal_catedral'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_catedral'])
        
        self.vaos['pedestal_estatua'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_estatua'])
        
        self.vaos['pedestal_estatua2'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_estatua2'])
        
        self.vaos['pedestal_moai'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['pedestal_moai'])
        
        
        
        ######################################################################################################
        
        
        self.vaos['estatua3'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['estatua3'])
        
        self.vaos['banco1'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['banco1'])
        
        self.vaos['banco2'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['banco2'])
        
        self.vaos['banco3'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['banco3'])
        
        self.vaos['banco4'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['banco4'])
        
        self.vaos['arbol1'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['arbol1'])
        
        self.vaos['arbol2'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['arbol2'])
        
        self.vaos['arbol3'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['arbol3'])
        
        self.vaos['arbol4'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['arbol4'])
        
        self.vaos['arbol5'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['arbol5'])
        
        self.vaos['arbol6'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['arbol6'])
        
        
        self.vaos['castillo'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['castillo'])
        
        self.vaos['columpio'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['columpio'])
        
        self.vaos['mujer'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['mujer'])
        
        #####################################################################################################
        
        
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # advanced_skybox vao
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])
        
        self.vaos['museo4'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['museo4'])


    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao
    
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()