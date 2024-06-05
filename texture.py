import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/box.jpg')
        self.textures[1] = self.get_texture(path='textures/texture.jpg')
        self.textures['eiffel'] = self.get_texture(path='objects/Eiffel/10067_Eiffel_Tower_v1_diffuse.JPG')
        self.textures['coliseo'] = self.get_texture(path='objects/Coliseo/10064_colosseum_diffuse.jpg')
        
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