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

        for valor in finditer(regex, lista[linha]):

            inicio_regex = valor.start()
            final_regex = valor.end()

            usado = cor + " <,> " + palavra + " <,> " + regex + " <,> " + str(linha) + " <,> " + str(inicio_regex) + " <,> " + str(final_regex)
            #usado = cor + " <,> " + palavra + " <,> " + regex + " <,> " + str(inicio_regex) + " <,> " + str(final_regex)

            self.historico_coloracao.append(usado)
            Colorir.realiza_coloracao(self, str(usado), str(linha + 1), inicio_regex, final_regex, cor)

            if usado not in self.lista_todos_coloracao:
                self.lista_todos_coloracao.append(usado)

                print("****** COLORACAO REALIZADA")

    def anl_cor(self, palavra, cor, lista):
        """ vale/=, '#ffffff', textoLista """

        if palavra == "||" or palavra == "":
            return 0

        """ Realiza a coloração seguindo instruções """
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


    def def_cor(self, chave_comando,   chave_cor,   lista):
        """ atribuicao_dados, 'lista',   lista_linhas  """
 
        for comando in self.dic_comandos[chave_comando]["comando"]:

    
            "vale, recebe, é igual"
            Colorir.anl_cor(
                self,
                comando[0].strip(),
                self.cor_do_comando[chave_cor],
                lista)

    def coordena_coloracao(self, event, tx_codfc, primeira_vez=False):
        start = time()

        self.tx_codfc = tx_codfc

        # não modifica o código
        if event is not None:
            print("[OK] tecla pressinada => ", event.keysym)
            if event.keysym in ('Down', 'Up', 'Left', 'Right'):
                return 0

        lista_linhas = self.tx_codfc.get(1.0, END).lower().split('\n')

        self.historico_coloracao = []
        for chave, comando in self.dic_comandos.items():
            Colorir.def_cor(self, chave, str(comando["cor"]), lista_linhas)

        Colorir.anl_cor(self, 'numerico', self.cor_do_comando["numerico"], lista_linhas)
        Colorir.anl_cor(self, 'comentario', self.cor_do_comando["comentario"], lista_linhas)
        Colorir.anl_cor(self, '"', self.cor_do_comando["string"], lista_linhas)

        bool_alterado = False

        # Primeira vez não remove ninguém
        for palavra_nao_colorida in self.lista_todos_coloracao:
            if palavra_nao_colorida not in self.historico_coloracao:
                bool_alterado = True
                try:
                    self.tx_codfc.tag_delete(palavra_nao_colorida)
                    self.lista_todos_coloracao.remove(palavra_nao_colorida)
                except:
                    pass

        print("Alterado =>", bool_alterado)
        self.tx_codfc.update()
        if self.tela is not None:
            self.tela.update()
        
        print("Delay: ", time() - start)

        return 0



