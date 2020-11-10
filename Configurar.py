from interpretador.interpretador import Interpretador


class ConfigurarInterpretador:
    def __init__(self):
        pass

    def gerar_regex_compilado_interpretador(self, dicLetras, dic_comandos, idioma) -> tuple:
        """Compila todos os regex que o interpretador poderá usar
        Args:
        Returns: (regex_compilado, regex_comandos)
        """
        diretorio_base = ''
        bool_ignorar_todos_breakpoints = True
        bool_logs = False
        dic_regex_compilado = None
        re_comandos = None

        instancia = Interpretador(
            bool_logs,
            [],
            bool_ignorar_todos_breakpoints,
            diretorio_base,
            dicLetras,
            dic_comandos,
            idioma,
            dic_regex_compilado,
            re_comandos)

        dic_regex_compilado = instancia.dic_regex_compilado
        re_comandos = instancia.re_comandos

        del instancia
        del diretorio_base
        del bool_ignorar_todos_breakpoints
        del bool_logs

        return (dic_regex_compilado, re_comandos)

    def carregar_dicionario_letra(self, dic_comandos:dict) -> dict:
        """
        Carrega um dicionário com as primeiras letras de todos os comandos disponíveis
        """
        dic_letras = {}

        # Anda por todos os comandos
        for k, v in dic_comandos.items():

            # Cria uma lista pela chave de cada comando
            dic_letras[k] = []

            # Para cada subcomando
            for valor in v["comando"]:

                # Pega a primeira letra do subcomando
                valor = valor[0].strip()

                # Adiona no dicionário a primeira letra do comando
                if valor == "":
                    dic_letras[k].append(valor)
                else:
                    valor = valor.lower()

                    if valor[0] not in dic_letras[k]:
                        dic_letras[k].append(valor[0])
        return dic_letras
