import os.path
import os
import regex as re
import shutil
from shutil import rmtree

class FLocal:
    directorio_archivo = "./Archivo"
    def __init__(self):
        pass

    def comandoCrear(self,nombre,contenido,ruta):
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        #Se explora la ruta para crear las carpetas necesarias
        self.crear_ruta(nueva_ruta)
        #Se crea el archivo y se detecta si no existe uno con nombre igual
        if os.path.exists(nueva_ruta+nombre):
            nombre = nombre+"(1)"
        f = open(nueva_ruta+nombre,"x")
        f.write(contenido)
        f.close()
    
    def comandoEliminar(self,nombre,ruta):
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        #Se unen todos los parametros para crear el directorio
        ruta_eliminar = nueva_ruta+nombre
        print(ruta_eliminar)
        #Se verifica la existencia de la ruta a eliminar
        if os.path.exists(ruta_eliminar):
            #Se determina si el directorio corresponde a un archivo para elegir como elimnar dicho directorio
            if os.path.isfile(ruta_eliminar):
                os.remove(ruta_eliminar)
            else:
                rmtree(ruta_eliminar)

    def comandoRenombrar(self,ruta,nuevo_nombre):
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        #Se reestructura la ruta para el nuevo nombre
        partes = nueva_ruta.split("/")
        nueva_partes = [x for x in partes if x != '']
        rta = ""
        for x in nueva_partes:
            if not re.search(".*\.txt",x):
                rta=rta+x+"/"
            else:
                rta+=nuevo_nombre
                break
        #Se comparan las rutas para verificar que no se repitan
        if nueva_ruta != rta:
            if os.path.exists(nueva_ruta):
                os.rename(nueva_ruta,rta)
    
    def comandoModificar(self,ruta,nuevo_contenido):
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        if os.path.exists(nueva_ruta):
            f = open(nueva_ruta,"w")
            f.write(nuevo_contenido)
            f.close()
    
    def comandoAgregar(self,ruta,contenido_extra):
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        if os.path.exists(nueva_ruta):
            f = open(nueva_ruta,"a")
            f.write(contenido_extra)
            f.close()

    def crear_ruta(self,ruta):
        partes = ruta.split("/")
        nueva_partes = [x for x in partes if x != '']
        rta = ""
        for x in nueva_partes:
            rta=rta+x+"/"
            if not os.path.exists(rta) and not re.search(".*\.txt",x):
                os.makedirs(rta)

    def transferir_archivos_directorio(self, origen, destino):

        if os.path.isdir(origen):
            if os.path.isdir(destino):

                print('entra')

                nombre_carpeta = os.path.basename(os.path.dirname(origen))
                ruta_nueva = str(destino) + str(nombre_carpeta)
                        
                if os.path.exists(ruta_nueva):

                    print('entra')

                    contador = 1
                    nombre_carpeta_original = os.path.basename(os.path.dirname(origen))
                    nuevo_nombre_carpeta = nombre_carpeta_original + "(" + str(contador) + ")"

                    print(str(destino) + str(nuevo_nombre_carpeta))
                
                    while os.path.exists(str(destino) + str(nuevo_nombre_carpeta)):

                        contador = contador + 1
                        nuevo_nombre_carpeta = str(nombre_carpeta_original) + "(" + str(contador) + ")"

                    nueva_ruta_nombre_y_ruta_nuevo_archivo = os.path.join(destino, nuevo_nombre_carpeta)
                    shutil.copytree(origen, nueva_ruta_nombre_y_ruta_nuevo_archivo)

                else:

                    print('entra2')
                    print("Transfiriendo carpeta")
                    print(origen)
                    print(destino)
                    shutil.copytree(origen, str(destino) + nombre_carpeta)

            else:
                print("Ruta destino no existe")
                print("Intentando crear")
                os.makedirs(destino)
                print("directorio creado")
                self.transferir_archivos_directorio(origen,destino)

        elif os.path.isfile(origen):

            if os.path.isdir(destino):

                if os.path.exists(origen):            

                    nombre_archivo = os.path.basename(origen)

                    #print(str(destino) + str(nombre_archivo))
            
                    if os.path.exists(str(destino) + str(nombre_archivo)):

                        print("El archivo existe")

                        contador = 1

                        nombre_archivo_original = os.path.splitext(os.path.basename(origen))[0]
                        nuevo_nombre_archivo = nombre_archivo_original + "(" + str(contador) + ")"
                        extencion_archivo = os.path.splitext(os.path.basename(origen))[1]

                        print(str(destino) + str(nuevo_nombre_archivo)  + str(extencion_archivo))
                    

                        while os.path.exists(str(destino) + str(nuevo_nombre_archivo)  + str(extencion_archivo)):

                            contador = contador + 1
                            nuevo_nombre_archivo = str(nombre_archivo_original) + "(" + str(contador) + ")"
                        

                        nuevo_nombre_archivo = nuevo_nombre_archivo + extencion_archivo
                        
                        destino = os.path.join(destino, nuevo_nombre_archivo)
                        shutil.copy2(origen, destino)
                    
                    else:
        
                        nueva_ruta_nombre_y_ruta_nuevo_archivo = os.path.join(destino, nombre_archivo)
                        shutil.copy2(origen, nueva_ruta_nombre_y_ruta_nuevo_archivo)
            
                else:

                    print("El archivo no existe")
            else:
                print("La ruta destino no exite")
                print("Intentando crear")
                os.makedirs(destino)
                print("directorio creado")
                self.transferir_archivos_directorio(origen,destino)
        else:
            print("No encontro nada ni directorio ni archivo")

    def copiar_archivos_directorio(self, origen, destino):

        if os.path.isdir(origen):

            if os.path.isdir(destino):

                print('entra')

                nombre_carpeta = os.path.basename(os.path.dirname(origen))
                ruta_nueva = str(destino) + str(nombre_carpeta)
                        
                if os.path.exists(ruta_nueva):

                    print('entra')

                    contador = 1
                    nombre_carpeta_original = os.path.basename(os.path.dirname(origen))
                    nuevo_nombre_carpeta = nombre_carpeta_original + "(" + str(contador) + ")"
                    extencion_archivo = os.path.splitext(os.path.basename(origen))[1]

                    print(str(destino) + str(nuevo_nombre_carpeta))
                
                    while os.path.exists(str(destino) + str(nuevo_nombre_carpeta)):

                        contador = contador + 1
                        nuevo_nombre_carpeta = str(nombre_carpeta_original) + "(" + str(contador) + ")"

                    nueva_ruta_nombre_y_ruta_nuevo_archivo = os.path.join(destino, nuevo_nombre_carpeta)
                    shutil.copytree(origen, nueva_ruta_nombre_y_ruta_nuevo_archivo)
                    shutil.rmtree(origen)

                else:

                    print('entra2')
                    print("Copiando carpeta")
                    print(origen)
                    print(destino)
                    shutil.copytree(origen, str(destino) + nombre_carpeta)
                    shutil.rmtree(origen)

            else:
                print("Ruta destino no existe")

        elif os.path.isfile(origen):

            if os.path.isdir(destino):

                if os.path.exists(origen):            

                    nombre_archivo = os.path.basename(origen)

                    #print(str(destino) + str(nombre_archivo))
            
                    if os.path.exists(str(destino) + str(nombre_archivo)):

                        print("El archivo existe")

                        contador = 1

                        nombre_archivo_original = os.path.splitext(os.path.basename(origen))[0]
                        nuevo_nombre_archivo = nombre_archivo_original + "(" + str(contador) + ")"
                        extencion_archivo = os.path.splitext(os.path.basename(origen))[1]

                        print(str(destino) + str(nuevo_nombre_archivo)  + str(extencion_archivo))
                    

                        while os.path.exists(str(destino) + str(nuevo_nombre_archivo)  + str(extencion_archivo)):

                            contador = contador + 1
                            nuevo_nombre_archivo = str(nombre_archivo_original) + "(" + str(contador) + ")"
                        

                        nuevo_nombre_archivo = nuevo_nombre_archivo + extencion_archivo
                        
                        destino = os.path.join(destino, nuevo_nombre_archivo)
                        shutil.copy2(origen, destino)
                        os.remove(origen)

                    else:
        
                        nueva_ruta_nombre_y_ruta_nuevo_archivo = os.path.join(destino, nombre_archivo)
                        shutil.copy2(origen, nueva_ruta_nombre_y_ruta_nuevo_archivo)
                        os.remove(origen)
            
                else:

                    print("El archivo no existe")
            else:
                print("La ruta destino no exite")
        else:
            print("No encontro nada ni directorio ni archivo")

    def limpiarRuta(self,ruta):
        partes = ruta.split("/")
        nueva_partes = [x for x in partes if x != '']
        rtalimpia = self.directorio_archivo+"/"
        for x in nueva_partes:
            if "\"" in x:
                x = x.replace('\"','')
            if not re.search(".*\.txt",x):
                rtalimpia = rtalimpia+x+"/"
            else:
                rtalimpia = rtalimpia+x
        return rtalimpia

fun = FLocal()
#fun.comandoCopiar("./carpeta1/","./carpeta2/")
#fun.comandoTransferir("./carpeta1/","","")
#FORMATO DE ENTRADA
#fun.comandoCrear("Archivo1.txt","Archivo de Prueba","carpeta1")
#fun.crear_ruta("/carpeta1/carpeta2/carpeta3/archivo.txt")


