import os
import pyglet
import trimesh
from pyglet.gl import *
from pyglet.window import key

# Configuración de la ventana
window = pyglet.window.Window(800, 600, "3D Model Viewer")

# Configuración de la escena
scene = pyglet.graphics.Batch()

# Obtener la ruta del archivo .obj dentro del directorio 'LibertyStatue'
base_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_path, 'LibertyStatue', 'LibertStatue.obj')

# Cargar el modelo usando trimesh
mesh = trimesh.load(model_path)

# Convertir el modelo a una lista de vértices y caras para pyglet
vertices = mesh.vertices.flatten()
faces = mesh.faces.flatten()

# Crear un objeto vertex_list para renderizar el modelo
vertex_list = scene.add_indexed(len(vertices) // 3,
                                GL_TRIANGLES,
                                None,
                                faces,
                                ('v3f', vertices))

@window.event
def on_draw():
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(30, 1, 0, 0)
    scene.draw()

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def main():
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()

if __name__ == "__main__":
    main()
