from tkinter import END
from random import randint
from time import sleep
from time import time
from re import findall
from re import search
from re import finditer
from re import compile
from os import listdir
from os import system
from os import path as os_path
from os import remove as os_remove

import util.funcoes as funcoes
from interpretador.mensagens import Mensagens

# Recursividade, CLasses, alocação de memória para as estruturas de Dinâmicas 

__author__ = 'Gabriel Gregório da Silva'
__email__ = 'gabriel.gregorio.1@outlook.com'
__project__ = 'Combratec'
__github__ = 'https://github.com/Combratec/'
__description__ = 'Interpretador de comandos'
__status__ = 'Desenvolvimento'
__version__ = '0.2'


class Interpretador():
    def __init__(self, bool_logs: bool,
        lst_breakpoints: list,
        bool_ignorar_todos_breakpoints: bool,
        diretorio_base: str,
        dicLetras: dict,
        dic_comandos: dict,
        idioma: str,
        dic_regex_compilado: dict,
        re_comandos: str):
        """Cria uma instância do interpretador

        Args:
            bool_logs (bool): Ativar Logs do interpretador (Reduz drasticamente o desempenho)
            lst_breakpoints (list): Lista com todos as linhas com breakpoints
            bool_ignorar_todos_breakpoints (bool): Ignorar todos os breakpoints
            diretorio_base (str): diretório onde o script será executado
            dicLetras (dict): Dicionário com letras iniciais de cada comando
            dic_comandos (dict): Dicionário com os comandos
            idioma (str): Idioma que o interpretador deverá ser executado
        """

        self.boo_orquestrador_iniciado = False

        # Avisa que aconteceu um erro, para quebrar todos os loops
        self.aconteceu_erro = False

        # Avisa que os erros já foram alertados
        self.erro_alertado = False

        # Marca que não é para ignorar erros
        self.ignorar_erros = False

        # linha que deu o erro
        self.linha_que_deu_erro = None

        # Captura algo que será digitado pelo usuário
        self.texto_digitado = None

        self.rgx_padrao_variavel = '[a-zA-Z0-9\\_]*'
        self.num_linha = "0"

        # Idioma padrão
        self.idioma = idioma

        # retorna intruções para para uma terminal
        self.controle_interpretador = ""

        # Script para dar dica sobre o erro
        self.dir_script_aju_erro = ""

        # Erro que estorou
        self.mensagem_erro = ""

        # Variáveis
        self.dic_variaveis = {}

        # Funções
        self.dic_funcoes = {}

        # Número de vezes que o orquestrador foi chamado
        self.numero_threads_ativos = 0

        # Ignorar todos os breakpoints
        self.bool_ignorar_todos_breakpoints = bool_ignorar_todos_breakpoints

        # Lista com os pontos de breakpoints
        self.lst_breakpoints = lst_breakpoints

        # Diretório que o script está
        self.diretorio_base = diretorio_base

        # Analisar os comandos
        self.dic_comandos = dic_comandos

        # Rastrear os logs
        self.bool_logs = bool_logs

        # Letras iniciais de cada tipo de comando, para otimização
        self.dicLetras = dicLetras

        self.inicio = time()

        # Carregar as mensagens do interpretador
        self.msg_inst = Mensagens(self.idioma)
        self.msg = lambda acesso="": self.msg_inst.text(acesso)


        if re_comandos is not None:
            self.re_comandos = re_comandos
        else:
            self.re_comandos = compile("(\\<[a-zA-Z\\_]*\\>)")

        # Regex não compilado!
        # Se foi informando um dicionário com o regex preparado
        if dic_regex_compilado is not None:
            self.dic_regex_compilado = dic_regex_compilado
            self.compilado = True
        else:
            # Se o dicionário compilado não está pronto
            self.compilado = False
            self.dic_regex_compilado = {}
    
            self.interpretador(linha='[0] ............')
            self.comandos_uso_geral(possivel_variavel= '.................')
            self.tiver_valor_lista(linha='.................')
            self.compilado = True


    def analisa_inicio_codigo(self, linha:str) -> str:
        """Obtem uma linha de código e retorna o número da linha

        Args:
            linha (str): linha de código

        Returns:
            str: Retorna a linha do código
        """
        linha = linha.strip()
        posicoes = finditer(r'^(\[\d*\])', linha)

        num_linha = 0
        for uma_posicao in posicoes:
            num_linha = uma_posicao.end()
            break

        return num_linha

    def cortar_comentarios(self, codigo: str) -> str:
        """ Remover os comentários

        Args:
            codigo (str): O código completo com os comentários

        Returns:
            str: O código com todos os comentários removidos
        """
        lista = codigo.split('\n')

        string = ""
        for linha in lista:
            linha = linha.strip()
            iniciou_string = False

            temp = ""

            for char in range(len(linha)):

                if linha[char] == '"':
                    if not iniciou_string:
                        iniciou_string = True
                    else:
                        iniciou_string = False
                    temp += linha[char]
                    continue

                if not iniciou_string:
                    if linha[char] == "#" or linha[char:char+2] == "//":
                        break

                temp += linha[char]

            temp = temp.strip()

            if self.analisa_inicio_codigo(temp) != len(temp):
                string += temp + "\n"

        return string

    def aguardar_liberacao_breakPoint(self) -> None:
        """Fica em um loop aguardando o Breakpoint ser liberado

        Returns:
            None: 
        """

        if not self.bool_ignorar_todos_breakpoints:
            self.controle_interpretador = "aguardando_breakpoint"

            while self.controle_interpretador != "":
                if self.aconteceu_erro:
                    return [False, "Interrompido", "exibirNaTela"]

                sleep(0.0001)

    def orq_erro(self, msg_log:str, linhaAnalise:str, dir_script_erro:str) -> None:
        """Executa as rotinas para avisar o sistema que aconteceu um erro

        Args:
            msg_log (str): Mensagem de erro
            linhaAnalise (str): Linha que o erro foi detectado
            dir_script_erro (str): Script recomendado para a solução do problema

        Returns:
            None: None
        """

        if self.ignorar_erros:
            return "Ignorar Erro"

        self.aconteceu_erro = True

        if msg_log not in ["Erro ao iniciar o Interpretador", "indisponibilidade_terminal", "Interrompido"]:

            if not self.erro_alertado:

                self.dir_script_aju_erro = dir_script_erro
                self.mensagem_erro = msg_log
                self.linha_que_deu_erro = linhaAnalise

                self.erro_alertado = True

    def orq_exibir_tela(self, lst_retorno_ultimo_comando:list) -> list:
        """Controla a exibição de mensagens na tela

        Args:
            lst_retorno_ultimo_comando (list): Lista com instruções no formato [sucesso, mensagem, ação]

        Returns:
            list: Instruções no formato [sucesso, mensagem, ação]
        """
        regex = r"^\:(.*?)\:(.*?)\:(.*?)\:(.*)"
        valores = search(regex, str(lst_retorno_ultimo_comando[1]))

        instrucao = valores.group(1)
        cor = valores.group(3)
        linha = valores.group(4)

        if instrucao == "nessaLinha":
            self.controle_interpretador = ':nessaLinha:exibirCor:{}:{}'.format(cor ,linha)
        else:
            self.controle_interpretador = ':mostreLinha:exibirCor:{}:{}'.format(cor ,linha)

        while self.controle_interpretador != "":
            if self.aconteceu_erro:
                return [False, "Interrompido", "exibirNaTela"]
            sleep(0.0001)

    def log(self, msg_log: str) -> str:
        """ Exibe um log no terminal

        Args:
            msg_log (str): a mensagem para exibir
        """
        if self.bool_logs:
            agora = time() - self.inicio
            self.inicio = agora

            print('[{0:<15.3f}] => '.format(agora), r'{}'.format(msg_log))

    def orquestrador_interpretador_(self, txt_codigo:str) -> list:
        """Controla a execução de um código, separando blocos, comandos e executando eles

        Args:
            txt_codigo (str): Bloco completo de código

        Returns:
            list: Instruções no formato [sucesso, mensagem, tipo_mensagem, ação]
        """


        self.numero_threads_ativos += 1
        self.boo_orquestrador_iniciado = True

        len_cod = len(txt_codigo)

        bool_erro_tentar = False
        salvar_bloco = False
        bool_ultimo_teste = False
        bool_string = False

        txt_linha_comando = ""
        str_bloco_salvo = ""
        txt_char = ""

        historico_fluxo_de_dados = []
        int_profundidade_bloco = 0

        for num_txt_char, txt_char in enumerate(txt_codigo):
            txt_dois_char = txt_codigo[num_txt_char:num_txt_char+2]

            # Executar o comando de uma linha
            # Se chegar no fim da linha ou iniciar um bloco e um bloco não estiver sendo salvo e nem estiver em uma string
            if (txt_char == "\n" or txt_char == ";" or txt_char == "{" and not salvar_bloco and not bool_string):

                # Se tiver alguma coisa na linha
                if len(txt_linha_comando.strip()) > 0:

                    # Remoção de lixo
                    txt_linha_comando = txt_linha_comando.replace("\n","").strip()

                    lst_analisa =self.interpretador(txt_linha_comando)
                    if lst_analisa[0][2] == "continuarLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, "continuarLoop"]

                    if lst_analisa[0][2] == "pararLoop":
                        self.numero_threads_ativos -= 1
                        return lst_analisa[0]

                    if lst_analisa[0][2] == "retornarOrquestrador":
                        self.numero_threads_ativos -= 1
                        return [True, lst_analisa[0][1],  "retornarOrquestrador"]

                    if lst_analisa[0][2] == 'linhaVazia': # A linha estava em branco
                        txt_linha_comando = ""

                    else:
                        lst_ultimo_teste = lst_analisa
                        txt_comando_testado = txt_linha_comando
                        num_linha_analisada = lst_ultimo_teste[1]
                        arq_script_erro = lst_ultimo_teste[2]
                        lst_ultimo_teste = lst_ultimo_teste[0]

                        if lst_ultimo_teste[0] == False: # Seu erro

                            self.numero_threads_ativos -= 1
                            if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                            return lst_ultimo_teste

                        if lst_ultimo_teste[2] == 'exibirNaTela':
                            self.orq_exibir_tela(lst_ultimo_teste)

                        if lst_ultimo_teste[2] in ['fazerNada', 'exibirNaTela']: # Adiciona no fluxo de dados
                            historico_fluxo_de_dados.append('acaoDiversa')

                        txt_linha_comando = ""

                        if txt_char == "\n" and lst_ultimo_teste[2] == 'fazerNada':
                            continue

            # Quando começar uma string
            if txt_char == '"' and not bool_string and not salvar_bloco:
                bool_string = True

            elif txt_char == '"' and bool_string and not salvar_bloco:
                bool_string = False

            # Quando começar um bloco
            if txt_char == "{" and not bool_string:
                int_profundidade_bloco += 1
                salvar_bloco = True

            elif txt_char == "}" and not bool_string:
                int_profundidade_bloco -= 1

            # Quando finalizar um bloco
            if txt_char == "}" and not bool_string and int_profundidade_bloco == 0:
                ##self.log('!<Analisa bloco salvo>:"' + str_bloco_salvo + '"')

                salvar_bloco = False

                if lst_ultimo_teste[2] == 'declararLoop':
                    historico_fluxo_de_dados.append('declararLoop') # Encaixa Loop

                    # Enquanto a condição for verdadeira
                    while lst_ultimo_teste[1]:
                        if self.aconteceu_erro:
                            return [False, "Interrompido", "exibirNaTela"]


                        # Executar o bloco completo
                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[2] == "pararLoop":
                            break

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            self.numero_threads_ativos -= 1
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)

                            return lst_resultado_execucao

                        # Testar novamente a condição do loop
                        lst_ultimo_teste =self.interpretador(txt_comando_testado)

                        num_linha_analisada = lst_ultimo_teste[1]
                        arq_script_erro = lst_ultimo_teste[2]
                        lst_ultimo_teste = lst_ultimo_teste[0]

                        if lst_ultimo_teste[0] == False:

                            self.numero_threads_ativos -= 1
                            if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                            return lst_ultimo_teste

                        if lst_ultimo_teste[2] == "retornarOrquestrador":
                            return [True, lst_ultimo_teste[1], "retornarOrquestrador"]

                elif lst_ultimo_teste[2] == "declararLoopRepetir":
                    historico_fluxo_de_dados.append('declararLoopRepetir') # Encaixa Loop

                    lst_ultimo_teste[2] = 'fazerNada'

                    for valor in range(0, lst_ultimo_teste[1]):
                        if self.aconteceu_erro:
                            return [False, "Interrompido", "exibirNaTela"]

                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[2] == "pararLoop":
                            break

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    lst_ultimo_teste[1] = 0
                    lst_ultimo_teste = [True, False]

                elif lst_ultimo_teste[2] == "declararLoopParaItemString":
                    historico_fluxo_de_dados.append('declararLoopParaItemString') # Encaixa Loop

                    lst_ultimo_teste[2] = 'fazerNada'

                    variavel_string, variavel_atribuir = lst_ultimo_teste[1]

                    for valor in variavel_string[1]:
                        # Se for uma lista
                        if isinstance(valor, list):
                            valor = valor[0]

                        if self.aconteceu_erro:
                            return [False, "Interrompido", "exibirNaTela"]

                        criar_variavel = self.funcao_realizar_atribu(variavel_atribuir, '"{}"'.format(valor))

                        if criar_variavel[0] == False:
                            self.numero_threads_ativos -= 1
                            return criar_variavel

                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[2] == "pararLoop":
                            break

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    lst_ultimo_teste[1] = 0
                    lst_ultimo_teste = [True, False]

                elif lst_ultimo_teste[2] == "declararLoopParaCada":
                    historico_fluxo_de_dados.append('declararLoopParaCada') # Encaixa Loop

                    lst_ultimo_teste[2] = 'fazerNada'

                    # Valor de inicio e fim
                    passo_para_cada = lst_ultimo_teste[1][3]
                    if passo_para_cada == 1:
                        inici_para_cada = lst_ultimo_teste[1][1]
                        final_para_cada = lst_ultimo_teste[1][2] + 1

                    else:
                        inici_para_cada = lst_ultimo_teste[1][1]
                        final_para_cada = lst_ultimo_teste[1][2] - 1

                    for valor in range(inici_para_cada, final_para_cada, passo_para_cada):
                        if self.aconteceu_erro:
                            return [False, "Interrompido", "exibirNaTela"]

                        criar_variavel = self.funcao_realizar_atribu(lst_ultimo_teste[1][0], str(valor))
                        if criar_variavel[0] == False:
                            self.numero_threads_ativos -= 1
                            return criar_variavel

                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[2] == "pararLoop":
                            break

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    lst_ultimo_teste[1] = 0
                    lst_ultimo_teste = [True, False]

                elif lst_ultimo_teste[2] == "declararFuncao":
                    lst_ultimo_teste[2] = "fazerNada"

                    self.dic_funcoes[lst_ultimo_teste[3]] = {'parametros':self.dic_funcoes[lst_ultimo_teste[3]]['parametros'], 'bloco':str_bloco_salvo[1:].strip()}


                elif lst_ultimo_teste[2] == 'declararCondicional':
                    historico_fluxo_de_dados.append('declararCondicional')
                    lst_ultimo_teste[2] = "fazerNada"

                    if lst_ultimo_teste[1]:
                        bool_ultimo_teste = True

                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[2] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, "continuarLoop"]

                        if lst_resultado_execucao[2] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, "pararLoop"]

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)

                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    else:
                        bool_ultimo_teste == False

                elif lst_ultimo_teste[2] == 'declararSenaoSe':

                    if len(historico_fluxo_de_dados) == 0:
                        self.orq_erro(self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1

                        return [False, self.msg("precisa_def_p_cond_senao"), "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'declararCondicional':
                        self.orq_erro(self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1

                        return [False, self.msg("precisa_def_p_cond_senao"), "fazerNada"]

                    # Condição se ou senão anterior era falsa
                    if bool_ultimo_teste == False:

                        # Teste senão é verdadeiro
                        if lst_ultimo_teste[1]:
                            bool_ultimo_teste = True # Condição agora foi executada

                            lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())
                            if lst_resultado_execucao[2] == "continuarLoop":
                                self.numero_threads_ativos -= 1
                                return [True, True, "continuarLoop"]

                            if lst_resultado_execucao[2] == "pararLoop":
                                self.numero_threads_ativos -= 1
                                return lst_resultado_execucao

                            if lst_resultado_execucao[2] == "retornarOrquestrador":
                                self.numero_threads_ativos -= 1
                                return [True, lst_resultado_execucao[1], "retornarOrquestrador"]

                            if lst_resultado_execucao[0] == False:

                                if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                    self.numero_threads_ativos -= 1
                                    return [True, 'Orquestrador Finalizado', "fazerNada"]

                                self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                                self.numero_threads_ativos -= 1
                                return lst_resultado_execucao

                # É um senao se e o teste
                elif lst_ultimo_teste[2] == 'declararSenao':

                    if len(historico_fluxo_de_dados) == 0:
                        self.orq_erro(self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_p_cond_senao"), "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'declararCondicional':
                        self.orq_erro(self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_p_cond_senao"), "fazerNada"]

                    # Condição se ou senão anterior era falsa
                    if bool_ultimo_teste == False:
                        bool_ultimo_teste = True # Condição agora foi executada
                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[2] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, "continuarLoop"]

                        if lst_resultado_execucao[2] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                # É tente algo
                elif lst_ultimo_teste[2] == 'tenteAlgo':
                    self.ignorar_erros = True
                    historico_fluxo_de_dados.append("tenteAlgo")
                    lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())

                    if lst_resultado_execucao[2] == "continuarLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, "continuarLoop"]

                    if lst_resultado_execucao[2] == "pararLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, "pararLoop"]

                    if lst_resultado_execucao[2] == "retornarOrquestrador":
                        self.numero_threads_ativos -= 1
                        return [True, lst_resultado_execucao[1],  "retornarOrquestrador"]

                    bool_erro_tentar = False

                    if lst_resultado_execucao[0] == False:
                        bool_erro_tentar = True

                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            self.numero_threads_ativos -= 1
                            return [True, 'Orquestrador Finalizado', "fazerNada"]

                        lst_resultado_execucao = [True, "", "linhaVazia", "fazerNada"]
                    self.ignorar_erros = False

                elif lst_ultimo_teste[2] == 'seDerErro':

                    if len(historico_fluxo_de_dados) == 0:
                        self.orq_erro(self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        self.orq_erro(self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), "fazerNada"]

                    # Teste deu erro
                    if bool_erro_tentar:
                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[2] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, "continuarLoop"]

                        if lst_resultado_execucao[2] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1],  "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[2] == 'seNaoErro':

                    if len(historico_fluxo_de_dados) == 0:
                        self.orq_erro(self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        self.orq_erro(self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), "fazerNada"]

                    # Teste deu erro
                    if bool_erro_tentar == False:
                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[2] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, "continuarLoop"]

                        if lst_resultado_execucao[2] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1],  "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[2] == 'seDerErro':

                    if len(historico_fluxo_de_dados) == 0:
                        self.orq_erro(self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        self.orq_erro(self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), "fazerNada"]

                    # Teste deu erro
                    if bool_erro_tentar:

                        lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[2] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, "continuarLoop"]

                        if lst_resultado_execucao[2] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[2] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1],  "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', "fazerNada"]

                            self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[2] == 'emQualquerCaso':

                    if len(historico_fluxo_de_dados) == 0:
                        self.orq_erro(self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        self.orq_erro(self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), "fazerNada"]
                    lst_resultado_execucao = self.orquestrador_interpretador_(str_bloco_salvo[1:].strip())
                    if lst_resultado_execucao[2] == "continuarLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, "continuarLoop"]

                    if lst_resultado_execucao[2] == "pararLoop":
                        self.numero_threads_ativos -= 1
                        return lst_resultado_execucao

                    if lst_resultado_execucao[2] == "retornarOrquestrador":
                        self.numero_threads_ativos -= 1
                        return [True, lst_resultado_execucao[1],  "retornarOrquestrador"]

                    if lst_resultado_execucao[0] == False:

                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            self.numero_threads_ativos -= 1
                            return [True, 'Orquestrador Finalizado', "fazerNada"]

                        self.orq_erro(lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                        self.numero_threads_ativos -= 1
                        return lst_resultado_execucao

                str_bloco_salvo = ""
                continue

            # Se for para salvar bloco, salve o txt_char
            if salvar_bloco:
                str_bloco_salvo += txt_char

            # Armazene os comandos
            else:
                txt_linha_comando += txt_char

        # Se chegar no final do código e tiver comando para analisar
        if len(txt_linha_comando.strip()) > 0 and len_cod -1 == num_txt_char:

            txt_linha_comando = txt_linha_comando.replace("\n","").strip()
            lst_ultimo_teste =self.interpretador(txt_linha_comando)

            if lst_ultimo_teste[0][2] == "continuarLoop":
                self.numero_threads_ativos -= 1
                return [True, True, "continuarLoop"]

            if lst_ultimo_teste[0][2] == "pararLoop":
                self.numero_threads_ativos -= 1
                return [True, True, "pararLoop"]

            if lst_ultimo_teste[0][2] == "retornarOrquestrador":
                self.numero_threads_ativos -= 1
                return [True, lst_ultimo_teste[0][1], "retornarOrquestrador"]

            txt_comando_testado = txt_linha_comando
            num_linha_analisada = lst_ultimo_teste[1]
            arq_script_erro = lst_ultimo_teste[2]
            lst_ultimo_teste = lst_ultimo_teste[0]

            if lst_ultimo_teste[0] == False:

                self.numero_threads_ativos -= 1
                if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                    return [True, 'Orquestrador Finalizado', "fazerNada"]

                self.orq_erro(lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                return lst_ultimo_teste

            if lst_ultimo_teste[2] == 'exibirNaTela':
                self.orq_exibir_tela(lst_ultimo_teste)

        # Aviso de erros de profundidade
        self.numero_threads_ativos -= 1
        if int_profundidade_bloco > 0:
            return [False, self.msg("nao_abriu_chave"), "fazerNada"]

        elif int_profundidade_bloco < 0:
            return [False, self.msg("nao_fechou_chave"), "fazerNada"]

        return [True, 'Orquestrador Finalizado', "fazerNada"]

    def analisa_instrucao(self, comando, texto:str, compilado:bool) -> list:
        comando_original = comando
        re_groups = findall(self.re_comandos, comando)
        if re_groups == None:
            return [False]

        dic_options = {}

        if not compilado:
            # Anda pelos grupos <se>, <esperar>
            for grupo in re_groups:

                # Anda pelos comandos no dicionários, [se], [if]...
                for n_comando in range(0, len(self.dic_comandos[grupo[1:-1]]["comando"])):

                    # Obtem um comando. se, if
                    txt_comando_analisar = self.dic_comandos[grupo[1:-1]]["comando"][n_comando][0]

                    # Substitui o grupo pelo comando. <se>, if
                    comando_analise = comando.replace(grupo, txt_comando_analisar)

                    try:
                        dic_options[grupo] = dic_options[grupo] + "|" + str(txt_comando_analisar)
                    except Exception as err:
                        dic_options[grupo] = txt_comando_analisar

            for k, v in dic_options.items():
                v_add = v.replace(' ', '[\\s{1,}|_]')
                comando = comando.replace(k, v_add)

            # o ? evita a gulidisse do .*, ele pode remover um passando parametros e considerar só o parametros, por exemplo
            comando = comando.replace('(.*)', '(\\"[^\\"]*\\"|.*?)')

            # Marca o padrão de variável
            comando = comando.replace('__var__', '({})'.format(self.rgx_padrao_variavel))

            # SE FOR APENAS PARA COMPILAR O REGEX
            self.dic_regex_compilado[comando_original] = compile(comando)
            return [False, 0]
        else:
            comando = self.dic_regex_compilado[comando_original]

        # Aplicar no texto
        re_texto = findall(comando, texto)

        if re_texto == []:
            return [False, 0]

        if str(type(re_texto[0])) == "<class 'str'>":
            lista_itens = [re_texto[0]]
        else:
            lista_itens = list(re_texto[0])  # Remover indexação a partir do zero

        lista_itens.insert(0, "")
        return [True, [saida.strip() for saida in lista_itens]]

    def interpretador(self, linha):
        #self.log('\n\ninterpretador')

        # [[False, 'indisponibilidade_terminal', 'string', 'exibirNaTela'], "0", ""]

        if self.aconteceu_erro:
            return [[False, 'Erro ao iniciar o Interpretador', 'exibirNaTela'], "0", ""]

        linha = linha.replace('\n', '')
        linha = linha.strip()

        if linha == '':
            return [[True, None, 'linhaVazia'], "0", ""]

        else:
            self.num_linha = "0"
            posicoes = finditer(r'^(\[\d*\])', linha)

            # Obter o número da linha
            for uma_posicao in posicoes:
                self.num_linha = linha[1: uma_posicao.end() - 1]
                linha = linha[uma_posicao.end():]
                linha = linha.strip()
                break

            # Se estiver em um breakpoint, aguarde.
            if int(self.num_linha) in self.lst_breakpoints:
               self.aguardar_liberacao_breakPoint()

            if linha == '':
                return [[True, None, 'linhaVazia'], "0", ""]

            caractere = linha[0]

            ##################################################################
            #                          LIMPAR A TELA                         #
            ##################################################################

            if caractere in self.dicLetras["limpatela"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<limpatela>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_limpar_o_termin(), self.num_linha, ""]

            ##################################################################
            #                             RETORNE                            #
            ##################################################################

            if caractere in self.dicLetras["retorne"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<retorne>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_retorne(__resultado[1][2]), self.num_linha, ""]

            ##################################################################
            #                            EXIBIÇÃO                            #
            ##################################################################

            if caractere in self.dicLetras["mostreNessa"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<mostreNessa>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_exibir_mesma_ln(__resultado[1][2]), self.num_linha, "Exibir"]

            if caractere in self.dicLetras["mostre"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<mostre>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_exibir_outra_ln(__resultado[1][2]), self.num_linha, "Exibir"]

            ##################################################################
            #                              LOOPS                             #
            ##################################################################

            if caractere in self.dicLetras["continue"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<continue>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_continuar(), self.num_linha, "continue"]

            if caractere in self.dicLetras["pare"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<pare>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_parar(), self.num_linha, "pare"]

            if caractere in self.dicLetras["interrompa"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<interrompa>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_interrompa(), self.num_linha, "interrompa"]

            if caractere in self.dicLetras["enquanto"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<enquanto>)(.*)(<enquanto_final>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_loops_enquantox(__resultado[1][2]), self.num_linha, "Enquanto"]

            if caractere in self.dicLetras["repita"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<repita>)(.*)(<repitaVezes>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_repetir_n_vezes(__resultado[1][2]), self.num_linha, "Repita"]

            if caractere in self.dicLetras["para_cada"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<para_cada>)__var__(<para_cada_de>)(.*)(<para_cada_ate>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_loop_para_cada_(__resultado[1][2], __resultado[1][4], __resultado[1][6]), self.num_linha, "para_cada_item_da_lista"]


            ##################################################################
            #                             ESPERA                             #
            ##################################################################

            if caractere in self.dicLetras["aguarde"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<aguarde>)(.*)(<esperaEm>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_esperar_n_tempo(__resultado[1][2], __resultado[1][3]), self.num_linha, "Espere"]

            ##################################################################
            #                             ENTRADA                            #
            ##################################################################

            if caractere in self.dicLetras["digitado"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<digitado>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_ovalor_digitado(__resultado[1][1]), self.num_linha, "Digitado"]

            ##################################################################
            #                         NUMERO ALEATÓRIO                       #
            ##################################################################

            if caractere in self.dicLetras["aleatorio"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_numer_aleatorio(__resultado[1][2], __resultado[1][4]), self.num_linha, "aleatorio"]

            ##################################################################
            #                           BIBLIOTECAS                          #
            ##################################################################

            if caractere in self.dicLetras["importe"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<importe>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_importe(__resultado[1][2]), self.num_linha, "bibliotecas"]

            ##################################################################
            #                    TENTE EXECUTAR O COMANDO                    #
            ##################################################################

            if caractere in self.dicLetras["se_der_erro"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<se_der_erro>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_se_der_erro(), self.num_linha, "Tente"]

            if caractere in self.dicLetras["senao_der_erro"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<senao_der_erro>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_senao_der_erro(), self.num_linha, "Tente"]

            if caractere in self.dicLetras["em_qualquer_caso"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<em_qualquer_caso>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_em_qualquer_caso(), self.num_linha, "Tente"]

            if caractere in self.dicLetras["tente"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<tente>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_tente(), self.num_linha, "Tente"]

            ##################################################################
            #                     MANIPULAÇÃO DE ARQUIVOS                    #
            ##################################################################

            if caractere in self.dicLetras["crie_arquivo"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<crie_arquivo>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_criar_arquivo(__resultado[1][2]), self.num_linha, "Arquivos"]

            if caractere in self.dicLetras["delete_arquivo"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<delete_arquivo>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_excluir_arquivo(__resultado[1][2]), self.num_linha, "Arquivos"]

            if caractere in self.dicLetras["arquivo_existe"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<arquivo_existe_completo>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_arquivo_existe(__resultado[1][2]), self.num_linha, "Arquivos"]

                __resultado = self.analisa_instrucao('^(<arquivo_existe>)(.*)(<arquivo_existe_nao_sub_existe>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_arquivo_nao_existe(__resultado[1][2]), self.num_linha, "Arquivos"]

                __resultado = self.analisa_instrucao('^(<arquivo_existe>)(.*)(<arquivo_existe_sub_existe>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_arquivo_existe(__resultado[1][2]), self.num_linha, "Arquivos"]




            if caractere in self.dicLetras["adicione_texto_arquivo"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<adicione_texto_arquivo>)(.*)(<adicione_texto_arquivo_sub>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_adicionar_arquivo(__resultado[1][2], __resultado[1][4]), self.num_linha, "Arquivos"]

            if caractere in self.dicLetras["sobrescreva_texto_arquivo"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<sobrescreva_texto_arquivo>)(.*)(<sobrescreva_texto_arquivo_sub>)(.*)(<sobrescreva_texto_arquivo_sub_sub>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_sobrescrever_arquivo(__resultado[1][2], __resultado[1][4]), self.num_linha, "Arquivos"]

            if caractere in self.dicLetras["leia_arquivo"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<leia_arquivo>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_ler_arquivo(__resultado[1][2]), self.num_linha, "Arquivos"]

            ##################################################################
            #                            CONDIÇÔES                           #
            ##################################################################

            if caractere in self.dicLetras["se_nao_se"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<se_nao_se>)(.*)(<se_final>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_senao_se(__resultado[1][2]), self.num_linha, "Condicoes"]

            if caractere in self.dicLetras["se_nao"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<se_nao>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_senao(), self.num_linha, "Condicoes"]

            if caractere in self.dicLetras["se"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<se>)(.*)(<se_final>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_testar_condicao(__resultado[1][2]), self.num_linha, "Condicoes"]

            ##################################################################
            #                            VARIAVEIS                           #
            ##################################################################

            __resultado = self.analisa_instrucao('^([a-zA-Z_0-9]*)(<declara_variaveis>)(.*)$', linha, self.compilado)
            if __resultado[0]: return [self.funcao_realizar_atribu(__resultado[1][1], __resultado[1][3]), self.num_linha, "Variaveis"]

            if caractere in self.dicLetras["incremente"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<incremente>)(.*)(<incremente_decremente>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_incremente_vari(__resultado[1][2], __resultado[1][4]), self.num_linha, "Incremente-decremente"]

            if caractere in self.dicLetras["decremente"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<decremente>)(.*)(<incremente_decremente>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_decremente_vari(__resultado[1][2], __resultado[1][4]), self.num_linha, "Incremente-decremente"]

            if caractere in self.dicLetras["tipo_variavel"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<tipo_variavel>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_tipo_variavel(__resultado[1][2]), self.num_linha, ""]

            if caractere in self.dicLetras["substitua"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<substitua>)(.*)(<substitua_por>)(.*)(<substitua_na_variavel>)(\\s*[A-Z0-9a-z\\_]*\\s*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_substituir_texto(__resultado[1][2],__resultado[1][4],__resultado[1][6] ), self.num_linha, ""]

            ##################################################################
            #                              LISTA                             #
            ##################################################################

            if caractere in self.dicLetras["tiver_lista"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<tiver_lista>)(.*)(<tiver_interno_lista>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_tiver_valor_lst(__resultado[1][2], __resultado[1][4]), self.num_linha, ""]

            if caractere in self.dicLetras["tamanho_da_lista"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<tamanho_da_lista>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_otamanho_da_lst(__resultado[1][2]), self.num_linha, "Listas"]

            if caractere in self.dicLetras["remover_itens_listas"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<remover_itens_listas>)(.*)(<remover_itens_listas_interno>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_rem_itns_na_lst(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]

            if caractere in self.dicLetras["adicionarItensListas"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<adicionarItensListas>)(.*)(<listaNaPosicao>)(.*)(<addItensListaInternoPosicaoFinaliza>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_add_itns_lst_ps(__resultado[1][2], __resultado[1][4], __resultado[1][6]), self.num_linha, "Listas"]

                __resultado = self.analisa_instrucao('^(<adicionarItensListas>)(.*)(<addItensListaInternoFinal>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_add_itns_na_lst(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]

                __resultado = self.analisa_instrucao('^(<adicionarItensListas>)(.*)(<addItensListaInternoInicio>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_add_itns_lst_in(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]

                __resultado = self.analisa_instrucao('^(<adicionarItensListas>)(.*)(<addItensListaInterno>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_add_itns_na_lst(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]


            if caractere in self.dicLetras["declaraListas"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<declaraListas>)(.*)(<listaNaPosicao>)(.*)(<recebeDeclaraListas>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_add_lst_na_posi(__resultado[1][2], __resultado[1][4], __resultado[1][6]), self.num_linha, "Listas"]

                __resultado = self.analisa_instrucao('^(<declaraListas>)(.*)(<listaCom>)(.*)(<listaPosicoesCom>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_dec_lst_posicoe(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]

                __resultado = self.analisa_instrucao('^(<declaraListas>)(.*)(<recebeDeclaraListas>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_declarar_listas(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]

                __resultado = self.analisa_instrucao('^(<declaraListas>)(\\s*[a-zA-Z\\_0-9]*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_retornar_lista(__resultado[1][2], ), self.num_linha, "Listas"]


            if caractere in self.dicLetras["declaraListasObterPosicao"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)(<declara_variaveis>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_realiza_atribuica_posicao_lista(__resultado[1][2], __resultado[1][4], __resultado[1][6]), self.num_linha, "Listas"]

                __resultado = self.analisa_instrucao('^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_obter_valor_lst(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]

            __resultado = self.analisa_instrucao('^(<percorra_items>)(.*)(<percorra_items_lista_sub>)(.*)$', linha, self.compilado)
            if __resultado[0]: return [self.funcao_percorra_string(__resultado[1][2], __resultado[1][4]), self.num_linha, "Listas"]

            ##################################################################
            #                             FUNÇÕES                            #
            ##################################################################

            if caractere in self.dicLetras["funcoes"] or not self.compilado:
                __resultado = self.analisa_instrucao('^(<funcoes>)(.*)(<recebeParametros_parentese_abre>)(.*)(<recebeParametros_parentese_fecha>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_declarar_funcao(__resultado[1][2], __resultado[1][4]),self.num_linha, "Funcoes"]

                __resultado = self.analisa_instrucao('^(<funcoes>)(.*)(<recebeParametros>)(.*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_declarar_funcao(__resultado[1][2], __resultado[1][4]),self.num_linha, "Funcoes"]

                __resultado = self.analisa_instrucao('^(<funcoes>)(\\s*[\\w*\\_]*\\s*)(<recebeParametros_parentese_abre>)\\s*(<recebeParametros_parentese_fecha>)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_declarar_funcao(__resultado[1][2]), self.num_linha, "Funcoes"]

                __resultado = self.analisa_instrucao('^(<funcoes>)(\\s*[\\w*\\_]*\\s*)$', linha, self.compilado)
                if __resultado[0]: return [self.funcao_declarar_funcao(__resultado[1][2]), self.num_linha, "Funcoes"]

            __resultado = self.analisa_instrucao('^(.*)(<passandoParametros>)(.*)$', linha, self.compilado)
            if __resultado[0]: return [self.funcao_executar_funcao(__resultado[1][1], __resultado[1][3]), self.num_linha, "Funcoes"]

            __resultado = self.analisa_instrucao('^(.*)(<passando_parametros_abrir>)(.*)(<passando_parametros_fechar>)$', linha, self.compilado)
            if __resultado[0]:
                return [self.funcao_executar_funcao(__resultado[1][1], __resultado[1][3]), self.num_linha, "Funcoes"]

            #__resultado = self.analisa_instrucao('^[A-Z0-9a-z_]*\\s*$', linha, self.compilado)
            #if __resultado[0]: return [self.funcao_executar_funcao(__resultado[1][1]), self.num_linha, "Funcoes"]

            return [ [False, "{}'{}'".format(  self.msg('comando_desconhecido'), linha  ), 'fazerNada'], self.num_linha, ""]

        return [[True, None, 'fazerNada'], str(self.num_linha), ""]

    def comandos_uso_geral(self, possivel_variavel):
        #self.log("comandos_uso_geral: '{}'".format(possivel_variavel))
        possivel_variavel = str(possivel_variavel).strip()

        caractere = None
        if possivel_variavel != "":
            caractere = possivel_variavel[0]

        ##################################################################
        #                         NUMERO ALEATÓRIO                       #
        ##################################################################

        if caractere in self.dicLetras["aleatorio"] or not self.compilado:
            __resultado = self.analisa_instrucao('^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_numer_aleatorio(__resultado[1][2], __resultado[1][4])

        ##################################################################
        #                              LISTA                             #
        ##################################################################

        if caractere in self.dicLetras["declaraListas"] or not self.compilado:
             __resultado = self.analisa_instrucao('^(<declaraListas>)(\\s*[a-zA-Z\\_0-9]*)$', possivel_variavel, self.compilado)
             if __resultado[0]: return self.funcao_retornar_lista(__resultado[1][2])

        __resultado = self.analisa_instrucao('^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_obter_valor_lst(__resultado[1][2], __resultado[1][4])

        if caractere in self.dicLetras["tiver_lista"] or not self.compilado:
            __resultado = self.analisa_instrucao('^(<tiver_lista>)(.*)(<tiver_interno_lista>)(.*)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_tiver_valor_lst(__resultado[1][2], __resultado[1][4])

        if caractere in self.dicLetras["tamanho_da_lista"] or not self.compilado:
            __resultado = self.analisa_instrucao('^(<tamanho_da_lista>)(.*)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_otamanho_da_lst(__resultado[1][2])


        ##################################################################
        #                             ENTRADA                            #
        ##################################################################

        if caractere in self.dicLetras["digitado"] or not self.compilado:
            __resultado = self.analisa_instrucao('^(<digitado>)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_ovalor_digitado(__resultado[1][1])

        ##################################################################
        #                     MANIPULAÇÃO DE ARQUIVOS                    #
        ##################################################################
 
        if caractere in self.dicLetras["arquivo_existe"] or not self.compilado:
            __resultado = self.analisa_instrucao('^(<arquivo_existe_completo>)(.*)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_arquivo_existe(__resultado[1][2])

            __resultado = self.analisa_instrucao('^(<arquivo_existe>)(.*)(<arquivo_existe_nao_sub_existe>)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_arquivo_nao_existe(__resultado[1][2])

            __resultado = self.analisa_instrucao('^(<arquivo_existe>)(.*)(<arquivo_existe_sub_existe>)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_arquivo_existe(__resultado[1][2])

        if caractere in self.dicLetras["leia_arquivo"] or not self.compilado:
            __resultado = self.analisa_instrucao('^(<leia_arquivo>)(.*)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_ler_arquivo(__resultado[1][2])

        ##################################################################
        #                            VARIAVEIS                           #
        ##################################################################

        __resultado = self.analisa_instrucao('^(\\s*[\\w*\\_]*)(<percorrer_lst_str_a_cada>)(.*)(<percorrer_lst_str_a_cada_subum>)(.*)(<percorrer_lst_str_a_cada_subdois>)(.*)(<percorrer_lst_str_a_cada_final>)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_fatiamento(__resultado[1][1], __resultado[1][3], __resultado[1][5], __resultado[1][7])

        __resultado = self.analisa_instrucao('^(\\s*[\\w*\\_]*)(<percorrer_lst_str_ate>)(.*)(<percorrer_lst_str_ate_sub>)(.*)(<percorrer_lst_str_ate_final>)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_fatiamento(__resultado[1][1], __resultado[1][3], __resultado[1][5])

        if caractere in self.dicLetras["tipo_variavel"] or not self.compilado:
            __resultado = self.analisa_instrucao('^(<tipo_variavel>)(.*)$', possivel_variavel, self.compilado)
            if __resultado[0]: return self.funcao_tipo_variavel(__resultado[1][2])

        __resultado = self.analisa_instrucao('^(.*)(<to_upper>)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_para_maiusculo(__resultado[1][1])

        __resultado = self.analisa_instrucao('^(.*)(<to_lower>)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_para_minusculo(__resultado[1][1])

        __resultado = self.analisa_instrucao('^(.*)(<to_captalize>)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_para_captalize(__resultado[1][1])



        ##################################################################
        #                            DIVERSOS                            #
        ##################################################################

        __resultado = self.analisa_instrucao('^(.*)(<na_cor>)(.*)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_na_cor(__resultado[1][1], __resultado[1][3])

        # DEBAIXO DO NA COR
        __resultado = self.analisa_instrucao('^(".*?"|.*)(<formatar_textos>)(.*)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_formatar_texto(__resultado[1][1], __resultado[1][3])

        ##################################################################
        #                            FUNÇÔES                             #
        ##################################################################

        __resultado = self.analisa_instrucao('^(.*)(<passandoParametros>)(.*)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_executar_funcao(__resultado[1][1], __resultado[1][3])


        __resultado = self.analisa_instrucao('^(.*)(<passando_parametros_abrir>)(.*)(<passando_parametros_fechar>)$', possivel_variavel, self.compilado)
        if __resultado[0]: return self.funcao_executar_funcao(__resultado[1][1], __resultado[1][3])


        #__resultado = self.analisa_instrucao('^[A-Z0-9a-z_]*\\s*$', possivel_variavel, self.compilado)
        #if __resultado[0]: return self.funcao_executar_funcao(__resultado[1][1])


        return [True, None]


    def verificar_se_existe(self, arquivo_diretorio, ja_foi_abstraido = False):
        #self.log("verificar_se_existe")

        if not ja_foi_abstraido:
            teste_arquivo = self.abstrair_valor_linha(arquivo_diretorio)
            if not teste_arquivo[0]:
                return teste_arquivo
        else:
            teste_arquivo = [True, arquivo_diretorio]

        if os_path.exists(teste_arquivo[1]):
            return [True, True, "fazerNada"]
        return [True, False, "fazerNada"]

    def testar_existencia(self, arquivo):
        #self.log("testar_existencia")

        # Abstrair o valor do arquivo e do objetivo
        teste_arquivo = self.abstrair_valor_linha(arquivo)
        if not teste_arquivo[0]: return teste_arquivo

        # Verificar se o diretório e o objetivo existem
        teste_erro =  self.verificar_se_existe(teste_arquivo[1], ja_foi_abstraido = True)
        if not teste_erro[0]:
            return teste_erro #[False, self.msg("arquivo_nao_existe").format(teste_arquivo[1]), 'string', 'fazerNada']

        return teste_arquivo


    def operacoes_variaveis(self, entrada, pipeline):
        """
            pipeline = [
                ["obter_valor_variavel", "", "", ""],
                ["teste_tipo", "!=", "lista", ""],
                ["teste_tipo", "!=", "string", ""],
                ["abstrair_valor_linha", "", "", ""]
            ]
        """
        saida = entrada
        for passo in pipeline:
            operacao, teste, esperado, msg = passo

            if operacao == "obter_valor_variavel":
                testa_entrada = self.obter_valor_variavel(saida)
                if not testa_entrada[0]: return testa_entrada
                saida = testa_entrada
            
            elif operacao == "teste_tipo":
                if teste == "==":
                    if saida[2] == esperado: return [False, self.msg("__LISTA__NAO_DEFINIDA__"), 'fazerNada']

                elif teste == "!=":
                    if saida[2] == esperado: return [False, self.msg("__LISTA__NAO_DEFINIDA__"), 'fazerNada']
                saida = saida

            elif operacao == "abstrair_valor_linha":
                teste_abstracao = self.abstrair_valor_linha(saida)
                if not teste_abstracao[0]: return teste_abstracao
                saida = teste_abstracao

            return saida


    def funcao_percorra_string(self, variavel, variavel_atribuir):
        #self.log("__funcao_percorra_string")

        testa_valor = self.operacoes_variaveis(variavel,
            pipeline = [
                ["abstrair_valor_linha", "", "", ""],
                ["teste_tipo", "!=", "string", ""]
            ]
        )
        if not testa_valor[0]: return testa_valor
        # variável => teste_variavel[1]
        testa_existencia = self.operacoes_variaveis(variavel_atribuir,
            pipeline = [
                ["obter_valor_variavel", "", "", ""]
            ]
        )
        # Variável não existe
        if not testa_existencia[0]:
            criar_variavel = self.funcao_realizar_atribu(variavel_atribuir, "0")

            if not criar_variavel[0]:
                return criar_variavel


        return [True, [testa_valor, variavel_atribuir], "declararLoopParaItemString"]

    def funcao_substituir_texto(self, encontrar:str, substituir:str, variavel:str) -> list:
        #self.log("__funcao_substituir_texto")

        teste_variavel = self.operacoes_variaveis(variavel,
            pipeline = [
                ["obter_valor_variavel", "", "", ""],
                ["teste_tipo", "!=", "string", "p_usar_substituicao_variavel"]
            ]
        )
        if not teste_variavel[0]: return teste_variavel
 
        abs_encontrar = self.operacoes_variaveis(encontrar,
            pipeline = [
                ["abstrair_valor_linha", "", "", ""],
                ["teste_tipo", "!=", "string", self.msg("p_substituir_texto_valor").format(1, 1, "__abs_encontrar[2])__")]
            ]
        )
        if not abs_encontrar[0]: return abs_encontrar

        abs_substituir = self.operacoes_variaveis(encontrar,
            pipeline = [
                ["abstrair_valor_linha", "", "", ""],
                ["teste_tipo", "!=", "string", self.msg("p_substituir_texto_valor").format(1, 1, "__abs_substituir[2])__")]
            ]
        )
        if not abs_substituir[0]: return abs_substituir

        self.dic_variaveis[variavel] = self.dic_variaveis[variavel].replace(abs_encontrar[1], abs_substituir[1])

        return [True, True, 'fazerNada']


    def funcao_limpar_o_termin(self):
        #self.log("__funcao_limpar_o_termin")

        self.controle_interpretador = "limpar_tela"

        while self.controle_interpretador != "":

            if self.aconteceu_erro:
                return [False, "Interrompido", "exibirNaTela"]
            sleep(0.000001)

        return [True, None, 'fazerNada']

    def funcao_interrompa(self):
        #self.log("__funcao_interrompa")

        #self.log('<funcao_interrompa>:')
        self.aconteceu_erro = True
        return [False, 'indisponibilidade_terminal', "fazerNada"]


    def funcao_fatiamento(self, variavel, de, ate, cada=None):
        variavel = variavel.strip()
        #self.log("__funcao_fatiamento")

        abstrair_variavel = self.obter_valor_variavel(variavel)
        if not abstrair_variavel[0]: return abstrair_variavel
        if self.verificar_tipo(abstrair_variavel[1]) not in ("string", "lista"):
            return [False, self.msg("p_usar_substituicao_variavel"), 'fazerNada']

        # Obter o valor do de
        abstrair_de = self.abstrair_valor_linha(de)
        if not abstrair_de[0]: return abstrair_de

        if self.verificar_tipo(abstrair_de[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', abstrair_de[1])
    

        # Obter o valor do ate
        abstrair_ate = self.abstrair_valor_linha(ate)
        if not abstrair_ate[0]: return abstrair_ate

        if self.verificar_tipo(abstrair_ate[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', abstrair_ate[1])

        if cada is not None:
            # Obter o valor do cada
            abstrair_cada = self.abstrair_valor_linha(cada)
            if not abstrair_cada[0]: return abstrair_cada

            if self.verificar_tipo(abstrair_cada[1]) != 'float':
                return self.msg_variavel_numerica('naoNumerico', abstrair_cada[1])


        de = int(abstrair_de[1])
        ate = int(abstrair_ate[1])
        if cada is not None:
            cada = int(abstrair_cada[1])
    
        if self.verificar_tipo(abstrair_variavel[1]) == "string":
            texto = abstrair_variavel[1]
            texto_final = ""
            tamanho_string = len(texto)

            if ate > tamanho_string:
                return [False, 'O valor inicial precisa ser menor que o tamanho total do texto. O texto tem {} você digitou {}'.format(tamanho_string, ate), 'fazerNada']

            if de > tamanho_string:
                return [False, 'O valor inicial precisa ser menor que o tamanho total do texto. O texto tem {} você digitou {}'.format(tamanho_string, de), 'fazerNada']

            if ate <= 0:
                return [False, 'O final precisa ser maior do que 0. Você digitou {}'.format(ate), 'fazerNada']
            if de <= 0:
                return [False, 'O final precisa ser maior do que 0. Você digitou {}'.format(de), 'fazerNada']

            if de == ate:
                return [True, texto[ate], 'fazerNada']

            if cada is not None:
                if cada <= 0:
                    return [False, 'O final precisa ser maior do que 0. Você digitou {}'.format(cada), 'fazerNada']
            
            if de > ate:
                maior = de + 1
                marcar = 0 if cada is None else cada
                for x in range(ate, de+1):
                    if marcar == 0:
                        marcar = 0 if cada is None else cada
                        texto_final = texto[maior-x-1] + texto_final
                    else:
                        marcar -= 1

            if de < ate:
                marcar = 0 if cada is None else cada
                for char in range(de, ate+1):
                    if marcar == 0:
                        marcar = 0 if cada is None else cada
                        texto_final += texto[char-1] 
                    else:
                        marcar -= 1
            return [True, texto_final, 'fazerNada']

        return [False, "Erro, não era um dos tipos esperados!", 'fazerNada']



    def funcao_formatar_texto(self, texto, itens):
        #self.log("__funcao_formatar_texto: texto = {}, itens= {}".format(texto, itens))

        abstrair = self.abstrair_valor_linha(texto)
        if not abstrair[0]: return abstrair

        if self.verificar_tipo(abstrair[1]) != 'string':
            return 'not string'


        lista_itens = []
        testa = self.verifica_se_tem(itens, ",")
        if testa != []:
            inicio = 0
            for i, f in testa:

                item = itens[inicio:i].strip()

                abstrair_itens = self.abstrair_valor_linha(item)
                if not abstrair_itens[0]: return abstrair_itens

                lista_itens.append(abstrair_itens)
                inicio = f

            item = itens[inicio:].strip()

            abstrair_itens = self.abstrair_valor_linha(item)
            if not abstrair_itens[0]: return abstrair_itens

            lista_itens.append(abstrair_itens)


        else:
            abstrair_itens = self.abstrair_valor_linha(itens)
            if not abstrair_itens[0]: return abstrair_itens
            lista_itens = [abstrair_itens]


        qtd_format = len(lista_itens)
        qtd_replace = abstrair[1].count('%')






        if qtd_format != qtd_replace:
            return 'ddos invalidos numero'

        lista_texto = abstrair[1].split('%')
        texto_formatado = ""

        for n in range(len(lista_itens)):
            texto_formatado = texto_formatado + str(lista_texto[n]) + str(lista_itens[n][1])
        texto_formatado = texto_formatado + str(lista_texto[-1])


        return [True, texto_formatado, "fazerNada"]




    def funcao_para_maiusculo(self, texto):
        #self.log("__funcao_para_maiusculo")

        abstrair = self.abstrair_valor_linha(texto)
        if not abstrair[0]: return abstrair

        if self.verificar_tipo(abstrair[1]) != "string":
            return [False, self.msg("p_maiusc_minusc_cap_texto").format("maiusculo"), 'fazerNada']

        return [True, abstrair[1].upper(), "fazerNada"]

    def funcao_para_minusculo(self, texto):
        #self.log("__funcao_para_minusculo")

        abstrair = self.abstrair_valor_linha(texto)
        if not abstrair[0]: return abstrair

        if self.verificar_tipo(abstrair[1]) != "string":
            return [False, self.msg("p_maiusc_minusc_cap_texto").format("minusculo") , 'fazerNada']

        return [True, abstrair[1].lower(), "fazerNada"]

    def funcao_para_captalize(self, texto):
        #self.log("__funcao_para_captalize")

        abstrair = self.abstrair_valor_linha(texto)
        if not abstrair[0]: return abstrair

        if self.verificar_tipo(abstrair[1]) != "string":
            return [False,  self.msg("p_maiusc_minusc_cap_texto").format("captalização"), 'fazerNada']

        return [True, abstrair[1].capitalize(), "fazerNada"]

    def funcao_retorne(self, valor):
        #self.log("__funcao_retorne")

        abstrair =self.abstrair_valor_linha(valor)
        if not abstrair[0]: return abstrair

        return [True, abstrair[1], "retornarOrquestrador"]

    def funcao_parar(self):
        #self.log("__funcao_parar")

        return [True, True, "pararLoop"]

    def funcao_continuar(self):
        #self.log("__funcao_continuar")

        return [True, True, "continuarLoop"]

    def funcao_tente(self):
        #self.log("__funcao_tente")

        return [True, True, 'tenteAlgo']

    def funcao_se_der_erro(self):
        #self.log("__funcao_se_der_erro")

        return [True, True, 'seDerErro']

    def funcao_senao_der_erro(self):
        #self.log("__funcao_senao_der_erro")

        return [True, True, 'seNaoErro']

    def funcao_em_qualquer_caso(self):
        #self.log("__funcao_em_qualquer_caso")

        return [True, True, 'emQualquerCaso']

    def funcao_senao(self):
        #self.log("__funcao_senao")

        return [True, True, 'declararSenao']

    def formatar_arquivo(self, nome_arquivo):
        #self.log("formatar_arquivo")

        if "/" not in nome_arquivo:
            nome_arquivo = self.diretorio_base + nome_arquivo
        else:
            if nome_arquivo[0] != '/':
                nome_arquivo = self.diretorio_base + nome_arquivo
        return nome_arquivo

    def msg_variavel_numerica(self, msg, variavel):
        #self.log("msg_variavel_numerica")

        if msg == 'naoNumerico':
            return [False, self.msg("variavel_nao_numerica").format(variavel), 'exibirNaTela']

    def analisa_padrao_variavel(self, variavel):
        #self.log("analisa_padrao_variavel")

        variavel = str(variavel)
        variavel = variavel.replace("_", "")  # _ também é valido
        variavel = variavel.strip()

        if len(variavel) == 0:
            return [False, self.msg("variaveis_comecar_por_letra"), 'exibirNaTela']
    
        if not variavel[0].isalpha():
            return [False, self.msg("variaveis_comecar_por_letra"), 'exibirNaTela']

        if not variavel.isalnum():
            return [False, self.msg("variaveis_devem_conter"), 'exibirNaTela']

        return [True, True]

    def verifica_se_tem(self, linha, a_buscar):
        #self.log("verifica_se_tem")

        analisar = True
        lista = []

        for caractere in range(len(linha)):
            if linha[caractere] == '"' and analisar == True:
                analisar = False

            elif linha[caractere] == '"' and analisar == False:
                analisar = True

            if analisar:
                if len(linha) >= caractere + len(a_buscar):

                    if linha[caractere: caractere + len(a_buscar)] == a_buscar:
                        lista.append([caractere, caractere + len(a_buscar)])

        return lista

    def obter_valor_variavel(self, variavel):
        variavel = str(variavel)
        #self.log("obter_valor_variavel:: '{}'".format(variavel))

        variavel = variavel.strip()
        variavel = variavel.replace('\n', '')

        try:
            self.dic_variaveis[variavel]
        except:
            return [False, "{} '{}'".format(self.msg("voce_precisa_definir_variavel"), variavel), 'fazerNada']
        else:
            return [True, self.dic_variaveis[variavel], 'fazerNada']

    def obter_valor_lista(self, linha):
        #self.log("obter_valor_lista")

        teste = self.obter_valor_variavel(linha)

        if not teste[0]:
            return teste

        if self.verificar_tipo(teste[1]) != 'lista':
            return [False, "{} {}".format(linha,self.msg("nao_e_lista"))]

        return teste





    def verificar_tipo(self, valor):

        if isinstance(valor, str): return 'string'
        elif isinstance(valor, bool): return 'booleano'
        elif isinstance(valor, int): return 'float'
        elif isinstance(valor, float): return 'float'
        elif isinstance(valor, list): return 'lista'
        else: return 'vazio'


    def funcao_retornar_lista(self, variavel):
        #self.log("__funcao_retornar_lista")

        teste_variavel = self.obter_valor_lista(variavel)

        if teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], self.verificar_tipo(teste_variavel[1]), 'exibirNaTela']

        return [True, teste_variavel[1], 'fazerNada']

    def funcao_otamanho_da_lst(self, variavel):
        #self.log("__funcao_otamanho_da_lst")

        variavel = variavel.strip()

        teste =self.obter_valor_lista(variavel)
        if not teste[0]:
            return [teste[0], teste[1], 'exibirNaTela']

        try:
            return [True, len(self.dic_variaveis[variavel]), 'fazerNada']
        except Exception as erro:
            return [True, '{} {}'.format(self.msg("erro_obter_tamanho_lista"), erro), 'exibirNaTela']

    def funcao_ovalor_digitado(self, linha):
        #self.log("__funcao_ovalor_digitado: {}".format(linha))

        self.controle_interpretador = ':input:'

        self.texto_digitado = None
        while self.controle_interpretador != "":
            if self.aconteceu_erro:
                return [False, "Interrompido", "exibirNaTela"]
            sleep(0.000001)

        digitado = self.texto_digitado

        # SE FOR NUMÉRICO
        if 'numerica' in linha or 'numeric' in linha or 'number' in linha or 'numero' in linha:
            try:
                float(digitado)
            except:
                return [False, '{} "{}"'.format(self.msg("digitou_caractere"), digitado), 'fazerNada']
            else:
                return [True, float(digitado), 'fazerNada']
        else:
            return [True, digitado, 'fazerNada']

    # ======== métodos altamente depdendentes ============= #
    # ======== métodos altamente depdendentes ============= #
    # ======== métodos altamente depdendentes ============= #
    # ======== métodos altamente depdendentes ============= #

    def obter_valor_string(self, string):
        #self.log("obter_valor_string")

        valorFinal = ''
        anterior = 0

        for valor in finditer("""\"[^"]*\"""", string):

            abstrair =self.abstrair_valor_linha(string[anterior:valor.start()])
            if not abstrair[0]: return abstrair

            valorFinal = valorFinal + str(abstrair[1]) + string[valor.start() + 1:valor.end() - 1]
            anterior = valor.end()

        abstrair =self.abstrair_valor_linha(string[anterior:])
        if not abstrair[0]: return abstrair
        valorFinal = valorFinal + str(abstrair[1])

        return [True, valorFinal]




    def localiza_transforma_variavel(self, linha):
        #self.log("localiza_transforma_variavel:{}".format(linha))
        anterior = 0
        normalizacao = 0

        nova_linha = ""

        for valor in finditer('\\s{1,}', linha):
            palavra_analise =  linha[anterior:valor.start()]
            palavra_analise = palavra_analise.strip()

            if palavra_analise.isalnum():
                abstrair = self.abstrair_valor_linha(palavra_analise)
                if not abstrair[0]:
                    return abstrair


                if self.verificar_tipo(abstrair[1]) == 'string':
                    palavra_analise = '"' + str(abstrair[1]) + '"'
                else:
                    palavra_analise = str(abstrair[1])


            nova_linha = nova_linha + palavra_analise
            anterior = valor.end()

        nova_linha = nova_linha + linha[anterior:]

        return [True, nova_linha]


    def fazer_contas(self, linha):
        #self.log("fazer_contas:linha={}".format(linha))

        for comando in self.dic_comandos["matematica_mult"]["comando"]:
            linha = linha.replace(comando[0], ' * ')

        for comando in self.dic_comandos["matematica_div"]["comando"]:
            linha = linha.replace(comando[0], ' / ')

        for comando in self.dic_comandos["matematica_elev"]["comando"]:
            linha = linha.replace(comando[0], ' ** ')

        for comando in self.dic_comandos["matematica_mod"]["comando"]:
            linha = linha.replace(comando[0], ' % ')

        for comando in self.dic_comandos["matematica_add"]["comando"]:
            linha = linha.replace(comando[0], ' + ')

        for comando in self.dic_comandos["matematica_sub"]["comando"]:
            linha = linha.replace(comando[0], ' - ')

        for comando in self.dic_comandos["logico_true"]["comando"]:
            linha = linha.replace(comando[0], ' True ')

        for comando in self.dic_comandos["logico_false"]["comando"]:
            linha = linha.replace(comando[0], ' False ')


        #if '"' in linha: return [False, "Isso é uma string", 'string']

        linha = ' {} '.format(linha)

        simbolos = ['+', '-', '*', '/', '%', '(', ')']
        quantidade_simbolos = 0

        # Deixando todos os itens especiais com espaço em relação aos valores
        for iten in simbolos:

            if iten in linha:
                quantidade_simbolos += 1

            linha = linha.replace(iten, ' {} '.format(iten))

        # Se não tiver nenhuma operação
        if quantidade_simbolos == 0:

            return [False, self.msg("nao_possui_operacao_matematica"), 'string']

        # Correção de caracteres
        linha = linha.replace('*  *', '**')
        linha = linha.replace('< =', '<=')
        linha = linha.replace('> =', '>=')
        linha = linha.replace("! =", '!=')

        # Abstrai o valor de todas as variáveis
        linha =self.localiza_transforma_variavel(linha)

        if not linha[0]: return linha

        # Se sobrou texto
        #for caractere in linha[1]:
        #    if str(caractere).isalpha():
        #        return [False, self.msg("nao_possivel_conta_string") + str(linha[1]), 'string']

        # Tente fazer uma conta com isso

        try:
            resutadoFinal = eval(linha[1])
        except Exception as erro:

            return [False, "{} |{}|".format(self.msg("nao_possivel_fazer_conta"), linha[1])]
        else:
            return [True, resutadoFinal]

    def abstrair_mostre_valor(self, possivel_variavel):
        #self.log("abstrair_mostre_valor")
        possivel_variavel = possivel_variavel.strip()
        if possivel_variavel == '':
            return [True, '', 'exibirNaTela']

        # Caso existam contas entre strings ( Formatação )
        #if possivel_variavel[0] == ',':
        #    possivel_variavel = possivel_variavel[1:]

        # Caso existam contas entre strings ( Formatação )
        #if len(possivel_variavel) > 1:
        #    if possivel_variavel[-1] == ',':
        #        possivel_variavel = possivel_variavel[0:-1]

        #testa = self.verifica_se_tem(possivel_variavel, ",")
        #if testa != []:

        #    listaLinhas = [possivel_variavel[: testa[0][0]], possivel_variavel[testa[0][1]:]]
        #    listaValores = ''

        #    for linha in listaLinhas:
        #        valor =self.abstrair_valor_linha(linha)

        #        if not valor[0]:
        #            return valor

        #        listaValores += str(valor[1])

        #    return [True, listaValores, "string"]

        return self.abstrair_valor_linha(possivel_variavel)

    def abstrair_valor_linha(self, possivel_variavel:str):
        possivel_variavel = str(possivel_variavel)
        #self.log("abstrair_valor_linha: possivel_variavel = '{}'".format(possivel_variavel))

        possivel_variavel = str(possivel_variavel).strip()

        if possivel_variavel == '':
            return [True, "", "fazerNada"]

        # Caso existam contas entre strings ( Formatação )
        #if possivel_variavel[0] == ',':
        #    possivel_variavel = possivel_variavel[1:]

        # Caso existam contas entre strings ( Formatação )
        #if len(possivel_variavel) > 1:
        #    if possivel_variavel[-1] == ',':
        #        possivel_variavel = possivel_variavel[0:-1]

        #testa = self.verifica_se_tem(possivel_variavel, ",")
        #if testa != []:

        #    listaLinhas = [possivel_variavel[: testa[0][0]], possivel_variavel[testa[0][1]:]]
        #    listaValores = ''

        #    for linha in listaLinhas:
        #        valor =self.abstrair_valor_linha(linha)

        #        if not valor[0]:
        #            return valor

        #        listaValores += str(valor[1])

        #    return [True, listaValores, "string"]

        # Sem dados
        #if possivel_variavel == '':
        #     return [True, '', 'string']

        # Sem dados
        #if possivel_variavel[-1] == ',':
        #    possivel_variavel = possivel_variavel[:-1]

        # Sem dados
        #if possivel_variavel == '':
        #    return [True, '', 'string']

        # Valor Booleando
        if possivel_variavel.lower() in [comando[0] for comando in self.dic_comandos["logico_true"]["comando"]]:
            return [True, True]

        if possivel_variavel.lower() in [comando[0] for comando in self.dic_comandos["logico_false"]["comando"]]:
            return [True, False]

        if possivel_variavel[0] == '"':
            if len(possivel_variavel) > 1:
                pos = possivel_variavel[1:].find('"')
                if pos != -1:
                    if pos+1 == len(possivel_variavel)-1:
                        return [True, possivel_variavel[1:-1]]


        # Tentar fazer Contas
        resultado =self.fazer_contas(possivel_variavel)
        if resultado[0]: return resultado


        # Aplicação de possíveis comandos internos
        resultado = self.comandos_uso_geral(possivel_variavel)
        if resultado != [True, None]:
            return resultado


        # Se estourar um erro e com valor
        if resultado[0] and resultado[1] != None:
            return resultado

        # Se não estourar erro, obtenção do valor foi bem sucedida
        elif not resultado[0]:
            return resultado

        # Verificando se tem strings dentro do comando
        testa = self.verifica_se_tem(possivel_variavel, '"')
        if testa != []:
            # Isola Strings de variáveis
            return self.obter_valor_string(possivel_variavel)

        # Tentar converter o valor para número
        try:
            numero = float(possivel_variavel)
        except Exception as TypeError:
            # Então o valor deve ser uma variável
            return self.obter_valor_variavel(possivel_variavel)


        else:
            return [True, numero]

    # ======== fim métodos altamente depdendentes ============= #
    # ======== fim métodos altamente depdendentes ============= #
    # ======== fim métodos altamente depdendentes ============= #
    # ======== fim métodos altamente depdendentes ============= #

    def funcao_importe(self, biblioteca):
        #self.log("__funcao_importe: biblioteca = '{}'".format(biblioteca))

        biblioteca = self.formatar_arquivo(biblioteca) + str(".safira")

        # Tenta abrir o texto da biblioteca
        teste = funcoes.abrir_arquivo(biblioteca)
        if teste[0] == None:
            return [False, self.msg("erro_abrir_biblioteca").format(biblioteca, teste[1]), "fazerNada"]

        # Carrega a biblioteca
        resultadoOrquestrador =self.orquestrador_interpretador_(teste[0])

        if resultadoOrquestrador[0] == False:
            return resultadoOrquestrador

        return [True, None, 'fazerNada']

    def funcao_tipo_variavel(self, variavel):
        #self.log("__funcao_tipo_variavel")

        resultado =self.abstrair_valor_linha(variavel)

        if not resultado[0]:
            return resultado

        if self.verificar_tipo(resultado[1]) == 'string':
            resultado[1] = str(resultado[1]).replace("\\n", "\n")

        return [resultado[0], self.verificar_tipo(resultado[1]), self.verificar_tipo(resultado[1]), 'exibirNaTela']

    # =================== ARQUIVOS =================== #
    def funcao_ler_arquivo(self, nome_arquivo):
        #self.log("__funcao_ler_arquivo")

        teste_valor_arquivo =self.abstrair_valor_linha(nome_arquivo)
        if teste_valor_arquivo[0] == False: return teste_valor_arquivo

        if teste_valor_arquivo[1] == "":
            return [False, self.msg("precisa_nome_arquivo"), ' exibirNaTela']

        nome_arquivo = str(teste_valor_arquivo[1])
        nome_arquivo = self.formatar_arquivo(nome_arquivo)

        if os_path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "r")
                texto = f.read()
                f.close()

            except Exception as e:
                return [False, self.msg("erro_abrir_arquivo").format(nome_arquivo, e), 'exibirNaTela']
            else:
                return [True, str(texto), "fazerNada"]
            return [True, True, "fazerNada"]

        return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), ' exibirNaTela']

    def funcao_sobrescrever_arquivo(self, texto, nome_arquivo):
        #self.log("__funcao_sobrescrever_arquivo")

        teste_valor_arquivo =self.abstrair_valor_linha(nome_arquivo)
        teste_valor_texto =self.abstrair_valor_linha(texto)

        if teste_valor_arquivo[0] == False: return teste_valor_arquivo
        if teste_valor_texto[0] == False: return teste_valor_texto

        if teste_valor_arquivo[1] == "":
            return [False, self.msg("precisa_nome_arquivo"), ' exibirNaTela']

        nome_arquivo = str(teste_valor_arquivo[1])
        nome_arquivo = self.formatar_arquivo(nome_arquivo)
        texto = str(teste_valor_texto[1])
        texto = texto.replace("\\n", "\n")

        if os_path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "w", encoding="utf8")
                f.write(texto)
                f.close()

            except Exception as e:
                return [False,
                        self.msg("erro_adicionar_texto_arquivo").format(texto, nome_arquivo, e), ' exibirNaTela']

            return [True, True, "fazerNada"]
        return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), ' exibirNaTela']

    def funcao_adicionar_arquivo(self, texto, nome_arquivo):
        #self.log("__funcao_adicionar_arquivo")

        teste_valor_arquivo =self.abstrair_valor_linha(nome_arquivo)
        teste_valor_texto =self.abstrair_valor_linha(texto)

        if teste_valor_arquivo[0] == False: return teste_valor_arquivo
        if teste_valor_texto[0] == False: return teste_valor_texto

        if teste_valor_arquivo[1] == "":
            return [False, self.msg("precisa_nome_arquivo"), ' exibirNaTela']

        nome_arquivo = str(teste_valor_arquivo[1])
        nome_arquivo = self.formatar_arquivo(nome_arquivo)

        texto = str(teste_valor_texto[1])
        texto = texto.replace("\\n", "\n")

        if os_path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "a", encoding="utf8")
                f.write(texto)
                f.close()

            except Exception as e:
                return [False,  self.msg("erro_adicionar_texto_arquivo").format(texto, nome_arquivo, e), ' exibirNaTela']
            return [True, True, "fazerNada"]
        return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), ' exibirNaTela']

    def funcao_listar_arquivos(self, nome_diretorio):
        #self.log("__funcao_listar_arquivos")

        if nome_diretorio == "":
            return [False, self.msg("precisa_nome_diretorio"), ' exibirNaTela']

        teste_valor =self.abstrair_valor_linha(nome_diretorio)
        if teste_valor[0] == False: return teste_valor

        nome_diretorio = str(teste_valor[1])
        nome_diretorio = self.formatar_arquivo(nome_diretorio)
        teste_diretorio = self.funcao_diretorio_existe('"{}"'.format(nome_diretorio))
        if not teste_diretorio[0]:
            return teste_diretorio

        if not teste_diretorio[1]:
            return [False, self.msg('diretório_não_existe').format(nome_diretorio), 'fazerNada']

        lista_retorno = listdir(nome_diretorio)
        lista_resultado = [[x] for x in lista_retorno]

        return [True, lista_resultado, "fazerNada"]

    def funcao_diretorio_existe(self, nome_diretorio):
        #self.log("__funcao_diretorio_existe")

        if nome_diretorio == "":
            return [False, self.msg("precisa_nome_diretorio"), ' exibirNaTela']

        teste_valor =self.abstrair_valor_linha(nome_diretorio)
        if teste_valor[0] == False: return teste_valor

        nome_diretorio = str(teste_valor[1])
        nome_diretorio = self.formatar_arquivo(nome_diretorio)

        if os_path.exists(nome_diretorio):
            return [True, True, "fazerNada"]
        else:
            return [True, False, "fazerNada"]

    def funcao_diretorio_nao_existe(self, nome_diretorio):
        #self.log("__funcao_diretorio_nao_existe")

        if nome_diretorio == "":
            return [False, self.msg("precisa_nome_diretorio"), ' exibirNaTela']

        teste_valor =self.abstrair_valor_linha(nome_diretorio)
        if teste_valor[0] == False: return teste_valor

        nome_diretorio = str(teste_valor[1])
        nome_diretorio = self.formatar_arquivo(nome_diretorio)

        if os_path.exists(nome_diretorio):
            return [True, False, "fazerNada"]
        else:
            return [True, True, "fazerNada"]

    # Precisa disferenciar diretório de arquivo
    def funcao_arquivo_existe(self, nome_arquivo):
        #self.log("__funcao_arquivo_existe")

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), ' exibirNaTela']

        teste_valor =self.abstrair_valor_linha(nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = self.formatar_arquivo(nome_arquivo)

        if os_path.exists(nome_arquivo):
            return [True, True, "fazerNada"]
        else:
            return [True, False, "fazerNada"]

    def funcao_arquivo_nao_existe(self, nome_arquivo):
        #self.log("__funcao_arquivo_nao_existe"+ nome_arquivo)

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), ' exibirNaTela']

        teste_valor =self.abstrair_valor_linha(nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = self.formatar_arquivo(nome_arquivo)

        if os_path.exists(nome_arquivo):
            return [True, False, "fazerNada"]
        else:
            return [True, True, "fazerNada"]

    def funcao_excluir_arquivo(self, nome_arquivo: str) -> list:
        """ Recebe um diretóirio e exclui um arquivo

        Args:
            nome_arquivo (str): diretório e o arquivo, exemplo: /home/gabriel/ola.txt
                                ele também pode passar um arquivo que esteja no mesmo
                                caminho relativo do script.

        Returns:
            list: [sucesso: bool, mensagem: str, tipo_mensagem: str, acao: str]
        """

        #self.log("__funcao_excluir_arquivo")

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), ' exibirNaTela']

        teste_valor =self.abstrair_valor_linha(nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = self.formatar_arquivo(nome_arquivo)

        try:
            os_remove(nome_arquivo)
        except FileNotFoundError:
            return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), ' exibirNaTela']
        except Exception as erro:
            return [False, self.msg("erro_deletar_arquivo").format(erro), ' exibirNaTela']
        else:
            return [True, "", "fazerNada"]
            

    def funcao_criar_arquivo(self, nome_arquivo):
        #self.log("__funcao_criar_arquivo")

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), ' exibirNaTela']

        teste_valor =self.abstrair_valor_linha(nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = self.formatar_arquivo(nome_arquivo)

        if not os_path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "w", encoding='utf8')
                f.write("")
                f.close()

            except Exception as erro:
                return [False, self.msg("erro_criar_arquivo").format(erro), ' exibirNaTela']

        return [True, "", "fazerNada"]

    def funcao_incremente_vari(self, valor, variavel):
        #self.log("__funcao_incremente_vari")

        return self.incremente_decremente(valor, variavel, 'incremente')

    def funcao_decremente_vari(self, valor, variavel):
        #self.log("__funcao_decremente_vari")

        return self.incremente_decremente(valor, variavel, 'decremente')

    def incremente_decremente(self, valor, variavel, acao):
        #self.log("incremente_decremente")

        teste_exist =self.obter_valor_variavel(variavel)
        teste_valor =self.abstrair_valor_linha(valor)

        if teste_exist[0] == False: return teste_exist
        if teste_valor[0] == False: return teste_valor

        if self.verificar_tipo(teste_exist[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', variavel)

        if self.verificar_tipo(teste_valor[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', teste_valor[1])

        if acao == "incremente":
            self.dic_variaveis[variavel] = self.dic_variaveis[variavel] + teste_valor[1]

        else:
            self.dic_variaveis[variavel] = self.dic_variaveis[variavel] - teste_valor[1]

        return [True, True, "fazerNada"]

    def teste_generico_lista(self, variavel, valor):
        #self.log("teste_generico_lista")

        if variavel == '' or valor == '':
            return [False,self.msg("variavel_valor_nao_informado"), 'exibirNaTela']

        teste_variavel = self.obter_valor_lista(variavel)
        teste_valor = self.abstrair_valor_linha(valor)

        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], 'exibirNaTela']

        if not teste_valor[0]:
            return [teste_valor[0], teste_valor[1], 'exibirNaTela']

        return [True, teste_variavel, teste_valor]

    def funcao_rem_itns_na_lst(self, valor, variavel):
        #self.log("__funcao_rem_itns_na_lst")

        teste_generico = self.teste_generico_lista(variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        try:
            self.dic_variaveis[variavel].remove(teste_valor[1])
        except Exception as erro:
            return [False, '"{}" {} "{}"!'.format(teste_valor[1],self.msg("nao_esta_na_lista"), variavel), 'exibirNaTela']
        return [True, None, 'fazerNada']

    def funcao_add_itns_na_lst(self, valor, variavel):
        #self.log("__funcao_add_itns_na_lst")

        teste_generico = self.teste_generico_lista(variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        try:
            self.dic_variaveis[variavel].append(teste_valor[1])
        except Exception as erro:
            return [False, '"{}" {} "{}"!'.format(teste_valor[1],self.msg("nao_esta_na_lista"), variavel), 'exibirNaTela']
        return [True, None, 'fazerNada']

    def funcao_add_itns_lst_in(self, valor, variavel):
        #self.log("__funcao_add_itns_lst_in")

        teste_generico = self.teste_generico_lista(variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        self.dic_variaveis[variavel].insert(0, teste_valor[1])
        return [True, None, 'fazerNada']

    def funcao_add_itns_lst_ps(self, valor, posicao, variavel):
        #self.log("__funcao_add_itns_lst_ps")

        if variavel == '' or valor == '':
            return [False, self.msg("necessario_informar_variavel_valor") ]

        teste_generico = self.teste_generico_lista(variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        teste_posicao =self.abstrair_valor_linha(posicao)
        if not teste_posicao[0]: return [teste_posicao[0], teste_posicao[1], 'exibirNaTela']

        if self.verificar_tipo(teste_posicao[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', teste_posicao[1])

        posicao = int(teste_posicao[1])

        if posicao - 1 > len(self.dic_variaveis[variavel]):
            return [False,self.msg("posicao_maior_limite_lista"), 'exibirNaTela']

        if posicao < 1:
            return [False,self.msg("posicao_menor_limite_lista"), 'exibirNaTela']

        self.dic_variaveis[variavel].insert(posicao - 1, teste_valor[1])
        return [True, True, 'fazerNada']

    # ============ mostre ==================#
    def funcao_exibir_outra_ln(self, linha):
        #self.log("__funcao_exibir_outra_ln: {}".format(linha))

        resultado = self.abstrair_mostre_valor(linha)
        if not resultado[0]:
            return resultado

        if self.verificar_tipo(resultado[1]) == 'string':
            resultado[1] = str(resultado[1]).replace("\\n", "\n")


        if len(resultado) == 3:
            if "exibirCor" in resultado[2]:
                return [resultado[0], ':mostreLinha:{}'.format(resultado[2]) + str(resultado[1]), 'exibirNaTela']
        return [resultado[0], ':mostreLinha:::' + str(resultado[1]), 'exibirNaTela']


    def funcao_exibir_mesma_ln(self, linha):
        #self.log("__funcao_exibir_mesma_ln: {}".format(linha))

        resultado = self.abstrair_mostre_valor(linha)


        if not resultado[0]:
            return resultado


        if self.verificar_tipo(resultado[1]) == 'string':
            resultado[1] = str(resultado[1]).replace("\\n", "\n")


        if len(resultado) > 3:
            if "exibirCor" in resultado[2]:
                return [resultado[0], ':nessaLinha:{}'.format(resultado[2]) + str(resultado[1]), 'exibirNaTela']
        return [resultado[0], ':nessaLinha:::' + str(resultado[1]), 'exibirNaTela']

    def funcao_na_cor(self, linha, cor):
        #self.log("___funcao_na_cor: linha={}, cor={}".format(linha, cor))

        teste_linha = self.abstrair_valor_linha(linha)
        if not teste_linha[0]:
            return teste_linha

        teste_cor = self.abstrair_valor_linha(cor)
        if not teste_cor[0]:
            return teste_cor

        return [True, teste_linha[1], "exibirCor:{}:".format(teste_cor[1])]



    def funcao_esperar_n_tempo(self, tempo, tipo_espera):
        #self.log("__funcao_esperar_n_tempo: tempo = '{}', espera = '{}'".format(tempo, tipo_espera))

        resultado =self.abstrair_valor_linha(tempo)
        if not resultado[0]: return resultado

        if tipo_espera in [comando[0].strip() for comando in self.dic_comandos['esperaEmSegundos']['comando']]:
            sleep(resultado[1])

        elif tipo_espera in [ comando[0].strip() for comando in self.dic_comandos['esperaEmMs']['comando']]:
            sleep(resultado[1] / 1000)

        return [True, None, 'fazerNada']

    def tiver_valor_lista(self, linha):
        #self.log("tiver_valor_lista")

        linha = linha.strip()

        __resultado = self.analisa_instrucao('^(<tiver_lista>)(.*)(<tiver_interno_lista>)(.*)$', linha, self.compilado)
        if __resultado[0]:
            return self.funcao_tiver_valor_lst(__resultado[1][2], __resultado[1][4])

        return [True, None]

    def funcao_senao_se(self, condicao):
        #self.log("__funcao_senao_se")

        resultado =self.funcao_testar_condicao(condicao)
        return [resultado[0], resultado[1],'declararSenaoSe']

    def funcao_loops_enquantox(self, linha):
        #self.log("__funcao_loops_enquantox")

        resultado =self.funcao_testar_condicao(linha)
        return [resultado[0], resultado[1], 'declararLoop']

    def funcao_loop_para_cada_(self, variavel, inicio, fim):
        #self.log("__funcao_loop_para_cada_")

        teste_exist =self.obter_valor_variavel(variavel)
        teste_valorI =self.abstrair_valor_linha(inicio)
        teste_valorF =self.abstrair_valor_linha(fim)

        if teste_valorI[0] == False:
            return teste_valorI

        if teste_valorF[0] == False:
            return teste_valorF

        if self.verificar_tipo(teste_valorI[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', teste_valorI[1])

        if self.verificar_tipo(teste_valorF[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', teste_valorF[1])

        # Variável não existe
        if teste_exist[0] == False:
            criar_variavel = self.funcao_realizar_atribu(variavel, '0')

            if not criar_variavel[0]:
                return criar_variavel
        passo = 1

        if (int(teste_valorI[1]) > int(teste_valorF[1])):
            passo = -1

        return [True, [variavel, int(teste_valorI[1]), int(teste_valorF[1]), passo], "declararLoopParaCada"]

    def funcao_add_lst_na_posi(self, variavelLista, posicao, valor):
        #self.log("__funcao_add_lst_na_posi")

        if variavelLista == '' or posicao == '' or valor == '':  # Veio sem dados
            return [False, self.msg('add_lst_posicao_separador'), ' exibirNaTela']

        teste_exist =self.obter_valor_variavel(variavelLista)
        teste_posic =self.abstrair_valor_linha(posicao)
        teste_valor =self.abstrair_valor_linha(valor)

        if not teste_exist[0]:
            return teste_exist

        if not teste_posic[0]:
            return teste_posic

        if not teste_valor[0]:
            return teste_valor

        if self.verificar_tipo(teste_exist[1]) != 'lista':
            return [False, '{} {}'.format(variavelLista,self.msg("nao_e_lista"))]

        if self.verificar_tipo(teste_posic[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', teste_posic[1])

        posicao = int(teste_posic[1])

        # Posição estoura posições da lista
        if posicao - 1 > len(self.dic_variaveis[variavelLista]):
            return [False, '{} {}'.format(self.msg("posicao_maior_limite_lista"), posicao), 'exibirNaTela']

        if posicao < 1:
            return [False, '{} {}'.format(self.msg("posicao_menor_limite_lista"), posicao), 'exibirNaTela']

        self.dic_variaveis[variavelLista][posicao - 1] = teste_valor[1]
        return [True, True, 'fazerNada']

    def funcao_obter_valor_lst(self, variavel, posicao):
        #self.log("__funcao_obter_valor_lst")

        if variavel == '' or posicao == '':
            return [False, self.msg("variavel_posicao_nao_informada"), 'exibirNaTela']

        teste_posicao = self.abstrair_valor_linha(posicao)
        teste_variavel = self.obter_valor_lista(variavel)

        if not teste_posicao[0]:
            return [teste_posicao[0], teste_posicao[1], 'exibirNaTela']

        elif self.verificar_tipo(teste_posicao[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', teste_posicao[1])

        elif teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], 'exibirNaTela']

        posicao = int(teste_posicao[1])
        resultado = teste_variavel[1]

        if posicao < 1:
            return [False, self.msg("posicao_menor_limite_lista"), 'exibirNaTela']

        if len(resultado) < posicao:
            return [False, self.msg("posicao_maior_limite_lista"), 'exibirNaTela']

        return [True, resultado[posicao-1], resultado[posicao-1], 'exibirNaTela']

    def funcao_tiver_valor_lst(self, valor, variavel):
        #self.log("__funcao_tiver_valor_lst")

        if variavel == '' or valor == '':
            return [False, self.msg("variavel_valor_nao_informado"), 'exibirNaTela']

        teste_variavel =self.obter_valor_variavel(variavel)
        resultado_valor =self.abstrair_valor_linha(valor)

        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], 'exibirNaTela']

        if self.verificar_tipo(teste_variavel[1]) != 'lista':
            return [False, '{} {}'.format(teste_variavel[1], self.msg("nao_e_lista")), 'exibirNaTela']

        if not resultado_valor[0]:
            return [resultado_valor[0], resultado_valor[1], 'exibirNaTela']

        if resultado_valor[1] in self.dic_variaveis[variavel]:
            return [True, True, 'fazerNada']
        return [True, False, 'fazerNada']

    def funcao_dec_lst_posicoe(self, variavel, posicoes):
        #self.log("__funcao_dec_lst_posicoe")

        #self.log('<funcao_dec_lst_posicoe>:')
        teste =self.analisa_padrao_variavel(variavel)
        resultado =self.abstrair_valor_linha(posicoes)

        if not teste[0]:
            return teste

        if not resultado[0]:
            return resultado

        if self.verificar_tipo(resultado[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', resultado[1])

        lista_itens_declarar = []
        for posicao in range(int(posicoes)):
            lista_itens_declarar.append('')

        self.dic_variaveis[variavel] = lista_itens_declarar
        return [True, None, 'fazerNada']

    def funcao_repetir_n_vezes(self, linha):
        #self.log("__funcao_repetir_n_vezes")

        linha = linha.replace('vezes', '')
        linha = linha.replace('vez', '')
        linha = linha.replace('times', '')
        linha = linha.replace('veces', '')

        linha = linha.strip()
        linha =self.abstrair_valor_linha(linha)

        if not linha[0]:
            return [linha[0], linha[1], 'exibirNaTela']

        if self.verificar_tipo(linha[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', linha[1])

        try:
            int(linha[1])
        except:
            return [False, '{} "{}"'.format(self.msg("repetir_nao_informou_inteiro"), linha[1]), 'exibirNaTela']
        else:
            funcao_repita = int(linha[1])
            return [True, funcao_repita, 'declararLoopRepetir']

    def funcao_numer_aleatorio(self, num1, num2):
        #self.log("__funcao_numer_aleatorio: num1 = '{}', num2 = '{}'".format(num1, num2))

        num1 =self.abstrair_valor_linha(num1)
        num2 =self.abstrair_valor_linha(num2)

        if not num1[0]: return num1
        if not num2[0]: return num2

        try:
            int(num1[1])
        except:
            return [False, self.msg("aleatorio_valor1_nao_numerico"), 'exibirNaTela']

        try:
            int(num2[1])
        except:
            return [False, self.msg("aleatorio_valor2_nao_numerico"), 'exibirNaTela']

        n1 = int(num1[1])
        n2 = int(num2[1])

        if n1 == n2:
            return [False, self.msg("aleatorio_valor1_igual_valo2"), 'exibirNaTela']

        elif n1 > n2:
            return [False, self.msg("aleatorio_valor1_maior_valo2"), 'exibirNaTela']

        return [True, randint(n1, n2), 'fazerNada']

    def funcao_realizar_atribu(self, variavel, valor):
        #self.log("__funcao_realizar_atribu: variavel = '{}', valor='{}'".format(variavel, valor))

        if variavel == '' or valor == '':
            return [False, self.msg("variavel_valor_nao_informado"), 'exibirNaTela']

        teste_padrao = self.analisa_padrao_variavel(variavel)
        if not teste_padrao[0]:
            return teste_padrao

        valor = valor.replace('\n', '')
        valor = valor.strip()

        resultado =self.abstrair_valor_linha(valor)
        if not resultado[0]: return resultado

        if resultado[0]:
            self.dic_variaveis[variavel] = resultado[1]
            return [True, None, 'fazerNada']

        return [resultado[0], resultado[1], 'fazerNada']

    def funcao_realiza_atribuica_posicao_lista(self, variavel, posicao, itens):
        #self.log("__funcao_realiza_atribuica_posicao_lista")

        variavel = variavel.strip()
        posicao = posicao.strip()
        itens = itens.strip()

        if itens == '' or variavel == '' or posicao == '':
            return [False,self.msg("variavel_posicao_nao_informada"), 'exibirNaTela']

        teste_variavel = self.obter_valor_variavel(variavel)
        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], 'exibirNaTela']

        if self.verificar_tipo(teste_variavel[1]) != 'lista':
            return [False, '{} {}'.format(teste_variavel[1], self.msg("nao_e_lista")), 'exibirNaTela']

        resultado_posicao = self.abstrair_valor_linha(posicao)
        if not resultado_posicao[0]:
            return resultado_posicao
        if self.verificar_tipo(resultado_posicao[1]) != 'float':
            return self.msg_variavel_numerica('naoNumerico', linha[1])

        tamanho_lista = self.funcao_otamanho_da_lst(variavel)
        if not tamanho_lista[0]:
            return tamanho_lista

        # Verifica se estorou o limite da lista
        if resultado_posicao[1] > tamanho_lista[1]:
            return [False,self.msg("posicao_maior_limite_lista"), 'exibirNaTela']

        if resultado_posicao[1] < 1:
            return [False,self.msg("posicao_menor_limite_lista"), 'exibirNaTela']

        resultado_itens = self.abstrair_valor_linha(itens)
        if not resultado_itens[0]: return resultado_itens

        self.dic_variaveis[variavel][int(resultado_posicao[1]) - 1] = resultado_itens[1]
        return [True, None, 'fazerNada']

    # ========== FUNÇÔES GRANDES ======================= #

    def funcao_declarar_listas(self, variavel, itens):
        #self.log("__funcao_declarar_listas")

        if itens == '' or variavel == '':
            return [False,self.msg("variavel_posicao_nao_informada"), 'exibirNaTela']

        variavel = variavel.strip()

        teste =self.analisa_padrao_variavel(variavel)
        testa =self.verifica_se_tem(itens, ', ')

        if not teste[0]: return teste

        if testa != []:
            lista_itens = []
            anterior = 0

            for valor_item in testa:
                if len(itens[anterior: valor_item[0]]) > 0:
                    lista_itens.append(itens[anterior: valor_item[0]])

                anterior = valor_item[1]

            if len(itens[anterior:]) > 0:
                lista_itens.append(itens[anterior:])

            lista_itens_declarar = []

            for item in lista_itens:
                obter_valor =self.abstrair_valor_linha(item)

                if obter_valor[0] == False:
                    return [obter_valor[0], obter_valor[1], 'exibirNaTela']

                #lista_itens_declarar.append([obter_valor[1], obter_valor[2]])
                lista_itens_declarar.append(obter_valor[1])

            self.dic_variaveis[variavel] = lista_itens_declarar
            return [True, None, 'fazerNada']

        else:
            obter_valor =self.abstrair_valor_linha(itens)
            if obter_valor[0] == False:
                return [obter_valor[0], obter_valor[1], 'exibirNaTela']

            lista = []
            #lista.append([obter_valor[1], obter_valor[2]])
            lista.append(obter_valor[1])

            self.dic_variaveis[variavel] = lista
            return [True, None, 'fazerNada']


    def funcao_declarar_funcao(self, nome_funcao:str, parametros=None, classe:bool=True):
        #self.log("__funcao_declarar_funcao: nome_funcao = '{}', parametros = '{}'".format(nome_funcao, parametros))

        if parametros is not None:
            if parametros.strip() == "":
                parametros = None

        # Se o nome da função não está no padrão
        teste =self.analisa_padrao_variavel(nome_funcao)
        if not teste[0]:
            return teste

        # Se não tem parâmetros
        if parametros is None:
            self.dic_funcoes[nome_funcao] = {'parametros': None, 'bloco': 'bloco'}

            return [True, True, 'declararFuncao', nome_funcao]

        # Verifica se tem mais de um parâmetro
        testa =self.verifica_se_tem(parametros, ', ')

        # Tem mais de um parametro
        if testa != []:
            lista_parametros = []
            anterior = 0

            for valor_item in testa:
                if parametros[anterior: valor_item[0]]:
                    lista_parametros.append(parametros[anterior: valor_item[0]])

                anterior = valor_item[1]

            if len(parametros[anterior:]) > 0:
                lista_parametros.append(parametros[anterior:])

            listaFinalDeParametros = []
            for parametro in lista_parametros:
                listaFinalDeParametros.append(parametro.strip())

                teste =self.analisa_padrao_variavel(parametro.strip())
                if not teste[0]: return teste

            # Adicionar Função
            self.dic_funcoes[nome_funcao] = {'parametros': listaFinalDeParametros, 'bloco': 'bloco'}

        # Não multiplos parâmetros
        else:

            # Verifica se o parâmetro está no padrão
            teste =self.analisa_padrao_variavel(parametros)
            if not teste[0]:
                return teste

            # Adicionar Função
            self.dic_funcoes[nome_funcao] = {'parametros': [parametros], 'bloco': 'bloco'}

        funcao_em_analise = nome_funcao
        return [True, True, 'declararFuncao', funcao_em_analise]

    def funcao_executar_funcao(self, nome_funcao, parametros=None):
        #self.log("__funcao_executar_funcao: nome_funcao = '{}', parametros='{}'".format(nome_funcao, parametros))

        if parametros is not None:
            if parametros.strip() == "":
                parametros = None
            
        try:
            self.dic_funcoes[nome_funcao]
        except Exception as erro:
            return [False, self.msg("funcao_nao_existe").format(nome_funcao), 'exibirNaTela']

        # Se não veio parâmetros
        if parametros is None:
            # Se a função tem parâmetros, mas não foi informando nenhum
            if self.dic_funcoes[nome_funcao]['parametros'] != None:
                return [False,self.msg("funcao_nao_passou_parametros").format(nome_funcao, len(
                    self.dic_funcoes[nome_funcao]['parametros'])), 'exibirNaTela']

            # Executa o bloco de instrução da função
            resultado_orquestrador = self.orquestrador_interpretador_(self.dic_funcoes[nome_funcao]['bloco'])

            # Se deu erro
            if not resultado_orquestrador[0]:
                return [resultado_orquestrador[0], resultado_orquestrador[1], 'exibirNaTela']


            if resultado_orquestrador[2] != 'retornarOrquestrador':
                # Sem retorno
                return [True, "", 'fazerNada']
            else:
                return [True, resultado_orquestrador[1], resultado_orquestrador[2]]




        # Verifica se tem virgulas separando os parâmetros
        testa = self.verifica_se_tem(parametros, ',')

        # Se tinha multiplos parâmetros
        if testa != []:
            anterior = 0
            lista_parametros = []

            # Anda pelos parâmetros
            for valor_item in testa:

                # Obtem os parâmetros
                if len(parametros[anterior:valor_item[0]]) > 0:
                    lista_parametros.append(parametros[anterior: valor_item[0]])
                    anterior = valor_item[1]

            if len(parametros[anterior:]) > 0:
                lista_parametros.append(parametros[anterior:])

            lista_final_parametros = []

            # Anda pelos parâmetros
            for parametro in lista_parametros:
                lista_final_parametros.append(parametro.strip())

            # Foi informando parâmetros, mas a função não tem parâmetros
            if self.dic_funcoes[nome_funcao]['parametros'] is None:
                return [False,self.msg("funcao_informou_mais_parametros").format(nome_funcao), 'exibirNaTela']

            # Se a quantidade de itens for a mesma dessa funcao
            if len(self.dic_funcoes[nome_funcao]['parametros']) == len(lista_final_parametros):

                for parametros_declarar in range(len(self.dic_funcoes[nome_funcao]['parametros'])):
                    resultado = self.funcao_realizar_atribu(self.dic_funcoes[nome_funcao]['parametros'][
                        parametros_declarar], lista_final_parametros[parametros_declarar])

                    if resultado[0] == False:
                        return [resultado[0], resultado[1], 'exibirNaTela']
            else:
                return [False,self.msg("funcao_tem_parametros_divergentes").format(
                    nome_funcao,
                    len(self.dic_funcoes[nome_funcao]['parametros']),
                    len(lista_final_parametros)), 'fazerNada']


        # Se não vieram parâmetros
        elif parametros is not None:

            # Foi informando parâmetros, mas a função não tem parâmetros
            if self.dic_funcoes[nome_funcao]['parametros'] is None:
                return [False,self.msg("funcao_informou_mais_parametros").format(nome_funcao), 'exibirNaTela']


            if len(self.dic_funcoes[nome_funcao]['parametros']) == 1:
                resultado =self.funcao_realizar_atribu(self.dic_funcoes[nome_funcao]['parametros'][0], parametros)

                if not resultado[0]:
                    return [resultado[0], resultado[1], 'exibirNaTela']
            else:
                 return [False,self.msg("funcao_passou_um_parametros").format(nome_funcao, len(self.dic_funcoes[nome_funcao]['parametros'])), 'exibirNaTela']

        resultado_orquestrador = self.orquestrador_interpretador_(self.dic_funcoes[nome_funcao]['bloco'])

        if not resultado_orquestrador[0]:
            return [resultado_orquestrador[0], resultado_orquestrador[1], 'exibirNaTela']

        if resultado_orquestrador[2] != 'retornarOrquestrador':
            # Sem retorno
            return [True, "", 'fazerNada']
        else:
            return [True, resultado_orquestrador[1], 'fazerNada']

    def filtrar_comando(self, linha, comando, substituicao):
        #self.log("filtrar_comando")

        for comando in self.dic_comandos[comando]["comando"]:
            linha = linha.replace(comando[0], substituicao)

        return linha

    def funcao_testar_condicao(self, linha):
        #self.log("__funcao_testar_condicao")

        linha = self.filtrar_comando(linha, "logico_maior_igual", ' >= ')
        linha = self.filtrar_comando(linha, "logico_menor_igual", ' <= ')
        linha = self.filtrar_comando(linha, "logico_diferente", ' != ')
        linha = self.filtrar_comando(linha, "logico_maior", ' > ')
        linha = self.filtrar_comando(linha, "logico_menor", ' < ')
        linha = self.filtrar_comando(linha, "logico_igual", ' == ')
        linha = self.filtrar_comando(linha, "logico_e", '  and  ')
        linha = self.filtrar_comando(linha, "logico_ou", '  or  ')

        linha = ' ' + str(linha) + ' '
        simbolos = ['>=', '<=', '!=', '>', '<', '==', '(', ')', ' and ', ' or ', ' tiver ']
        quantidade_simbolos = 0

        # Deixando todos os itens especiais com espaço em relação aos valores
        for item in simbolos:

            # Se tiver o simbolo especial na linha, some +1
            if item in linha:
                quantidade_simbolos += 1

                # Adiciona espaço para cada simbolos
                linha = linha.replace(item, '  {}  '.format(item))

        # Coreção de bugs ao usar o recurso de deixar espaços
        linha = linha.replace('* *', '**')
        linha = linha.replace('> =', '>=')
        linha = linha.replace('< =', '<=')
        linha = linha.replace('! =', '!=')

        linha = linha.replace('   tiver   ', ' tiver ')

        linha = linha.strip()
        simbolos_arrumados = [' >= ', ' <= ', ' != ', ' > ', ' < ', ' == ', ' ( ', ' ) ', ' and ', ' or ']

        # Marcar os simbolos para correta captura do regex
        for simbolo in range(len(simbolos_arrumados)):
            linha = linha.replace(
                simbolos_arrumados[simbolo], '_._' + simbolos_arrumados[simbolo] + '_._')

        linha = linha.replace('_._ < _._ =', '_._ <= _._')
        linha = linha.replace('_._ > _._ =', '_._ >= _._')

        # Usando Regex para isolar os simbolos
        anterior = 0
        final = ''

        for item in finditer("_\\._[^_]*_\\._", linha):

            # Abstrai um valor qual
            resultado = self.abstrair_valor_linha(linha[anterior:item.start()])

            if resultado[0] is False:
                return resultado

            saida = resultado[1]

            if self.verificar_tipo(resultado[1]) == 'string':
                saida = '"' + resultado[1] + '"'

            # Reover marcadores de simbolos
            final += str(saida) + linha[item.start() + 3:item.end() - 3]

            anterior = item.end()

        tem_tiver_lista = False
        resultado = self.tiver_valor_lista(linha[anterior:].strip())

        if not resultado[0]:
            return resultado

        if self.verificar_tipo(resultado[1]) == 'booleano':

            if resultado[1] == 'sim':
                final += ' True '
                tem_tiver_lista = True

            elif resultado[1] == 'nao':
                final += ' False '
                tem_tiver_lista = True

        if not tem_tiver_lista:

            resultado =self.abstrair_valor_linha(linha[anterior:])
            if not resultado[0]:
                return resultado

            saida = resultado[1]
            if self.verificar_tipo(resultado[1]) == 'string':
                saida = '"' + resultado[1] + '"'

            final += str(saida)

        # Tente fazer a condição com isso
        try:
            resutadoFinal = eval(final)

        except Exception as erro:
            return [False, "{} |{}|".format(self.msg("nao_possivel_fazer_condicao"), final),  'exibirNaTela']

        else:
            return [True, resutadoFinal, 'declararCondicional']
