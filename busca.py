
from tkinter import *
from tkinter import ttk

tela = Tk()
tela.geometry('1000x500+100+100')
tela.rowconfigure((1, 2, 3), weight=1)
tela.grid_columnconfigure(1, weight=1)

fr_vazio = Frame(tela)
fr_vazio.grid(row=1, column=1, rowspan=2, sticky=NSEW)


### ======================================= ##
fr_pesquisar = Frame(tela, bg='#343434')
fr_pesquisar.grid_columnconfigure(2, weight=1)
fr_pesquisar.grid(row=3, column=1, sticky=NSEW)

lista_valores = ['texto', 'regex']
largura = 0

for i in lista_valores:
	if len(i) > largura:
		largura = len(i)
largura += 2


combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'blue',
                                       'fieldbackground': '#343434',
                                       'background': '#343434',
                                       'foreground': '#ffffff',
                                       'relief': 'flat'
                                       }}}
                         )
# ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
combostyle.theme_use('combostyle') 


countryvar = StringVar()
cbx = ttk.Combobox(fr_pesquisar, values=lista_valores, width=largura)
cbx.set(lista_valores[0])
print(cbx.get())
cbx.grid(row=1, column=1)

et_pesquisa = Entry(fr_pesquisar)
et_pesquisa.grid(row=1, column=2, sticky=NSEW)

bt_pesquisar = Button(fr_pesquisar, text='lupa', background='#ffaa3b')
bt_pesquisar.grid(row=1, column=3)




tela.mainloop()

