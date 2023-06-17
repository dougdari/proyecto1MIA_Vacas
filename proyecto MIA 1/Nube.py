from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import regex as re
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

        obtener_archivos = f"'{raiz}' in parents and title = '{carpeta_nombre}' and mimeType = 'application/vnd.google-apps.folder'"
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
    
#crear_archivo_texto('Ejemplo1.txt','Contenido de archivo',id_folder)
#crear_archivo(id_folder,'/Mi Carpeta/Hola/','archivoPrueba.txt','Este es el contenido del archivo \n otra linea')
nb = NubeCm()
nb.eliminar('/\"Mi Carpeta\"/')
#nb.crear_archivo(id_folder,'/Mi Carpeta/Hola/','archivoPrueba.txt','Este es el contenido del archivo \n otra linea')