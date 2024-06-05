
import pywavefront
import numpy as np
import moderngl as mgl

class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['eiffel'] = EiffelVBO(ctx)
        self.vbos['coliseo'] = ColiseoVBO(ctx)
        
    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]
        


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attrib: list = None
        
    def get_vbo(self):
        # Método para obtener el búfer de vértices
        vertex_data = self.get_vertex_data()
        #VBO es un objeto de OpenGL que contiene un buffer de datos de vértices almacenados en la memoria de la GPU
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        self.vbo.release()
        
class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal' ,'in_position']
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
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

class ColiseoVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
    
    def get_vertex_data(self):
        
        try:
            objs = pywavefront.Wavefront('objects/Coliseo/10064_colosseum_v1_Iteration0.obj', cache=True, parse=True)
            obj = objs.materials.popitem()[1]
            vertex_data = obj.vertices
            vertex_data = np.array(vertex_data, dtype='f4')
        except Exception as e:
            print("Error:", e)
            
        return vertex_data
    
class EiffelVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
    
    def get_vertex_data(self):
        
        try:
            objs = pywavefront.Wavefront('objects/Eiffel/10067_Eiffel_Tower_v1_max2010_it1.obj', cache=True, parse=True)
            obj = objs.materials.popitem()[1]
            vertex_data = obj.vertices
            vertex_data = np.array(vertex_data, dtype='f4')
        except Exception as e:
            print("Error:", e)
            
        return vertex_data
    

        
        