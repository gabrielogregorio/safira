
from tkinter import *
from tkinter import ttk

tela = Tk()
tela.geometry('1000x500+100+100')
tela.rowconfigure((1, 2), weight=1)
tela.grid_columnconfigure(1, weight=1)

fr_vazio = Frame(tela)
fr_vazio.grid(row=1, column=1, rowspan=2, sticky=NSEW)

tx = Text(fr_vazio,wrap=WORD,  font=('', 14), bd=0, padx=0, pady=0, inactiveselectbackground='#11fdfd', selectbackground='white', relief=FLAT)
ys = Scrollbar(fr_vazio, orient = 'vertical', command = tx.yview)
xs = Scrollbar(fr_vazio, orient = 'horizontal', command = tx.xview)
tx['yscrollcommand'] = ys.set
tx['xscrollcommand'] = xs.set
tx.grid()



### ======================================= ##
fr_pesquisar = Frame(tela, bg='#343434', pady=10)
fr_pesquisar.grid_columnconfigure(2, weight=1)
fr_pesquisar.grid(row=3, column=1, sticky=NSEW)

lista_valores = ['texto', 'regex']
largura = 0

for i in lista_valores:
	if len(i) > largura:
		largura = len(i)
largura += 2

def pesquisar(texto, regexp=True):
	try:
		tx.tag_delete('search')
	except Exception as erro:
		print(erro)

	countVar = StringVar()
	pos = tx.search(texto, "1.0", stopindex="end", count=countVar, regexp=regexp)
	if pos == '': return 0

	inicio = str(pos)

	x, y = inicio.split('.')
	y = int(y) + int(countVar.get())
	fim = '{}.{}'.format(x, y)

	tx.tag_add ('search', str(pos),  fim)
	tx.tag_configure('search', background='#52d9ff') 


countryvar = StringVar()
cbx = ttk.Combobox(fr_pesquisar, values=lista_valores, width=largura)
cbx.set(lista_valores[0])
print(cbx.get())
cbx.grid(row=1, column=1)

et_pesquisa = Entry(fr_pesquisar, bg='#343434', fg='white', relief=SUNKEN, bd=1, highlightcolor='#373737')
et_pesquisa.grid(row=1, column=2, sticky=NSEW)
img = PhotoImage(file='imagens/ic_pesquisa.png')
img = img.subsample(3,3)
et_pesquisa.get()

bt_pesquisar = Button(fr_pesquisar, image=img, background='#343434', activebackground='#343434', relief=SUNKEN, bd=0)
bt_pesquisar['command'] = lambda et=et_pesquisa: pesquisar(et.get())
bt_pesquisar.grid(row=1, column=3)




tela.mainloop()

