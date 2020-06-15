from threading import Thread
from tkinter   import END
from copy      import deepcopy
from re        import finditer
from time      import time

class Colorir():
    def __init__(self, cor_do_comando, dic_comandos):
        self.cor_do_comando = cor_do_comando
        self.dic_comandos = dic_comandos
        self.tx_codfc = None
        self.tela = None
        self.historico_coloracao = []
        self.lista_todos_coloracao = []

    def alterar_cor_comando(self, novo_cor_do_comando):
        self.cor_do_comando = novo_cor_do_comando

    def __realiza_coloracao(self, palavra, linha, valor1, valor2, cor):
        linha1 = '{}.{}'.format(linha, valor1)
        linha2 = '{}.{}'.format(linha, valor2)

        self.tx_codfc.tag_add(palavra, linha1, linha2)
        self.tx_codfc.tag_config(palavra, foreground=cor)

        self.tela.update()

    def __marcar_coloracao(self, regex, lista, linha, palavra, cor):

        for valor in finditer(regex, lista[linha]):

            inicio_regex = valor.start()
            final_regex  = valor.end()

            usado = cor + str(palavra) + str(regex) + str(inicio_regex) + str(final_regex) + str(linha+1)

            self.historico_coloracao.append(usado)
            Colorir.__realiza_coloracao(self, str(usado), str(linha + 1), inicio_regex, final_regex, cor)

            if usado not in self.lista_todos_coloracao:
                self.lista_todos_coloracao.append(usado)


    def __filtrar_palavras(palavra):
        # Coreção para regex
        palavra_comando = palavra.replace('+', '\\+')
        palavra_comando = palavra_comando.replace('/', '\\/')
        palavra_comando = palavra_comando.replace('*', '\\*')
        palavra_comando = palavra_comando.replace(' ', '\\s*')

        return palavra_comando

    def __colorir_comandos(self, lista_linhas):
        for chave_comando, dicionario_comandos in self.dic_comandos.items():
            cor = self.cor_do_comando[ dicionario_comandos["cor"] ]["foreground"]

            for comando in dicionario_comandos["comando"]:

                palavra_analise = comando[0].strip()

                if palavra_analise == "": continue

                palavra_comando = Colorir.__filtrar_palavras(palavra_analise)
                regex = '(^|\\s){}(\\s|$)'.format(palavra_comando)

                for linha in range(len(lista_linhas)):
                    Colorir.__marcar_coloracao(self, regex, lista_linhas, linha, palavra_comando, cor)


    def __colorir_especial(self, lista):

        for linha in range(len(lista)):

            regex_comentario = '(#|\\/\\/).*$'
            regex_numerico = '(^|\\s|\\,)([0-9\\.]\\s*){1,}($|\\s|\\,)'
            regex_string = """\"[^"]*\""""

            cor_comentario = self.cor_do_comando["comentario"]["foreground"]
            cor_numerico = self.cor_do_comando["numerico"]["foreground"]
            cor_string = self.cor_do_comando["string"]["foreground"]

            Colorir.__marcar_coloracao(self, regex_numerico,lista,linha,'numerico',cor_numerico)
            Colorir.__marcar_coloracao(self, regex_string, lista, linha, '"', cor_string)
            Colorir.__marcar_coloracao(self, regex_comentario, lista, linha, 'comentario', cor_comentario)


    def coordena_coloracao(self, event, tx_codfc):
        self.tx_codfc = tx_codfc

        lista_linhas = self.tx_codfc.get(1.0, END).lower().split('\n')

        self.historico_coloracao = []

        Colorir.__colorir_comandos(self, lista_linhas)
        Colorir.__colorir_especial(self, lista_linhas)

        for palavra_nao_colorida in self.lista_todos_coloracao:
            if palavra_nao_colorida not in self.historico_coloracao:
                self.tx_codfc.tag_delete(palavra_nao_colorida)
                self.lista_todos_coloracao.remove(palavra_nao_colorida)

        if self.tela is not None:
            self.tela.update()

        return 0



