from threading import Thread
from tkinter import Toplevel
from tkinter import Label
from tkinter import Frame
from tkinter import Button
from tkinter import NSEW
from tkinter import FLAT
from tkinter import PhotoImage
from webbrowser import open as webbrowser_open


class ReportBug(object):
    def __init__(self):
        self.__bt_report = None
        self.__image_bug = None
        self.__bt_cancel = None
        self.__fr_botoes = None
        self.__lb_label3 = None
        self.__lb_label2 = None
        self.__lb_label1 = None
        self.__tp_princi = None

    def __acessar_site_reporte(self):
        website_forms = "https://forms.gle/J4kE2Li8c58fz4hh6"

        self.__bt_report.configure(
            text=self.interface_idioma["abrir_formulario"][self.idioma])

        t = Thread(target=lambda event=None: webbrowser_open(website_forms))
        t.start()

        self.__destruir_interface()

    def __destruir_interface(self):
        self.__bt_report.destroy()
        self.__bt_cancel.destroy()
        self.__fr_botoes.destroy()
        self.__lb_label3.destroy()
        self.__lb_label2.destroy()
        self.__lb_label1.destroy()
        self.__tp_princi.destroy()

    def bug_carregar_tela(self):
        self.__image_bug = PhotoImage(file="imagens/bug.png")
        self.__image_bug = self.__image_bug.subsample(4) 

        self.__tp_princi = Toplevel(self.master, bd=10, bg=self.design.dic["bug_lb1_encontrou_bug"]["bg"])
        self.__tp_princi.resizable(False, False)
        self.__tp_princi.title(self.interface_idioma["titulo_reporte_bug"][self.idioma])
        self.__tp_princi.tk.call('wm', 'iconphoto', self.__tp_princi._w, self.icon)
        self.__tp_princi.withdraw()

        try:
            self.__tp_princi.wm_attributes('-type', 'splash')
        except Exception as erro:
            print("Erro ao remover barra de titulos => ", erro)

        self.__lb_label1 = Label(self.__tp_princi)
        self.__lb_label2 = Label(self.__tp_princi)
        self.__lb_label3 = Label(self.__tp_princi)

        self.__lb_label1.configure(self.design.dic["bug_lb1_encontrou_bug"])
        self.__lb_label2.configure(self.design.dic["bug_lb2_encontrou_bug"])
        self.__lb_label3.configure(self.design.dic["bug_lb3_encontrou_bug"])

        self.__lb_label1.configure(text=self.interface_idioma["encontrou_bug"][self.idioma])
        self.__lb_label2.configure(image=self.__image_bug)
        self.__lb_label3.configure(text=self.interface_idioma["texto_reportar_bug"][self.idioma])

        self.__fr_botoes = Frame(self.__tp_princi, self.design.dic["bug_fr_bt_encontrou_bug"])
        self.__bt_cancel = Button(self.__fr_botoes, self.design.dic["bug_bt_canc_encontrou_bug"], text=self.interface_idioma["texto_depois"][self.idioma], relief=FLAT)
        self.__bt_report = Button(self.__fr_botoes, self.design.dic["bug_bt_report_encontrou_bug"], text=self.interface_idioma["texto_reporte_bug"][self.idioma], relief=FLAT)

        self.__tp_princi.grid_columnconfigure(1, weight=1)
        self.__fr_botoes.grid_columnconfigure(1, weight=1)
        self.__fr_botoes.grid_columnconfigure(2, weight=1)

        self.__bt_cancel.configure(command=lambda event=None: self.__destruir_interface())
        self.__bt_report.configure(command=lambda event=None: self.__acessar_site_reporte())

        self.__lb_label1.grid(row=1, column=1, sticky=NSEW)
        self.__lb_label2.grid(row=2, column=1, sticky=NSEW)
        self.__lb_label3.grid(row=3, column=1, sticky=NSEW)
        self.__fr_botoes.grid(row=4, column=1, sticky=NSEW)
        self.__bt_cancel.grid(row=1, column=1)
        self.__bt_report.grid(row=1, column=2)

        self.__tp_princi.update() 
        self.__tp_princi.deiconify()
