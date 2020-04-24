from re import finditer
from tkinter import END


class Colorir():
    def __init__(self, cor_do_comando, dic_comandos):
        self.cor_do_comando = cor_do_comando
        self.dic_comandos = dic_comandos
        self.tx_codfc = None

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
        for valor in finditer(regex, lista[linha]):
            Colorir.realiza_coloracao(self, str(palavra), str(linha + 1), valor.start(), valor.end(), cor)

    def def_cor(self, chave_comando, chave_cor, lista):
        for comando in self.dic_comandos[chave_comando]:
            Colorir.anl_cor(
                self,
                comando[0].strip(),
                self.cor_do_comando[chave_cor],
                lista)

    def anl_cor(self, palavra, cor, lista):
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
                Colorir.marcar_coloracao(self, '(^|\\s){}(\\s|$)'.format(palavra_comando), lista, linha, palavra, cor)

    def coordena_coloracao(self, event, tx_codfc):
        self.tx_codfc = tx_codfc


        # não modifica o código
        if event is not None:
            print( event.keysym )
            if event.keysym in ('Down', 'Up', 'Left', 'Right'):
                return 0

        try:
            lista = self.tx_codfc.get(1.0, END).lower().split('\n')
            Colorir.def_cor(self, 'para_cada', "condicionais", lista)
            Colorir.def_cor(self, 'para_cada_de', "condicionais", lista)
            Colorir.def_cor(self, 'para_cada_ate', "condicionais", lista)
            Colorir.def_cor(self, 'repita', "lista", lista)
            Colorir.def_cor(self, 'se', "condicionais", lista)

            Colorir.def_cor(self, 'addItensListaInternoPosicaoFinaliza', "lista", lista)
            Colorir.def_cor(self, 'addItensListaInternoFinal', "lista", lista)
            Colorir.def_cor(self, 'addItensListaInternoPosicao', "lista", lista)
            Colorir.def_cor(self, 'addItensListaInternoInicio', "lista", lista)
            Colorir.def_cor(self, 'declaraListasObterPosicao', "lista", lista)
            Colorir.def_cor(self, 'RemoverItensListasInterno', "lista", lista)
            Colorir.def_cor(self, 'declaraVariaveis', "atribuicao", lista)
            Colorir.def_cor(self, 'passandoParametros', "tempo", lista)
            Colorir.def_cor(self, 'RemoverItensListas', "lista", lista)
            Colorir.def_cor(self, 'incrementeDecremente', "tempo", lista)
            Colorir.def_cor(self, 'recebeDeclaraListas', "lista", lista)
            Colorir.def_cor(self, 'tiverInternoLista', "lista", lista)
            Colorir.def_cor(self, 'aleatorioEntre', "lista", lista)
            Colorir.def_cor(self, 'listaPosicoesCom', "lista", lista)
            Colorir.def_cor(self, 'listaNaPosicao', "lista", lista)
            Colorir.def_cor(self, 'listaCom', "lista", lista)
            Colorir.def_cor(self, 'declaraListas', "lista", lista)
            Colorir.def_cor(self, 'adicionarItensListas', "lista", lista)
            Colorir.def_cor(self, 'tamanhoDaLista', "lista", lista)
            Colorir.def_cor(self, 'digitado', "tempo", lista)
            Colorir.def_cor(self, 'enquanto', "lista", lista)
            Colorir.def_cor(self, 'mostreNessa', "exibicao", lista)
            Colorir.def_cor(self, 'funcoes', "tempo", lista)
            Colorir.def_cor(self, 'aguarde', "tempo", lista)
            Colorir.def_cor(self, 'aleatorio', "tempo", lista)
            Colorir.def_cor(self, 'limpatela', "tempo", lista)
            Colorir.def_cor(self, 'incremente', "tempo", lista)
            Colorir.def_cor(self, 'decremente', "logico", lista)
            Colorir.def_cor(self, 'tiverLista', "lista", lista)
            Colorir.def_cor(self, 'recebeParametros', "tempo", lista)
            Colorir.def_cor(self, 'esperaEm', "tempo", lista)
            Colorir.def_cor(self, 'repitaVezes', "lista", lista)
            Colorir.def_cor(self, 'logico', "logico", lista)
            Colorir.def_cor(self, 'mostre', "exibicao", lista)
            Colorir.def_cor(self, 'ler_tecla_por', "lista", lista)

            Colorir.def_cor(self, 'matematica', "contas", lista)
            Colorir.anl_cor(self, 'numerico', self.cor_do_comando["numerico"], lista)
            Colorir.anl_cor(self, 'comentario', self.cor_do_comando["comentario"], lista)
            Colorir.anl_cor(self, '"', self.cor_do_comando["string"], lista)

            self.tx_codfc.update()

        except Exception as erro:
            print("Erro ao atualizar coloracao", erro)

        return tx_codfc
