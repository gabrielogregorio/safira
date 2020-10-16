from tkinter import *

tela = Tk()
#tela.withdraw()
#tela.overrideredirect(1)


LARGURA = int(tela.winfo_screenwidth() / 6)
t_heigth = tela.winfo_screenheight()
print(LARGURA)

design = {'bg':'white'}

fr_texto = Frame(tela, width=LARGURA)
fr_texto.grid_columnconfigure(1, weight=1)
fr_texto.grid(column=1, sticky= NSEW)


def add_image():
    #tx.image_create(END, image = img)
    tx.window_create(END, window = Label(tx, image = img, bg='blue'))

def add_text(texto):
    tx.insert(END, texto)

tx = Text(fr_texto, design,wrap=WORD,  font=('', 14), bd=0, padx=0, pady=0, inactiveselectbackground='#11fdfd', selectbackground='white', relief=FLAT)
ys = Scrollbar(tela, orient = 'vertical', command = tx.yview)
xs = Scrollbar(tela, orient = 'horizontal', command = tx.xview)
tx['yscrollcommand'] = ys.set
tx['xscrollcommand'] = xs.set

tx.grid()
img = PhotoImage(file = "exemplo.png")

 

tx.tag_add ('destaque', 1.0,  'end')

tx.tag_configure('destaque', background='yellow', font=('',20))
tx.insert (END, 'novo material a inserir', ('destaque'))


add_text("""\nOrigem: red     car Wikipédia, """) #a enciclopédia livre. Saltar par Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort Origem: Wikipédia, a enciclopédia livre. Saltar para a navegaçãoSaltar para a pesquisa Merge sort fim, esta é a uma linha da bagaça

countVar = StringVar()
pos = tx.search("red\\s*car", "1.0", stopindex="end", count=countVar, regexp=True)
inicio = str(pos)

x, y = inicio.split('.')
y = int(y) + int(countVar.get())
fim = '{}.{}'.format(x, y)

tx.tag_add ('search', str(pos),  fim)
tx.tag_configure('search', background='green', font=('',20))

print()



#add_image()




tx.configure(state=DISABLED)

tx.see(END)
tela.mainloop()