print('oi  '.count('%'))

quit()

from tkinter import *
import re
class Tutorial():
    def __init__(self, tela, design, idioma, interface_idioma, icon):
        self.tela = tela

        LARGURA = int(tela.winfo_screenwidth() / 6)
        t_heigth = tela.winfo_screenheight()

        design = {'bg':'white'}

        fr_texto = Frame(tela, width=LARGURA)
        fr_texto.grid_columnconfigure(1, weight=1)
        fr_texto.rowconfigure(1, weight=1)
        fr_texto.grid(row=1, column=1, sticky= NSEW)

        self.tx_tutorial = Text(fr_texto, design,wrap=WORD, font=('', 14), bd=0, padx=0, pady=0, inactiveselectbackground='#11fdfd', selectbackground='white', relief=FLAT)
        ys = Scrollbar(tela, orient='vertical', command=self.tx_tutorial.yview)
        xs = Scrollbar(tela, orient='horizontal', command=self.tx_tutorial.xview)

        self.tx_tutorial.configure(yscrollcommand=ys.set)
        self.tx_tutorial.configure(xscrollcommand=xs.set)
        self.tx_tutorial.grid(row=1, column=1, sticky=NSEW)

        self.escrever_tutorial('tutoriais/pt-br/apresentação.md')

        self.fr_botoes = Frame(tela, bg='red', height=30)
        self.fr_botoes.grid(row=2, column=1, sticky=NSEW)
        self.fr_botoes.grid_columnconfigure((1,2), weight=1)

        self.botao_anterior = Button(self.fr_botoes, text="", relief=FLAT)
        self.botao_anterior.grid(row=1, column=1, stick=NSEW)

        self.botao_anterior = Button(self.fr_botoes, text="Primeiro Programa", relief=FLAT)
        self.botao_anterior.grid(row=1, column=2, stick=NSEW)


    def ler_tutorial(self, dir_arquivo):
        with open(dir_arquivo, 'r', encoding='utf-8') as file:
            texto_tutorial = file.read()

        linhas = texto_tutorial.split('\n')

        acoes = []
        for linha in linhas:
            texto = linha.strip()
            if texto.startswith('- ['):
                linha = re.search('.*\\[(.*)\\]', texto)
                acoes.append(['lista', linha.group(1)])

            elif texto.startswith('####'):
                linha = re.search('#{1,}\\s*(.*)', texto)
                acoes.append(['subtitulo2', linha.group(1)])

            elif texto.startswith('###'):
                linha = re.search('#{1,}\\s*(.*)', texto)
                acoes.append(['subtitulo1', linha.group(1)])

            elif texto.startswith('##'):
                linha = re.search('#{1,}\\s*(.*)', texto)
                acoes.append(['subtitulo', linha.group(1)])

            elif texto.startswith('#'):
                linha = re.search('#{1,}\\s*(.*)', texto)
                acoes.append(['titulo', linha.group(1)])


            elif texto.startswith('*'):
                linha = re.search('\\*\\*(.*)\\*\\*', linha)
                acoes.append(['negrito', linha.group(1)])


            elif texto.startswith(';'):
                continue
            else:
                acoes.append(['texto', linha])

        return acoes

    def escrever_tutorial(self, dir_arquivo):

        acoes = self.ler_tutorial(dir_arquivo)
        #img = PhotoImage(file = "exemplo.png")
        #img = img.subsample(5, 5)
        # self.tx_tutorial.window_create(END, window = Label(self.tx_tutorial, image = img, bg='blue'))

        for acao in acoes:
            if acao[0] == 'lista':
                self.tx_tutorial.insert(END, '\n* {}'.format(acao[1]), ('texto'))

            elif acao[0] == 'titulo':
                self.tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('titulo'))

            elif acao[0] == 'subtitulo':
                self.tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('subtitulo'))

            elif acao[0] == 'texto':
                self.tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('texto'))

            elif acao[0] == 'negrito':
                self.tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('negrito'))

        self.tx_tutorial.tag_configure('titulo', font=('',20, 'bold'), selectbackground='#5b0391')
        self.tx_tutorial.tag_configure('subtitulo', font=('',15, 'bold'), selectbackground='#5b0391')
        self.tx_tutorial.tag_configure('subtitulo1', font=('',15), selectbackground='#5b0391')
        self.tx_tutorial.tag_configure('subtitulo2', font=('',14), selectbackground='#5b0391')

        self.tx_tutorial.tag_configure('texto', font=('',13), selectbackground='#5b0391')
        self.tx_tutorial.tag_configure('negrito', font=('',13, 'bold'), selectbackground='#5b0391')




        self.tx_tutorial.insert(END, '\n')
        self.tx_tutorial.configure(state=DISABLED)
        #self.tx_tutorial.see(END)




master = Tk()

#design = Design()
#design.update_design_dic()

# Configurações da IDE
#arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

# Idioma que a safira está configurada
#idioma = arquivo_configuracoes['idioma']
#interface_idioma = funcoes.carregar_json("configuracoes/interface.json")

#icon = PhotoImage(file='imagens/icone.png')
design = None
idioma =None
interface_idioma = None
icon = None
idioma = Tutorial(master, design, idioma, interface_idioma, icon)

master.mainloop()