from tkinter import Frame
from tkinter import Label
from tkinter import Label
from tkinter import NSEW
from tkinter import Tk, Text
from time import sleep
from design import Design
from tkinter import *

tela = Tk()
#tela.withdraw()
#tela.overrideredirect(1)
tela.rowconfigure(1, weight=1)
tela.grid_columnconfigure(1, weight=1)


design = {'bg':'white'}


def criar_h1(texto):
    fr = Label(tela, design, text=texto, font=('', 26))
    fr.grid()

def criar_h2(texto):
    fr = Label(tela, design, text=texto, font=('', 24))
    fr.grid()

def criar_h3(texto):
    fr = Label(tela, design, text=texto, font=('', 22))
    fr.grid()

def criar_h4(texto):
    fr = Label(tela, design, text=texto, font=('', 20))
    fr.grid()

def criar_h5(texto):
    fr = Label(tela, design, text=texto, font=('', 18))
    fr.grid()

def criar_texto(texto):
    tx = Text(tela, design, font=('', 14), bd=0, padx=0, pady=0, inactiveselectbackground='#11fdfd', selectbackground='white')
    tx.insert(1.0, texto)
    tx.configure(state=DISABLED)
    tx.grid()




criar_h1('Merge sort')
criar_texto('Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort')

tela.mainloop()
