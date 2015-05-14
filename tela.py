from tkinter import *


class MenuBar(Menu):
    def __init__(self, master):
        Menu.__init__(self, master)
        fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):       
        vazar = messagebox.askyesno(title='Sair', message='Deseja realmente sair?')
        if vazar:
            self.master.destroy()
        else:
            pass

app.py

from tkinter import *
from menu import *

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)      

if __name__ == "__main__":
    app=App()
    app.mainloop()