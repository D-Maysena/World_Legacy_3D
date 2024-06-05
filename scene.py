from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # n, s = 30, 3
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))

        add(PisaTower(app, pos=(0, -1, -5)))
        
        add(Catedral(app, pos=(10, -2, -5)))

    def render(self):
        for obj in self.objects:
            obj.render()