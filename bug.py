from threading             import Thread
import webbrowser
from tkinter               import Toplevel
from tkinter               import Label
from tkinter               import Frame
from tkinter               import Button
from tkinter import FLAT, NSEW
from tkinter               import PhotoImage


class Bug():
    def __init__(self, tela, design):
        self.design =design
        self.tela = tela
        self.bt_report = None
        self.image_bug = None
        self.bt_cancel = None
        self.fr_botoes = None
        self.lb_label3 = None
        self.lb_label2 = None
        self.lb_label1 = None
        self.tp_princi = None

    def __acessar_site_reporte(self):
        self.bt_report.configure(text="Abrindo formulário do Google")

        t = Thread(target=lambda event=None: webbrowser.open("https://forms.gle/J4kE2Li8c58fz4hh6") )
        t.start()        

        Bug.__destruir_interface(self)

    def __destruir_interface(self):
        self.bt_report.destroy()
        self.bt_cancel.destroy()
        self.fr_botoes.destroy()
        self.lb_label3.destroy()
        self.lb_label2.destroy()
        self.lb_label1.destroy()
        self.tp_princi.destroy()

    def interface(self):
        self.image_bug = PhotoImage(file="imagens/bug.png")
        self.image_bug = self.image_bug.subsample(4)

        self.tp_princi = Toplevel(self.tela, bd=10, bg="#3e4045")
        # self.design.dic[""]


        self.tp_princi.withdraw()

        try:
            self.tp_princi.wm_attributes('-type','splash')
        except Exception as erro:
            print("Erro ao remover barra de titulos => ", erro)

        self.lb_label1 = Label(self.tp_princi, self.design.dic["lb1_encontrou_bug"],  text="  Então você encontrou um bug?  ")
        self.lb_label2 = Label(self.tp_princi, self.design.dic["lb2_encontrou_bug"], image = self.image_bug)
        self.lb_label3 = Label(self.tp_princi, self.design.dic["lb3_encontrou_bug"], text="""\nVocê gostaria de reportar para nós?\n Isso nos ajuda a produzir algo melhor, vamos\n ficar felizes em ter o seu feedback!\n""")

        self.fr_botoes = Frame(self.tp_princi, self.design.dic["fr_bt_encontrou_bug"])
        self.bt_cancel = Button(self.fr_botoes, self.design.dic["bt_canc_encontrou_bug"], text="Depois", relief=FLAT)
        self.bt_report = Button(self.fr_botoes, self.design.dic["bt_report_encontrou_bug"], text="Reportar o BUG", relief=FLAT)

        self.tp_princi.grid_columnconfigure(1, weight=1)
        self.fr_botoes.grid_columnconfigure(1, weight=1)
        self.fr_botoes.grid_columnconfigure(2, weight=1)

        self.bt_cancel.configure(command=lambda event=None: Bug.__destruir_interface(self))
        self.bt_report.configure(command=lambda event=None: Bug.__acessar_site_reporte(self))

        self.lb_label1.grid(row=1, column=1, sticky=NSEW)
        self.lb_label2.grid(row=2, column=1, sticky=NSEW)
        self.lb_label3.grid(row=3, column=1, sticky=NSEW)
        self.fr_botoes.grid(row=4, column=1, sticky=NSEW)
        self.bt_cancel.grid(row=1, column=1)
        self.bt_report.grid(row=1, column=2)

        self.tp_princi.deiconify()
        self.tp_princi.update()