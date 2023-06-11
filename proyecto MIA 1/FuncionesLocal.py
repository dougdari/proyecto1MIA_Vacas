import os.path
import os

class FLocal:
    def __init__(self):
        pass

    def comandoCrear(self,nombre,contenido,carpeta):

        #Creacion de carpeta en caso de no encontrar alguna
        if not os.path.exists("./"+carpeta):
            os.makedirs(carpeta)
        
        if not os.path.exists("./"+carpeta+"/"+nombre):
            f = open("./"+carpeta+"/"+nombre,"x")
            f.write(contenido)
            f.close()

fun = FLocal()
#FORMATO DE ENTRADA
fun.comandoCrear("Archivo1.txt","Archivo de Prueba","carpeta1")


