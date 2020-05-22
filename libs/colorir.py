from re import finditer
from tkinter import END
from copy import deepcopy

class Colorir():
    def __init__(self, cor_do_comando, dic_comandos):
        self.cor_do_comando = cor_do_comando
        self.dic_comandos = dic_comandos
        self.primeira_vez = False
        self.tx_codfc = None
        self.tela = None
        self.palavras_analisadas = []
        self.historico_coloracao = []

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

    def marcar_coloracao(self, regex, lista, linha, palavra, cor):
        #vale, lista_p, linh_p, palavra, cor 
        
        for valor in finditer(regex, lista[linha]):
            usado = palavra
            usado = usado + str(linha) + str(valor.start()) + str(valor.end())
            self.historico_coloracao.append(usado)

            if usado not in self.palavras_analisadas or self.primeira_vez:
                Colorir.realiza_coloracao(self, str(usado), str(linha + 1), valor.start(), valor.end(), cor)

    def def_cor(self, chave_comando,   chave_cor,   lista):
        """         atribuicao_dados, 'lista',   lista_linhas  """
 
        for comando in self.dic_comandos[chave_comando]["comando"]:
            "vale, recebe, é igual"
            Colorir.anl_cor(
                self,
                comando[0].strip(),
                self.cor_do_comando[chave_cor],
                lista)
            


    def anl_cor(self, palavra, cor, lista):
        """            vale/=, '#ffffff', textoLista """
        if palavra == "||":
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

            if event.keysym in ('Down', 'Up', 'Left', 'Right'):
                return 0

        try:
            lista = self.tx_codfc.get(1.0, END).lower().split('\n')

            self.palavras_analisadas = deepcopy( self.historico_coloracao )
            self.historico_coloracao = []
            for chave, comando in self.dic_comandos.items():
                Colorir.def_cor(self, chave, str(comando["cor"]), lista)

            Colorir.anl_cor(self, 'numerico', self.cor_do_comando["numerico"], lista)
            Colorir.anl_cor(self, 'comentario', self.cor_do_comando["comentario"], lista)
            Colorir.anl_cor(self, '"', self.cor_do_comando["string"], lista)

            # Primeira vez não remove ninguém
            if not self.primeira_vez:
                for palavra_nao_colorida in self.palavras_analisadas:
                    if palavra_nao_colorida not in self.historico_coloracao:
                        self.tx_codfc.tag_delete(palavra_nao_colorida)

            self.tx_codfc.update()
            if self.tela is not None:
                self.tela.update()

        except Exception as erro:
            print("Erro ao atualizar coloracao", erro)

        self.primeira_vez = primeira_vez
        return 0


