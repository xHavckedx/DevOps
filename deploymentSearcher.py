import os
import sys
# developer: leo.gomez(CTT)
# Carpeta en la que deseas buscar archivos
carpeta_raiz = './'

# Patrón que deseas buscar en el contenido de los archivos
patron = sys.argv[1]

# Lista para almacenar las rutas de los archivos que coinciden con el patrón
archivos_coincidentes = []

if len(sys.argv) != 2:
    print("Uso: python deploymentSearcher.py <patron>")
    print("El script empieza a buscar en la localización del mismo.")
    sys.exit(1)
else:
    # Itera sobre los directorios dentro de la carpeta raíz
    for directorio, subdirectorios, archivos in os.walk(carpeta_raiz):
        # Itera sobre los archivos en el directorio actual
        for nombre_archivo in archivos:
            # Ruta completa del archivo
            ruta_archivo = os.path.join(directorio, nombre_archivo)
            
            # Verifica si el archivo es un archivo regular (no un directorio)
            if os.path.isfile(ruta_archivo):
                # Lee el contenido del archivo
                with open(ruta_archivo, 'r') as archivo:
                    contenido = archivo.read()
                    
                    # Verifica si el patrón está en el contenido del archivo
                    if patron in contenido:
                        archivos_coincidentes.append(ruta_archivo)

    # Imprime las rutas de los archivos que coinciden con el patrón
    for archivo in archivos_coincidentes:
        print(archivo.replace("./", ""))
    sys.exit(0)

    

