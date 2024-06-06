import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/ceramica.png')
        self.textures[1] = self.get_texture(path='textures/foto2.png')
        self.textures[2] = self.get_texture(path='textures/foto3.png')
        self.textures['estatua'] = self.get_texture(path='objects/10085_egypt_sphinx_V2_L3.123cedbb80cc-eec4-4899-a587-d46dd8eff3b9/10085_egyptSphinxDiffuseMap.jpg')
        
        self.textures['estatua2'] = self.get_texture(path='objects/Statue_v1_L2.123cc93d694a-81fb-4c81-8a75-7fa010dfa777/DavidFixedDiff.jpg')
        
        
        
    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        
        #mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        #AF
        texture.anisotropy = 32.0
        return texture

        
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]