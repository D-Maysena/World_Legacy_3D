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

        n, s = 80, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))

        add(Coliseo(app, pos=(-20, -2, -10), scale=(0.002, 0.002, 0.002)))
        add(Eiffel(app, pos=(20, -2, -10), scale=(0.0006, 0.0006, 0.0006)))
        add(PisaTower(app, pos=(0, -1, -5)))
        add(Catedral(app, pos=(10, -2, -5)))
        add(Estatua(app, pos=(0, 10, -10)))
        add(Estatua2(app, pos=(5, 10, -10)))
        add(Bigben(app, pos=(0, -2, -10)))
        add(moai(app, pos=(-4, -2, -10)))

        # Add lights
        self.add_light(self.app.light)
        self.add_light(AdditionalLight(position=(0, -3, -10), color=(1.0, 0.0, 0.0)))
        self.add_light(AdditionalLight2(position=(0, 20, -10), color=(1, 0.5, 0.5)))

    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()

