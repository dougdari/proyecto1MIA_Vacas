import tkinter as tk
from tkinter import messagebox

#myWindow = tk.Tk()

#myWindow.title("Proyecto MIA 1")
#myWindow.geometry("1000x600")
#myWindow.resizable(False,False)
#myWindow.mainloop()

coordenada_x = 0
coordenada_y = 0

usuario_nombre_logueado = ""
usuario_contrasenia_logueado = ""

def generar_pantalla_login():

    pantalla1.withdraw()
    pantallaLogin = tk.Tk()    
    pantallaLogin.title("Proyecto MIA 1 login")
    pantallaLogin.geometry("1000x600")
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

    def ir_a_pantalla_principal():

        print(campo_usuario.get())
        print(campo_contrasenia.get())

        #Agregar en esta area el codigo o funcion para verificar si la contrasenia es valida

        if campo_usuario.get() == "archivos" and campo_contrasenia.get() == '12345':
            pantallaLogin.destroy()
            pantalla1.deiconify()  
        else:
            messagebox.showinfo("Aviso", "password incorrecto.")

        

    boton = tk.Button(pantallaLogin, text="Ir a pantalla principal", command=ir_a_pantalla_principal, width=55)
    boton.place(x=50, y=215)
    #boton.grid(row=6, column=3)
    #boton.pack()

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

    boton_configure = tk.Button(pantalla, text="Configure", width=30)
    boton_configure.place(x = 610, y = 48)

    boton_create= tk.Button(pantalla, text="Create", width=30)
    boton_create.place(x = 610, y = 88)

    boton_delete = tk.Button(pantalla, text="Delete", width=30)
    boton_delete.place(x = 610, y = 128)

    boton_copy = tk.Button(pantalla, text="Copy", width=30)
    boton_copy.place(x = 610, y = 168)

    boton_backup = tk.Button(pantalla, text="Backup", width=30)
    boton_backup.place(x = 610, y = 208)

    boton_transfer = tk.Button(pantalla, text="Transfer", width=30)
    boton_transfer.place(x = 610, y = 248)

    boton_rename = tk.Button(pantalla, text="Rename", width=30)
    boton_rename.place(x = 610, y = 288)

    boton_modify = tk.Button(pantalla, text="Modify", width=30)
    boton_modify.place(x = 610, y = 328)

    boton_add = tk.Button(pantalla, text="Add", width=30)
    boton_add.place(x = 610, y = 368)

    boton_add = tk.Button(pantalla, text="Exec", width=30)
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

    generar_pantalla_login()
    pantalla1.mainloop()

    


main()