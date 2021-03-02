from tkinter import *
import re
from os import listdir
from os import path


class Tutorial():
    def __init__(self, tela_referencia_tutorial:object):
        self.tela_referencia_tutorial = tela_referencia_tutorial

        LARGURA = int(self.tela_referencia_tutorial.winfo_screenwidth() / 6)
        t_heigth = self.tela_referencia_tutorial.winfo_screenheight()

        self.tutorial_fr_texto = Frame(self.tela_referencia_tutorial, width=LARGURA)
        self.tutorial_fr_texto.grid_columnconfigure(1, weight=1)
        self.tutorial_fr_texto.rowconfigure(2, weight=1)
        
        self.tutorial_barra_superior = Frame(self.tutorial_fr_texto, self.design.get("tutorial_barra_superior"))
        self.tutorial_barra_superior.grid(row=1, column=1, sticky=NSEW)

        self.__fr_principal = Frame(self.tutorial_fr_texto)
        self.__fr_principal.grid_columnconfigure(1, weight=1)
        self.__fr_principal.rowconfigure(1, weight=1)

        self.__tx_tutorial = Text(self.__fr_principal, self.design.get("tutorial_tx_tutorial"), wrap=WORD)
        self.__ys = Scrollbar(self.__fr_principal, orient='vertical', command=self.__tx_tutorial.yview)
        self.__tx_tutorial.configure(yscrollcommand=self.__ys.set)
        
        self.__tx_tutorial.grid(row=1, column=1, sticky=NSEW)
        self.__ys.grid(row=1, column=2, sticky=NS)
        self.__fr_principal.grid(row=2, column=1, sticky=NSEW)

        self.__dir_file = 'tutoriais/pt-br/'
        self.__arquivos = listdir(self.__dir_file)
        self.__arquivos.sort(reverse=False)
        self.__posicao = -1
        
        self.tutorial_fr_botoes = Frame(self.tela_referencia_tutorial, self.design.get("tutorial_fr_botoes"))
        self.tutorial_fr_botoes.grid_columnconfigure((1,2), weight=1)

        self.__botao_anterior = Button(self.tutorial_fr_botoes,  self.design.get("tutorial_botao_anterior"), text="{:^22}".format(""), command=lambda: self.tutorial_anterior())
        self.__botao_anterior.grid(row=1, column=1, stick=NSEW)

        self.__botao_proximo = Button(self.tutorial_fr_botoes,  self.design.get("tutorial_botao_proximo"), text='{:^22}'.format("Proxima Aula"), command=lambda: self.tutorial_proximo())
        self.__botao_proximo.grid(row=1, column=2, stick=NSEW)

        self.tutorial_proximo()

    def tutorial_proximo(self):
        if self.__posicao == len(self.__arquivos)-1:
            return 0

        self.__posicao += 1
        print(self.__posicao,  self.__arquivos[self.__posicao])
        arquivo = path.join(self.__dir_file, self.__arquivos[self.__posicao])

        self.tutorial_escrever_tutorial(arquivo)

        if self.__posicao == len(self.__arquivos)-1:
            self.__botao_proximo['text'] = '{:^22}'.format("Finalizar Tutorial")
        elif self.__posicao != 0:
            self.__botao_anterior['text'] = '{:^22}'.format('Voltar Aula')

    def tutorial_anterior(self):
        if self.__posicao < 1:
            return 0

        self.__posicao -= 1
        print(self.__posicao, self.__arquivos[self.__posicao])

        arquivo = path.join(self.__dir_file, self.__arquivos[self.__posicao])

        self.tutorial_escrever_tutorial(arquivo)

        if self.__posicao > 1:
            self.__botao_proximo['text'] = '{:^22}'.format("Proxima Aula")
        elif self.__posicao == 0:
            self.__botao_anterior['text'] = '{:^22}'.format(' ')


    def tutorial_ler_tutorial(self, dir_arquivo:str):
        with open(dir_arquivo, 'r', encoding='utf-8') as file:
            texto_tutorial = file.read()

        linhas = texto_tutorial.split('\n')
        inicio_codigo = False
        acoes = []
        texto_codigo = ""
        for linha in linhas:
            if linha == '```' and not inicio_codigo:
                inicio_codigo = True
                continue

            if inicio_codigo and linha != '```':
                texto_codigo = texto_codigo + linha + '\n'
                continue

            if inicio_codigo and linha == '```':
                inicio_codigo = False
                acoes.append(['codigo', texto_codigo])
                texto_codigo = ""
                continue

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

    def tutorial_escrever_tutorial(self, dir_arquivo:str):

        self.__tx_tutorial.configure(state=NORMAL)
        self.__tx_tutorial.delete('1.0', END)
        acoes = self.tutorial_ler_tutorial(dir_arquivo)

        for acao in acoes:
            if acao[0] == 'lista':
                self.__tx_tutorial.insert(END, '\n* {}'.format(acao[1]), ('texto'))

            elif acao[0] == 'titulo':
                self.__tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('titulo'))

            elif acao[0] == 'subtitulo':
                self.__tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('subtitulo'))

            elif acao[0] == 'texto':
                self.__tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('texto'))

            elif acao[0] == 'negrito':
                self.__tx_tutorial.insert(END, '\n{}'.format(acao[1]), ('negrito'))

            elif acao[0] == 'codigo':
                self.__tx_tutorial.insert(END, '\n{}'.format(""), ('texto'))
                self.__tx_tutorial.insert(END, '{}'.format(acao[1]), ('codigo'))
                self.__tx_tutorial.insert(END, '\n{}'.format(""), ('texto'))

        self.__tx_tutorial.tag_configure('titulo', self.design.get("tutorial_tag_titulo"))
        self.__tx_tutorial.tag_configure('subtitulo',  self.design.get("tutorial_tag_subtitulo"))
        self.__tx_tutorial.tag_configure('subtitulo1',  self.design.get("tutorial_tag_subtitulo1"))
        self.__tx_tutorial.tag_configure('subtitulo2',  self.design.get("tutorial_tag_subtitulo2"))

        self.__tx_tutorial.tag_configure('texto',  self.design.get("tutorial_tag_texto"))
        self.__tx_tutorial.tag_configure('negrito', self.design.get("tutorial_tag_negrito"))

        self.__tx_tutorial.tag_configure('codigo', self.design.get("tutorial_tag_codigo"))

        self.__tx_tutorial.insert(END, '\n')
        self.__tx_tutorial.configure(state=DISABLED)
        #self.__tx_tutorial.see(END)
