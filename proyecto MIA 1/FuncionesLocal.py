import os.path
import os
import regex as re
class FLocal:
    def __init__(self):
        pass

    def comandoCrear(self,nombre,contenido,ruta):
        self.crear_ruta(ruta)
        if not os.path.exists("."+ruta+nombre):
            f = open("."+ruta+nombre,"x")
            f.write(contenido)
            f.close()
    
    def comandoEliminar(self,nombre,ruta):
        if os.path.exists("."+ruta+nombre):
            os.remove("."+ruta+nombre)
    
    def comandoRenombrar(self,ruta,nuevo_nombre):
        #Se reestructura la ruta para el nuevo nombre
        partes = ruta.split("/")
        partes.remove("")
        rta = "./"
        for x in partes:
            if not re.search(".*\.txt",x):
                rta+=rta+x+"/"
            else:
                rta+=nuevo_nombre
                break
        if os.path.exists("."+ruta):
            os.rename("."+ruta,rta)
        

    def crear_ruta(self,ruta):
        partes = ruta.split("/")
        partes.remove("")
        rta = "./"
        for x in partes:
            rta=rta+x+"/"
            if not os.path.exists(rta) and not re.search(".*\.txt",x):
                os.makedirs(rta)

fun = FLocal()
#FORMATO DE ENTRADA
#fun.comandoCrear("Archivo1.txt","Archivo de Prueba","carpeta1")
#fun.crear_ruta("/carpeta1/carpeta2/carpeta3/archivo.txt")


