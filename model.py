import numpy as np
import glm
import pygame as pg

class Cube:
    def __init__(self, app):
        # Inicialización de la clase Triangle
        self.app = app
        self.ctx = app.ctx
        self.shader_program = self.get_shader_program('default')  # Primero, inicializa el programa de shader
        self.vbo = self.get_vbo()  # Luego, inicializa el búfer de vértices
        self.vao = self.get_vao()  # Finalmente, inicializa el array de vértices
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='textures/box.jpg')
        self.on_init()
        
        
    def get_texture(self, path):
        #Cargamos la textura y la convertimos en un formato RGB
        texture = pg.image.load(path).convert()
        #Volteamos la imagen
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        #Luego convertimos la imagen a una textura de opengl, el primer parametro es el tamaño de la imange, el segundo
        # son los componentes que usa (RGB) y el ultimo son los datos de la imagen, el cual usaremos el tostring, para obtener 
        #los datos de los pixeles en formato rgb
        texture = self.ctx.texture(size=texture.get_size(), components=3, 
                                   data=pg.image.tostring(texture, 'RGB'))
        return texture 
    
    def uptdate(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0,1,0))
        self.shader_program['m_model'].write(m_model)    
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['camPos'].write(self.app.camera.position)
        
    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model    
        
    def on_init(self):
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.Id'].write(self.app.light.Id)
        self.shader_program['light.Is'].write(self.app.light.Is)
        #toma la matriz de proyección (m_proj) de la cámara de la aplicación (self.app.camera)
        # y la escribe en el uniforme m_proj del programa de shaders.
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)
        #Pasamos la textura al fragmentshader
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        
    def get_shader_program(self, shader_name):
        # Método para obtener el programa de shader
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
            
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()    
        
        #Crea un programa de shader utilizando estos shaders.
        #Este programa de shader se utilizará para especificar cómo se deben procesar los vértices y los fragmentos durante la renderización de los objetos en OpenGL.
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
    
    def get_vertex_data(self):
        # Método para obtener los datos de los vértices del triángulo
        #coordenadas de los vertices del triangulo
        #vertex_data = [(-0.6, -0.8, 00), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        #Se convierte la lista de vértices en un array de Numpy. El parámetro dtype='f4' especifica que el 
        # tipo de datos del array será de precisión simple
        #vertex_data = np.array(vertex_data, dtype='f4')
        vertices = [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1),
                    (-1,1,-1), (-1,-1,-1), (1,-1,-1), (1,1,-1)]
        
        indices = [(0,2,3), (0,1,2),
                   (1,7,2), (1,6,7),
                   (6,5,4), (4,7,6),
                   (3,4,5), (3,5,0),
                   (3,7,4), (3,2,7),
                   (0,6,1), (0,5,6),
                   ]
        vertex_data = self.get_data(vertices, indices)
        
        tex_coord = [(0,0), (1,0), (1,1), (0,1)]
        tex_coord_indices = [(0,2,3), (0,1,2),
                             (0,2,3), (0,1,2), 
                             (0,1,2), (2,3,0),
                             (2,3,0), (2,0,1),
                             (0,2,3), (0,1,2),
                             (3,1,2), (3,0,1)]
        
        
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)
        
        normals = [(0,0,1) * 6,
                    (1,0,0) * 6,
                    (0,0,-1) * 6,
                    (-1,0,0) * 6,
                    (0,1,0) * 6,
                    (0,-1,0) * 6,]
        
        normals = np.array(normals, dtype='f4').reshape(36, 3)
        vertex_data = np.hstack([normals, vertex_data])
        #concatena horizontalmente dos matrices NumPy: tex_coord_data y vertex_data.
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        
        return vertex_data
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
    def get_vbo(self):
        # Método para obtener el búfer de vértices
        vertex_data = self.get_vertex_data()
        #VBO es un objeto de OpenGL que contiene un buffer de datos de vértices almacenados en la memoria de la GPU
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_vao(self):
        #El vao encapsula toda la configuración necesaria para renderizar un objeto
        # Método para obtener el array de vértices
        #toma un shader program y una lista que describe cómo los datos de los vértices almacenados en los VBOs 
        # se relacionan con los atributos definidos en el shader program. Cada elemento de 
        # la lista es un tuple que contiene un VBO, el formato de los datos de los vértices y el nombre del atributo en el shader program.
       #ada vértice tiene dos componentes de coordenadas de textura seguidas de tres componentes de coordenadas de posición.
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f', 'in_texcoord_0', 'in_normal' ,'in_position')])  
        return vao
    
    def render(self):
        self.uptdate()
        # Método para renderizar el triángulo
        self.vao.render()
    
    def destroy(self):
        # Método para liberar los recursos del triángulo
        #Libreamos memoria para cada uno de los objemos que creamos y le asignamos
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
