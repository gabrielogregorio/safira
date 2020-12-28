# -*- coding: utf-8 -*-

# ESSE PROGRAMA NAO PODE MUDAR.
# BIBLIOTECAS NOVAS DEVERÃO SER ANALISADAS COM CALMA.
from tkinter import Tk
from include.PhotoImage import PhotoImage

from sys import version

print(version)

# Colocado antes da inicialização de qualquer componente, prevenção de erro de inicialização do Tkinter no MacOS.
tela = Tk()

# Algum módulo está inicializando o Tk de forma errada, por isso a inicialização foi feita antes da importação dos módulos.
from telas.ide import Interface

# Instância de tela principal
tela.withdraw()
tela.rowconfigure(1, weight=1)
#tela.overrideredirect(1)
tela.grid_columnconfigure(1, weight=1)

# Traz barra de titulo
#tela.overrideredirect(0)

# Ocultar tkinter
tela.withdraw()
tela.title('Safira')
icon = PhotoImage(file='imagens/icone.png')
tela.call('wm', 'iconphoto', tela._w, icon)

instancia = Interface(tela, icon)
func_fechar_tela = lambda inst=tela: instancia.fechar_janela(inst)
tela.protocol("WM_DELETE_WINDOW", func_fechar_tela)

tela.mainloop()
