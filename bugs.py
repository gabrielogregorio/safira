from tkinter import Button
from tkinter import Label
from tkinter import NSEW, Frame, FLAT
from tkinter import Button, Toplevel
from tkinter import Tk
from tkinter import PhotoImage
import webbrowser
from threading import Thread


class Bug():
    def __init__(self, tela):
        self.tela = tela
        self.bt_report = None
        self.image_bug = None
        self.bt_cancel = None
        self.fr_botoes = None
        self.lb3 = None
        self.lb2 = None
        self.lb1 = None
        self.tp_bug = None

    def __acessar_site_reporte(self):
        self.bt_report.configure(text="Abrindo formulário do Google")
        t = Thread(target=lambda event=None: webbrowser.open("https://forms.gle/J4kE2Li8c58fz4hh6") )
        t.start()        

        Bug.__destruir_interface(self)

    def __destruir_interface(self):
        self.bt_report.destroy()
        self.bt_cancel.destroy()
        self.fr_botoes.destroy()
        self.lb3.destroy()
        self.lb2.destroy()
        self.lb1.destroy()
        self.tp_bug.destroy()

    def interface(self):
        self.image_bug = PhotoImage(file="imagens/bug.png")
        self.image_bug = self.image_bug.subsample(4)

        self.tp_bug = Toplevel(self.tela, bd=10, bg="#3e4045")
        self.tp_bug.withdraw()
        self.tp_bug.wm_attributes('-type','splash')
        
        self.lb1 = Label(self.tp_bug, text="  Então você encontrou um bug?  ", font=("",20), bg="#3e4045", fg="#efefef")
        self.lb2 = Label(self.tp_bug, bg="#3e4045", fg="#efefef", image = self.image_bug)
        self.lb3 = Label(self.tp_bug, text="""\nVocê gostaria de reportar para nós?\n Isso nos ajuda a produzir algo melhor, vamos\n ficar felizes em ter o seu feedback!\n""")

        self.fr_botoes = Frame(self.tp_bug, bg='#3e4045')
        self.bt_cancel = Button(self.fr_botoes, text="Depois")
        self.bt_report = Button(self.fr_botoes, text="Reportar o BUG")

        self.tp_bug.grid_columnconfigure(1, weight=1)
        self.fr_botoes.grid_columnconfigure(1, weight=1)
        self.fr_botoes.grid_columnconfigure(2, weight=1)

        self.lb3.configure(font=("",11), bg="#3e4045", fg="#efefef")

        self.bt_cancel.configure(font=("",13), highlightbackground="#972121", relief=FLAT, bg="#a83232", fg="white", activebackground="#a83232", activeforeground="#efefef", command=lambda event=None: Bug.__destruir_interface(self))
        self.bt_report.configure(font=("",13), highlightbackground="#219791", relief=FLAT, bg="#1d6965", fg="white", activebackground="#1d6965", activeforeground="#efefef", command=lambda event=None: Bug.__acessar_site_reporte(self))

        self.lb1.grid(row=1, column=1, sticky=NSEW)
        self.lb2.grid(row=2, column=1, sticky=NSEW)
        self.lb3.grid(row=3, column=1, sticky=NSEW)

        self.fr_botoes.grid(row=4, column=1, sticky=NSEW)
        self.bt_cancel.grid(row=1, column=1)
        self.bt_report.grid(row=1, column=2)

        self.tp_bug.deiconify()
        self.tp_bug.update()
        

if __name__ == "__main__":
    tela = Tk()
    tela.grid_columnconfigure(1, weight=1)

    b = Bug(tela)
    b.interface()

    tela.mainloop()