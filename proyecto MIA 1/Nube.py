from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import regex as re
import os

direc_credenciales = 'credentials_module.json'
id_folder = '1ba5thhoBgCP04YAXIeIWeRZg9YMmFT_P'


class NubeCm:
    def iniciosesion(self,):
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = direc_credenciales
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(direc_credenciales)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile(direc_credenciales)
        credenciales = GoogleDrive(gauth)
        return credenciales

    def crear_archivo_texto(self,file_name, content,id_folder):
        credenciales = self.iniciosesion()
        arch = credenciales.CreateFile({'title': file_name,
                                        'parents': [{"kind":"drive#fileLink",
                                                    "id":id_folder}]})
        arch.SetContentString(content)
        arch.Upload()
        pass

    def encontrar_directorio(self,credenciales, raiz, carpeta_nombre):

        obtener_archivos = f"'{raiz}' in parents and title = '{carpeta_nombre}' and mimeType = 'application/vnd.google-apps.folder' and trashed=false"
        archivos_carpetas = credenciales.ListFile({'q': obtener_archivos}).GetList()
        if len(archivos_carpetas) > 0:
            return True, archivos_carpetas[0]['id']
        else:
            return False, None

    def agregar_carpeta(self,credenciales, raiz, carpeta_nombre):

        agregar_directorio = {'title': carpeta_nombre, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': raiz}]}
        credenciales.CreateFile(agregar_directorio).Upload()

    def recorrer_ruta_agregar_archivo(self,raiz, credenciales, ruta):

        if ruta[0] == '/':
            ruta = ruta[ 1:len(ruta)]

        if ruta[len(ruta)-1] == '/':
            ruta = ruta[ 0:len(ruta) -1]

        carpetas_anidadas = ruta.split('/')    
        auxRaiz = raiz

        for subCarpeta in carpetas_anidadas:

            SeEncontro, subcarpetaRaiz = self.encontrar_directorio(credenciales, auxRaiz, subCarpeta)

            if SeEncontro:

                auxRaiz = subcarpetaRaiz
            else:

                self.agregar_carpeta(credenciales, auxRaiz, subCarpeta)
                nada, subcarpetaRaiz = self.encontrar_directorio(credenciales, auxRaiz, subCarpeta)
                auxRaiz = subcarpetaRaiz

        return auxRaiz

    def crear_archivo(self,id_folder,ruta,nombre,contenido):

        credenciales = self.iniciosesion()
        destinoId = self.recorrer_ruta_agregar_archivo(id_folder,credenciales,ruta)
        arch = credenciales.CreateFile({'title': nombre,
                                        'parents': [{"kind":"drive#fileLink",
                                                    "id":destinoId}]})
        arch.SetContentString(contenido)
        arch.Upload()
        pass

    def limpiarRuta(self,ruta):
        partes = ruta.split("/")
        nueva_partes = [x for x in partes if x != '']
        rtalimpia = "/"
        for x in nueva_partes:
            if "\"" in x:
                x = x.replace('\"','')
            if not re.search(".*\.txt",x):
                rtalimpia = rtalimpia+x+"/"
            else:
                rtalimpia = rtalimpia+x
        return rtalimpia
    
    def encontrar_direcotrio_archivo(self, credenciales, raiz, carpeta_o_archivo_nombre):

        posible_archivo = carpeta_o_archivo_nombre.split('.') 

        if len(posible_archivo) > 1:

            obtener_archivos = f"'{raiz}' in parents and trashed=false and title='{carpeta_o_archivo_nombre}'"
            archivos = credenciales.ListFile({'q': obtener_archivos}).GetList()

            if len(archivos) > 0:
                return True, archivos[0]['id']
            else:
                return False, None

        else: 
            return self.encontrar_directorio(credenciales, raiz, carpeta_o_archivo_nombre)

    def recorrer_ruta_agregar_archivo_retornar_id(self,raiz, credenciales, ruta):

        ruta = self.limpiarRuta(ruta)

        if ruta[0] == '/':
            ruta = ruta[ 1:len(ruta)]

        if ruta[len(ruta)-1] == '/':
            ruta = ruta[ 0:len(ruta) -1]

        carpetas_anidadas = ruta.split('/')    
        auxRaiz = raiz

        for subCarpeta in carpetas_anidadas:

            seEncontro, subcarpetaRaiz = self.encontrar_direcotrio_archivo(credenciales, auxRaiz, subCarpeta)

            if seEncontro:

                auxRaiz = subcarpetaRaiz
            else:

                return None

        return auxRaiz
    
    def eliminar(self,ruta):
        credenciales = self.iniciosesion()
        ruta_limpia = self.limpiarRuta(ruta)
        id = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder,credenciales,ruta_limpia)
        if(id != None):
            archivo_eliminar = credenciales.CreateFile({'id':id})
            archivo_eliminar.Delete()

    def cambiar_nombre_archivo(self, ruta, nombre):

        credenciales = self.iniciosesion()

        id = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder, credenciales, ruta)
        if(id != None):
            archivo = credenciales.CreateFile({'id': id})
            archivo['title'] = nombre
            archivo.Upload()
        else:
            print("No existe la ruta")
  
    def cambiar_contenido_archivo(self, ruta, nuevo_contenido):

        credenciales = self.iniciosesion()

        id = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder, credenciales, ruta)
        if(id != None):
            archivo = credenciales.CreateFile({'id': id})
            archivo.SetContentString(nuevo_contenido)
            archivo.Upload()
        else:
            print("No existe la ruta")

    def agregar_contenido_al_final(self, ruta, nuevo_contenido):

        credenciales = self.iniciosesion()

        id = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder, credenciales, ruta)
        if(id != None):
            archivo = credenciales.CreateFile({'id': id})
            contenido_actual = archivo.GetContentString()
            contenido_archivo = contenido_actual + str(nuevo_contenido)
            archivo.SetContentString(contenido_archivo)
            archivo.Upload()
        else:
            print("No existe la ruta")
    
    def copiar(self,ruta_origen,ruta_destino):
        credenciales = self.iniciosesion()
        ruta_origen_limpia = self.limpiarRuta(ruta_origen)
        ruta_destino_limpia = self.limpiarRuta(ruta_destino)

        id_origen = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder,credenciales,ruta_origen_limpia)
        id_destino = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder,credenciales,ruta_destino_limpia)
        #Se determina si el archivo a Copiar es una Carpeta o un Archivo
        n = credenciales.CreateFile({'id':id_origen})
        if id_origen != None and id_destino != None:
            if(re.search(".*\.txt",n['title'])):
                credenciales.auth.service.files().copy(fileId=id_origen,body={"parents": [{"kind": "drive#fileLink","id": id_destino}], 'title': n['title']}).execute()
            else:
                #Creo la primera carpeta
                self.agregar_carpeta(credenciales,id_destino,n['title'])
                #Se crea el contenido de cada carpeta de manera iterativa
                file_list = credenciales.ListFile({'q': "'"+id_destino+"'"+" in parents and trashed=false"}).GetList()
                ruta_destino=self.get_IDFolder(file_list,n)
                self.crear_ruta_ct(id_origen,ruta_destino)
                  
    def transferir(self,ruta_origen,ruta_destino):
        credenciales = self.iniciosesion()
        ruta_origen_limpia = self.limpiarRuta(ruta_origen)
        ruta_destino_limpia = self.limpiarRuta(ruta_destino)

        id_origen = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder,credenciales,ruta_origen_limpia)
        id_destino = self.recorrer_ruta_agregar_archivo_retornar_id(id_folder,credenciales,ruta_destino_limpia)
        #Se determina si el archivo a Copiar es una Carpeta o un Archivo
        n = credenciales.CreateFile({'id':id_origen})
        if id_origen != None and id_destino != None:
            if(re.search(".*\.txt",n['title'])):
                credenciales.auth.service.files().copy(fileId=id_origen,body={"parents": [{"kind": "drive#fileLink","id": id_destino}], 'title': n['title']}).execute()
            else:
                #Creo la primera carpeta
                self.agregar_carpeta(credenciales,id_destino,n['title'])
                file_list = credenciales.ListFile({'q': "'"+id_destino+"'"+" in parents and trashed=false"}).GetList()
                ruta_destino=self.get_IDFolder(file_list,n)
                #Se crea el contenido de cada carpeta de manera iterativa
                self.crear_ruta_ct(id_origen,ruta_destino)
        #Se eliminan los archivos originales para terminar el transfer
        self.eliminar(ruta_origen_limpia)
            
    def crear_ruta_ct(self,id_carpeta_expandir,ruta_almacen):
        credenciales = self.iniciosesion()
        file_list = credenciales.ListFile({'q': "'"+id_carpeta_expandir+"'"+" in parents and trashed=false"}).GetList()
        for arch in file_list:
            if(re.search(".*\.txt",arch['title'])):
               credenciales.auth.service.files().copy(fileId=arch['id'],body={"parents": [{"kind": "drive#fileLink","id": ruta_almacen}], 'title': arch['title']}).execute()
            else:
                self.agregar_carpeta(credenciales,ruta_almacen,arch['title'])
                lista2 = credenciales.ListFile({'q': "'"+ruta_almacen+"'"+" in parents and trashed=false"}).GetList()
                ruta_destino=self.get_IDFolder(lista2,arch)
                self.crear_ruta_ct(arch['id'],ruta_destino)

    def get_IDFolder(self,file_list,file_padre):
        for x in file_list:
            if(x['title'] == file_padre['title']):
                ruta_destino = x['id']
        return ruta_destino
    
def backup_local_a_drive(self, ruta, destino, destino_anidado=None):

    credenciales = self.iniciosesion()

    if ruta[0] == '/':
        ruta = ruta[ 1:len(ruta)]

    if ruta[len(ruta)-1] == '/':
        ruta = ruta[ 0:len(ruta) -1]
 
    posible_nombre = os.path.basename(ruta)    
    existeCarpeta, posibleCarpetaId = self.encontrar_directorio(credenciales, destino, posible_nombre)

    print(existeCarpeta)
    print(posibleCarpetaId)

    agregar_directorio = {'title': str(posible_nombre), 'mimeType':  'application/vnd.google-apps.folder', 'parents': [{'id': destino}]}
    agregar_folder_ = credenciales.CreateFile(agregar_directorio)

    print('pasa')

    if destino_anidado:
        print('Entra')
        agregar_folder_['parents'] = [{'id': destino_anidado}]

    if not existeCarpeta:
        print('Entra2')
        print('no existe')
        agregar_folder_.Upload()
    else:
        print('Entra3')
        verificar_archivo = False
        for archivo_carpeta in credenciales.ListFile({'q': f"'{destino}' in parents and trashed=false"}).GetList():
            if archivo_carpeta['title'] == posible_nombre and archivo_carpeta['id'] == posibleCarpetaId:
                verificar_archivo = True
                archivo_carpeta.Delete()  
                print('eliminado')
                break
        
        if verificar_archivo:
            agregar_folder_.Upload()
            print('re subido')

    for contenido in os.listdir(ruta):
        anidado = os.path.join(ruta, contenido)
        if os.path.isdir(anidado):         

            self.backup_local_a_drive(anidado, destino, destino_anidado=agregar_folder_['id'])
        else:  
            
            existe_archivo_dentro = False

            for archivo_o_carpeta in credenciales.ListFile({'q': f"'{agregar_folder_['id']}' in parents and trashed=false"}).GetList():

                if archivo_o_carpeta['title'] == contenido:
                    existe_archivo_dentro = True
                    break
            
            if not existe_archivo_dentro:

                agregar_archivo = credenciales.CreateFile({ 'title': contenido,'parents': [{'id': agregar_folder_['id']}]})
                agregar_archivo.SetContentFile(anidado)
                agregar_archivo.Upload()
        

#crear_archivo_texto('Ejemplo1.txt','Contenido de archivo',id_folder)
#crear_archivo(id_folder,'/Mi Carpeta/Hola/','archivoPrueba.txt','Este es el contenido del archivo \n otra linea')
nb = NubeCm()
nb.transferir('/Mi Carpeta/Hola/','/Carpeta 2/')
#nb.crear_archivo(id_folder,'/Mi Carpeta/Hola/','archivoPrueba.txt','Este es el contenido del archivo \n otra linea')