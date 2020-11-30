from threading import Thread
from tkinter import END
from copy import deepcopy
from re import finditer
from re import search
from re import sub
from time import time
from re import compile


class Colorir():
    def __init__(self, cor_do_comando, dic_comandos):
        self.cor_do_comando = cor_do_comando
        self.dic_comandos = dic_comandos

        self.tx_editor_codigo = None

        self.historico_coloracao = []
        self.lista_coloracao_atual = []

        self.linhas_ignorar = []

        # Lista de comandos compilados
        self.lista_comandos = []
        self.cor_comandos = []
        self.carregar_expressoes()

        self.regex_comentario = compile('(#|\\/\\/).*$')
        self.regex_numerico = compile('(^|\\s|\\,)([0-9\\.]\\s*){1,}($|\\s|\\,)')
        self.regex_string = compile("""\"[^"]*\"""")
        self.regex_chave = compile("{|}")
        self.regex_cor = compile("na\\s*cor\\s*\"(.*?)\"")

        self.num = 0

    def alterar_cor_comando(self, novo_cor_do_comando):
        self.cor_do_comando = novo_cor_do_comando
        self.carregar_expressoes()

    def __realiza_coloracao(self, palavra, linha, valor1, valor2, cor):
        self.tx_editor_codigo.tag_add(palavra, str(linha) + '.' + str(valor1), str(linha) + '.' + str(valor2))
        self.tx_editor_codigo.tag_config(palavra, foreground=cor)
        self.num += 1
        #print('-> ', self.num, str(linha) + '.' + str(valor1), str(linha) + '.' + str(valor2), palavra)

    def __marcar_coloracao(self, regex, lista, linha, palavra, i):

        for valor in finditer(regex, lista[linha]):

            inici_regex = valor.start()
            final_regex = valor.end()
            if inici_regex == final_regex: return 0

            cor = self.cor_comandos[i]

            usado = str(i + inici_regex + final_regex + linha) + str(palavra)

            self.lista_coloracao_atual.append(usado)

            if usado not in self.historico_coloracao:
                Colorir.__realiza_coloracao(self, str(usado), str(linha + 1), inici_regex, final_regex, cor)

    def __filtrar_palavras(palavra):
        palavra_comando = palavra.replace('+', '\\+')
        palavra_comando = palavra_comando.replace('/', '\\/')
        palavra_comando = palavra_comando.replace('*', '\\*')
        palavra_comando = palavra_comando.replace(' ', '[\\s{1,}|_]')
        return palavra_comando


    def carregar_expressoes(self):
        # cor, [re_comando1, re_comando2, re_comando3]
        self.lista_comandos = []
        self.cor_comandos = []

        for _, dicionario_comandos in self.dic_comandos.items():

            # Salva a cor de um comando
            self.cor_comandos.append(self.cor_do_comando[dicionario_comandos["cor"]]["foreground"])


            local_lista_comandos = []

            for comando in dicionario_comandos["comando"]:

                palavra_analise = comando[0].strip()

                if palavra_analise == "":
                    continue

                palavra_comando = Colorir.__filtrar_palavras(palavra_analise)

                regex = compile('(^|\\s){}(\\s|$)'.format(palavra_comando))

                local_lista_comandos.append(regex)

            self.lista_comandos.append(local_lista_comandos)


        # self.cor_comandos [comentario, numerico, logico, string]
        #    ..   ..    ..   -   -4        -3        -2      -1
        self.cor_comandos.append(self.cor_do_comando["comentario"]["foreground"])
        self.cor_comandos.append(self.cor_do_comando["numerico"]["foreground"])
        self.cor_comandos.append(self.cor_do_comando["logico"]["foreground"])
        self.cor_comandos.append(self.cor_do_comando["string"]["foreground"])


    def __colorir_comandos(self, lista_linhas):
        for i, comandos in enumerate(self.lista_comandos):
            for regex in comandos:
                for linha in range(len(lista_linhas)):
                    Colorir.__marcar_coloracao(self, regex, lista_linhas, linha, str(regex), i)

    def __colorir_especial(self, lista):

        for linha in range(len(lista)):

            # self.cor_comandos [comentario, numerico, logico, string]
            #    ..   ..    ..   -   -4        -3        -2      -1

            cor_cor = search(self.regex_cor, str(lista[linha]))

            Colorir.__marcar_coloracao(self, self.regex_numerico, lista, linha, 'numerico', -3)
            Colorir.__marcar_coloracao(self, self.regex_chave, lista, linha, 'chave', -2)
            Colorir.__marcar_coloracao(self, self.regex_string, lista, linha, '"', -1)

            if "#" in lista[linha]:
                Colorir.__marcar_coloracao(self, self.regex_comentario, lista, linha, 'comentario', -4)

            #if cor_cor is not None:
            #    cor_cor = str(cor_cor.group(1))
            #    Colorir.__marcar_coloracao(self, self.regex_cor, lista, linha, 'corcor', cor_cor)


    def coordena_coloracao(self, event, tx_editor_codigo):
        self.tx_editor_codigo = tx_editor_codigo

        lista_linhas = self.tx_editor_codigo.get(1.0, END).lower().split('\n')

        self.lista_coloracao_atual = []

        Colorir.__colorir_comandos(self, lista_linhas)
        Colorir.__colorir_especial(self, lista_linhas)

        for palavra_anterior in self.historico_coloracao:
            if palavra_anterior not in self.lista_coloracao_atual:
                self.tx_editor_codigo.tag_delete(palavra_anterior)
                self.historico_coloracao.remove(palavra_anterior)
        
        self.historico_coloracao = deepcopy(self.lista_coloracao_atual)

        return 0


