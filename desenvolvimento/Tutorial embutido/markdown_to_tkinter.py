from tkinter import *

tela = Tk()
tela.grid_columnconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)

LARGURA = int(tela.winfo_screenwidth() / 6)
t_heigth = tela.winfo_screenheight()


design = {'bg':'white'}

fr_texto = Frame(tela, width=LARGURA)
fr_texto.grid_columnconfigure(1, weight=1)
fr_texto.rowconfigure(1, weight=1)
fr_texto.grid(row=1, column=1, sticky= NSEW)




tx = Text(fr_texto, design,wrap=WORD, font=('', 14), bd=0, padx=0, pady=0, inactiveselectbackground='#11fdfd', selectbackground='white', relief=FLAT)
ys = Scrollbar(tela, orient='vertical', command=tx.yview)
xs = Scrollbar(tela, orient='horizontal', command=tx.xview)
tx.configure(yscrollcommand=ys.set)
tx.configure(xscrollcommand=xs.set)
tx.grid(row=1, column=1, sticky=NSEW)

img = PhotoImage(file = "exemplo.png")
img = img.subsample(5, 5)

tx.insert(END, 'Merge sort', ('titulo'))
tx.insert(END, '\nAlgoritmo de ordenação', ('subtitulo'))
tx.insert(END, '\n\nO merge sort, ou ordenação por mistura, é um exemplo de algoritmo de ordenação por comparação do tipo dividir-para-conquistar. Sua ideia básica consiste em Dividir e Conquistar.', ('texto'))

tx.tag_configure('titulo', font=('',20, 'bold'), selectbackground='#11fdfd')
tx.tag_configure('subtitulo', font=('',15), selectbackground='#11fdfd')
tx.tag_configure('texto', font=('',13), selectbackground='#11fdfd')

tx.window_create(END, window = Label(tx, image = img, bg='blue'))

tx.insert(END, '\n\n\n\n')



tx.window_create(END, window=Frame(tx, bg='red'))


tx.configure(state=DISABLED)

tx.see(END)
tela.mainloop()