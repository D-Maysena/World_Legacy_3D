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
        
        #n, s = 30,2
        #for x in range(-n, n, s):
         #   for z in range (-n, n, s):
          #      add(Cube(app, pos=(x, -s, z)))
        
        add(Coliseo(app, pos=(-20,-2, -10), scale=(0.002, 0.002, 0.002)))
        add(Eiffel(app, pos=(20,-2, -10), scale=(0.0006, 0.0006, 0.0006)))
        #add(Cube(app, pos=(50,-2, -10), scale=(10,10,10)))
        
        add(PisaTower(app, pos=(0, -1, -5)))
        
        add(Catedral(app, pos=(10, -2, -5)))
        add(Estatua(app, pos=(0, 10, -10)))
        add(Estatua2(app, pos=(5, 10, -10)))
        
    
    def render(self):
        for obj in self.objects: 
            obj.render()