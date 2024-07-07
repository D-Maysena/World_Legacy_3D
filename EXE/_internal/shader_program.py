import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['skybox'] = self.get_program('skybox')
        self.programs['advanced_skybox'] = self.get_program('advanced_skybox')
        
    def get_program(self, shader_program_name):
        # Método para obtener el programa de shader
        shader_dir = resource_path('shaders')  # Directorio donde están los shaders

        vertex_shader_path = resource_path(f'shaders/{shader_program_name}.vert')
        fragment_shader_path = resource_path(f'shaders/{shader_program_name}.frag')
        
        with open(vertex_shader_path) as file:
            vertex_shader = file.read()
            
        with open(fragment_shader_path) as file:
            fragment_shader = file.read()    
        #Crea un programa de shader utilizando estos shaders.
        #Este programa de shader se utilizará para especificar cómo se deben procesar los vértices y los fragmentos durante la renderización de los objetos en OpenGL.
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
    
    def destroy(self):
        [program.release() for program in self.programs.values()]
