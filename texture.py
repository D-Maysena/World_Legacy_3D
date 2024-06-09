import pygame as pg
import moderngl as mgl
class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/box.jpg')
        self.textures[1] = self.get_texture(path='textures/texture.jpg')
        
        self.textures[3] = self.get_texture(path='textures/alfombra1.png')
        self.textures[4] = self.get_texture(path='textures/alfombra2.png')
        self.textures[5] = self.get_texture(path='textures/alfombra3.png')
        self.textures[6] = self.get_texture(path='textures/alfombra4.png')
        self.textures['eiffel'] = self.get_texture(path='objects/Eiffel/10067_Eiffel_Tower_v1_diffuse.JPG')
        self.textures['coliseo'] = self.get_texture(path='objects/Coliseo/10064_colosseum_diffuse.jpg')
        self.textures['pisatower'] = self.get_texture(path='objects/pisatower/10076_pisa_tower_v1_diffuse.jpg')
        self.textures['catedral'] = self.get_texture(path='objects/catedral/10086_saint_basil_cathedral_v1_diffuse.jpg')
        self.textures['estatua'] = self.get_texture(path='objects/10085_egypt_sphinx_V2_L3.123cedbb80cc-eec4-4899-a587-d46dd8eff3b9/10085_egyptSphinxDiffuseMap.jpg')
        self.textures['estatua2'] = self.get_texture(path='objects/Statue_v1_L2.123cc93d694a-81fb-4c81-8a75-7fa010dfa777/DavidFixedDiff.jpg')
        self.textures['bigben'] = self.get_texture(path='objects/bigben/10059_big_ben_v1_diffuse.jpg')
        self.textures['moai'] = self.get_texture(path='objects/moai/txtr02.jpg')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox1/', ext='png')

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube
    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, 
                                   data=pg.image.tostring(texture, 'RGB'))
        
        #mipmaps
        #Los mipmaps son versiones precalculadas de una textura en diferentes niveles de resolución. 
        #Ayudan a mejorar el rendimiento y la calidad visual al renderizar objetos lejanos.
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        #genera los mipmaps para la textura. Esto implica crear versiones más pequeñas de la textura original a diferentes niveles de resolución.
        texture.build_mipmaps()

        #La anisotropía mejora la calidad de la textura al reducir el efecto de aliasing en ángulos oblicuos
        texture.anisotropy = 32.0
        return texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]    
