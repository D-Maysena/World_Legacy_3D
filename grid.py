import matplotlib.pyplot as plt
import numpy as np
import moderngl as mgl
import pywavefront

# Vértices del primer polígono
vertices = [
    [-43.8833, -76.0611],    
    [0.263605, -76.5851],        
    [43.8734, -76.213],        
    [66.3642, -38.2353],    
    [88.1478, 0.119104],    
    [65.9365, 38.1454],
    [43.8008, 76.1551],    
    [-0.0865726, 76.4481],    
    [-44.1507, 76.1202],
    [-66.0662, 38.0696],    
    [-87.9573, -0.117065],
    [-65.9321, -38.1097]
]

# Vértices del segundo polígono
verticesDentro = [
    [82.7697, -143.536],
    [124.845, -71.977],                
    [166.019, 0.0909767],
    [124.586, 71.9508],
    [82.9028, 143.642],
    [0.0916456, 143.655],
    [-82.9764, 143.754],          
    [-124.303, 71.7788],
    [-165.67, -0.0152953],
    [-124.435, -71.8302],
    [-82.7932, -143.398],
    [0.0952417, -143.648]
]

objs = pywavefront.Wavefront('objects/Museos/Museo4/modelo_editado.obj', cache=True, parse=True)
obj = objs.materials.popitem()[1]
vertex_data = obj.vertices
vertex_data = np.array(vertex_data, dtype='f4')
print("vertices")
verticesDentro = [(v[0], v[2]) for v in vertex_data.reshape(-1, 3)]  # Suponiendo que el modelo tiene vértices (x, y, z)
print(verticesDentro)


        # Extraer las coordenadas x e y (z en lugar de y)
x_coords1 = [v[0] for v in verticesDentro]
y_coords1 = [v[1] for v in verticesDentro]  # Aquí debería ser z, que corresponde a la coordenada y en el plano 2D

        # Añadir el primer vértice al final para cerrar el polígono
x_coords1.append(verticesDentro[0][0])
y_coords1.append(verticesDentro[0][1])


fig, ax = plt.subplots()

# Trazar el primer polígono
ax.plot(x_coords1, y_coords1, marker='o', label='Polígono 1')

# Trazar el segundo polígono

# Configurar los ejes para tener la misma escala
ax.set_aspect('equal')

# Añadir una cuadrícula para mejor visualización
ax.grid(True)

# Añadir una leyenda
ax.legend()

# Mostrar la figura
plt.show()
