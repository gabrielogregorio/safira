from telas.atualizar import Atualizar
from tkinter import Tk
from tkinter import PhotoImage
from telas.design import Design
from telas.bug import Bug
from telas.splash import Splash
from time import sleep
import util.funcoes as funcoes
import tkinter.font as tkFont
from tkinter import Button


def atualizar():
    master = Tk()

    design = Design()
    design.update_design_dic()

    # Configurações da IDE
    arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

    # Idioma que a safira está configurada
    idioma = arquivo_configuracoes['idioma']
    interface_idioma = funcoes.carregar_json("configuracoes/interface.json")
    icon = PhotoImage(file='imagens/icone.png')

    atualizar = Atualizar(master, design, idioma, interface_idioma, icon)

    # Quando a safira é iniciado
    # Verificar a primeira vez
    # Primeira vez não mostra mensagem de erro
    # e nem mensagem se estiver atualizado
    #atualizar.verificar_versao(primeira_vez=True)

    # Quando o usuário tenta buscar atualizações de
    atualizar.verificar_versao()
    #atualizar.aviso_aguarde_instalando('0.25')

    master.mainloop()






def bug():
    master = Tk()

    design = Design()
    design.update_design_dic()

    # Configurações da IDE
    arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

    # Idioma que a safira está configurada
    idioma = arquivo_configuracoes['idioma']
    interface_idioma = funcoes.carregar_json("configuracoes/interface.json")
    icon = PhotoImage(file='imagens/icone.png')

    bug = Bug(master, design, idioma, interface_idioma, icon)
    bug.interface()

    master.mainloop()


def splash():
    master = Tk()

    # Obter o Design de interfaces
    design = Design()
    design.update_design_dic()

    sp = Splash(design)
    sleep(5)
    sp.splash_fim()

    master.mainloop()


'''
root = Tk()
fonts=list(tkFont.families()) 

for fonte in sorted(fonts):
    if 'mono' in fonte.lower():
        print(fonte)

'''

from telas.tutorial import Tutorial
from tkinter import NSEW
def tutorial():
    master = Tk()

    design = Design()
    design.update_design_dic()

    # Configurações da IDE
    arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

    # Idioma que a safira está configurada
    idioma = arquivo_configuracoes['idioma']
    interface_idioma = funcoes.carregar_json("configuracoes/interface.json")
    icon = PhotoImage(file='imagens/icone.png')


    master.grid_columnconfigure(2, weight=1)
    master.rowconfigure(1, weight=1)

    tutorial = Tutorial(master, design, idioma, interface_idioma, icon)
    tutorial.barra_superior.grid(row=0, column=1, sticky=NSEW)
    tutorial.fr_texto.grid(row=1, column=2, columnspan=2, sticky= NSEW)
    tutorial.fr_botoes.grid(row=2, column=2, columnspan=2, sticky=NSEW)


    master.mainloop()

from telas.Inicio import Inicio
def tela_inicio():
    master = Tk()

    design = Design()
    design.update_design_dic()

    # Configurações da IDE
    arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

    # Idioma que a safira está configurada
    idioma = arquivo_configuracoes['idioma']
    interface_idioma = funcoes.carregar_json("configuracoes/interface.json")
    icon = PhotoImage(file='imagens/icone.png')


    master.grid_columnconfigure(2, weight=1)
    master.rowconfigure(1, weight=1)

    tela_inicio = Inicio(master, design, idioma, interface_idioma, icon)
    tela_inicio.barra_superior.grid(row=0, column=1, sticky=NSEW)
    tela_inicio.fr_texto.grid(row=1, column=2, columnspan=2, sticky= NSEW)


    master.mainloop()
tela_inicio()