from tkinter import Frame
from tkinter import Label
from tkinter import Label
from tkinter import NSEW

class Splash():
    def __init__(self, tela, design):
        self.frame_splash = None
        self.fr_splash = None
        self.l1_splash = None
        self.l2_splash = None
        self.tela = tela
        self.design = design

    def splash_inicio(self):
        self.frame_splash = Frame(self.tela)

        self.frame_splash.configure(background = self.design.dic["cor_intro"]["background"])
        self.frame_splash.rowconfigure(1, weight=1)
        self.frame_splash.grid_columnconfigure(0, weight=1)

        self.fr_splash = Frame(self.frame_splash)
        self.l1_splash = Label(self.frame_splash, self.design.dic["cor_intro"])
        self.l2_splash = Label(self.frame_splash, self.design.dic["cor_intro"])

        self.fr_splash.configure(background = self.design.dic["cor_intro"]["background"])
        self.l1_splash.configure(text=" COMBRATEC ", font=( "Lucida Sans", 90), bd=80)
        self.l2_splash.configure(text="Safira IDE beta 0.3", font=("Lucida Sans", 12))

        self.frame_splash.grid(row=1, column=1, sticky=NSEW)
        self.fr_splash.grid(row=0, column=1, sticky=NSEW)
        self.l1_splash.grid(row=1, column=1, sticky=NSEW)
        self.l2_splash.grid(row=2, column=1, sticky=NSEW)
        self.frame_splash.update()

        self.tela.update()
        self.tela.withdraw()

        j_width  = self.tela.winfo_reqwidth()
        j_height = self.tela.winfo_reqheight()

        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tela.geometry("+{}+{}".format( int(t_width / 2) - int(j_width / 2), int(t_heigth / 2 ) - int (j_height / 2) ))

        self.tela.deiconify()
        self.tela.update()
    def splash_fim(self):
        self.fr_splash.grid_forget()
        self.l1_splash.grid_forget()
        self.l2_splash.grid_forget()

        self.frame_splash.grid_forget()