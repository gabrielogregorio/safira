from tkinter import Frame
from tkinter import Label
from tkinter import Label
from tkinter import NSEW
from tkinter import Tk
from time import sleep
from platform import system as platform_system


""" Tela inicial de Splash """


class Splash:
    def __init__(self):

        self.__tela_splash = Tk()
        self.__tela_splash.withdraw()
        self.__tela_splash.overrideredirect(1)
        self.__tela_splash.rowconfigure(1, weight=1)
        self.__tela_splash.grid_columnconfigure(1, weight=1)

        self.__frame_splash= Frame(master=self.__tela_splash)

        self.__fr_splash = Frame(self.__frame_splash)
        self.__l1_splash = Label(self.__frame_splash, self.design.get("splash_cor_intro"))
        self.__l2_splash = Label(self.__frame_splash, self.design.get("splash_cor_intro"))

        try:
            background = self.design.get("splash_cor_intro")["background"]
        except Exception as erro:
            print(erro)
            background = "white"

        self.__frame_splash.configure(background=background)
        self.__frame_splash.rowconfigure(1, weight=1)
        self.__frame_splash.grid_columnconfigure(0, weight=1)

        self.__fr_splash.configure(background=background)
        self.__l1_splash.configure(text=" SAFIRA 0.3", font=("Lucida Sans", 90), bd=80)

        self.__frame_splash.grid(row=1, column=1, sticky=NSEW)
        self.__fr_splash.grid(row=0, column=1, sticky=NSEW)
        self.__l1_splash.grid(row=1, column=1, sticky=NSEW)
        self.__l2_splash.grid(row=2, column=1, sticky=NSEW)

        # Ocultar tela
        self.__frame_splash.update()
        self.__tela_splash.update()
        self.__tela_splash.withdraw()

        j_width = self.__tela_splash.winfo_reqwidth()
        j_height = self.__tela_splash.winfo_reqheight()

        t_width = self.__tela_splash.winfo_screenwidth()
        t_heigth = self.__tela_splash.winfo_screenheight()

        geometria = "+{}+{}".format(int(t_width/2)-int(j_width/2), int(t_heigth/2)-int(j_height/2))

        # Tornar tela visível
        self.__tela_splash.geometry(geometria)
        self.__tela_splash.deiconify()
        self.__tela_splash.update()

    def splash_fim(self):
        self.__frame_splash.update()
        self.__tela_splash.update()
        self.__tela_splash.withdraw()

        self.__fr_splash.destroy()
        self.__l1_splash.destroy()
        self.__l2_splash.destroy()
        self.__frame_splash.destroy()
        self.__tela_splash.destroy()
