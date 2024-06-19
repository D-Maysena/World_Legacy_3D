import numpy as np
import moderngl as mgl
import pywavefront

class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['eiffel'] = EiffelVBO(ctx)
        self.vbos['coliseo'] = ColiseoVBO(ctx)
        self.vbos['pisatower'] = PisaTowerVBO(ctx)
        self.vbos['catedral'] = CatedralVBO(ctx)
        self.vbos['estatua'] = EstatuaVBO(ctx)
        self.vbos['bigben'] = bigbenVBO(ctx)
        self.vbos['moai'] = moaiVBO(ctx)
        self.vbos['estatua2'] =  Estatua2VBO(ctx)
        self.vbos['skybox'] = SkyBoxVBO(ctx)
        self.vbos['advanced_skybox'] = AdvancedSkyBoxVBO(ctx)
        self.vbos['estatua2'] =  Estatua2VBO(ctx)
        self.vbos['museo3'] =  museo3VBO(ctx)
        self.vbos['museo4'] =  museo4VBO(ctx)
        #################################################################
        self.vbos['pedestal_bigben'] =  Pedestal_bigbenVBO(ctx)
        self.vbos['pedestal_eiffel'] =  Pedestal_eiffelVBO(ctx)
        self.vbos['pedestal_coliseo'] =  Pedestal_coliseoVBO(ctx)
        self.vbos['pedestal_pisatower'] =  Pedestal_pisatowerVBO(ctx)
        self.vbos['pedestal_catedral'] =  Pedestal_catedralVBO(ctx)
        self.vbos['pedestal_estatua'] =  Pedestal_estatuaVBO(ctx)
        self.vbos['pedestal_estatua2'] =  Pedestal_estatua2VBO(ctx)
        self.vbos['pedestal_moai'] =  Pedestal_moaiVBO(ctx)
        ################################################################
        self.vbos['estatua3'] =  Estatua3_AVBO(ctx)
        self.vbos['banco1'] =  Banco1_VBO(ctx)
        self.vbos['banco2'] =  Banco2_VBO(ctx)
        self.vbos['banco3'] =  Banco3_VBO(ctx)
        self.vbos['banco4'] =  Banco4_VBO(ctx)
        self.vbos['arbol1'] =  Arbol1_VBO(ctx)
        self.vbos['arbol2'] =  Arbol2_VBO(ctx)
        self.vbos['arbol3'] =  Arbol3_VBO(ctx)
        self.vbos['arbol4'] =  Arbol4_VBO(ctx)
        self.vbos['arbol5'] =  Arbol5_VBO(ctx)
        self.vbos['arbol6'] =  Arbol6_VBO(ctx)
        
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

class PisaTowerVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/pisatower/10076_pisa_tower_v1_max2009_it0.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
class CatedralVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/catedral/10086_saint_basil_cathedral_v1_L3.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data


class EstatuaVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        
    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/10085_egypt_sphinx_V2_L3.123cedbb80cc-eec4-4899-a587-d46dd8eff3b9/10085_egypt_sphinx_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class Estatua2VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        
    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Statue_v1_L2.123cc93d694a-81fb-4c81-8a75-7fa010dfa777/12330_Statue_v1_L2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class bigbenVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/bigben/10059_big_ben_v2_max2011_it1.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

class moaiVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/moai/10805_Moai_L3.mb.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
    # Pedestales #######################################################################################################################################################
    
    
class Pedestal_bigbenVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Pedestal_eiffelVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Pedestal_coliseoVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Pedestal_pisatowerVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Pedestal_catedralVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class Pedestal_estatuaVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Pedestal_estatua2VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class Pedestal_moaiVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Pedestal/10421_square_pedastal_iterations-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
    ################################################################################################################################################################
    
    #Ambiente

class Estatua3_AVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Estatua_A/12328_Statue_v1_L2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
    
class Banco1_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Banco/ConcreteBench-L3.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Banco2_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Banco/ConcreteBench-L3.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class Banco3_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Banco/ConcreteBench-L3.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    

    
    
class Banco4_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Banco/ConcreteBench-L3.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class Arbol1_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Arbol/10446_Palm_Tree_v1_max2010_iteration-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

class Arbol2_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Arbol/10446_Palm_Tree_v1_max2010_iteration-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class Arbol3_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Arbol/10446_Palm_Tree_v1_max2010_iteration-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Arbol4_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Arbol/10446_Palm_Tree_v1_max2010_iteration-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class Arbol5_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Arbol/10446_Palm_Tree_v1_max2010_iteration-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
class Arbol6_VBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/Arbol/10446_Palm_Tree_v1_max2010_iteration-2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
    
    
    ################################################################################
    
class SkyBoxVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order='C')
        return vertex_data


class AdvancedSkyBoxVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    def get_vertex_data(self):
        # in clip space
        z = 0.9999
        vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
        vertex_data = np.array(vertices, dtype='f4')
        return vertex_data

class museo3VBO(BaseVBO):
        def __init__(self, app):
            super().__init__(app)
            self.format = '2f 3f 3f'
            self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

        def get_vertex_data(self):
            objs = pywavefront.Wavefront('objects/Museos/Museo3/modelo_editado.obj', cache=True, parse=True)
            obj = objs.materials.popitem()[1]
            vertex_data = obj.vertices
            vertex_data = np.array(vertex_data, dtype='f4')
            return vertex_data
        
class museo4VBO(BaseVBO):
        def __init__(self, app):
            super().__init__(app)
            self.format = '2f 3f 3f'
            self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

        def get_vertex_data(self):
            objs = pywavefront.Wavefront('objects/Museos/Museo4/modelo_editado.obj', cache=True, parse=True)
            obj = objs.materials.popitem()[1]
            vertex_data = obj.vertices
            vertex_data = np.array(vertex_data, dtype='f4')
            return vertex_data

