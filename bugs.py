from tkinter import Button
from tkinter import Label
from tkinter import NSEW
from tkinter import Button
from tkinter import Tk
from tkinter import PhotoImage
import webbrowser

def acessar_site_reporte(event = None):
    bt_report.configure(text="Abrindo formulário do Google")
    webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSdVCN6eIPVs9KHlLZ2PiiAA6xcNM9jeQVLrLG1XvMXNWsAIkQ/viewform?usp=pp_url") 

tela = Tk()
lb1 = Label(tela, text="  Então você encontrou um bug?  ", font=("",30), bg="#363636", fg="#efefef")

try:
    image_bug = PhotoImage(file="imagens/bug.png")
    image_bug = image_bug.subsample(2)
    lb2 = Label(tela, image=image_bug, bg="#363636", fg="#efefef")

except Exception as erro:
    lb2 = Label(tela, text="\n\nErro ao carregar imagem de BUG, erro: " + str(erro), bg="#363636", fg="#efefef")

lb3 = Label(tela, text="""\nVocê gostaria de reportar para nós?\n\n Isso nos ajuda a produzir algo melhor, vamos\n ficar felizes em ter o seu feedback!\n""")
bt_report = Button(tela, text="Reportar o BUG", fg="#efefef")

lb3.configure(font=("",15), bg="#363636", fg="#efefef")
bt_report.configure(font=("",15), bg="#363636", fg="#efefef", activebackground="#393939", activeforeground="#efefef", highlightcolor="red", highlightbackground="#494949", command=acessar_site_reporte)

lb1.grid(row=1, column=1, sticky=NSEW)
lb2.grid(row=2, column=1, sticky=NSEW)
lb3.grid(row=3, column=1, sticky=NSEW)
bt_report.grid(row=4, column=1, sticky=NSEW)

tela.mainloop()