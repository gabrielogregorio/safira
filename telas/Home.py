from tkinter import *
from tkinter import Canvas 
import re
from os import listdir
from os import path
import util.funcoes as funcoes

 
class Home():
    def __init__(self, frame_referencia:object):
        self.inicio_lista_botoes = []

        self.__tema_claro = PhotoImage(file='imagens/tema_claro.png')
        self.__tema_escuro = PhotoImage(file='imagens/tema_escuro.png')
        self.__tema_simples = PhotoImage(file='imagens/tema_simples.png')

        self.__tema_claro = self.__tema_claro.subsample(4, 4)
        self.__tema_escuro = self.__tema_escuro.subsample(4, 4)
        self.__tema_simples = self.__tema_simples.subsample(4, 4)

        self.frame_referencia = frame_referencia

        LARGURA = int(self.frame_referencia.winfo_screenwidth() / 6)
        t_heigth = self.frame_referencia.winfo_screenheight()

        self.inicio_fr_texto = Frame(self.frame_referencia, width=LARGURA)
        self.inicio_fr_texto.grid_columnconfigure(1, weight=1)
        self.inicio_fr_texto.rowconfigure(2, weight=1)

        self.__fr_principal = Frame(self.inicio_fr_texto, self.design.get("inicio_fr_principal"))
        self.__fr_principal.grid_columnconfigure(1, weight=1)
        self.__fr_principal.rowconfigure(2, weight=1)
        self.__fr_principal.grid(row=2, column=1, sticky=NSEW)

        # PARTE SUPERIOR #
        self.__fr_botoes_superiores = Frame(self.__fr_principal, self.design.get("inicio_fr_botoes_superiores"))
        self.__fr_botoes_superiores.grid_columnconfigure(1, weight=1)
        self.__fr_botoes_superiores.grid(row=0, column=1, sticky=NSEW)

        self.__frame_botoes = Frame(self.__fr_botoes_superiores, self.design.get("inicio_frame_botoes"))
        self.__frame_botoes.grid(row=1, column=1, sticky=NSEW)

        self.__bt_abrir_programa = Button(self.__frame_botoes, self.design.get("inicio_bt_abrir_programa"), text="Abrir Programa")
        self.__bt_abrir_programa.grid(row=1, column=1)

        self.__lb_espaco = Label(self.__frame_botoes,self.design.get("inicio_lb_espaco"), text=" ", ).grid(row=1, column=2)

        self.__bt_nova_aba = Button(self.__frame_botoes, self.design.get("inicio_bt_abrir_programa"), text="Nova Aba")
        self.__bt_nova_aba.grid(row=1, column=3)

        self.__frame_cor_tema = Frame(self.__fr_botoes_superiores, self.design.get("inicio_frame_cor_tema"))
        self.__frame_cor_tema.grid(row=1, column=2)

        self.__lb_tema_cores = Label(self.__frame_cor_tema, self.design.get("inicio_lb_tema_cores"), text="Tema de Cores")
        self.__lb_tema_cores.grid(row=1, column=1, columnspan=3, stick=NSEW)

        self.__bt_tema_1 = Button(self.__frame_cor_tema, self.design.get("inicio_bt_tema"), image=self.__tema_simples, )
        self.__bt_tema_1.grid(row=2, column=1, sticky=NSEW)

        self.__bt_tema_2 = Button(self.__frame_cor_tema, self.design.get("inicio_bt_tema"), image=self.__tema_escuro)
        self.__bt_tema_2.grid(row=2, column=2, sticky=NSEW)

        self.__bt_tema_3 = Button(self.__frame_cor_tema, self.design.get("inicio_bt_tema"), image=self.__tema_claro)
        self.__bt_tema_3.grid(row=2, column=3, sticky=NSEW)

        self.__lb_espaco = Label(self.__frame_cor_tema, self.design.get("inicio_lb_espaco2")).grid(row=2, column=4, sticky=NSEW)

        # Lista de cores/temas
        self.inicio_lista_botoes = [[self.__bt_tema_1, 'simples.json'], [self.__bt_tema_2, 'escuro.json'], [self.__bt_tema_3, 'claro.json']]

        # Meio
        self.__lb_espaco = Label(self.__fr_principal, self.design.get("inicio_lb_espaco2")).grid(row=1, column=4)

        # PARTE INFERIOR #
        self.__fr_opcoes_inferior = Frame(self.__fr_principal, self.design.get("inicio_fr_opcoes"))
        self.__fr_opcoes_inferior.grid_columnconfigure((1, 2) , weight=1)
        self.__fr_opcoes_inferior.grid(row=2, column=1, sticky=NSEW)

        self.__fr_aprender = Frame(self.__fr_opcoes_inferior, self.design.get("inicio_fr_opcoes"))
        self.__fr_aprender.grid_columnconfigure(1, weight=1)
        self.__fr_aprender.grid(row=1, column=1, sticky=NSEW)

        dic_completo = dict(funcoes.ler_configuracoes())

        lista = dic_completo['abertos']
        itens = []
        if lista is not None:
            for item in lista:
                itens.append([item, item])

        self.__carregar_opcoes('Recentes', self.__fr_aprender,  {
            "tipo": "tutorial", # código
            "itens": itens
        })

        self.__fr_recentes = Frame(self.__fr_opcoes_inferior, self.design.get("inicio_fr_recentes"))
        self.__fr_recentes.grid_columnconfigure(1, weight=1)
        self.__fr_recentes.grid(row=1, column=2, sticky=NSEW)

        self.__carregar_opcoes('Aprender', self.__fr_recentes, {
            "tipo": "tutorial", # código
            "itens": [
                #["texto", "link"]
                ["Meu Primeiro Programa.safira","programas/introdução.md"],
                ["aula dav.safira","programas/conceitos.md"],
                ["Olá.safira","hello.safira"]
            ]
        })

    def __carregar_opcoes(self, nome:str, pai:object, dados:list):

        lb_aprender = Label(pai, self.design.get("inicio_lb_especial"), text=nome)
        lb_aprender.grid(row=1, column=1, sticky='w')

        fr_aprender = Frame(pai, self.design.get("inicio_fr_especial"))
        fr_aprender.grid(row=2, column=1, sticky=NSEW)
        fr_aprender.grid_columnconfigure(1, weight=1)

        pos = 1
        tipo = dados["tipo"]

        for k, v in dados["itens"]:
            if pos == 15:
                break

            bt_item = Button(fr_aprender, self.design.get("inicio_bt_especial"), text=v)
            bt_item['command'] = lambda link = v: self.__abrir_script(link)
            bt_item.grid(row=pos, column=1, sticky='w')
            pos = pos + 1


    def __abrir_script(self, link:str):
        self.abrir_nova_aba(None)
        self.manipular_arquivos(None, "abrirArquivo", link)
