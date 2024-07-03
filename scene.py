from model import *
from light import Light, AdditionalLight, AdditionalLight2

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.lights = []
        self.load()
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)

    def load(self):
        app = self.app
        add = self.add_object

        n, s = 100, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))
        add(Coliseo(app, pos=(26, 5.5, -136), scale=(0.00035, 0.00035, 0.00035)))
        add(Eiffel(app, pos=(-33, 5, 137), scale=(0.00030, 0.00030, 0.00030)))
        add(PisaTower(app, pos=(-126, 6, 60)))
        add(Catedral(app, pos=(116, 5, -73)))
        add(Estatua(app, pos=(-39, 5, -136)))
        add(Estatua2(app, pos=(-111, 5, -81)))
        add(Bigben(app, pos=(120, 5, 63)))
        add(moai(app, pos=(25, 5, 136)))
        add(museo4(app,pos=(0,0,0), scale=(0.2,0.2,0.2)))
        
        #Pedestales
        add(Pedestal_bigben(app, pos=(120, 0, 63), rot=(-90,0, 180)))
        add(Pedestal_eiffel(app, pos=(-33, 0, 137)))
        add(Pedestal_coliseo(app, pos=(26, 0, -136)))
        add(Pedestal_pisatower(app, pos=(-126, 0, 60)))
        add(Pedestal_catedral(app, pos=(116, 0, -73)))
        add(Pedestal_estatua(app, pos=(-39, 0, -136)))
        add(Pedestal_estatua2(app, pos=(-111, 0, -81)))
        add(Pedestal_moai(app, pos=(25, 0, 136)))
        
        #Ambientes
        add(Estatua3(app, pos=(0, -1, 0)))
        add(Banco1(app, pos=(-4, -1, 73)))
        add(Banco2(app, pos=(-4, -1, -73)))
        add(Banco3(app, pos=(69, -1, 27)))
        add(Banco4(app, pos=(-70, -1, 25)))
        
        add(Arbol1(app, pos=(40, -1, 50)))
        add(Arbol2(app, pos=(-40, -1, 50)))
        add(Arbol3(app, pos=(-35, -1, -68)))
        add(Arbol4(app, pos=(27, -1, -68)))
        add(Arbol5(app, pos=(-68, -1, 1)))
        add(Arbol6(app, pos=(68, -1, 1)))
        
        
        add(Castillo(app, pos=(45, -1, -40)))
        add(Columpio(app, pos=(-50, -1, -40)))
        add(Mujer(app, pos=(8, -1, 8)))


        # Add lights
        self.add_light(self.app.light)
        self.add_light(AdditionalLight(position=(0, -3, -10), color=(1.0, 0.0, 0.0)))
        self.add_light(AdditionalLight2(position=(0, 20, -10), color=(1, 0.5, 0.5)))


    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()