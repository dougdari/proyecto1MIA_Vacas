import os.path
import os
import regex as re
import shutil
from shutil import rmtree
import analizadorEntrada
from datetime import date
from datetime import datetime

class FLocal:
    directorio_archivo = "./Archivo"
    def __init__(self):
        pass

    def ejecutarComando(self,arreglo):
        if(arreglo[0][0].lower() == "configure"):
            print("Configurar")
        elif(arreglo[0][0].lower() == "create"):
            self.comandoCrear(arreglo[0][1],arreglo[0][3],arreglo[0][2])
        elif(arreglo[0][0].lower() == "delete"):
            self.comandoEliminar(arreglo[0][1],arreglo[0][2])
        elif(arreglo[0][0].lower() == "copy"):
            ruta_origen1 = self.limpiarRuta(arreglo[0][1])
            ruta_destino1 = self.limpiarRuta(arreglo[0][2])
            self.copiar_archivos_directorio(ruta_origen1,ruta_destino1)
        elif(arreglo[0][0].lower() == "transfer"):
            ruta_origen = self.limpiarRuta(arreglo[0][1])
            ruta_destino = self.limpiarRuta(arreglo[0][2])
            self.transferir_archivos_directorio(ruta_origen,ruta_destino,arreglo[0][3])
        elif(arreglo[0][0].lower() == "rename"):
            self.comandoRenombrar(arreglo[0][1],arreglo[0][2])
        elif(arreglo[0][0].lower() == "modify"):
            self.comandoModificar(arreglo[0][1],arreglo[0][2])
        elif(arreglo[0][0].lower() == "add"):
            self.comandoAgregar(arreglo[0][1],arreglo[0][2])
        elif(arreglo[0][0].lower() == "backup"):
            print("Respaldo")
        elif(arreglo[0][0].lower() == "exec"):
            self.ejecutarArchivo(arreglo[0][1])

    def ejecutarArchivo(self,ruta):
        archivo = open("."+ruta,"r")
        for linea in archivo:
            analizadorEntrada.comandos = []
            self.ejecutarComando(analizadorEntrada.parser.parse(linea, lexer=analizadorEntrada.lexer))
            
    def comandoCrear(self,nombre,contenido,ruta):
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        print(ruta)
        #Se explora la ruta para crear las carpetas necesarias
        self.crear_ruta(nueva_ruta)
        #Se crea el archivo y se detecta si no existe uno con nombre igual
        if os.path.exists(nueva_ruta+nombre):
            nombre = nombre+"(1)"
        f = open(nueva_ruta+nombre,"x")
        f.write(contenido)
        f.close()
        #Se crea el contenido para la bitacora
        input_bt = "create -name:"+nombre+" -path:"+ruta+" -body:"+contenido
        output_bt = "Archivo Creado Exitosamente"
        self.generar_registro(input_bt,output_bt)

    def comandoEliminar(self,nombre,ruta):
        input_bt = "delete -name:"+nombre+" -path:"+ruta
        output_bt = "Archivo Eliminado Exitosamente"
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        #Se unen todos los parametros para crear el directorio
        ruta_eliminar = nueva_ruta+nombre
        #Se verifica la existencia de la ruta a eliminar
        if os.path.exists(nueva_ruta):
            if os.path.exists(ruta_eliminar):
            #Se determina si el directorio corresponde a un archivo para elegir como elimnar dicho directorio
                if os.path.isfile(ruta_eliminar):
                    os.remove(ruta_eliminar)
                else:
                    rmtree(ruta_eliminar)
            else:
                output_bt = "El Archivo No Existe"
        else:
            output_bt = "El Directorio No Existe"
        self.generar_registro(input_bt,output_bt)
        
    def comandoRenombrar(self,ruta,nuevo_nombre):
        input_bt = "rename -path:"+ruta+" -name:"+nuevo_nombre
        output_bt = "Archivo Renombrado Exitosamente"
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
                dir_carpeta = rta
                rta+=nuevo_nombre
                break
        continuar = True
        if os.path.exists(nueva_ruta):
            #Se compara archivo existentes para verificar si no se repiten
            for x in os.listdir(dir_carpeta):
                if(x == nuevo_nombre):
                    continuar = False
                    break
            if continuar:
                os.rename(nueva_ruta,rta)
            else:
                output_bt = "Imposible Renombrar, Existe un Archivo con el mismo nombre"
        else:
            output_bt = "Imposible de Renombrar, El Directorio o Archivo No Existe"
        self.generar_registro(input_bt,output_bt)
        
    def comandoModificar(self,ruta,nuevo_contenido):
        input_bt = "rename -path:"+ruta+" -body:"+nuevo_contenido
        output_bt = "Archivo Modificado Exitosamente"
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        if os.path.exists(nueva_ruta):
            f = open(nueva_ruta,"w")
            f.write(nuevo_contenido)
            f.close()
        else:
            output_bt = "El Directorio o Archivo No Existe"
        self.generar_registro(input_bt,output_bt)
    
    def comandoAgregar(self,ruta,contenido_extra):
        input_bt = "add -path:"+ruta+" -body:"+contenido_extra
        output_bt = "Contenido Agregado al Archivo Exitosamente"
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = self.limpiarRuta(ruta)
        if os.path.exists(nueva_ruta):
            f = open(nueva_ruta,"a")
            f.write("\n"+contenido_extra)
            f.close()
        else:
            output_bt = "El Directorio o Archivo No Existe"
        self.generar_registro(input_bt,output_bt)
        
    def crear_ruta(self,ruta):
        partes = ruta.split("/")
        nueva_partes = [x for x in partes if x != '']
        rta = ""
        for x in nueva_partes:
            rta=rta+x+"/"
            if not os.path.exists(rta) and not re.search(".*\.txt",x):
                os.makedirs(rta)

    def transferir_archivos_directorio(self, origen, destino,modo):
        input_bt = "transfer -from:"+origen+" -to:"+destino
        output_bt = "Archivo o Carpeta Transferido Exitosamente"
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
                    output_bt = "El archivo o directorio a transferir no existe"
            else:
                output_bt = "La ruta destino no exite"
                #print("Intentando crear")
                os.makedirs(destino)
                #print("directorio creado")
                self.transferir_archivos_directorio(origen,destino)
        else:
            output_bt ="No se encontró nada en el directorio: "+origen+"para mover a: "+destino
        self.generar_registro(input_bt,output_bt)

    def copiar_archivos_directorio(self, origen, destino):
        input_bt = "copy -from:"+origen+" -to:"+destino
        output_bt = "Archivo o Carpeta copiado Exitosamente"
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
                    output_bt = "El archivo o directorio a copiar no existe"
            else:
                output_bt = "La ruta destino no existe"
        else:
            output_bt = "No se encontró nada en el directorio: "+origen+"para mover a: "+destino
        self.generar_registro(input_bt,output_bt)

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
    
    def llenar_log(self,contenido):
        ruta = "/logs/"+str(date.today())+"/"
        #Se comprueba la existencia del directorio
        if not os.path.exists(self.directorio_archivo+ruta):
            nombre = "log_archivos.txt"
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
        else:
            f = open(self.directorio_archivo+ruta+"log_archivos.txt","a")
            f.write(contenido)
            f.close()
            
    def generar_registro(self,entrada,salida):
        tiempo = datetime.now()
        tiempo_string = tiempo.strftime("%d/%m/%Y %H:%M:%S")
        cnt_bitacora = tiempo_string + " - Input - "+entrada+"\n"
        cnt_bitacora += tiempo_string + " - Output - "+salida+"\n"
        self.llenar_log(cnt_bitacora)

    
fun = FLocal()
#fun.comandoCopiar("./carpeta1/","./carpeta2/")
#fun.comandoTransferir("./carpeta1/","","")
#FORMATO DE ENTRADA
#fun.comandoCrear("Archivo1.txt","Archivo de Prueba","carpeta1")
#fun.crear_ruta("/carpeta1/carpeta2/carpeta3/archivo.txt")


