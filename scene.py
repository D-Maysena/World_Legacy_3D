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
        add(Coliseo(app, pos=(25, 4.5, -150), scale=(0.00035, 0.00035, 0.00035)))
        add(Eiffel(app, pos=(-33, 4, 130), scale=(0.00030, 0.00030, 0.00030)))
        add(PisaTower(app, pos=(-126, 5, 60)))
        add(Catedral(app, pos=(118, 4, -80)))
        add(Estatua(app, pos=(-33, 4, -150)))
        add(Estatua2(app, pos=(-125, 4, -80)))
        add(Bigben(app, pos=(116, 4, 60)))
        add(moai(app, pos=(25, 4, 130)))
        add(museo4(app,pos=(-4,-0.99,-10), scale=(0.2,0.2,0.2)))
        
        #Pedestales
        add(Pedestal_bigben(app, pos=(116, -1, 60), rot=(-90,0, 180)))
        add(Pedestal_eiffel(app, pos=(-33, -1, 130)))
        add(Pedestal_coliseo(app, pos=(25, -1, -150)))
        add(Pedestal_pisatower(app, pos=(-126, -1, 60)))
        add(Pedestal_catedral(app, pos=(118, -1, -80)))
        add(Pedestal_estatua(app, pos=(-33, -1, -150)))
        add(Pedestal_estatua2(app, pos=(-125, -1, -80)))
        add(Pedestal_moai(app, pos=(25, -1, 130)))
        
        #Ambientes
        add(Estatua3(app, pos=(0, -1, 0)))
        add(Banco1(app, pos=(-4, -1, 62)))
        add(Banco2(app, pos=(-4, -1, -82)))
        add(Banco3(app, pos=(60, -1, 25)))
        add(Banco4(app, pos=(-68, -1, 25)))
        
        add(Arbol1(app, pos=(40, -1, 50)))
        add(Arbol2(app, pos=(-40, -1, 50)))
        add(Arbol3(app, pos=(-35, -1, -68)))
        add(Arbol4(app, pos=(27, -1, -68)))
        add(Arbol5(app, pos=(-68, -1, 1)))
        add(Arbol6(app, pos=(68, -1, 1)))
        

        # Add lights
        self.add_light(self.app.light)
        self.add_light(AdditionalLight(position=(0, -3, -10), color=(1.0, 0.0, 0.0)))
        self.add_light(AdditionalLight2(position=(0, 20, -10), color=(1, 0.5, 0.5)))


    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()

