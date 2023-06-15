import LoginLogic as Lg
import FuncionesLocal as LocalOptions
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import analizadorEntrada

#logL = Lg.LoginLg()
#logL.abrirarchivo()

localOp = LocalOptions.FLocal()

coordenada_x = 0
coordenada_y = 0

usuario_nombre_logueado = ""
usuario_contrasenia_logueado = ""

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

        if resv:
            pantallaLogin.destroy()
            pantalla1.deiconify()  
        else:
            messagebox.showinfo("Aviso", "password incorrecto.")

        

    boton = tk.Button(pantallaLogin, text="Ir a pantalla principal", command=ir_a_pantalla_principal, width=55)
    boton.place(x=50, y=215)
    #boton.grid(row=6, column=3)
    #boton.pack()

def comando_EXEC(path):

    entrada = open(path,"r", encoding="utf-8")
    comandos = entrada.read()

    #entrada = "exec -path->/home/Desktop/calificacion.mia modify -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\" add -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\""
    resultado = analizadorEntrada.parser.parse(comandos, lexer=analizadorEntrada.lexer)
    print(resultado)

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
        comando_EXEC(path)

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
        localOp.comandoAgregar(path,body)
    
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
        localOp.comandoModificar(path,body)
    
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
        localOp.comandoRenombrar(path,name)
    
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
        print(from_ + " " + to_ + " " + mode)
        localOp.transferir_archivos_directorio(from_,to_)

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
        type =  campo_type.get()
        log = campo_encrypt_log.get()
        read = campo_encrypt_read.get()
        llave = campo_llave.get()
        print(type + " " + log + " " + read + " " + llave)

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
        localOp.copiar_archivos_directorio(path,name)

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
        localOp.comandoEliminar(name,path)

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
        localOp.comandoCrear(name,body,path)

    boton_add = tk.Button(pantalla_comando_create, command=obtener_parametros_create, text="Ejecutar", width=30)
    boton_add.place(x = 155, y = 250)

def generar_pantalla_principal():

    pantalla  = tk.Tk()
    pantalla.title("Proyecto MIA 1")
    pantalla.geometry("1000x600")
    pantalla.resizable(False,False)  

    etiqueta_area_de_respuestas = tk.Label(pantalla, text="Respuesta e historial de comandos ingresados:")
    etiqueta_area_de_respuestas.place(x=50, y=30)

    area_de_respuestas = tk.Text(pantalla, height=29, width=68)
    area_de_respuestas.config(state="disabled")
    area_de_respuestas.place(x=45, y=50)

    etiqueta_entrada = tk.Label(pantalla, text="Ingrese un comando:")
    etiqueta_entrada.place(x=50, y=530)

    entrada = tk.Entry(pantalla, width=90)
    entrada.place(x=47, y=550)
    entrada.focus() 

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

pantalla1 = generar_pantalla_principal()
ancho_monitor = pantalla1.winfo_screenwidth()
alto_monitor = pantalla1.winfo_screenheight()
coordenada_x = (ancho_monitor - 872) // 2
coordenada_y = (alto_monitor - 600) // 2
pantalla1.geometry(f"{872}x{600}+{coordenada_x}+{coordenada_y}")


def main():  

    #generar_pantalla_login()
    pantalla1.mainloop()

    


main()