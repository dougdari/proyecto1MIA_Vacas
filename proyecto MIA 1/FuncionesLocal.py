import os.path
import os
import regex as re
import shutil

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
    
    def comandoCopiar(self,rutaFrom,rutaTo):
        pass
    
    def comandoTransferir(self,rutaFrom,rutaTo,Modo):
        if os.path.isfile(rutaFrom):
        #En caso de ser directorio de archivo
            shutil.move(rutaFrom,rutaTo)
        #En caso de ser directorio de carpeta
        else:
            #Se revisa cada directorio con sus respectivos archivos o subcarpetas
            print("En carpetas")
        pass

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
    
    def comandoModificar(self,ruta,nuevo_contenido):
        if os.path.exists("."+ruta):
            f = open("."+ruta,"w")
            f.write(nuevo_contenido)
            f.close()
    
    def comandoAgregar(self,ruta,contenido_extra):
        if os.path.exists("."+ruta):
            f = open("."+ruta,"a")
            f.write(contenido_extra)
            f.close()

    def crear_ruta(self,ruta):
        partes = ruta.split("/")
        partes.remove("")
        rta = "./"
        for x in partes:
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


fun = FLocal()
#fun.comandoCopiar("./carpeta1/","./carpeta2/")
fun.comandoTransferir("./carpeta1/","","")
#FORMATO DE ENTRADA
#fun.comandoCrear("Archivo1.txt","Archivo de Prueba","carpeta1")
#fun.crear_ruta("/carpeta1/carpeta2/carpeta3/archivo.txt")


