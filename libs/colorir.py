from re import finditer
from tkinter import END
from copy import deepcopy
from threading import Thread

class Colorir():
    def __init__(self, cor_do_comando, dic_comandos):
        self.cor_do_comando = cor_do_comando
        self.dic_comandos = dic_comandos
        self.primeira_vez = False
        self.tx_codfc = None
        self.tela = None
        self.aba_focada = 0

        self.palavras_analisadas = {}
        self.historico_coloracao = {}

        self.palavras_analisadas[self.aba_focada] = []
        self.historico_coloracao[self.aba_focada] = []

    def alterar_cor_comando(self, novo_cor_do_comando):
        self.cor_do_comando = novo_cor_do_comando

    def realiza_coloracao(self, palavra, linha, valor1, valor2, cor):
        """
            Realiza a coloracao de uma unica palavra
        """
        linha1 = '{}.{}'.format(linha, valor1)
        linha2 = '{}.{}'.format(linha, valor2)

        self.tx_codfc.tag_add(palavra, linha1, linha2)
        self.tx_codfc.tag_config(palavra, foreground=cor)

        self.tela.update()
        self.tx_codfc.update()


    def marcar_coloracao(self, regex, lista, linha, palavra, cor):
        #vale, lista_p, linh_p, palavra, cor 
        
        for valor in finditer(regex, lista[linha]):

            inicio_regex = valor.start()
            final_regex = valor.end()

            usado = cor + " <,> " + palavra + " <,> " + regex + " <,> " + str(linha) + " <,> " + str(inicio_regex) + " <,> " + str(final_regex)
            self.historico_coloracao[self.aba_focada].append(usado)
            Colorir.realiza_coloracao(self, str(usado), str(linha + 1), inicio_regex, final_regex, cor)


    def def_cor(self, chave_comando,   chave_cor,   lista):
        """         atribuicao_dados, 'lista',   lista_linhas  """
 
        for comando in self.dic_comandos[chave_comando]["comando"]:
            comando2 = comando[0].strip()
            "vale, recebe, é igual"
            Colorir.anl_cor(
                self,
                comando2,
                self.cor_do_comando[chave_cor],
                lista)

    def anl_cor(self, palavra, cor, lista):
        """            vale/=, '#ffffff', textoLista """
        if palavra == "||" or palavra == "":
            return 0

        """
            Realiza a coloração seguindo instruções
        """
        cor = cor['foreground'] # !==> "#ffffff"        

        palavra_comando = palavra.replace('+', '\\+')
        palavra_comando = palavra_comando.replace('/', '\\/')
        palavra_comando = palavra_comando.replace('*', '\\*')

        for linha in range(len(lista)):
            if palavra == "numerico":
                Colorir.marcar_coloracao(
                    self,
                    '(^|\\s|\\,)([0-9\\.]\\s*){1,}($|\\s|\\,)',
                    lista,
                    linha,
                    palavra,
                    cor)

            elif palavra == "comentario":
                Colorir.marcar_coloracao(self, '(#|\\/\\/).*$', lista, linha, palavra, cor)
                Colorir.marcar_coloracao(self, '(\\/\\*[^\\*\\/]*\\*\\/)', lista, linha, palavra + "longo", cor)

            elif palavra == '"':
                Colorir.marcar_coloracao(self, """\"[^"]*\"""", lista, linha, palavra, cor)
            else:
                palavra_comando = palavra_comando.replace(' ', '\\s*')
                #vale, lista_p, linh_p, palavra, cor 
                Colorir.marcar_coloracao(self, '(^|\\s){}(\\s|$)'.format(palavra_comando), lista, linha, palavra, cor)

    def coordena_coloracao(self, event, tx_codfc, primeira_vez=False):
        if primeira_vez:
            self.primeira_vez = primeira_vez
        self.tx_codfc = tx_codfc

        # não modifica o código
        if event is not None:
            print(event.keysym)

            if event.keysym in ('Down', 'Up', 'Left', 'Right'):
                return 0


        #try:
        lista = self.tx_codfc.get(1.0, END).lower().split('\n')

        # Verifica se existe
        try:
            self.historico_coloracao[self.aba_focada]
        except Exception as e:
            #print("Chave inexistente, nova chave", self.aba_focada)
            self.historico_coloracao[self.aba_focada] = []

        self.palavras_analisadas[self.aba_focada] = deepcopy( self.historico_coloracao[self.aba_focada] )
        self.historico_coloracao[self.aba_focada] = []
        for chave, comando in self.dic_comandos.items():
            Colorir.def_cor(self, chave, str(comando["cor"]), lista)

        Colorir.anl_cor(self, 'numerico', self.cor_do_comando["numerico"], lista)
        Colorir.anl_cor(self, 'comentario', self.cor_do_comando["comentario"], lista)
        Colorir.anl_cor(self, '"', self.cor_do_comando["string"], lista)

        # Primeira vez não remove ninguém
        if not self.primeira_vez:
            for palavra_nao_colorida in self.palavras_analisadas[self.aba_focada]:
                if palavra_nao_colorida not in self.historico_coloracao[self.aba_focada]:

                    # Se houve uma variação na quantidade de palavras
                    if len(self.historico_coloracao[self.aba_focada]) != len(self.palavras_analisadas[self.aba_focada]):
                        print("delete", palavra_nao_colorida)
                        self.tx_codfc.tag_delete(palavra_nao_colorida)

        self.tx_codfc.update()
        if self.tela is not None:
            self.tela.update()

        #except Exception as erro:
        #    print("Erro ao atualizar coloracao", erro)

        self.primeira_vez = primeira_vez

        #print(" ")
        #print("hst ",self.historico_coloracao)
        #print("plv ",self.palavras_analisadas)
        return 0



