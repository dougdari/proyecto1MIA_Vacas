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

if __name__ == '__main__':
    id_folder = '1woQAJWf0cI0Cv23WmjsCfmQiA0ulyHAD'
    crear_archivo_texto('Ejemplo1.txt','Contenido de archivo',id_folder)
