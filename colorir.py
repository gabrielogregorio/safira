from re import finditer
from tkinter import END

class Colorir():
    def __init__(self, cor_do_comando, dic_comandos):
        self.cor_do_comando = cor_do_comando
        self.dic_comandos = dic_comandos
        self.tx_codfc = None

    def realiza_coloracao(self, palavra, linha, valor1, valor2, cor):
        """
            Realiza a coloracao de uma unica palavra
        """
        linha1 = '{}.{}'.format(linha , valor1)
        linha2 = '{}.{}'.format(linha , valor2)

        self.tx_codfc.tag_add(palavra, linha1 , linha2)
        self.tx_codfc.tag_config(palavra, foreground = cor)


    def marcar_coloracao(self, regex, lista, linha, palavra, cor):
        for valor in finditer(regex, lista[linha]):
            Colorir.realiza_coloracao(self, str(palavra), str(linha + 1), valor.start(), valor.end(), cor)

    def define_coloracao(self, chave_comando, chave_cor, lista):
        for comando in self.dic_comandos[ chave_comando ]:
            Colorir.analisa_coloracao(self, comando[0].strip(), self.cor_do_comando[ chave_cor ], lista)

    def analisa_coloracao(self, palavra, cor, lista):
        """
            Realiza a coloração seguindo instruções
        """

        cor = cor['foreground']
        self.tx_codfc.tag_delete(palavra)

        palavra_comando = palavra.replace('+', '\\+')
        palavra_comando = palavra_comando.replace('/', '\\/')
        palavra_comando = palavra_comando.replace('*', '\\*')

        for linha in range(len(lista)):

            if palavra == "numerico":
                Colorir.marcar_coloracao(self, '(^|\\s|\\,)([0-9\\.]\\s*){1,}($|\\s|\\,)', lista, linha, palavra, cor)

            elif palavra == "comentario":
                Colorir.marcar_coloracao(self, '(#|\\/\\/).*$', lista, linha, palavra, cor)
                Colorir.marcar_coloracao(self, '(\\/\\*[^\\*\\/]*\\*\\/)', lista, linha, palavra + "longo", cor)

            elif palavra == '"':
                Colorir.marcar_coloracao(self, """\"[^"]*\"""", lista, linha, palavra, cor)

            else:
                palavra_comando = palavra_comando.replace(' ','\\s*')
                Colorir.marcar_coloracao(self, '(^|\\s){}(\\s|$)'.format(palavra_comando), lista, linha, palavra, cor)

    def coordena_coloracao(self, event, tx_codfc):
        self.tx_codfc = tx_codfc

        if event != None: # não modifica o código
            if event.keysym in ('Down','Up','Left','Right'):
                return 0

        try:
            lista = self.tx_codfc.get(1.0, END).lower().split('\n')

            Colorir.define_coloracao(self, 'addItensListaInternoPosicaoFinaliza', "lista", lista)
            Colorir.define_coloracao(self, 'addItensListaInternoFinal', "lista", lista)
            Colorir.define_coloracao(self, 'addItensListaInternoPosicao', "lista", lista)
            Colorir.define_coloracao(self, 'addItensListaInternoInicio', "lista", lista)
            Colorir.define_coloracao(self, 'declaraListasObterPosicao', "lista", lista)
            Colorir.define_coloracao(self, 'RemoverItensListasInterno', "lista", lista)
            Colorir.define_coloracao(self, 'declaraVariaveis', "atribuicao", lista)
            Colorir.define_coloracao(self, 'passandoParametros', "tempo", lista)
            Colorir.define_coloracao(self, 'RemoverItensListas', "lista", lista)
            Colorir.define_coloracao(self, 'incrementeDecremente', "tempo", lista)
            Colorir.define_coloracao(self, 'recebeDeclaraListas', "lista", lista)
            Colorir.define_coloracao(self, 'tiverInternoLista', "lista", lista)
            Colorir.define_coloracao(self, 'aleatorioEntre', "lista", lista)
            Colorir.define_coloracao(self, 'listaPosicoesCom', "lista", lista)
            Colorir.define_coloracao(self, 'listaNaPosicao', "lista", lista)
            Colorir.define_coloracao(self, 'listaCom', "lista", lista)
            Colorir.define_coloracao(self, 'declaraListas', "lista", lista)
            Colorir.define_coloracao(self, 'adicionarItensListas', "lista", lista)
            Colorir.define_coloracao(self, 'tamanhoDaLista', "lista", lista)
            Colorir.define_coloracao(self, 'digitado', "tempo", lista)
            Colorir.define_coloracao(self, 'enquanto', "lista", lista)
            Colorir.define_coloracao(self, 'mostreNessa', "exibicao", lista)
            Colorir.define_coloracao(self, 'funcoes', "tempo", lista)
            Colorir.define_coloracao(self, 'aguarde', "tempo", lista)
            Colorir.define_coloracao(self, 'aleatorio', "tempo", lista)
            Colorir.define_coloracao(self, 'limpatela', "tempo", lista)
            Colorir.define_coloracao(self, 'incremente', "tempo", lista)
            Colorir.define_coloracao(self, 'decremente', "logico", lista)
            Colorir.define_coloracao(self, 'tiverLista', "lista", lista)
            Colorir.define_coloracao(self, 'recebeParametros', "tempo", lista)
            Colorir.define_coloracao(self, 'esperaEm', "tempo", lista)
            Colorir.define_coloracao(self, 'matematica', "contas", lista)
            Colorir.define_coloracao(self, 'repitaVezes', "lista", lista)
            Colorir.define_coloracao(self, 'logico', "logico", lista)
            Colorir.define_coloracao(self, 'repita', "lista", lista)
            Colorir.define_coloracao(self, 'mostre', "exibicao", lista)
            Colorir.define_coloracao(self, 'se', "condicionais", lista)

            Colorir.analisa_coloracao(self, 'numerico'     , self.cor_do_comando["numerico"], lista)
            Colorir.analisa_coloracao(self, 'comentario'   , self.cor_do_comando["comentario"], lista)
            Colorir.analisa_coloracao(self, '"'            , self.cor_do_comando["string"], lista)

            self.tx_codfc.update()

        except Exception as erro:
            print("Erro ao atualizar coloracao", erro)
