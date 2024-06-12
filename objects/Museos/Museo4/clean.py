# Nombre del archivo OBJ original
archivo_original = 'modelo.obj'

# Nombre del archivo donde se guardará la versión editada
archivo_editado = 'modelo_editado.obj'

# Abre el archivo original para lectura y el archivo editado para escritura
with open(archivo_original, 'r') as archivo_entrada, open(archivo_editado, 'w') as archivo_salida:
    # Itera sobre cada línea del archivo original
    for linea in archivo_entrada:
        # Si la línea no comienza con 's', escríbela en el archivo editado
        if not linea.startswith('s'):
            archivo_salida.write(linea)

print("Edición completa. El archivo editado se ha guardado como:", archivo_editado)
