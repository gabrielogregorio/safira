from tkinter import *
import re
from os import listdir
from os import path

class Inicio():
    def __init__(self, tela, design, idioma, interface_idioma, icon):
        self.tela = tela

        LARGURA = int(tela.winfo_screenwidth() / 6)
        t_heigth = tela.winfo_screenheight()

        design = {'bg':'white'}

        self.fr_texto = Frame(tela, width=LARGURA)
        self.fr_texto.grid_columnconfigure(1, weight=1)
        self.fr_texto.rowconfigure(2, weight=1)

        self.barra_superior = Frame(self.fr_texto, height=10 ,bg='#f2f2f2')
        self.barra_superior.grid(row=1, column=1, sticky=NSEW)

        self.fr_principal = Frame(self.fr_texto)
        self.fr_principal.grid_columnconfigure(1, weight=1)
        self.fr_principal.rowconfigure(1, weight=1)
        self.fr_principal.grid(row=2, column=1, sticky=NSEW)


        #|                                    |        Tema de cores      |
        #| Abrir Programa  |          |       tema1 tema2 tema3   |
        #|----------------------------------------------------------------
        self.fr_botoes_superiores = Frame(self.fr_principal, height=100, bg='blue')
        self.fr_botoes_superiores.grid_columnconfigure(1, weight=1)
        self.fr_botoes_superiores.grid(row=0, column=1, sticky=NSEW)

        self.frame_botoes = Frame(self.fr_botoes_superiores)
        self.frame_botoes.grid(row=1, column=1, sticky=NSEW)

        self.bt_abrir_programa = Button(self.frame_botoes, text="Abrir Programa")
        self.bt_abrir_programa.grid(row=1, column=1)

        self.bt_nova_aba = Button(self.frame_botoes, text="Nova Aba")
        self.bt_nova_aba.grid(row=1, column=2)



        self.frame_cor_tema = Frame(self.fr_botoes_superiores)
        self.frame_cor_tema.grid(row=1, column=2)

        self.lb_tema_cores = Label(self.frame_cor_tema, text="Tema de Cores")
        self.lb_tema_cores.grid(row=1, column=1, columnspan=3, stick=NSEW)

        self.bt_tema_1 = Button(self.frame_cor_tema, text="Dark")
        self.bt_tema_1.grid(row=2, column=1, sticky=NSEW)

        self.bt_tema_2 = Button(self.frame_cor_tema, text="Escuro")
        self.bt_tema_2.grid(row=2, column=2, sticky=NSEW)

        self.bt_tema_3 = Button(self.frame_cor_tema, text="Claro")
        self.bt_tema_3.grid(row=2, column=3, sticky=NSEW)



        #|---------------------------------------------|
        #| Aprender                       Recentes     |
        #| Opções                         Opções       |
        self.fr_opcoes_inferior = Frame(self.fr_principal, height=500, bg='red')
        self.fr_opcoes_inferior.grid_columnconfigure((1, 2) , weight=1)
        self.fr_opcoes_inferior.grid(row=1, column=1, sticky=NSEW)

        self.fr_aprender = Frame(self.fr_opcoes_inferior)
        self.fr_aprender.grid_columnconfigure(1, weight=1)
        self.fr_aprender.grid(row=1, column=1, sticky=NSEW)

        self.carregar_opcoes(self.fr_aprender,  {
            "tipo": "tutorial", # código
            "itens": [
                #["texto", "link"]
                ["Introdução a Safira","tutorial/introdução.md"],
                ["Conceitos de programação","tutorial/conceitos.md"],
                ["Como usar a Safira","tutorial/comoUsarSafira.md"]
            ]
        })

        self.fr_recentes = Frame(self.fr_opcoes_inferior)
        self.fr_recentes.grid_columnconfigure(1, weight=1)
        self.fr_recentes.grid(row=1, column=2, sticky=NSEW)

        self.carregar_opcoes(self.fr_recentes, {
            "tipo": "tutorial", # código
            "itens": [
                #["texto", "link"]
                ["Meu Primeiro Programa.safira","programas/introdução.md"],
                ["aula dav.safira","programas/conceitos.md"],
                ["Olá.safira","hello.safira"]
            ]
        })


    def carregar_opcoes(self, pai, dados):

        lb_aprender = Label(pai, text="Aprender")
        lb_aprender.grid(row=1, column=1, sticky=NSEW)

        fr_aprender = Frame(pai)
        fr_aprender.grid(row=2, column=1, sticky=NSEW)
        fr_aprender.grid_columnconfigure(1, weight=1)

        pos = 1
        tipo = dados["tipo"]

        for k, v in dados["itens"]:
            bt_item = Button(fr_aprender, text="opc1")
            bt_item.grid(row=pos, column=1, sticky=NSEW)
            pos = pos + 1






        
