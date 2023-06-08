import Encriptador as e
listaUsuarios = []

class LoginLg:
    def __init__(self):
        pass
    
    def abrirarchivo(self):
        f = open("./usuarios.txt","r")
        for x in f:
            listaUsuarios.append(x)
        pass

    def verificar(self,usuario,contrasenia):
        enc = e.AESencriptador()
        flagC = False
        size = len(listaUsuarios)
        i = 0
        while(i+1<size):
            if(usuario == listaUsuarios[i].replace("\n","") and contrasenia == enc.desencriptar(listaUsuarios[i+1].replace("\n","")).decode("utf-8","ignore")):
                #print("INGRESADO")
                flagC = True
                break
            i=i+2
        return flagC


l = LoginLg()
l.abrirarchivo()
l.verificar('usuario1','junio1234')