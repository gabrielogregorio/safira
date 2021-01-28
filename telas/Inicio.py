from tkinter import *
from tkinter import Canvas 
import re
from os import listdir
from os import path

import util.funcoes as funcoes





class Inicio():
    def __init__(self, tela, design, idioma, interface_idioma, icon):

        self.tema_claro = PhotoImage(file='imagens/tema_claro.png')
        self.tema_escuro = PhotoImage(file='imagens/tema_escuro.png')
        self.tema_simples = PhotoImage(file='imagens/tema_simples.png')

        self.tema_claro = self.tema_claro.subsample(4, 4)
        self.tema_escuro = self.tema_escuro.subsample(4, 4)
        self.tema_simples = self.tema_simples.subsample(4, 4)





        self.tela = tela


        LARGURA = int(tela.winfo_screenwidth() / 6)
        t_heigth = tela.winfo_screenheight()


        design = {'bg':'#222232'}

        self.fr_texto = Frame(tela, width=LARGURA)
        self.fr_texto.grid_columnconfigure(1, weight=1)
        self.fr_texto.rowconfigure(2, weight=1)

        # ESPAÇO
        self.barra_superior = Frame(self.fr_texto, height=10, bg='#222232')
        self.barra_superior.grid(row=1, column=1, sticky=NSEW)

        self.fr_principal = Frame(self.fr_texto, bg='#222232')
        self.fr_principal.grid_columnconfigure(1, weight=1)
        self.fr_principal.rowconfigure(2, weight=1)
        self.fr_principal.grid(row=2, column=1, sticky=NSEW)




        # PARTE SUPERIOR #

        self.fr_botoes_superiores = Frame(self.fr_principal, height=100, bg='#222232')
        self.fr_botoes_superiores.grid_columnconfigure(1, weight=1)
        self.fr_botoes_superiores.grid(row=0, column=1, sticky=NSEW)

        self.frame_botoes = Frame(self.fr_botoes_superiores, bg='#222232')
        self.frame_botoes.grid(row=1, column=1, sticky=NSEW)

        self.bt_abrir_programa = Button(self.frame_botoes, text="Abrir Programa", relief='flat', fg="#bb33ff", activeforeground="#bb33ff", bg='#222232', activebackground="#222232", highlightthickness=4, font=("", 14), pady=5, bd=0)
        self.bt_abrir_programa.grid(row=1, column=1)

        self.lb_espaco = Label(self.frame_botoes,text=" ", bg='#222232').grid(row=1, column=2)

        self.bt_nova_aba = Button(self.frame_botoes, text="Nova Aba", relief='flat', fg="#bb33ff",activeforeground="#bb33ff", bg='#222232', activebackground="#222232", highlightthickness=4, font=("", 14), pady=5, bd=0)
        self.bt_nova_aba.grid(row=1, column=3)

        self.frame_cor_tema = Frame(self.fr_botoes_superiores, bg='#222232')
        self.frame_cor_tema.grid(row=1, column=2)

        self.lb_tema_cores = Label(self.frame_cor_tema, text="Tema de Cores", bg='#222232', foreground="white")
        self.lb_tema_cores.grid(row=1, column=1, columnspan=3, stick=NSEW)

        self.bt_tema_1 = Button(self.frame_cor_tema, image=self.tema_simples, bd=0, activebackground="#222232", bg='#222232', foreground="white")
        self.bt_tema_1.grid(row=2, column=1, sticky=NSEW)

        self.bt_tema_2 = Button(self.frame_cor_tema, image=self.tema_escuro, bd=0, activebackground="#222232", bg='#222232', foreground="white")
        self.bt_tema_2.grid(row=2, column=2, sticky=NSEW)

        self.bt_tema_3 = Button(self.frame_cor_tema, image=self.tema_claro, bd=0, activebackground="#222232", bg='#222232', foreground="white")
        self.bt_tema_3.grid(row=2, column=3, sticky=NSEW)

        self.lb_espaco = Label(self.frame_cor_tema,  bg="#222232",text=" ", font=("", 20)).grid(row=2, column=4, sticky=NSEW)



        # Meio
        self.lb_espaco = Label(self.fr_principal,  bg="#222232",text=" ", font=("", 20)).grid(row=1, column=4)


        # PARTE INFERIOR #         

        self.fr_opcoes_inferior = Frame(self.fr_principal, height=500, bg='#222232')
        self.fr_opcoes_inferior.grid_columnconfigure((1, 2) , weight=1)
        self.fr_opcoes_inferior.grid(row=2, column=1, sticky=NSEW)

        self.fr_aprender = Frame(self.fr_opcoes_inferior, bg='#222232')
        self.fr_aprender.grid_columnconfigure(1, weight=1)
        self.fr_aprender.grid(row=1, column=1, sticky=NSEW)



        dic_completo = dict(funcoes.ler_configuracoes())

        lista = dic_completo['abertos']
        itens = []
        if lista is not None:
            for item in lista:
                itens.append([item, item])





        self.carregar_opcoes('Recentes', self.fr_aprender,  {
            "tipo": "tutorial", # código
            "itens": itens
        })

        self.fr_recentes = Frame(self.fr_opcoes_inferior, bg='#222232')
        self.fr_recentes.grid_columnconfigure(1, weight=1)
        self.fr_recentes.grid(row=1, column=2, sticky=NSEW)

        self.carregar_opcoes('Aprender', self.fr_recentes, {
            "tipo": "tutorial", # código
            "itens": [
                #["texto", "link"]
                ["Meu Primeiro Programa.safira","programas/introdução.md"],
                ["aula dav.safira","programas/conceitos.md"],
                ["Olá.safira","hello.safira"]
            ]
        })


    def carregar_opcoes(self, nome, pai, dados):

        lb_aprender = Label(pai, text=nome, bg="#222232", fg="white", font=("", 14))
        lb_aprender.grid(row=1, column=1, sticky='w')

        fr_aprender = Frame(pai, bg="#222232")
        fr_aprender.grid(row=2, column=1, sticky=NSEW)
        fr_aprender.grid_columnconfigure(1, weight=1)

        pos = 1
        tipo = dados["tipo"]

        for k, v in dados["itens"]:
            bt_item = Button(fr_aprender, text=v,bd=0, activebackground="#222232", bg="#222232", justify="left", fg="#3399ff", activeforeground="#dd33ff")
            bt_item.grid(row=pos, column=1, sticky='w')
            pos = pos + 1






        
