import LoginLogic as Lg
import FuncionesLocal as LocalOptions
import Nube as CloudOptions
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import Encriptador as enc
import analizadorEntrada
import os.path
import os
from datetime import date
from datetime import datetime
logL = Lg.LoginLg()
logL.abrirarchivo()

localOp = LocalOptions.FLocal()
CloudOp = CloudOptions.NubeCm()
encriptador = enc.AESencriptador()

coordenada_x = 0
coordenada_y = 0

usuario_nombre_logueado = ""
usuario_contrasenia_logueado = ""
global llave_enc
llave_enc = ""
#PARAMETROS QUE ALMACENARÁN LOS VALORES DE LA OP CONFIG

def generar_pantalla_login():
    
    pantalla1.withdraw()
    pantallaLogin = tk.Tk()    
    pantallaLogin.title("Proyecto MIA 1 login")
    pantallaLogin.resizable(False,False)
    ancho_monitor_login = pantalla1.winfo_screenwidth()
    alto_monitor_login = pantalla1.winfo_screenheight()
    coordenada_x_login = (ancho_monitor_login - 500) // 2
    coordenada_y_login = (alto_monitor_login - 320) // 2  
    pantallaLogin.geometry(f"{500}x{320}+{coordenada_x_login}+{coordenada_y_login}")       

    etiqueta_titulo = tk.Label(pantallaLogin, text="Ingrese un usuario y password valido!")
    etiqueta_titulo.place(x=50, y=45)

    etiqueta_campo_usuario = tk.Label(pantallaLogin, text="Usuario:")
    etiqueta_campo_usuario.place(x=50, y=115)

    campo_usuario = tk.Entry(pantallaLogin, width=55)
    campo_usuario.place(x=110, y=115)
    #campo_usuario.grid(row=2, column=3)
    #campo_usuario.pack()

    etiqueta_campo_contrasenia = tk.Label(pantallaLogin, text="Password:")
    etiqueta_campo_contrasenia.place(x=50, y=165)

    campo_contrasenia = tk.Entry(pantallaLogin, show="*", width=55)
    campo_contrasenia.place(x=110, y=165)
    #campo_contrasenia.grid(row=4, column=3)
    #campo_contrasenia.pack()

    #print("cadena para analizar")
    #entrada = "exec -path->/home/Desktop/calificacion.mia modify -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\" add -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\""
    #resultado = analizadorEntrada.parser.parse(entrada, lexer=analizadorEntrada.lexer)
    #print("Resultado: {}".format(resultado))

    def ir_a_pantalla_principal():
        resv = logL.verificar(campo_usuario.get(),campo_contrasenia.get())
        #Agregar en esta area el codigo o funcion para verificar si la contrasenia es valida
        tiempo = datetime.now()
        tiempo_string = tiempo.strftime("%d/%m/%Y %H:%M:%S")
        cnt_bitacora = tiempo_string + " - Input - "+campo_usuario.get()+" Inicia Sesión\n"
        if resv:
            cnt_bitacora += tiempo_string + " - Output - Sesión Iniciada Correctamente\n"
            crear_llenar_bitacora(cnt_bitacora)
            pantallaLogin.destroy()
            pantalla1.deiconify()  
        else:
            cnt_bitacora += tiempo_string + " - Output - Sesión Iniciada Incorrectamente\n"
            crear_llenar_bitacora(cnt_bitacora)
            messagebox.showinfo("Aviso", "password incorrecto.")
            

        

    boton = tk.Button(pantallaLogin, text="Ir a pantalla principal", command=ir_a_pantalla_principal, width=55)
    boton.place(x=50, y=215)
    #boton.grid(row=6, column=3)
    #boton.pack()

def comando_EXEC(path):

    entrada = open(path,"r", encoding="utf-8")
    comandos = entrada.read()
    resultado = analizadorEntrada.parser.parse(comandos, lexer=analizadorEntrada.lexer)
    for comando in resultado:
        print(comando)
    entrada.close()
    
def generar_pantall_comando_exec():

    pantalla_comando_exec = tk.Toplevel(pantalla1)
    pantalla_comando_exec.title("Comando \"Exec\"")
    pantalla_comando_exec.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_exec.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_exec, text="Ingrese los parametros para el comando \"Exec\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_path = tk.Label(pantalla_comando_exec, text="-path (*)")
    etiqueta_campo_path.place(x=50, y=55)

    campo_path = tk.Entry(pantalla_comando_exec,  width=45)
    campo_path.place(x=155, y=55)

    def obtener_parametros_exec():
        path =  campo_path.get()
        primer_linea_exec(path)
        #localOp.ejecutarArchivo(path,area_de_respuestas)

    boton_add = tk.Button(pantalla_comando_exec, command=obtener_parametros_exec, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantall_comando_add():

    pantalla_comando_add = tk.Toplevel(pantalla1)
    pantalla_comando_add.title("Comando \"Modify\"")
    pantalla_comando_add.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_add.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_add, text="Ingrese los parametros para el comando \"Modify\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_path = tk.Label(pantalla_comando_add, text="-path (*)")
    etiqueta_campo_path.place(x=50, y=55)

    campo_path = tk.Entry(pantalla_comando_add,  width=45)
    campo_path.place(x=155, y=55)

    etiqueta_campo_body = tk.Label(pantalla_comando_add, text="-body (*)")
    etiqueta_campo_body.place(x=50, y=105)

    campo_body = tk.Entry(pantalla_comando_add,  width=45)
    campo_body.place(x=155, y=105)

    def obtener_parametros_add():
        path =  campo_path.get()
        body = campo_body.get()
        if tipo_config == "local":
            localOp.comandoAgregar(path,body,area_de_respuestas)
        else:
            CloudOp.agregar_contenido_al_final(path,body,area_de_respuestas)
    boton_add = tk.Button(pantalla_comando_add, command=obtener_parametros_add, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantall_comando_modify():

    pantalla_comando_modify = tk.Toplevel(pantalla1)
    pantalla_comando_modify.title("Comando \"Modify\"")
    pantalla_comando_modify.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_modify.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_modify, text="Ingrese los parametros para el comando \"Modify\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_path = tk.Label(pantalla_comando_modify, text="-path (*)")
    etiqueta_campo_path.place(x=50, y=55)

    campo_path = tk.Entry(pantalla_comando_modify,  width=45)
    campo_path.place(x=155, y=55)

    etiqueta_campo_body = tk.Label(pantalla_comando_modify, text="-body (*)")
    etiqueta_campo_body.place(x=50, y=105)

    campo_body = tk.Entry(pantalla_comando_modify,  width=45)
    campo_body.place(x=155, y=105)

    def obtener_parametros_modify():
        path =  campo_path.get()
        body = campo_body.get()
        if tipo_config == "local":
            localOp.comandoModificar(path,body,area_de_respuestas)
        else:
            CloudOp.cambiar_contenido_archivo(path,body,area_de_respuestas)
    
    boton_add = tk.Button(pantalla_comando_modify, command=obtener_parametros_modify, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantall_comando_rename():

    pantalla_comando_rename = tk.Toplevel(pantalla1)
    pantalla_comando_rename.title("Comando \"Rename\"")
    pantalla_comando_rename.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_rename.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_rename, text="Ingrese los parametros para el comando \"Rename\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_path = tk.Label(pantalla_comando_rename, text="-path (*)")
    etiqueta_campo_path.place(x=50, y=55)

    campo_path = tk.Entry(pantalla_comando_rename,  width=45)
    campo_path.place(x=155, y=55)

    etiqueta_campo_name = tk.Label(pantalla_comando_rename, text="-name (*)")
    etiqueta_campo_name.place(x=50, y=105)

    campo_name = tk.Entry(pantalla_comando_rename,  width=45)
    campo_name.place(x=155, y=105)

    def obtener_parametros_rename():
        path =  campo_path.get()
        name = campo_name.get()
        if tipo_config=="local":
            localOp.comandoRenombrar(path,name,area_de_respuestas)
        else:
            CloudOp.cambiar_nombre_archivo(path,name,area_de_respuestas)
    
    boton_add = tk.Button(pantalla_comando_rename, command=obtener_parametros_rename, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantall_comando_transfer():

    pantalla_comando_transfer = tk.Toplevel(pantalla1)
    pantalla_comando_transfer.title("Comando \"Transfer\"")
    pantalla_comando_transfer.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_transfer.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_transfer, text="Ingrese los parametros para el comando \"Transfer\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_from = tk.Label(pantalla_comando_transfer, text="-from (*)")
    etiqueta_campo_from.place(x=50, y=55)

    campo_from = tk.Entry(pantalla_comando_transfer,  width=45)
    campo_from.place(x=155, y=55)

    etiqueta_campo_to = tk.Label(pantalla_comando_transfer, text="-to (*)")
    etiqueta_campo_to.place(x=50, y=105)

    campo_to = tk.Entry(pantalla_comando_transfer,  width=45)
    campo_to.place(x=155, y=105)

    opciones_valor_booleano = ["Local","Cloud"]

    etiqueta_campo_mode = tk.Label(pantalla_comando_transfer, text="-mode (*)")
    etiqueta_campo_mode.place(x=50, y=155)

    campo_mode = ttk.Combobox(pantalla_comando_transfer, values=opciones_valor_booleano, state="readonly", width=42)
    campo_mode.place(x=155, y=155)

    def obtener_parametros_transfer():
        from_ =  campo_from.get()
        to_ = campo_to.get()
        mode = campo_mode.get()
        if tipo_config=="local":
            localOp.transferir_archivos_directorio("./Archivo"+from_,"./Archivo"+to_,mode,area_de_respuestas)
        else:
            CloudOp.transferir(from_,to_,mode,area_de_respuestas)

    boton_add = tk.Button(pantalla_comando_transfer, command=obtener_parametros_transfer, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantall_comando_backup():

    pantalla_comando_backup = tk.Toplevel(pantalla1)
    pantalla_comando_backup.title("Comando \"Backup\"")
    pantalla_comando_backup.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_backup.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

def generar_pantalla_comando_configure():

    pantalla_comando_configure = tk.Toplevel(pantalla1)
    pantalla_comando_configure.title("Comando \"Configure\"")
    pantalla_comando_configure.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_configure.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_configure, text="Ingrese los parametros para el comando \"Configure\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_type = tk.Label(pantalla_comando_configure, text="-type (*)")
    etiqueta_campo_type.place(x=50, y=55)

    opciones_campo_type = ["Local","Cloud"]

    campo_type = ttk.Combobox(pantalla_comando_configure, values=opciones_campo_type, state="readonly", width=45)
    campo_type.place(x=155, y=55)

    etiqueta_campo_encrypt_log = tk.Label(pantalla_comando_configure, text="-encrypt_log (*)")
    etiqueta_campo_encrypt_log.place(x=50, y=105)

    opciones_valor_booleano = ["true","false"]

    campo_encrypt_log = ttk.Combobox(pantalla_comando_configure, values=opciones_valor_booleano, state="readonly", width=45)
    campo_encrypt_log.place(x=155, y=105)

    etiqueta_campo_encrypt_read = tk.Label(pantalla_comando_configure, text="-encrypt_read (*)")
    etiqueta_campo_encrypt_read.place(x=50, y=155)

    campo_encrypt_read = ttk.Combobox(pantalla_comando_configure, values=opciones_valor_booleano, state="readonly", width=45)
    campo_encrypt_read.place(x=155, y=155)
    
    etiqueta_llave = tk.Label(pantalla_comando_configure, text="-llave")
    etiqueta_llave.place(x=50, y=205)

    campo_llave = tk.Entry(pantalla_comando_configure, width=48)
    campo_llave.place(x=155, y=205)

    def obtener_parametros_configure():
        type =  campo_type.get().lower()
        log = campo_encrypt_log.get()
        read = campo_encrypt_read.get()
        llave = campo_llave.get()
        #SE ESTABLECEN LOS PARAMETROS
        global tipo_config
        tipo_config = type
        global encrypt_log
        encrypt_log = log
        global encrypt_read
        encrypt_read = read
        entrada = ""
        if(llave != ""):
            global llave_enc
            llave_enc = llave
            entrada = "configure -type->"+tipo_config+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read+" -llave->"+llave_enc
        else:
            entrada = "configure -type->"+tipo_config+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read
        crear_llenar_bitacora(entrada)
        #print(type + " " + log + " " + read + " " + llave)

    boton_add = tk.Button(pantalla_comando_configure, command=obtener_parametros_configure, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantalla_comando_copy():
    
    pantalla_comando_copy = tk.Toplevel(pantalla1)
    pantalla_comando_copy.title("Comando \"Copy\"")
    pantalla_comando_copy.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_copy.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_copy, text="Ingrese los parametros para el comando \"Copy\"")
    etiqueta_titulo.place(x=50, y=15) 

    etiqueta_campo_path = tk.Label(pantalla_comando_copy, text="-from (*)")
    etiqueta_campo_path.place(x=50, y=55)

    campo_path = tk.Entry(pantalla_comando_copy, width=45)
    campo_path.place(x=155, y=55)

    etiqueta_campo_destino = tk.Label(pantalla_comando_copy, text="-to (*)")
    etiqueta_campo_destino.place(x=50, y=105)

    campo_destino = tk.Entry(pantalla_comando_copy, width=45)
    campo_destino.place(x=155, y=105)

    def obtener_parametros_copy():
        path = campo_path.get()
        name = campo_destino.get()
        print(path + " " + name)
        if tipo_config=="local":
            localOp.copiar_archivos_directorio("./Archivo"+path,"./Archivo"+name,area_de_respuestas)
        else:
            CloudOp.copiar(path,name,area_de_respuestas)

    boton_add = tk.Button(pantalla_comando_copy, command=obtener_parametros_copy, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantalla_comando_delete():

    pantalla_comando_delete = tk.Toplevel(pantalla1)
    pantalla_comando_delete.title("Comando \"Delete\"")
    pantalla_comando_delete.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_delete.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_delete, text="Ingrese los parametros para el comando \"Delete\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_path = tk.Label(pantalla_comando_delete, text="-path (*)")
    etiqueta_campo_path.place(x=50, y=55)

    campo_path = tk.Entry(pantalla_comando_delete, width=45)
    campo_path.place(x=155, y=55)

    etiqueta_campo_name = tk.Label(pantalla_comando_delete, text="-name")
    etiqueta_campo_name.place(x=50, y=105)

    campo_name = tk.Entry(pantalla_comando_delete, width=45)
    campo_name.place(x=155, y=105)

    def obtener_parametros_delete():
        path = campo_path.get()
        name = campo_name.get()
        if tipo_config=="local":
            localOp.comandoEliminar(name,path,area_de_respuestas)
        else:
            CloudOp.eliminar(name,path,area_de_respuestas)

    boton_add = tk.Button(pantalla_comando_delete, command=obtener_parametros_delete, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantalla_comando_create():

    pantalla_comando_create = tk.Toplevel(pantalla1)
    pantalla_comando_create.title("Comando \"Create\"")
    pantalla_comando_create.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_create.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_create, text="Ingrese los parametros para el comando \"Create\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_name = tk.Label(pantalla_comando_create, text="-name (*)")
    etiqueta_campo_name.place(x=50, y=55)

    campo_name = tk.Entry(pantalla_comando_create, width=45)
    campo_name.place(x=155, y=55)

    etiqueta_campo_body = tk.Label(pantalla_comando_create, text="-body (*)")
    etiqueta_campo_body.place(x=50, y=105)

    campo_body = tk.Entry(pantalla_comando_create, width=45)
    campo_body.place(x=155, y=105)

    etiqueta_campo_path = tk.Label(pantalla_comando_create, text="-path (*)")
    etiqueta_campo_path.place(x=50, y=155)

    campo_path = tk.Entry(pantalla_comando_create, width=45)
    campo_path.place(x=155, y=155)

    def obtener_parametros_create():
        name =  campo_name.get()
        body = campo_body.get()
        path = campo_path.get()
        if tipo_config=="local":
            localOp.comandoCrear(name,body,path,area_de_respuestas)
        else:
            CloudOp.crear_archivo(name,body,path,area_de_respuestas)

    boton_add = tk.Button(pantalla_comando_create, command=obtener_parametros_create, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantalla_principal():

    pantalla  = tk.Tk()
    pantalla.title("Proyecto MIA 1")
    pantalla.geometry("1000x600")
    pantalla.resizable(False,False)  

    etiqueta_area_de_respuestas = tk.Label(pantalla, text="Respuesta e historial de comandos ingresados:")
    etiqueta_area_de_respuestas.place(x=50, y=30)

    etiqueta_entrada = tk.Label(pantalla, text="Ingrese un comando:")
    etiqueta_entrada.place(x=50, y=530)

    entrada = tk.Entry(pantalla, width=75)
    entrada.place(x=47, y=550)
    entrada.focus() 

    def ejetular_linea_entrada():
        analizadorEntrada.comandos = []
        resultado = analizadorEntrada.parser.parse(entrada.get(), lexer=analizadorEntrada.lexer)
        if(resultado[0][0].lower() == "configure"):
            entrada_txt = ""
            global tipo_config
            tipo_config = resultado[0][1].lower()
            global encrypt_log
            encrypt_log = resultado[0][2].lower()
            global encrypt_read
            encrypt_read = resultado[0][3].lower()
            if(5 == len(resultado[0])):
                global llave_enc
                llave_enc = resultado[0][4].lower()
                entrada_txt = "configure -type->"+tipo_config+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read+" -llave->"+llave_enc
            else:
                entrada_txt = "configure -type->"+tipo_config+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read
            crear_llenar_bitacora(entrada_txt)
        elif(resultado[0][0].lower() == "exec"):
            primer_linea_exec(resultado[0][1])

        if(tipo_config == "local"):
            localOp.ejecutarComando(resultado,area_de_respuestas,encrypt_read,llave_enc)
        else:
            CloudOp.ejecutarComando(resultado,area_de_respuestas,encrypt_read,llave_enc)

    boton_ejectuar_linea= tk.Button(pantalla, command=ejetular_linea_entrada, text="Ejecutar", width=10)
    boton_ejectuar_linea.place(x = 513, y =543)

    boton_configure = tk.Button(pantalla, command=generar_pantalla_comando_configure, text="Configure", width=30)
    boton_configure.place(x = 610, y = 48)

    boton_create= tk.Button(pantalla, command=generar_pantalla_comando_create, text="Create", width=30)
    boton_create.place(x = 610, y = 88)

    boton_delete = tk.Button(pantalla, command=generar_pantalla_comando_delete, text="Delete", width=30)
    boton_delete.place(x = 610, y = 128)

    boton_copy = tk.Button(pantalla, command=generar_pantalla_comando_copy, text="Copy", width=30)
    boton_copy.place(x = 610, y = 168)

    boton_backup = tk.Button(pantalla, text="Backup", command=generar_pantall_comando_backup, width=30)
    boton_backup.place(x = 610, y = 208)

    boton_transfer = tk.Button(pantalla, command=generar_pantall_comando_transfer, text="Transfer", width=30)
    boton_transfer.place(x = 610, y = 248)

    boton_rename = tk.Button(pantalla, command=generar_pantall_comando_rename, text="Rename", width=30)
    boton_rename.place(x = 610, y = 288)

    boton_modify = tk.Button(pantalla, command=generar_pantall_comando_modify, text="Modify", width=30)
    boton_modify.place(x = 610, y = 328)

    boton_add = tk.Button(pantalla, text="Add", command=generar_pantall_comando_add, width=30)
    boton_add.place(x = 610, y = 368)

    boton_add = tk.Button(pantalla, text="Exec", command=generar_pantall_comando_exec, width=30)
    boton_add.place(x = 610, y = 408)

    boton_cerrar_secion = tk.Button(pantalla, command=generar_pantalla_login, text="Cerrar sesion", width=30)
    boton_cerrar_secion.place(x = 610, y = 448)

    return pantalla

def crear_llenar_bitacora(entrada):
    #Se crea el registro de configure y se agreg al area de output
    tiempo = datetime.now()
    tiempo_string = tiempo.strftime("%d/%m/%Y %H:%M:%S")
    cnt_bitacora = tiempo_string + " - Input - "+entrada+"\n"
    cnt_bitacora += tiempo_string + " - Output - Se ha configurado el sistema\n"
    area_de_respuestas.insert(tk.END,cnt_bitacora+"\n")

    #Se crea y determina la existencia de la bitacora
    ruta = "/logs/"+str(date.today())+"/"
    #Se comprueba la existencia del directorio
    if not os.path.exists(localOp.directorio_archivo+ruta):
        nombre = "log_archivos.txt"
        #Se limpia la ruta en caso alguna parte tenga doble comilla
        nueva_ruta = localOp.limpiarRuta(ruta)
        #Se explora la ruta para crear las carpetas necesarias
        localOp.crear_ruta(nueva_ruta)
        #Se crea el archivo y se detecta si no existe uno con nombre igual
        f = open(nueva_ruta+nombre,"a")
        f.write(cnt_bitacora)
        f.close()
    else:
        f = open(localOp.directorio_archivo+ruta+"log_archivos.txt","a")
        f.write(cnt_bitacora)
        f.close()

def primer_linea_exec(ruta):
    entrada_txt  = ""
    archivo = open("."+ruta,"r")
    #Se extrae la linea de configuración
    config_parametros = archivo.readline().split(" ")
    #SE ESTABLECEN LOS PARAMETROS
    global tipo_config
    tipo_config = config_parametros[1].split("->")[1].lower()
    global encrypt_log
    encrypt_log = config_parametros[2].split("->")[1].lower()
    global encrypt_read
    encrypt_read = config_parametros[3].split("->")[1].lower()
    if(5 == len(config_parametros)):
        global llave_enc
        llave_enc = config_parametros[4].split("->")[1].lower()
        entrada_txt = "configure -type->"+tipo_config+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read+" -llave->"+llave_enc
    else:
        entrada_txt = "configure -type->"+tipo_config+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read
    crear_llenar_bitacora(entrada_txt)
pantalla1 = generar_pantalla_principal()
ancho_monitor = pantalla1.winfo_screenwidth()
alto_monitor = pantalla1.winfo_screenheight()
coordenada_x = (ancho_monitor - 872) // 2
coordenada_y = (alto_monitor - 600) // 2
pantalla1.geometry(f"{872}x{600}+{coordenada_x}+{coordenada_y}")

area_de_respuestas = tk.Text(pantalla1, height=29, width=68)
area_de_respuestas.config(state="disabled")
area_de_respuestas.place(x=45, y=50)
area_de_respuestas['state'] = 'normal'

def main():  
    generar_pantalla_login()
    pantalla1.mainloop()
main()