from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

direc_credenciales = 'credentials_module.json'

def iniciosesion():
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

def crear_archivo_texto(file_name, content,id_folder):
    credenciales = iniciosesion()
    arch = credenciales.CreateFile({'title': file_name,
                                    'parents': [{"kind":"drive#fileLink",
                                                 "id":id_folder}]})
    arch.SetContentString(content)
    arch.Upload()
    pass

def encontrar_directorio(credenciales, raiz, carpeta_nombre):

    obtener_archivos = f"'{raiz}' in parents and title = '{carpeta_nombre}' and mimeType = 'application/vnd.google-apps.folder'"
    archivos_carpetas = credenciales.ListFile({'q': obtener_archivos}).GetList()
    if len(archivos_carpetas) > 0:
        return True, archivos_carpetas[0]['id']
    else:
        return False, None

def agregar_carpeta(credenciales, raiz, carpeta_nombre):

    agregar_directorio = {'title': carpeta_nombre, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': raiz}]}
    credenciales.CreateFile(agregar_directorio).Upload()

def recorrer_ruta_agregar_archivo(raiz, credenciales, ruta):

    print(ruta)

    if ruta[0] == '/':
        ruta = ruta[ 1:len(ruta)]

    if ruta[len(ruta)-1] == '/':
        ruta = ruta[ 0:len(ruta) -1]

    carpetas_anidadas = ruta.split('/')    

    print(carpetas_anidadas)

    auxRaiz = raiz

    for subCarpeta in carpetas_anidadas:
        print(subCarpeta)

        print(auxRaiz)

        exists, subcarpetaRaiz = encontrar_directorio(credenciales, auxRaiz, subCarpeta)

        print(subcarpetaRaiz)

        if exists:

            auxRaiz = subcarpetaRaiz
        else:

            print('llega')

            agregar_carpeta(credenciales, auxRaiz, subCarpeta)
            nada, subcarpetaRaiz = encontrar_directorio(credenciales, auxRaiz, subCarpeta)
            auxRaiz = subcarpetaRaiz

    return auxRaiz

def crear_archivo(id_folder,ruta,nombre,contenido):

    credenciales = iniciosesion()

    #print(ruta)

    destinoId = recorrer_ruta_agregar_archivo(id_folder,credenciales,ruta)

    print(destinoId)
    arch = credenciales.CreateFile({'title': nombre,
                                    'parents': [{"kind":"drive#fileLink",
                                                "id":destinoId}]})
    arch.SetContentString(contenido)
    arch.Upload()
    pass

if __name__ == '__main__':
    id_folder = '1woQAJWf0cI0Cv23WmjsCfmQiA0ulyHAD'
    crear_archivo_texto('Ejemplo1.txt','Contenido de archivo',id_folder)
    
    crear_archivo('/Mi Carpeta/Hola/','archivoPrueba.txt','Este es el contenido del archivo \n otra linea')
