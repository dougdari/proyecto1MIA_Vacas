import tkinter as tk

myWindow = tk.Tk()

myWindow.title("Proyecto MIA 1 - LOGIN")
myWindow.geometry("400x600")
myWindow.resizable(False,False)
myWindow.configure(background='#161c29')
label = tk.Label(text="Nombre de Usuario",background='#161c29',fg='white')
entry = tk.Entry()

label2 = tk.Label(text="Contraseña",background='#161c29',fg='white')
entry2 = tk.Entry()

boton = tk.Button(text="Ingresar")

label.pack()
entry.pack()
label2.pack()
entry2.pack()
boton.pack()

myWindow.mainloop()