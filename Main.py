import tkinter as tk


ventana = tk.Tk()
ventana.geometry('800x600')
ventana.config(bg='lightgrey')
ventana.title("Mi primer ventana")

ventana.rowconfigure([0,1], minsize=300)
ventana.columnconfigure([0,1], minsize=400)

# boton = tk.Button(ventana, text='Mi boton',width=60,height=20,bg='blue',fg='white')
# boton.grid(row= 0, column= 0)
# boton.bind('<Enter>', lambda event: boton.config(bg='green'))
# boton.bind('<Leave>',  lambda event: boton.config(bg='blue'))

ventana.mainloop()
