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
        add(Coliseo(app, pos=(-20,10, -10), scale=(0.002, 0.002, 0.002)))
        add(Eiffel(app, pos=(85,10, -20), scale=(0.0006, 0.0006, 0.0006)))
        
        add(PisaTower(app, pos=(0, 10, -5)))
        
        add(Catedral(app, pos=(10, 10, -5)))
        add(Estatua(app, pos=(0, 10, -10)))
        add(Estatua2(app, pos=(5, 10, -10)))
        
        add(Bigben(app, pos=(0, -2, -10)))
        add(moai(app,pos=(-4,10,-10)))
        add(museo4(app,pos=(-4,10,-10), scale=(0.2,0.2,0.2)))

    def render(self):
        for obj in self.objects:
            obj.render()