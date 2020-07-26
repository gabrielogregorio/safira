from tkinter import Tk, Button, Label, Frame, PhotoImage, FLAT
import os
tela = Tk()
tela.configure(bg="#efefef")

fr_top = Frame(tela, bg="#efefef")
fr_top.grid(row=1, column=1)

lb1 = Label(fr_top, fg="#343434", bg="#efefef", text="""
     Essa escolha afetará a Interface gráfica e o idioma que as mensagens     
                         de erros serão exibidas
""")
lb1.grid(row=1, column=1)

# ======= IDIOMAS ========== #
fr_idionas = Frame(tela, bg="#efefef")
fr_idionas.grid(row=2, column=1)

base= "imagens/"


file_br = base + "ic_pt_br.png"
file_us = base + "ic_en_us.png"

im_br = PhotoImage(file=file_br)
im_us = PhotoImage(file=file_us)

im_br = im_br.subsample(1, 1)
im_us = im_us.subsample(1, 1)

global lista_botoes
lista_botoes = []

def marca_opcao(botao):
    global lista_botoes

    for bandeira in lista_botoes:
        if bandeira[1] == botao:
            bandeira[0].configure(bg="#bbbbbb")
            bandeira[1].configure(bg="#bbbbbb", activebackground="#bbbbbb")
            bandeira[2].configure(bg="#bbbbbb", activebackground="#bbbbbb",fg="green" )

            print(bandeira[2]['text'])
        else:
            bandeira[0].configure(bg="#efefef")
            bandeira[1].configure(bg="#efefef", activebackground="#efefef")
            bandeira[2].configure(bg="#efefef", activebackground="#efefef", fg="black")

fr_pt_br = Frame(fr_idionas, bd=10, bg="#efefef")
bt_pt_br = Button(fr_pt_br,  image=im_br, bg="#efefef", activebackground="#efefef", highlightthickness=0, relief=FLAT, bd=0)
bt_pt_br_2 = Label(fr_pt_br,  text="pt-br", bg="#efefef", activebackground="#efefef", highlightthickness=0, relief=FLAT, bd=0)
bt_pt_br["command"] = lambda bt_pt_br=bt_pt_br : marca_opcao(bt_pt_br)
lista_botoes.append([fr_pt_br, bt_pt_br, bt_pt_br_2])

fr_en_us = Frame(fr_idionas, bd=10, bg="#efefef")
bt_en_us = Button(fr_en_us,  image=im_us, bg="#efefef", activebackground="#efefef", highlightthickness=0, relief=FLAT, bd=0)
bt_en_us_2 = Label(fr_en_us,  text="en-us", bg="#efefef", activebackground="#efefef", highlightthickness=0, relief=FLAT, bd=0)
bt_en_us["command"] = lambda bt_en_us=bt_en_us : marca_opcao(bt_en_us)
lista_botoes.append([fr_en_us, bt_en_us, bt_en_us_2])

fr_pt_br.grid(row=1, column=1)
fr_en_us.grid(row=1, column=2)

bt_pt_br.grid(row=1, column=1)
bt_pt_br_2.grid(row=2, column=1)
bt_en_us.grid(row=1, column=2)
bt_en_us_2.grid(row=2, column=2)


tela.mainloop()

