import threading 
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
import os.path
import os 

import shutil

import util.funcoes as funcoes
from interpretador.mensagens import Mensagens


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
    
            Interpretador.interpretador(self, linha='[0] ............')
            Interpretador.comandos_uso_geral(self, possivelVariavel= '.................')
            Interpretador.tiver_valor_lista(self, linha='.................')
            self.compilado = True


    def analisa_inicio_codigo(self, linha):
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

            if Interpretador.analisa_inicio_codigo(self, temp) != len(temp):
                string += temp + "\n"

        return string

    def aguardar_liberacao_breakPoint(self):

        if not self.bool_ignorar_todos_breakpoints:
            self.controle_interpretador = "aguardando_breakpoint"

            while self.controle_interpretador != "":
                if self.aconteceu_erro:
                    return [False, "Interrompido", "string", "exibirNaTela"]

                sleep(0.001)

    def orq_erro(self, msg_log, linhaAnalise, dir_script_erro):

        if self.ignorar_erros:
            return "Ignorar Erro"

        self.aconteceu_erro = True

        if msg_log not in ["Erro ao iniciar o Interpretador", "indisponibilidade_terminal", "Interrompido"]:

            if not self.erro_alertado:

                self.dir_script_aju_erro = dir_script_erro
                self.mensagem_erro = msg_log
                self.linha_que_deu_erro = linhaAnalise

                self.erro_alertado = True

    def orq_exibir_tela(self, lst_retorno_ultimo_comando):
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
                return [False, "Interrompido", "string", "exibirNaTela"]
            sleep(0.000001)

    def log(self, msg_log: str) -> str:
        """ Exibe um log no terminal

        Args:
            msg_log (str): a mensagem para exibir
        """
        if self.bool_logs:
            agora = time() - self.inicio
            self.inicio = agora

            print('[{0:<15.3f}] => '.format(agora), r'{}'.format(msg_log))

    def orquestrador_interpretador_(self, txt_codigo):
        #Interpretador.log(self, '<orquestrador_interpretador_>:' + txt_codigo)

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

                    lst_analisa =Interpretador.interpretador(self, txt_linha_comando)

                    if lst_analisa[0][3] == "continuarLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, 'booleano', "continuarLoop"]

                    if lst_analisa[0][3] == "pararLoop":
                        self.numero_threads_ativos -= 1
                        return lst_analisa[0]

                    if lst_analisa[0][3] == "retornarOrquestrador":
                        self.numero_threads_ativos -= 1
                        return [True, lst_analisa[0][1], lst_analisa[0][2], "retornarOrquestrador"]

                    if lst_analisa[0][3] == 'linhaVazia': # A linha estava em branco
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
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                            return lst_ultimo_teste

                        if lst_ultimo_teste[3] == 'exibirNaTela':
                            Interpretador.orq_exibir_tela(self, lst_ultimo_teste)

                        if lst_ultimo_teste[3] in ['fazerNada', 'exibirNaTela']: # Adiciona no fluxo de dados
                            historico_fluxo_de_dados.append('acaoDiversa')

                        txt_linha_comando = ""

                        if txt_char == "\n" and lst_ultimo_teste[3] == 'fazerNada':
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
                ##Interpretador.log(self, '!<Analisa bloco salvo>:"' + str_bloco_salvo + '"')

                salvar_bloco = False

                if lst_ultimo_teste[3] == 'declararLoop':
                    historico_fluxo_de_dados.append('declararLoop') # Encaixa Loop

                    # Enquanto a condição for verdadeira
                    while lst_ultimo_teste[1]:
                        if self.aconteceu_erro:
                            return [False, "Interrompido", "string", "exibirNaTela"]


                        # Executar o bloco completo
                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[3] == "pararLoop":
                            break

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            self.numero_threads_ativos -= 1
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)

                            return lst_resultado_execucao

                        # Testar novamente a condição do loop
                        lst_ultimo_teste =Interpretador.interpretador(self, txt_comando_testado)

                        num_linha_analisada = lst_ultimo_teste[1]
                        arq_script_erro = lst_ultimo_teste[2]
                        lst_ultimo_teste = lst_ultimo_teste[0]

                        if lst_ultimo_teste[0] == False:

                            self.numero_threads_ativos -= 1
                            if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                            return lst_ultimo_teste

                        if lst_ultimo_teste[3] == "retornarOrquestrador":
                            return [True, lst_ultimo_teste[1], lst_ultimo_teste[2], "retornarOrquestrador"]

                elif lst_ultimo_teste[3] == "declararLoopRepetir":
                    historico_fluxo_de_dados.append('declararLoopRepetir') # Encaixa Loop

                    lst_ultimo_teste[3] = 'fazerNada'

                    for valor in range(0, lst_ultimo_teste[1]):
                        if self.aconteceu_erro:
                            return [False, "Interrompido", "string", "exibirNaTela"]

                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[3] == "pararLoop":
                            break

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    lst_ultimo_teste[1] = 0
                    lst_ultimo_teste = [True, False, 'booleano']

                elif lst_ultimo_teste[3] == "declararLoopParaItemString":
                    historico_fluxo_de_dados.append('declararLoopParaItemString') # Encaixa Loop

                    lst_ultimo_teste[3] = 'fazerNada'

                    variavel_string, variavel_atribuir = lst_ultimo_teste[1]

                    for valor in variavel_string[1]:
                        if self.aconteceu_erro:
                            return [False, "Interrompido", "string", "exibirNaTela"]

                        criar_variavel = Interpretador.funcao_realizar_atribu(self, variavel_atribuir, '"{}"'.format(valor))

                        if criar_variavel[0] == False:
                            self.numero_threads_ativos -= 1
                            return criar_variavel

                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[3] == "pararLoop":
                            break

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    lst_ultimo_teste[1] = 0
                    lst_ultimo_teste = [True, False, 'booleano']

                elif lst_ultimo_teste[3] == "declararLoopParaItemLista":
                    historico_fluxo_de_dados.append('declararLoopParaItemLista') # Encaixa Loop

                    lst_ultimo_teste[3] = 'fazerNada'

                    variavel_listas, variavel_atribuir = lst_ultimo_teste[1]

                    for valor in variavel_listas[1]:
                        if self.aconteceu_erro:
                            return [False, "Interrompido", "string", "exibirNaTela"]

                        if valor[1] == 'string':
                            criar_variavel = Interpretador.funcao_realizar_atribu(self, variavel_atribuir, '"{}"'.format(valor[0]))
                        elif valor[1] == 'float':
                            criar_variavel = Interpretador.funcao_realizar_atribu(self, variavel_atribuir, str(valor[0]))

                        if criar_variavel[0] == False:
                            self.numero_threads_ativos -= 1
                            return criar_variavel

                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[3] == "pararLoop":
                            break

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    lst_ultimo_teste[1] = 0
                    lst_ultimo_teste = [True, False, 'booleano']

                elif lst_ultimo_teste[3] == "declararLoopParaCada":
                    historico_fluxo_de_dados.append('declararLoopParaCada') # Encaixa Loop

                    lst_ultimo_teste[3] = 'fazerNada'

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
                            return [False, "Interrompido", "string", "exibirNaTela"]

                        criar_variavel = Interpretador.funcao_realizar_atribu(self, lst_ultimo_teste[1][0], str(valor))
                        if criar_variavel[0] == False:
                            self.numero_threads_ativos -= 1
                            return criar_variavel

                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[3] == "pararLoop":
                            break

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    lst_ultimo_teste[1] = 0
                    lst_ultimo_teste = [True, False, 'booleano']

                elif lst_ultimo_teste[3] == "declararFuncao":
                    lst_ultimo_teste[3] = "fazerNada"

                    self.dic_funcoes[lst_ultimo_teste[4]] = {'parametros':self.dic_funcoes[lst_ultimo_teste[4]]['parametros'], 'bloco':str_bloco_salvo[1:].strip()}

                elif lst_ultimo_teste[3] == 'declararCondicional':
                    historico_fluxo_de_dados.append('declararCondicional')
                    lst_ultimo_teste[3] = "fazerNada"

                    if lst_ultimo_teste[1]:
                        bool_ultimo_teste = True

                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[3] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, 'booleano', "continuarLoop"]

                        if lst_resultado_execucao[3] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, 'booleano', "pararLoop"]

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)

                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                    else:
                        bool_ultimo_teste == False

                elif lst_ultimo_teste[3] == 'declararSenaoSe':

                    if len(historico_fluxo_de_dados) == 0:
                        Interpretador.orq_erro(self, self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1

                        return [False, self.msg("precisa_def_p_cond_senao"), 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'declararCondicional':
                        Interpretador.orq_erro(self, self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1

                        return [False, self.msg("precisa_def_p_cond_senao"), 'string', "fazerNada"]

                    # Condição se ou senão anterior era falsa
                    if bool_ultimo_teste == False:

                        # Teste senão é verdadeiro
                        if lst_ultimo_teste[1]:
                            bool_ultimo_teste = True # Condição agora foi executada

                            lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                            if lst_resultado_execucao[3] == "continuarLoop":
                                self.numero_threads_ativos -= 1
                                return [True, True, 'booleano', "continuarLoop"]

                            if lst_resultado_execucao[3] == "pararLoop":
                                self.numero_threads_ativos -= 1
                                return lst_resultado_execucao

                            if lst_resultado_execucao[3] == "retornarOrquestrador":
                                self.numero_threads_ativos -= 1
                                return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                            if lst_resultado_execucao[0] == False:

                                if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                    self.numero_threads_ativos -= 1
                                    return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                                Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                                self.numero_threads_ativos -= 1
                                return lst_resultado_execucao

                # É um senao se e o teste
                elif lst_ultimo_teste[3] == 'declararSenao':

                    if len(historico_fluxo_de_dados) == 0:
                        Interpretador.orq_erro(self, self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_p_cond_senao"), 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'declararCondicional':
                        Interpretador.orq_erro(self, self.msg("precisa_def_p_cond_senao"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_p_cond_senao"), 'string', "fazerNada"]

                    # Condição se ou senão anterior era falsa
                    if bool_ultimo_teste == False:
                        bool_ultimo_teste = True # Condição agora foi executada
                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[3] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, 'booleano', "continuarLoop"]

                        if lst_resultado_execucao[3] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                # É tente algo
                elif lst_ultimo_teste[3] == 'tenteAlgo':
                    self.ignorar_erros = True
                    historico_fluxo_de_dados.append("tenteAlgo")
                    lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())

                    if lst_resultado_execucao[3] == "continuarLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, 'booleano', "continuarLoop"]

                    if lst_resultado_execucao[3] == "pararLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, 'booleano', "pararLoop"]

                    if lst_resultado_execucao[3] == "retornarOrquestrador":
                        self.numero_threads_ativos -= 1
                        return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                    bool_erro_tentar = False

                    if lst_resultado_execucao[0] == False:
                        bool_erro_tentar = True

                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            self.numero_threads_ativos -= 1
                            return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                        lst_resultado_execucao = [True, "", "linhaVazia", "fazerNada"]
                    self.ignorar_erros = False

                elif lst_ultimo_teste[3] == 'seDerErro':

                    if len(historico_fluxo_de_dados) == 0:
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), 'string', "fazerNada"]

                    # Teste deu erro
                    if bool_erro_tentar:
                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[3] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, 'booleano', "continuarLoop"]

                        if lst_resultado_execucao[3] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[3] == 'seNaoErro':

                    if len(historico_fluxo_de_dados) == 0:
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), 'string', "fazerNada"]

                    # Teste deu erro
                    if bool_erro_tentar == False:
                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[3] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, 'booleano', "continuarLoop"]

                        if lst_resultado_execucao[3] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[3] == 'seDerErro':

                    if len(historico_fluxo_de_dados) == 0:
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_der_erro"), 'string', "fazerNada"]

                    # Teste deu erro
                    if bool_erro_tentar:

                        lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                        if lst_resultado_execucao[3] == "continuarLoop":
                            self.numero_threads_ativos -= 1
                            return [True, True, 'booleano', "continuarLoop"]

                        if lst_resultado_execucao[3] == "pararLoop":
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                        if lst_resultado_execucao[3] == "retornarOrquestrador":
                            self.numero_threads_ativos -= 1
                            return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads_ativos -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads_ativos -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[3] == 'emQualquerCaso':

                    if len(historico_fluxo_de_dados) == 0:
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Interpretador.orq_erro(self, self.msg("precisa_def_tente_p_n_der_erro"), "0", "")
                        self.numero_threads_ativos -= 1
                        return [False, self.msg("precisa_def_tente_p_n_der_erro"), 'string', "fazerNada"]

                    lst_resultado_execucao = Interpretador.orquestrador_interpretador_(self, str_bloco_salvo[1:].strip())
                    if lst_resultado_execucao[3] == "continuarLoop":
                        self.numero_threads_ativos -= 1
                        return [True, True, 'booleano', "continuarLoop"]

                    if lst_resultado_execucao[3] == "pararLoop":
                        self.numero_threads_ativos -= 1
                        return lst_resultado_execucao

                    if lst_resultado_execucao[3] == "retornarOrquestrador":
                        self.numero_threads_ativos -= 1
                        return [True, lst_resultado_execucao[1], lst_resultado_execucao[2], "retornarOrquestrador"]

                    if lst_resultado_execucao[0] == False:

                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            self.numero_threads_ativos -= 1
                            return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                        Interpretador.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
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
            lst_ultimo_teste =Interpretador.interpretador(self, txt_linha_comando)

            if lst_ultimo_teste[0][3] == "continuarLoop":
                self.numero_threads_ativos -= 1
                return [True, True, 'booleano', "continuarLoop"]

            if lst_ultimo_teste[0][3] == "pararLoop":
                self.numero_threads_ativos -= 1
                return [True, True, 'booleano', "pararLoop"]

            if lst_ultimo_teste[0][3] == "retornarOrquestrador":
                self.numero_threads_ativos -= 1
                return [True, lst_ultimo_teste[0][1], lst_ultimo_teste[0][2], "retornarOrquestrador"]

            txt_comando_testado = txt_linha_comando
            num_linha_analisada = lst_ultimo_teste[1]
            arq_script_erro = lst_ultimo_teste[2]
            lst_ultimo_teste = lst_ultimo_teste[0]

            if lst_ultimo_teste[0] == False:

                self.numero_threads_ativos -= 1
                if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                    return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                Interpretador.orq_erro(self, lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                return lst_ultimo_teste

            if lst_ultimo_teste[3] == 'exibirNaTela':
                Interpretador.orq_exibir_tela(self, lst_ultimo_teste)

        # Aviso de erros de profundidade
        self.numero_threads_ativos -= 1
        if int_profundidade_bloco > 0:
            return [False, self.msg("nao_abriu_chave"), 'string', "fazerNada"]

        elif int_profundidade_bloco < 0:
            return [False, self.msg("nao_fechou_chave"), 'string', "fazerNada"]

        return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

    def analisa_instrucao(self, comando, texto, compilado):
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
        #Interpretador.log(self, '\n\ninterpretador')

        # [[False, 'indisponibilidade_terminal', 'string', 'exibirNaTela'], "0", ""]

        if self.aconteceu_erro:
            return [[False, 'Erro ao iniciar o Interpretador', 'string', 'exibirNaTela'], "0", ""]

        linha = linha.replace('\n', '')
        linha = linha.strip()

        if linha == '':
            return [[True, None, 'vazio', 'linhaVazia'], "0", ""]

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
               Interpretador.aguardar_liberacao_breakPoint(self)

            if linha == '':
                return [[True, None, 'vazio', 'linhaVazia'], "0", ""]

            caractere_inicio = linha[0]

            ##################################################################
            #                          LIMPAR A TELA                         #
            ##################################################################

            if caractere_inicio in self.dicLetras["limpatela"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<limpatela>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_limpar_o_termin(self), self.num_linha, "limpaTela"]

            ##################################################################
            #                             RETORNE                            #
            ##################################################################

            if caractere_inicio in self.dicLetras["retorne"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<retorne>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_retorne(self, instrucao_analise[1][2]), self.num_linha, ""]

            ##################################################################
            #                              LOOPS                             #
            ##################################################################

            if caractere_inicio in self.dicLetras["continue"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<continue>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_continuar(self), self.num_linha, "continue"]

            if caractere_inicio in self.dicLetras["pare"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<pare>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_parar(self), self.num_linha, "pare"]

            if caractere_inicio in self.dicLetras["interrompa"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<interrompa>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_interrompa(self), self.num_linha, "interrompa"]

            if caractere_inicio in self.dicLetras["enquanto"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<enquanto>)(.*)(<enquanto_final>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_loops_enquantox(self, instrucao_analise[1][2]), self.num_linha, "enquanto"]

            if caractere_inicio in self.dicLetras["repita"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<repita>)(.*)(<repitaVezes>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_repetir_n_vezes(self, instrucao_analise[1][2]), self.num_linha, "repetir"]

            if caractere_inicio in self.dicLetras["para_cada"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<para_cada>)__var__(<para_cada_de>)(.*)(<para_cada_ate>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_loop_para_cada_(self, instrucao_analise[1][2], instrucao_analise[1][4], instrucao_analise[1][6]), self.num_linha, "para_cada"]

            ##################################################################
            #                            EXIBIÇÃO                            #
            ##################################################################

            if caractere_inicio in self.dicLetras["mostreNessa"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<mostreNessa>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_exibir_mesma_ln(self, instrucao_analise[1][2]), self.num_linha, "exibiçãoNaTela"]

            if caractere_inicio in self.dicLetras["mostre"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<mostre>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_exibir_outra_ln(self, instrucao_analise[1][2]), self.num_linha, "exibiçãoNaTela"]

            ##################################################################
            #                             ESPERA                             #
            ##################################################################

            if caractere_inicio in self.dicLetras["aguarde"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<aguarde>)(.*)(<esperaEm>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_esperar_n_tempo(self, instrucao_analise[1][2], instrucao_analise[1][3]), self.num_linha, "esperar"]

            ##################################################################
            #                             ENTRADA                            #
            ##################################################################

            if caractere_inicio in self.dicLetras["digitado"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<digitado>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_ovalor_digitado(self, instrucao_analise[1][1]), self.num_linha, "tudo_entradas"]

            ##################################################################
            #                         NUMERO ALEATÓRIO                       #
            ##################################################################

            if caractere_inicio in self.dicLetras["aleatorio"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_numer_aleatorio(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "aleatorio"]

            ##################################################################
            #                           BIBLIOTECAS                          #
            ##################################################################

            if caractere_inicio in self.dicLetras["importe"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<importe>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_importe(self, instrucao_analise[1][2]), self.num_linha, "importe"]

            ##################################################################
            #                    TENTE EXECUTAR O COMANDO                    #
            ##################################################################

            if caractere_inicio in self.dicLetras["se_der_erro"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<se_der_erro>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_se_der_erro(self), self.num_linha, "tente"]

            if caractere_inicio in self.dicLetras["senao_der_erro"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<senao_der_erro>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_senao_der_erro(self), self.num_linha, "tente"]

            if caractere_inicio in self.dicLetras["em_qualquer_caso"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<em_qualquer_caso>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_em_qualquer_caso(self), self.num_linha, "tente"]

            if caractere_inicio in self.dicLetras["tente"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tente>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_tente(self), self.num_linha, "tente"]

            ##################################################################
            #                     MANIPULAÇÃO DE ARQUIVOS                    #
            ##################################################################

            if caractere_inicio in self.dicLetras["crie_arquivo"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<crie_arquivo>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_criar_arquivo(self, instrucao_analise[1][2]), self.num_linha, "arquivos"]

            if caractere_inicio in self.dicLetras["delete_arquivo"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<delete_arquivo>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_excluir_arquivo(self, instrucao_analise[1][2]), self.num_linha, "arquivos"]

            if caractere_inicio in self.dicLetras["arquivo_existe"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<arquivo_existe>)(.*)(<arquivo_existe_nao_sub_existe>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_arquivo_nao_existe(self, instrucao_analise[1][2]), self.num_linha, "arquivos"]

                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<arquivo_existe>)(.*)(<arquivo_existe_sub_existe>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_arquivo_existe(self, instrucao_analise[1][2]), self.num_linha, "arquivos"]

            if caractere_inicio in self.dicLetras["adicione_texto_arquivo"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<adicione_texto_arquivo>)(.*)(<adicione_texto_arquivo_sub>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_adicionar_arquivo(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "arquivos"]

            if caractere_inicio in self.dicLetras["sobrescreva_texto_arquivo"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<sobrescreva_texto_arquivo>)(.*)(<sobrescreva_texto_arquivo_sub>)(.*)(<sobrescreva_texto_arquivo_sub_sub>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_sobrescrever_arquivo(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "arquivos"]

            if caractere_inicio in self.dicLetras["leia_arquivo"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<leia_arquivo>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_ler_arquivo(self, instrucao_analise[1][2]), self.num_linha, "arquivos"]

            ##################################################################
            #                            CONDIÇÔES                           #
            ##################################################################

            if caractere_inicio in self.dicLetras["se_nao_se"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<se_nao_se>)(.*)(<se_final>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_senao_se(self, instrucao_analise[1][2]), self.num_linha, "condicionais"]

            if caractere_inicio in self.dicLetras["se_nao"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<se_nao>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_senao(self), self.num_linha, "condicionais"]

            if caractere_inicio in self.dicLetras["se"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<se>)(.*)(<se_final>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_testar_condicao(self, instrucao_analise[1][2]), self.num_linha, "condicionais"]

            ##################################################################
            #                            VARIAVEIS                           #
            ##################################################################

            instrucao_analise = Interpretador.analisa_instrucao(self, '^([a-zA-Z_0-9]*)(<declaraVariaveis>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_realizar_atribu(self, instrucao_analise[1][1], instrucao_analise[1][3]), self.num_linha, "atribuicoes"]

            if caractere_inicio in self.dicLetras["incremente"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<incremente>)(.*)(<incrementeDecremente>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_incremente_vari(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "incremente_decremente"]

            if caractere_inicio in self.dicLetras["decremente"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<decremente>)(.*)(<incrementeDecremente>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_decremente_vari(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "incremente_decremente"]

            if caractere_inicio in self.dicLetras["tipo_variavel"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tipo_variavel>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_tipo_variavel(self, instrucao_analise[1][2]), self.num_linha, ""]

            if caractere_inicio in self.dicLetras["substitua"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<substitua>)(.*)(<substitua_por>)(.*)(<substitua_na_variavel>)(\\s*[A-Z0-9a-z\\_]*\\s*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_substituir_texto(self, instrucao_analise[1][2],instrucao_analise[1][4],instrucao_analise[1][6] ), self.num_linha, ""]

            ##################################################################
            #                              LISTA                             #
            ##################################################################

            if caractere_inicio in self.dicLetras["tiverLista"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_tiver_valor_lst(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "se tiver"]

            if caractere_inicio in self.dicLetras["tamanhoDaLista"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_otamanho_da_lst(self, instrucao_analise[1][2]), self.num_linha, "listas"]

            if caractere_inicio in self.dicLetras["RemoverItensListas"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<RemoverItensListas>)(.*)(<RemoverItensListasInterno>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_rem_itns_na_lst(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

            if caractere_inicio in self.dicLetras["adicionarItensListas"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<listaNaPosicao>)(.*)(<addItensListaInternoPosicaoFinaliza>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_add_itns_lst_ps(self, instrucao_analise[1][2], instrucao_analise[1][4], instrucao_analise[1][6]), self.num_linha, "listas"]

                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoFinal>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_add_itns_na_lst(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoInicio>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_add_itns_lst_in(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInterno>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_add_itns_na_lst(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaNaPosicao>)(.*)(<recebeDeclaraListas>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_add_lst_na_posi(self, instrucao_analise[1][2], instrucao_analise[1][4], instrucao_analise[1][6]), self.num_linha, "listas"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<percorra_lista>)(.*)(<percorra_items_lista_sub>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_percorra_lista(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<percorra_items>)(.*)(<percorra_items_lista_sub>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_percorra_string(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaCom>)(.*)(<listaPosicoesCom>)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_dec_lst_posicoe(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListas>)(.*)(<recebeDeclaraListas>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_declarar_listas(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "listas"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListas>)(\\s*[a-zA-Z\\_0-9]*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_retornar_lista(self, instrucao_analise[1][2], ), self.num_linha, "listas"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)(<declaraVariaveis>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_realiza_atribuica_posicao_lista(self, instrucao_analise[1][2], instrucao_analise[1][4], instrucao_analise[1][6]), self.num_linha, "lista"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_obter_valor_lst(self, instrucao_analise[1][2], instrucao_analise[1][4]), self.num_linha, "lista"]

            ##################################################################
            #                             FUNÇÕES                            #
            ##################################################################

            if caractere_inicio in self.dicLetras["funcoes"] or not self.compilado:
                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<funcoes>)(.*)(<recebeParametros_parentese_abre>)(.*)(<recebeParametros_parentese_fecha>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_declarar_funcao(self, instrucao_analise[1][2], instrucao_analise[1][4]),self.num_linha, "funcoes"]

                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<funcoes>)(.*)(<recebeParametros>)(.*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_declarar_funcao(self, instrucao_analise[1][2], instrucao_analise[1][4]),self.num_linha, "funcoes"]

                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<funcoes>)(\\s*[\\w*\\_]*\\s*)(<recebeParametros_parentese_abre>)\\s*(<recebeParametros_parentese_fecha>)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_declarar_funcao(self, instrucao_analise[1][2]), self.num_linha, "funcoes"]

                instrucao_analise = Interpretador.analisa_instrucao(self, '^(<funcoes>)(\\s*[\\w*\\_]*\\s*)$', linha, self.compilado)
                if instrucao_analise[0]: return [Interpretador.funcao_declarar_funcao(self, instrucao_analise[1][2]), self.num_linha, "funcoes"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<passandoParametros>)(.*)$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_executar_funcao(self, instrucao_analise[1][1], instrucao_analise[1][3]), self.num_linha, "funcoes"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<passando_parametros_abrir>)(.*)(<passando_parametros_fechar>)$', linha, self.compilado)
            if instrucao_analise[0]:
                return [Interpretador.funcao_executar_funcao(self, instrucao_analise[1][1], instrucao_analise[1][3]), self.num_linha, "funcoes"]

            instrucao_analise = Interpretador.analisa_instrucao(self, '^[A-Z0-9a-z_]*\\s*$', linha, self.compilado)
            if instrucao_analise[0]: return [Interpretador.funcao_executar_funcao(self, instrucao_analise[1][1]), self.num_linha, "funcoes"]

            return [ [False, "{}'{}'".format(  self.msg('comando_desconhecido'), linha  ), 'string', 'fazerNada'], self.num_linha, ""]

        return [[True, None, 'vazio', 'fazerNada'], str(self.num_linha), ""]

    def comandos_uso_geral(self, possivelVariavel):
        #Interpretador.log(self, "comandos_uso_geral: '{}'".format(possivelVariavel))
        possivelVariavel = str(possivelVariavel).strip()

        caractere_inicio = None
        if possivelVariavel != "":
            caractere_inicio = possivelVariavel[0]

        ##################################################################
        #                            DIVERSOS                            #
        ##################################################################
        instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<na_cor>)(.*)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_na_cor(self, instrucao_analise[1][1], instrucao_analise[1][3])

        ##################################################################
        #                         NUMERO ALEATÓRIO                       #
        ##################################################################

        if caractere_inicio in self.dicLetras["aleatorio"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_numer_aleatorio(self, instrucao_analise[1][2], instrucao_analise[1][4])

        ##################################################################
        #                              LISTA                             #
        ##################################################################

        if caractere_inicio in self.dicLetras["declaraListas"] or not self.compilado:
             instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListas>)(\\s*[a-zA-Z\\_0-9]*)$', possivelVariavel, self.compilado)
             if instrucao_analise[0]: return Interpretador.funcao_retornar_lista(self, instrucao_analise[1][2])

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_obter_valor_lst(self, instrucao_analise[1][2], instrucao_analise[1][4])

        if caractere_inicio in self.dicLetras["tiverLista"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_tiver_valor_lst(self, instrucao_analise[1][2], instrucao_analise[1][4])

        if caractere_inicio in self.dicLetras["tamanhoDaLista"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_otamanho_da_lst(self, instrucao_analise[1][2])

        ##################################################################
        #                            FUNÇÔES                             #
        ##################################################################

        if caractere_inicio in self.dicLetras["passandoParametros"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<passandoParametros>)(.*)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_executar_funcao(self, instrucao_analise[1][1], instrucao_analise[1][3])

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<passando_parametros_abrir>)(.*)(<passando_parametros_fechar>)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_executar_funcao(self, instrucao_analise[1][1], instrucao_analise[1][3])


        ##################################################################
        #                             ENTRADA                            #
        ##################################################################

        if caractere_inicio in self.dicLetras["digitado"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<digitado>)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_ovalor_digitado(self, instrucao_analise[1][1])

        ##################################################################
        #                     MANIPULAÇÃO DE ARQUIVOS                    #
        ##################################################################
 
        if caractere_inicio in self.dicLetras["arquivo_existe"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<arquivo_existe>)(.*)(<arquivo_existe_nao_sub_existe>)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_arquivo_nao_existe(self, instrucao_analise[1][2])

            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<arquivo_existe>)(.*)(<arquivo_existe_sub_existe>)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_arquivo_existe(self, instrucao_analise[1][2])

        if caractere_inicio in self.dicLetras["leia_arquivo"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<leia_arquivo>)(.*)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_ler_arquivo(self, instrucao_analise[1][2])

        ##################################################################
        #                            VARIAVEIS                           #
        ##################################################################

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(\\s*[\\w*\\_]*)(<percorrer_lst_str_a_cada>)(.*)(<percorrer_lst_str_a_cada_subum>)(.*)(<percorrer_lst_str_a_cada_subdois>)(.*)(<percorrer_lst_str_a_cada_final>)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_fatiamento(self, instrucao_analise[1][1], instrucao_analise[1][3], instrucao_analise[1][5], instrucao_analise[1][7])

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(\\s*[\\w*\\_]*)(<percorrer_lst_str_ate>)(.*)(<percorrer_lst_str_ate_sub>)(.*)(<percorrer_lst_str_ate_final>)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_fatiamento(self, instrucao_analise[1][1], instrucao_analise[1][3], instrucao_analise[1][5])

        if caractere_inicio in self.dicLetras["tipo_variavel"] or not self.compilado:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tipo_variavel>)(.*)$', possivelVariavel, self.compilado)
            if instrucao_analise[0]: return Interpretador.funcao_tipo_variavel(self, instrucao_analise[1][2])

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<to_upper>)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_para_maiusculo(self, instrucao_analise[1][1])

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<to_lower>)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_para_minusculo(self, instrucao_analise[1][1])

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<to_captalize>)$', possivelVariavel, self.compilado)
        if instrucao_analise[0]: return Interpretador.funcao_para_captalize(self, instrucao_analise[1][1])

        return [True, None, 'vazio']


    def verificar_se_existe(self, arquivo_diretorio, ja_foi_abstraido = False):
        #Interpretador.log(self, "verificar_se_existe")

        if not ja_foi_abstraido:
            teste_arquivo = Interpretador.abstrair_valor_linha(self, arquivo_diretorio)
            if not teste_arquivo[0]:
                return teste_arquivo
        else:
            teste_arquivo = [True, arquivo_diretorio]

        if os.path.exists(teste_arquivo[1]):
            return [True, True, "booleano", "fazerNada"]
        return [True, False, "booleano", "fazerNada"]

    def testar_existencia(self, arquivo):
        #Interpretador.log(self, "testar_existencia")

        # Abstrair o valor do arquivo e do objetivo
        teste_arquivo = Interpretador.abstrair_valor_linha(self, arquivo)
        if not teste_arquivo[0]: return teste_arquivo

        # Verificar se o diretório e o objetivo existem
        teste_erro =  Interpretador.verificar_se_existe(self, teste_arquivo[1], ja_foi_abstraido = True)
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
                testa_entrada = Interpretador.obter_valor_variavel(self, saida)
                if not testa_entrada[0]: return testa_entrada
                saida = testa_entrada
            
            elif operacao == "teste_tipo":
                if teste == "==":
                    if saida[2] == esperado: return [False, self.msg("__LISTA__NAO_DEFINIDA__"), 'string', 'fazerNada']

                elif teste == "!=":
                    if saida[2] == esperado: return [False, self.msg("__LISTA__NAO_DEFINIDA__"), 'string', 'fazerNada']
                saida = saida

            elif operacao == "abstrair_valor_linha":
                teste_abstracao = Interpretador.abstrair_valor_linha(self, saida)
                if not teste_abstracao[0]: return teste_abstracao
                saida = teste_abstracao

            return saida


    def funcao_percorra_lista(self, variavel, variavel_atribuir):
        #Interpretador.log(self, "__funcao_percorra_lista")

        teste_variavel = Interpretador.operacoes_variaveis(self, variavel,
            pipeline = [
                ["obter_valor_variavel", "", "", ""],
                ["teste_tipo", "!=", "lista", ""]
            ]
        )
        if not teste_variavel[0]: return teste_variavel
        # variável => teste_variavel[1]

        testa_existencia = Interpretador.operacoes_variaveis(self, variavel_atribuir,
            pipeline = [
                ["obter_valor_variavel", "", "", ""]
            ]
        )
        # Variável não existe
        if not testa_existencia[0]:
            criar_variavel = Interpretador.funcao_realizar_atribu(self, variavel_atribuir, "0")

            if not criar_variavel[0]:
                return criar_variavel


        return [True, [teste_variavel, variavel_atribuir], "lista", "declararLoopParaItemLista"]


    def funcao_percorra_string(self, variavel, variavel_atribuir):
        #Interpretador.log(self, "__funcao_percorra_string")

        testa_valor = Interpretador.operacoes_variaveis(self, variavel,
            pipeline = [
                ["abstrair_valor_linha", "", "", ""],
                ["teste_tipo", "!=", "string", ""]
            ]
        )
        if not testa_valor[0]: return testa_valor
        # variável => teste_variavel[1]
        testa_existencia = Interpretador.operacoes_variaveis(self, variavel_atribuir,
            pipeline = [
                ["obter_valor_variavel", "", "", ""]
            ]
        )
        # Variável não existe
        if not testa_existencia[0]:
            criar_variavel = Interpretador.funcao_realizar_atribu(self, variavel_atribuir, "0")

            if not criar_variavel[0]:
                return criar_variavel


        return [True, [testa_valor, variavel_atribuir], "lista", "declararLoopParaItemString"]

    def funcao_substituir_texto(self, valor1, valor2, variavel):
        #Interpretador.log(self, "__funcao_substituir_texto")

        teste_variavel = Interpretador.operacoes_variaveis(self, variavel,
            pipeline = [
                ["obter_valor_variavel", "", "", ""],
                ["teste_tipo", "!=", "string", "p_usar_substituicao_variavel"]
            ]
        )
        if not teste_variavel[0]: return teste_variavel
 
        abstrairv1 = Interpretador.operacoes_variaveis(self, valor1,
            pipeline = [
                ["abstrair_valor_linha", "", "", ""],
                ["teste_tipo", "!=", "string", self.msg("p_substituir_texto_valor").format(1, 1, "__abstrairv1[2])__")]
            ]
        )
        if not abstrairv1[0]: return abstrairv1

        abstrairv2 = Interpretador.operacoes_variaveis(self, valor1,
            pipeline = [
                ["abstrair_valor_linha", "", "", ""],
                ["teste_tipo", "!=", "string", self.msg("p_substituir_texto_valor").format(1, 1, "__abstrairv2[2])__")]
            ]
        )
        if not abstrairv2[0]: return abstrairv2

        self.dic_variaveis[variavel][0] = self.dic_variaveis[variavel][0].replace(abstrairv1[1], abstrairv2[1])

        return [True, True , 'booleano', 'fazerNada']

    def funcao_limpar_o_termin(self):
        #Interpretador.log(self, "__funcao_limpar_o_termin")

        self.controle_interpretador = "limpar_tela"

        while self.controle_interpretador != "":

            if self.aconteceu_erro:
                return [False, "Interrompido", "string", "exibirNaTela"]
            sleep(0.000001)

        return [True, None, 'vazio', 'fazerNada']

    def funcao_interrompa(self):
        #Interpretador.log(self, "__funcao_interrompa")

        #Interpretador.log(self, '<funcao_interrompa>:')
        self.aconteceu_erro = True
        return [False, 'indisponibilidade_terminal', "string", "fazerNada"]


    def funcao_fatiamento(self, variavel, de, ate, cada=None):
        variavel = variavel.strip()
        #Interpretador.log(self, "__funcao_fatiamento")

        abstrair_variavel = Interpretador.obter_valor_variavel(self, variavel)
        if not abstrair_variavel[0]: return abstrair_variavel
        if abstrair_variavel[2] not in ("string", "lista"):
            return [False, self.msg("p_usar_substituicao_variavel"), 'string', 'fazerNada']

        # Obter o valor do de
        abstrair_de = Interpretador.abstrair_valor_linha(self, de)
        if not abstrair_de[0]: return abstrair_de

        if abstrair_de[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', abstrair_de[1])
    

        # Obter o valor do ate
        abstrair_ate = Interpretador.abstrair_valor_linha(self, ate)
        if not abstrair_ate[0]: return abstrair_ate

        if abstrair_ate[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', abstrair_ate[1])

        if cada is not None:
            # Obter o valor do cada
            abstrair_cada = Interpretador.abstrair_valor_linha(self, cada)
            if not abstrair_cada[0]: return abstrair_cada

            if abstrair_cada[2] != 'float':
                return Interpretador.msg_variavel_numerica(self, 'naoNumerico', abstrair_cada[1])


        de = int(abstrair_de[1])
        ate = int(abstrair_ate[1])
        if cada is not None:
            cada = int(abstrair_cada[1])
    
        if abstrair_variavel[2] == "string":
            texto = abstrair_variavel[1]
            texto_final = ""
            tamanho_string = len(texto)

            if ate > tamanho_string:
                return [False, 'O valor inicial precisa ser menor que o tamanho total do texto. O texto tem {} você digitou {}'.format(tamanho_string, ate), 'string', 'fazerNada']

            if de > tamanho_string:
                return [False, 'O valor inicial precisa ser menor que o tamanho total do texto. O texto tem {} você digitou {}'.format(tamanho_string, de), 'string', 'fazerNada']

            if ate <= 0:
                return [False, 'O final precisa ser maior do que 0. Você digitou {}'.format(ate), 'string', 'fazerNada']
            if de <= 0:
                return [False, 'O final precisa ser maior do que 0. Você digitou {}'.format(de), 'string', 'fazerNada']

            if de == ate:
                return [True, texto[ate], 'string', 'fazerNada']

            if cada is not None:
                if cada <= 0:
                    return [False, 'O final precisa ser maior do que 0. Você digitou {}'.format(cada), 'string', 'fazerNada']
            
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
            return [True, texto_final, 'string', 'fazerNada']

        return [False, "Erro, não era um dos tipos esperados!", 'string', 'fazerNada']


    def funcao_para_maiusculo(self, texto):
        #Interpretador.log(self, "__funcao_para_maiusculo")

        abstrair = Interpretador.abstrair_valor_linha(self, texto)
        if not abstrair[0]: return abstrair

        if abstrair[2] != "string":
            return [False, self.msg("p_maiusc_minusc_cap_texto").format("maiusculo")  , 'string', 'fazerNada']

        return [True, abstrair[1].upper(), "string", "fazerNada"]

    def funcao_para_minusculo(self, texto):
        #Interpretador.log(self, "__funcao_para_minusculo")

        abstrair = Interpretador.abstrair_valor_linha(self, texto)
        if not abstrair[0]: return abstrair

        if abstrair[2] != "string":
            return [False, self.msg("p_maiusc_minusc_cap_texto").format("minusculo") , 'string', 'fazerNada']

        return [True, abstrair[1].lower(), "string", "fazerNada"]

    def funcao_para_captalize(self, texto):
        #Interpretador.log(self, "__funcao_para_captalize")

        abstrair = Interpretador.abstrair_valor_linha(self, texto)
        if not abstrair[0]: return abstrair

        if abstrair[2] != "string":
            return [False,  self.msg("p_maiusc_minusc_cap_texto").format("captalização"), 'string', 'fazerNada']

        return [True, abstrair[1].capitalize(), "string", "fazerNada"]

    def funcao_retorne(self, valor):
        #Interpretador.log(self, "__funcao_retorne")

        abstrair =Interpretador.abstrair_valor_linha(self, valor)
        if not abstrair[0]: return abstrair

        return [True, abstrair[1], abstrair[2], "retornarOrquestrador"]

    def funcao_parar(self):
        #Interpretador.log(self, "__funcao_parar")

        return [True, True, "booleano", "pararLoop"]

    def funcao_continuar(self):
        #Interpretador.log(self, "__funcao_continuar")

        return [True, True, "booleano", "continuarLoop"]

    def funcao_tente(self):
        #Interpretador.log(self, "__funcao_tente")

        return [True, True, 'string', 'tenteAlgo']

    def funcao_se_der_erro(self):
        #Interpretador.log(self, "__funcao_se_der_erro")

        return [True, True, 'string', 'seDerErro']

    def funcao_senao_der_erro(self):
        #Interpretador.log(self, "__funcao_senao_der_erro")

        return [True, True, 'string', 'seNaoErro']

    def funcao_em_qualquer_caso(self):
        #Interpretador.log(self, "__funcao_em_qualquer_caso")

        return [True, True, 'string', 'emQualquerCaso']

    def funcao_senao(self):
        #Interpretador.log(self, "__funcao_senao")

        return [True, True, 'string', 'declararSenao']

    def formatar_arquivo(self, nome_arquivo):
        #Interpretador.log(self, "formatar_arquivo")

        if "/" not in nome_arquivo:
            nome_arquivo = self.diretorio_base + nome_arquivo
        else:
            if nome_arquivo[0] != '/':
                nome_arquivo = self.diretorio_base + nome_arquivo
        return nome_arquivo

    def msg_variavel_numerica(self, msg, variavel):
        #Interpretador.log(self, "msg_variavel_numerica")

        if msg == 'naoNumerico':
            return [False, self.msg("variavel_nao_numerica").format(variavel), 'string', 'exibirNaTela']

    def analisa_padrao_variavel(self, variavel):
        #Interpretador.log(self, "analisa_padrao_variavel")

        variavel = str(variavel)
        variavel = variavel.replace("_", "")  # _ também é valido
        variavel = variavel.strip()

        if len(variavel) == 0:
            return [False, self.msg("variaveis_comecar_por_letra"), "string", 'exibirNaTela']
    
        if not variavel[0].isalpha():
            return [False, self.msg("variaveis_comecar_por_letra"), "string", 'exibirNaTela']

        if not variavel.isalnum():
            return [False, self.msg("variaveis_devem_conter"), 'string', 'exibirNaTela']

        return [True, True, 'booleano']

    def verifica_se_tem(self, linha, a_buscar):
        #Interpretador.log(self, "verifica_se_tem")

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
        #Interpretador.log(self, "obter_valor_variavel:: '{}'".format(variavel))

        variavel = variavel.strip()
        variavel = variavel.replace('\n', '')

        try:
            self.dic_variaveis[variavel]
        except:
            return [False, "{} '{}'".format(self.msg("voce_precisa_definir_variavel"), variavel),
                    'string', 'fazerNada']
        else:
            return [True, self.dic_variaveis[variavel][0], self.dic_variaveis[variavel][1], 'fazerNada']

    def obter_valor_lista(self, linha):
        #Interpretador.log(self, "obter_valor_lista")

        teste = Interpretador.obter_valor_variavel(self, linha)

        if not teste[0]:
            return teste

        if teste[2] != 'lista':
            return [False, "{} {}".format(linha,self.msg("nao_e_lista")), 'string']

        return teste

    def funcao_retornar_lista(self, variavel):
        #Interpretador.log(self, "__funcao_retornar_lista")

        teste_variavel = Interpretador.obter_valor_lista(self, variavel)

        if teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        return [True, teste_variavel[1], "lista", 'fazerNada']

    def funcao_otamanho_da_lst(self, variavel):
        #Interpretador.log(self, "__funcao_otamanho_da_lst")

        variavel = variavel.strip()

        teste =Interpretador.obter_valor_lista(self, variavel)
        if not teste[0]:
            return [teste[0], teste[1], teste[2], 'exibirNaTela']

        try:
            return [True, len(self.dic_variaveis[variavel][0]), 'float', 'fazerNada']
        except Exception as erro:
            return [True, '{} {}'.format(self.msg("erro_obter_tamanho_lista"), erro), 'string',
                    'exibirNaTela']

    def funcao_ovalor_digitado(self, linha):
        #Interpretador.log(self, "__funcao_ovalor_digitado: {}".format(linha))

        self.controle_interpretador = ':input:'

        self.texto_digitado = None
        while self.controle_interpretador != "":
            if self.aconteceu_erro:
                return [False, "Interrompido", "string", "exibirNaTela"]
            sleep(0.000001)

        digitado = self.texto_digitado

        # SE FOR NUMÉRICO
        if 'numero ' in linha or 'number' in linha:
            try:
                float(digitado)
            except:
                return [False, '{} "{}"'.format(self.msg("digitou_caractere"), digitado),
                        'string', 'fazerNada']
            else:
                return [True, float(digitado), 'float', 'fazerNada']
        else:
            return [True, digitado, 'string', 'fazerNada']

    # ======== métodos altamente depdendentes ============= #
    # ======== métodos altamente depdendentes ============= #
    # ======== métodos altamente depdendentes ============= #
    # ======== métodos altamente depdendentes ============= #

    def obter_valor_string(self, string):
        #Interpretador.log(self, "obter_valor_string")

        valorFinal = ''
        anterior = 0

        for valor in finditer("""\"[^"]*\"""", string):

            abstrair =Interpretador.abstrair_valor_linha(self, string[anterior:valor.start()])
            if not abstrair[0]: return abstrair

            valorFinal = valorFinal + str(abstrair[1]) + string[valor.start() + 1:valor.end() - 1]
            anterior = valor.end()

        abstrair =Interpretador.abstrair_valor_linha(self, string[anterior:])
        if not abstrair[0]: return abstrair
        valorFinal = valorFinal + str(abstrair[1])

        return [True, valorFinal, 'string']

    def localiza_transforma_variavel(self, linha):
        #Interpretador.log(self, "localiza_transforma_variavel:{}".format(linha))

        anterior = 0
        normalizacao = 0
        linha_base = linha
        tipos_obtidos = []

        for valor in finditer(' ', linha_base):
            # ([^\w^\d^\"]{1})([a-zA-Z]{1,}[\w\d\_]*)
            palavra = linha[anterior: valor.start() + normalizacao]

            if palavra.isalnum() and palavra[0].isalpha():

                variavelDessaVez =Interpretador.abstrair_valor_linha(self, palavra)
                if not variavelDessaVez[0]: return variavelDessaVez

                tipos_obtidos.append(variavelDessaVez[2])

                if variavelDessaVez[2] == 'string':
                    # coloca "" em caso de strings
                    linha = str(linha[:anterior]) + '"'+ str(
                        variavelDessaVez[1]) + '"' + str(
                        linha[valor.start() + normalizacao:])
                else:
                    # Só adiciona o valor da variável
                    linha = str(linha[:anterior]) + str(
                        variavelDessaVez[1]) + str(
                        linha[valor.start() + normalizacao:])

                if len(palavra) < len(str(variavelDessaVez[1])):
                    normalizacao += (len(str(variavelDessaVez[1])) - len(palavra))

                elif len(palavra) > len(str(variavelDessaVez[1])):
                    normalizacao -= (len(palavra) - len(str(variavelDessaVez[1])))

            anterior = valor.end() + normalizacao
        return [True, linha, 'string']

    def fazer_contas(self, linha):
        #Interpretador.log(self, "fazer_contas:linha={}".format(linha))

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

        simbolosEspeciais = ['+', '-', '*', '/', '%', '(', ')']
        qtd_simbolos_especiais = 0

        # Deixando todos os itens especiais com espaço em relação aos valores
        for iten in simbolosEspeciais:

            if iten in linha:
                qtd_simbolos_especiais += 1

            linha = linha.replace(iten, ' {} '.format(iten))

        # Se não tiver nenhuma operação
        if qtd_simbolos_especiais == 0:

            return [False, self.msg("nao_possui_operacao_matematica"), 'string']

        # Correção de caracteres
        linha = linha.replace('*  *', '**')
        linha = linha.replace('< =', '<=')
        linha = linha.replace('> =', '>=')
        linha = linha.replace("! =", '!=')

        # Abstrai o valor de todas as variáveis
        linha =Interpretador.localiza_transforma_variavel(self, linha)

        if not linha[0]: return linha

        # Se sobrou texto
        #for caractere in linha[1]:
        #    if str(caractere).isalpha():
        #        return [False, self.msg("nao_possivel_conta_string") + str(linha[1]), 'string']

        # Tente fazer uma conta com isso

        try:
            resutadoFinal = eval(linha[1])
        except Exception as erro:

            return [False, "{} |{}|".format(self.msg("nao_possivel_fazer_conta"), linha[1]),
                    'string']
        else:
            return [True, resutadoFinal, 'float']

    def abstrair_mostre_valor(self, possivelVariavel):
        #Interpretador.log(self, "abstrair_mostre_valor")
        possivelVariavel = possivelVariavel.strip()
        if possivelVariavel == '':
            return [True, '', 'vazio', 'exibirNaTela']

        # Caso existam contas entre strings ( Formatação )
        if possivelVariavel[0] == ',':
            possivelVariavel = possivelVariavel[1:]

        # Caso existam contas entre strings ( Formatação )
        if len(possivelVariavel) > 1:
            if possivelVariavel[-1] == ',':
                possivelVariavel = possivelVariavel[0:-1]

        testa = Interpretador.verifica_se_tem(self, possivelVariavel, ",")
        if testa != []:

            listaLinhas = [possivelVariavel[: testa[0][0]], possivelVariavel[testa[0][1]:]]
            listaValores = ''

            for linha in listaLinhas:
                valor =Interpretador.abstrair_valor_linha(self, linha)

                if not valor[0]:
                    return valor

                listaValores += str(valor[1])

            return [True, listaValores, "string"]

        return Interpretador.abstrair_valor_linha(self, possivelVariavel)

    def abstrair_valor_linha(self, possivelVariavel):
        #Interpretador.log(self, "abstrair_valor_linha: possivelVariavel = '{}'".format(possivelVariavel))

        possivelVariavel = str(possivelVariavel).strip()

        if possivelVariavel == '':
            return [True, "", "vazio", "fazerNada"]

        # Caso existam contas entre strings ( Formatação )
        if possivelVariavel[0] == ',':
            possivelVariavel = possivelVariavel[1:]

        # Caso existam contas entre strings ( Formatação )
        if len(possivelVariavel) > 1:
            if possivelVariavel[-1] == ',':
                possivelVariavel = possivelVariavel[0:-1]

        testa = Interpretador.verifica_se_tem(self, possivelVariavel, ",")
        if testa != []:

            listaLinhas = [possivelVariavel[: testa[0][0]], possivelVariavel[testa[0][1]:]]
            listaValores = ''

            for linha in listaLinhas:
                valor =Interpretador.abstrair_valor_linha(self, linha)

                if not valor[0]:
                    return valor

                listaValores += str(valor[1])

            return [True, listaValores, "string"]

        # Sem dados
        if possivelVariavel == '':
            return [True, '', 'string']

        # Sem dados
        if possivelVariavel[-1] == ',':
            possivelVariavel = possivelVariavel[:-1]

        # Sem dados
        if possivelVariavel == '':
            return [True, '', 'string']

        # Valor Booleando
        if possivelVariavel.lower() in [comando[0] for comando in self.dic_comandos["logico_true"]["comando"]]:
            return [True, 'True', 'booleano']

        if possivelVariavel.lower() in [comando[0] for comando in self.dic_comandos["logico_false"]["comando"]]:
            return [True, 'False', 'booleano']

        if possivelVariavel[0] == '"':
            if len(possivelVariavel) > 1:
                pos = possivelVariavel[1:].find('"')
                if pos != -1:
                    if pos+1 == len(possivelVariavel)-1:
                        return [True, possivelVariavel[1:-1], 'string']

        # Tentar fazer Contas
        resultado =Interpretador.fazer_contas(self, possivelVariavel)
        if resultado[0]: return resultado

        # Aplicação de possíveis comandos internos
        resultado = Interpretador.comandos_uso_geral(self, possivelVariavel)

        # Se estourar um erro e com valor
        if resultado[0] and resultado[1] != None:
            return resultado

        # Se não estourar erro, obtenção do valor foi bem sucedida
        elif not resultado[0]:
            return resultado

        # Verificando se tem strings dentro do comando
        testa = Interpretador.verifica_se_tem(self, possivelVariavel, '"')
        if testa != []:
            # Isola Strings de variáveis
            return Interpretador.obter_valor_string(self, possivelVariavel)

        # Tentar converter o valor para número
        try:
            numero = float(possivelVariavel)
        except:

            # Então o valor deve ser uma variável
            return Interpretador.obter_valor_variavel(self, possivelVariavel)

        else:
            return [True, numero, 'float']

    # ======== fim métodos altamente depdendentes ============= #
    # ======== fim métodos altamente depdendentes ============= #
    # ======== fim métodos altamente depdendentes ============= #
    # ======== fim métodos altamente depdendentes ============= #

    def funcao_importe(self, biblioteca):
        #Interpretador.log(self, "__funcao_importe: biblioteca = '{}'".format(biblioteca))

        biblioteca = Interpretador.formatar_arquivo(self, biblioteca.lower()) + str(".safira")

        # Tenta abrir o texto da biblioteca
        teste = funcoes.abrir_arquivo(biblioteca)
        if teste[0] == None:
            return [False, self.msg("erro_abrir_biblioteca").format(biblioteca, teste[1]), "string", "fazerNada"]

        # Carrega a biblioteca
        resultadoOrquestrador =Interpretador.orquestrador_interpretador_(self, teste[0])

        if resultadoOrquestrador[0] == False:
            return resultadoOrquestrador

        return [True, None, 'vazio', 'fazerNada']

    def funcao_tipo_variavel(self, variavel):
        #Interpretador.log(self, "__funcao_tipo_variavel")

        resultado =Interpretador.abstrair_valor_linha(self, variavel)

        if not resultado[0]:
            return resultado

        resultado[1] = str(resultado[1]).replace("\\n", "\n")
        return [resultado[0], resultado[2], resultado[2], 'exibirNaTela']

    # =================== ARQUIVOS =================== #
    def funcao_ler_arquivo(self, nome_arquivo):
        #Interpretador.log(self, "__funcao_ler_arquivo")

        teste_valor_arquivo =Interpretador.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor_arquivo[0] == False: return teste_valor_arquivo

        if teste_valor_arquivo[1] == "":
            return [False, self.msg("precisa_nome_arquivo"), 'string', ' exibirNaTela']

        nome_arquivo = str(teste_valor_arquivo[1])
        nome_arquivo = Interpretador.formatar_arquivo(self, nome_arquivo)

        if os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "r")
                texto = f.read()
                f.close()

            except Exception as e:
                return [False, self.msg("erro_abrir_arquivo").format(nome_arquivo, e), 'string',
                        ' exibirNaTela']
            else:
                return [True, str(texto), "string", "fazerNada"]
            return [True, True, "booleano", "fazerNada"]

        return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), 'string', ' exibirNaTela']

    def funcao_sobrescrever_arquivo(self, texto, nome_arquivo):
        #Interpretador.log(self, "__funcao_sobrescrever_arquivo")

        teste_valor_arquivo =Interpretador.abstrair_valor_linha(self, nome_arquivo)
        teste_valor_texto =Interpretador.abstrair_valor_linha(self, texto)

        if teste_valor_arquivo[0] == False: return teste_valor_arquivo
        if teste_valor_texto[0] == False: return teste_valor_texto

        if teste_valor_arquivo[1] == "":
            return [False, self.msg("precisa_nome_arquivo"), 'string', ' exibirNaTela']

        nome_arquivo = str(teste_valor_arquivo[1])
        nome_arquivo = Interpretador.formatar_arquivo(self, nome_arquivo)
        texto = str(teste_valor_texto[1])
        texto = texto.replace("\\n", "\n")

        if os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "w", encoding="utf8")
                f.write(texto)
                f.close()

            except Exception as e:
                return [False,
                        self.msg("erro_adicionar_texto_arquivo").format(texto, nome_arquivo, e),
                        'string', ' exibirNaTela']

            return [True, True, "booleano", "fazerNada"]
        return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), 'string', ' exibirNaTela']

    def funcao_adicionar_arquivo(self, texto, nome_arquivo):
        #Interpretador.log(self, "__funcao_adicionar_arquivo")

        teste_valor_arquivo =Interpretador.abstrair_valor_linha(self, nome_arquivo)
        teste_valor_texto =Interpretador.abstrair_valor_linha(self, texto)

        if teste_valor_arquivo[0] == False: return teste_valor_arquivo
        if teste_valor_texto[0] == False: return teste_valor_texto

        if teste_valor_arquivo[1] == "":
            return [False, self.msg("precisa_nome_arquivo"), 'string', ' exibirNaTela']

        nome_arquivo = str(teste_valor_arquivo[1])
        nome_arquivo = Interpretador.formatar_arquivo(self, nome_arquivo)

        texto = str(teste_valor_texto[1])
        texto = texto.replace("\\n", "\n")

        if os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "a", encoding="utf8")
                f.write(texto)
                f.close()

            except Exception as e:
                return [False,  self.msg("erro_adicionar_texto_arquivo").format(texto, nome_arquivo, e), 'string', ' exibirNaTela']
            return [True, True, "booleano", "fazerNada"]
        return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), 'string', ' exibirNaTela']

    def funcao_listar_arquivos(self, nome_diretorio):
        #Interpretador.log(self, "__funcao_listar_arquivos")

        if nome_diretorio == "":
            return [False, self.msg("precisa_nome_diretorio"), 'string', ' exibirNaTela']

        teste_valor =Interpretador.abstrair_valor_linha(self, nome_diretorio)
        if teste_valor[0] == False: return teste_valor

        nome_diretorio = str(teste_valor[1])
        nome_diretorio = Interpretador.formatar_arquivo(self, nome_diretorio)
        teste_diretorio = Interpretador.funcao_diretorio_existe(self, '"{}"'.format(nome_diretorio))
        if not teste_diretorio[0]:
            return teste_diretorio

        if not teste_diretorio[1]:
            return [False, self.msg('diretório_não_existe').format(nome_diretorio), 'string', 'fazerNada']

        lista_retorno = listdir(nome_diretorio)
        lista_resultado = [[x, "string"] for x in lista_retorno]

        return [True, lista_resultado, "lista", "fazerNada"]

    def funcao_diretorio_existe(self, nome_diretorio):
        #Interpretador.log(self, "__funcao_diretorio_existe")

        if nome_diretorio == "":
            return [False, self.msg("precisa_nome_diretorio"), 'string', ' exibirNaTela']

        teste_valor =Interpretador.abstrair_valor_linha(self, nome_diretorio)
        if teste_valor[0] == False: return teste_valor

        nome_diretorio = str(teste_valor[1])
        nome_diretorio = Interpretador.formatar_arquivo(self, nome_diretorio)

        if os.path.exists(nome_diretorio):
            return [True, True, "booleano", "fazerNada"]
        else:
            return [True, False, "booleano", "fazerNada"]

    def funcao_diretorio_nao_existe(self, nome_diretorio):
        #Interpretador.log(self, "__funcao_diretorio_nao_existe")

        if nome_diretorio == "":
            return [False, self.msg("precisa_nome_diretorio"), 'string', ' exibirNaTela']

        teste_valor =Interpretador.abstrair_valor_linha(self, nome_diretorio)
        if teste_valor[0] == False: return teste_valor

        nome_diretorio = str(teste_valor[1])
        nome_diretorio = Interpretador.formatar_arquivo(self, nome_diretorio)

        if os.path.exists(nome_diretorio):
            return [True, False, "booleano", "fazerNada"]
        else:
            return [True, True, "booleano", "fazerNada"]

    # Precisa disferenciar diretório de arquivo
    def funcao_arquivo_existe(self, nome_arquivo):
        #Interpretador.log(self, "__funcao_arquivo_existe")

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), 'string', ' exibirNaTela']

        teste_valor =Interpretador.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = Interpretador.formatar_arquivo(self, nome_arquivo)

        if os.path.exists(nome_arquivo):
            return [True, True, "booleano", "fazerNada"]
        else:
            return [True, False, "booleano", "fazerNada"]

    def funcao_arquivo_nao_existe(self, nome_arquivo):
        #Interpretador.log(self, "__funcao_arquivo_nao_existe"+ nome_arquivo)

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), 'string', ' exibirNaTela']

        teste_valor =Interpretador.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = Interpretador.formatar_arquivo(self, nome_arquivo)

        if os.path.exists(nome_arquivo):
            return [True, False, "booleano", "fazerNada"]
        else:
            return [True, True, "booleano", "fazerNada"]

    def funcao_excluir_arquivo(self, nome_arquivo: str) -> list:
        """ Recebe um diretóirio e exclui um arquivo

        Args:
            nome_arquivo (str): diretório e o arquivo, exemplo: /home/gabriel/ola.txt
                                ele também pode passar um arquivo que esteja no mesmo
                                caminho relativo do script.

        Returns:
            list: [sucesso: bool, mensagem: str, tipo_mensagem: str, acao: str]
        """

        #Interpretador.log(self, "__funcao_excluir_arquivo")

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), 'string', ' exibirNaTela']

        teste_valor =Interpretador.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = Interpretador.formatar_arquivo(self, nome_arquivo)

        try:
            os.remove(nome_arquivo)
        except FileNotFoundError:
            return [False, self.msg("arquivo_nao_existe").format(nome_arquivo), 'string', ' exibirNaTela']
        except Exception as erro:
            return [False, self.msg("erro_deletar_arquivo").format(erro), 'string', ' exibirNaTela']
        else:
            return [True, "", "vazio", "fazerNada"]
            

    def funcao_criar_arquivo(self, nome_arquivo):
        #Interpretador.log(self, "__funcao_criar_arquivo")

        if nome_arquivo == "":
            return [False, self.msg("precisa_nome_arquivo"), 'string', ' exibirNaTela']

        teste_valor =Interpretador.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])
        nome_arquivo = Interpretador.formatar_arquivo(self, nome_arquivo)

        if not os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "w", encoding='utf8')
                f.write("")
                f.close()

            except Exception as erro:
                return [False, self.msg("erro_criar_arquivo").format(erro), 'string', ' exibirNaTela']

        return [True, "", "vazio", "fazerNada"]

    def funcao_incremente_vari(self, valor, variavel):
        #Interpretador.log(self, "__funcao_incremente_vari")

        return Interpretador.incremente_decremente(self, valor, variavel, 'incremente')

    def funcao_decremente_vari(self, valor, variavel):
        #Interpretador.log(self, "__funcao_decremente_vari")

        return Interpretador.incremente_decremente(self, valor, variavel, 'decremente')

    def incremente_decremente(self, valor, variavel, acao):
        #Interpretador.log(self, "incremente_decremente")

        teste_exist =Interpretador.obter_valor_variavel(self, variavel)
        teste_valor =Interpretador.abstrair_valor_linha(self, valor)

        if teste_exist[0] == False: return teste_exist
        if teste_valor[0] == False: return teste_valor

        if teste_exist[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', variavel)

        if teste_valor[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', teste_valor[1])

        if acao == "incremente":
            self.dic_variaveis[variavel][0] = self.dic_variaveis[variavel][0] + teste_valor[1]

        else:
            self.dic_variaveis[variavel][0] = self.dic_variaveis[variavel][0] - teste_valor[1]

        return [True, True, "booleano", "fazerNada"]

    def teste_generico_lista(self, variavel, valor):
        #Interpretador.log(self, "teste_generico_lista")

        if variavel == '' or valor == '':
            return [False,self.msg("variavel_valor_nao_informado"), 'exibirNaTela']

        teste_variavel = Interpretador.obter_valor_lista(self, variavel)
        teste_valor = Interpretador.abstrair_valor_linha(self, valor)

        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if not teste_valor[0]:
            return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

        return [True, teste_variavel, teste_valor]

    def funcao_rem_itns_na_lst(self, valor, variavel):
        #Interpretador.log(self, "__funcao_rem_itns_na_lst")

        teste_generico = Interpretador.teste_generico_lista(self, variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        try:
            self.dic_variaveis[variavel][0].remove([teste_valor[1], teste_valor[2]])
        except Exception as erro:
            return [False, '"{}" {} "{}"!'.format(teste_valor[1],self.msg("nao_esta_na_lista"), variavel), 'string', 'exibirNaTela']
        return [True, None, 'vazio', 'fazerNada']

    def funcao_add_itns_na_lst(self, valor, variavel):
        #Interpretador.log(self, "__funcao_add_itns_na_lst")

        teste_generico = Interpretador.teste_generico_lista(self, variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        try:
            self.dic_variaveis[variavel][0].append([teste_valor[1], teste_valor[2]])
        except Exception as erro:
            return [False, '"{}" {} "{}"!'.format(teste_valor[1],self.msg("nao_esta_na_lista"),
                                                  variavel), 'string', 'exibirNaTela']
        return [True, None, 'vazio', 'fazerNada']

    def funcao_add_itns_lst_in(self, valor, variavel):
        #Interpretador.log(self, "__funcao_add_itns_lst_in")

        teste_generico = Interpretador.teste_generico_lista(self, variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        self.dic_variaveis[variavel][0].insert(0, [teste_valor[1], teste_valor[2]])
        return [True, None, 'vazio', 'fazerNada']

    def funcao_add_itns_lst_ps(self, valor, posicao, variavel):
        #Interpretador.log(self, "__funcao_add_itns_lst_ps")

        if variavel == '' or valor == '':
            return [False, self.msg("necessario_informar_variavel_valor") ]

        teste_generico = Interpretador.teste_generico_lista(self, variavel, valor)
        if not teste_generico[0]:
            return teste_generico

        teste_variavel = teste_generico[1]
        teste_valor = teste_generico[2]

        teste_posicao =Interpretador.abstrair_valor_linha(self, posicao)
        if not teste_posicao[0]: return [teste_posicao[0], teste_posicao[1], teste_posicao[2], 'exibirNaTela']

        if teste_posicao[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', teste_posicao[1])

        posicao = int(teste_posicao[1])

        if posicao - 1 > len(self.dic_variaveis[variavel][0]):
            return [False,self.msg("posicao_maior_limite_lista"), 'string', 'exibirNaTela']

        if posicao < 1:
            return [False,self.msg("posicao_menor_limite_lista"), 'string', 'exibirNaTela']

        self.dic_variaveis[variavel][0].insert(posicao - 1, [teste_valor[1], teste_valor[2]])
        return [True, True, 'booleano', 'fazerNada']

    # ============ mostre ==================#
    def funcao_exibir_outra_ln(self, linha):
        #Interpretador.log(self, "__funcao_exibir_outra_ln: {}".format(linha))

        resultado = Interpretador.abstrair_mostre_valor(self, linha)

        if not resultado[0]:
            return resultado

        resultado[1] = str(resultado[1]).replace("\\n", "\n")

        if len(resultado) > 3:
            if "exibirCor" in resultado[3]:
                return [resultado[0], ':mostreLinha:{}'.format(resultado[3]) + str(resultado[1]), resultado[2], 'exibirNaTela']
        return [resultado[0], ':mostreLinha:::' + str(resultado[1]), resultado[2], 'exibirNaTela']


    def funcao_exibir_mesma_ln(self, linha):
        #Interpretador.log(self, "__funcao_exibir_mesma_ln: {}".format(linha))

        resultado = Interpretador.abstrair_mostre_valor(self, linha)

        if not resultado[0]:
            return resultado

        resultado[1] = str(resultado[1]).replace("\\n", "\n")

        if len(resultado) > 3:
            if "exibirCor" in resultado[3]:
                return [resultado[0], ':nessaLinha:{}'.format(resultado[3]) + str(resultado[1]), resultado[2], 'exibirNaTela']
        return [resultado[0], ':nessaLinha:::' + str(resultado[1]), resultado[2], 'exibirNaTela']

    def funcao_na_cor(self, linha, cor):
        #Interpretador.log(self, "___funcao_na_cor: linha={}, cor={}".format(linha, cor))

        teste_linha = Interpretador.abstrair_valor_linha(self, linha)
        if not teste_linha[0]:
            return teste_linha

        teste_cor = Interpretador.abstrair_valor_linha(self, cor)
        if not teste_cor[0]:
            return teste_cor

        return [True, teste_linha[1], teste_linha[2], "exibirCor:{}:".format(teste_cor[1])]



    def funcao_esperar_n_tempo(self, tempo, tipo_espera):
        #Interpretador.log(self, "__funcao_esperar_n_tempo: tempo = '{}', espera = '{}'".format(tempo, tipo_espera))

        resultado =Interpretador.abstrair_valor_linha(self, tempo)
        if not resultado[0]: return resultado

        if tipo_espera in [comando[0].strip() for comando in self.dic_comandos['esperaEmSegundos']['comando']]:
            sleep(resultado[1])

        elif tipo_espera in [ comando[0].strip() for comando in self.dic_comandos['esperaEmMs']['comando']]:
            sleep(resultado[1] / 1000)

        return [True, None, 'vazio', 'fazerNada']

    def tiver_valor_lista(self, linha):
        #Interpretador.log(self, "tiver_valor_lista")

        linha = linha.strip()

        instrucao_analise = Interpretador.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha, self.compilado)
        if instrucao_analise[0]:
            return Interpretador.funcao_tiver_valor_lst(self, instrucao_analise[1][2], instrucao_analise[1][4])

        return [True, None, 'booleano']

    def funcao_senao_se(self, condicao):
        #Interpretador.log(self, "__funcao_senao_se")

        resultado =Interpretador.funcao_testar_condicao(self, condicao)
        return [resultado[0], resultado[1], resultado[2], 'declararSenaoSe']

    def funcao_loops_enquantox(self, linha):
        #Interpretador.log(self, "__funcao_loops_enquantox")

        resultado =Interpretador.funcao_testar_condicao(self, linha)
        return [resultado[0], resultado[1], resultado[2], 'declararLoop']

    def funcao_loop_para_cada_(self, variavel, inicio, fim):
        #Interpretador.log(self, "__funcao_loop_para_cada_")

        teste_exist =Interpretador.obter_valor_variavel(self, variavel)
        teste_valorI =Interpretador.abstrair_valor_linha(self, inicio)
        teste_valorF =Interpretador.abstrair_valor_linha(self, fim)

        if teste_valorI[0] == False:
            return teste_valorI

        if teste_valorF[0] == False:
            return teste_valorF

        if teste_valorI[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', teste_valorI[1])

        if teste_valorF[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', teste_valorF[1])

        # Variável não existe
        if teste_exist[0] == False:
            criar_variavel = Interpretador.funcao_realizar_atribu(self, variavel, '0')

            if not criar_variavel[0]:
                return criar_variavel
        passo = 1

        if (int(teste_valorI[1]) > int(teste_valorF[1])):
            passo = -1

        return [True, [variavel, int(teste_valorI[1]), int(teste_valorF[1]), passo], "lista", "declararLoopParaCada"]

    def funcao_add_lst_na_posi(self, variavelLista, posicao, valor):
        #Interpretador.log(self, "__funcao_add_lst_na_posi")

        if variavelLista == '' or posicao == '' or valor == '':  # Veio sem dados
            return [False, self.msg('add_lst_posicao_separador'), 'string', ' exibirNaTela']

        teste_exist =Interpretador.obter_valor_variavel(self, variavelLista)
        teste_posic =Interpretador.abstrair_valor_linha(self, posicao)
        teste_valor =Interpretador.abstrair_valor_linha(self, valor)

        if not teste_exist[0]:
            return teste_exist

        if not teste_posic[0]:
            return teste_posic

        if not teste_valor[0]:
            return teste_valor

        if teste_exist[2] != 'lista':
            return [False, '{} {}'.format(variavelLista,self.msg("nao_e_lista")), 'string']

        if teste_posic[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', teste_posic[1])

        posicao = int(teste_posic[1])

        # Posição estoura posições da lista
        if posicao - 1 > len(self.dic_variaveis[variavelLista][0]):
            return [False, '{} {}'.format(self.msg("posicao_maior_limite_lista"),'string', posicao),
                    'string', 'exibirNaTela']

        if posicao < 1:
            return [False, '{} {}'.format(self.msg("posicao_menor_limite_lista"), 'string', posicao),
                    'string', 'exibirNaTela']

        self.dic_variaveis[variavelLista][0][posicao - 1] = [ teste_valor[1], teste_valor[2] ]
        return [True, True, 'booleano', 'fazerNada']

    def funcao_obter_valor_lst(self, variavel, posicao):
        #Interpretador.log(self, "__funcao_obter_valor_lst")

        #Interpretador.log(self, '<funcao_obter_valor_lst>:')
        if variavel == '' or posicao == '':
            return [False, self.msg("variavel_posicao_nao_informada"), 'string', 'exibirNaTela']

        teste_posicao = Interpretador.abstrair_valor_linha(self, posicao)
        teste_variavel = Interpretador.obter_valor_lista(self, variavel)

        if not teste_posicao[0]:
            return [teste_posicao[0], teste_posicao[1], teste_posicao[2], 'exibirNaTela']

        elif teste_posicao[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', teste_posicao[1])

        elif teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        posicao = int(teste_posicao[1])
        resultado = teste_variavel[1]

        if posicao < 1:
            return [False, self.msg("posicao_menor_limite_lista"),'string', 'exibirNaTela']

        if len(resultado) < posicao:
            return [False, self.msg("posicao_maior_limite_lista"),'string', 'exibirNaTela']

        return [True, resultado[posicao - 1][0], resultado[posicao - 1][1], 'exibirNaTela']

    def funcao_tiver_valor_lst(self, valor, variavel):
        #Interpretador.log(self, "__funcao_tiver_valor_lst")

        if variavel == '' or valor == '':
            return [False, self.msg("variavel_valor_nao_informado"), 'exibirNaTela']

        teste_variavel =Interpretador.obter_valor_variavel(self, variavel)
        resultado_valor =Interpretador.abstrair_valor_linha(self, valor)

        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if teste_variavel[2] != 'lista':
            return [False, '{} {}'.format(teste_variavel[1], self.msg("nao_e_lista")), 'string', 'exibirNaTela']

        if not resultado_valor[0]:
            return [resultado_valor[0], resultado_valor[1], resultado_valor[2], 'exibirNaTela']

        if [resultado_valor[1], resultado_valor[2]] in self.dic_variaveis[variavel][0]:
            return [True, True, 'booleano', 'fazerNada']
        return [True, False, 'booleano', 'fazerNada']

    def funcao_dec_lst_posicoe(self, variavel, posicoes):
        #Interpretador.log(self, "__funcao_dec_lst_posicoe")

        #Interpretador.log(self, '<funcao_dec_lst_posicoe>:')
        teste =Interpretador.analisa_padrao_variavel(self, variavel)
        resultado =Interpretador.abstrair_valor_linha(self, posicoes)

        if not teste[0]:
            return teste

        if not resultado[0]:
            return resultado

        if resultado[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', resultado[1])

        listaItensDeclarar = []
        for posicao in range(int(posicoes)):
            listaItensDeclarar.append(['', 'string'])

        self.dic_variaveis[variavel] = [listaItensDeclarar, 'lista']
        return [True, None, 'vazio', 'fazerNada']

    def funcao_repetir_n_vezes(self, linha):
        #Interpretador.log(self, "__funcao_repetir_n_vezes")

        linha = linha.replace('vezes', '')
        linha = linha.replace('vez', '')
        linha = linha.replace('times', '')
        linha = linha.replace('veces', '')

        linha = linha.strip()
        linha =Interpretador.abstrair_valor_linha(self, linha)

        if not linha[0]:
            return [linha[0], linha[1], linha[2], 'exibirNaTela']

        if linha[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', linha[1])

        try:
            int(linha[1])
        except:
            return [False, '{} "{}"'.format(self.msg("repetir_nao_informou_inteiro"), linha[1]),
                    'string', 'exibirNaTela']
        else:
            funcao_repita = int(linha[1])
            return [True, funcao_repita, 'float', 'declararLoopRepetir']

    def funcao_numer_aleatorio(self, num1, num2):
        #Interpretador.log(self, "__funcao_numer_aleatorio: num1 = '{}', num2 = '{}'".format(num1, num2))

        num1 =Interpretador.abstrair_valor_linha(self, num1)
        num2 =Interpretador.abstrair_valor_linha(self, num2)

        if not num1[0]: return num1
        if not num2[0]: return num2

        try:
            int(num1[1])
        except:
            return [False, self.msg("aleatorio_valor1_nao_numerico"), 'string', 'exibirNaTela']

        try:
            int(num2[1])
        except:
            return [False, self.msg("aleatorio_valor2_nao_numerico"), 'string', 'exibirNaTela']

        n1 = int(num1[1])
        n2 = int(num2[1])

        if n1 == n2:
            return [False, self.msg("aleatorio_valor1_igual_valo2"), 'string', 'exibirNaTela']

        elif n1 > n2:
            return [False, self.msg("aleatorio_valor1_maior_valo2"), 'string', 'exibirNaTela']

        return [True, randint(n1, n2), 'float', 'fazerNada']

    def funcao_realizar_atribu(self, variavel, valor):
        #Interpretador.log(self, "__funcao_realizar_atribu: variavel = '{}', valor='{}'".format(variavel, valor))

        if variavel == '' or valor == '':
            return [False,self.msg("variavel_valor_nao_informado"), 'string', 'exibirNaTela']

        teste_padrao =Interpretador.analisa_padrao_variavel(self, variavel)
        if not teste_padrao[0]:
            return teste_padrao

        valor = valor.replace('\n', '')
        valor = valor.strip()

        resultado =Interpretador.abstrair_valor_linha(self, valor)
        if not resultado[0]: return resultado

        if resultado[0]:
            self.dic_variaveis[variavel] = [resultado[1], resultado[2]]
            return [True, None, 'vazio', 'fazerNada']

        return [resultado[0], resultado[1], resultado[2], 'fazerNada']

    def funcao_realiza_atribuica_posicao_lista(self, variavel, posicao, itens):
        #Interpretador.log(self, "__funcao_realiza_atribuica_posicao_lista")

        variavel = variavel.strip()
        posicao = posicao.strip()
        itens = itens.strip()

        if itens == '' or variavel == '' or posicao == '':
            return [False,self.msg("variavel_posicao_nao_informada"), 'string', 'exibirNaTela']

        teste_variavel = Interpretador.obter_valor_variavel(self, variavel)
        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if teste_variavel[2] != 'lista':
            return [False, '{} {}'.format(teste_variavel[1], self.msg("nao_e_lista")), 'string', 'exibirNaTela']

        resultado_posicao = Interpretador.abstrair_valor_linha(self, posicao)
        if not resultado_posicao[0]:
            return resultado_posicao
        if resultado_posicao[2] != 'float':
            return Interpretador.msg_variavel_numerica(self, 'naoNumerico', linha[1])

        tamanho_lista = Interpretador.funcao_otamanho_da_lst(self, variavel)
        if not tamanho_lista[0]:
            return tamanho_lista

        # Verifica se estorou o limite da lista
        if resultado_posicao[1] > tamanho_lista[1]:
            return [False,self.msg("posicao_maior_limite_lista"), 'string', 'exibirNaTela']

        if resultado_posicao[1] < 1:
            return [False,self.msg("posicao_menor_limite_lista"), 'string', 'exibirNaTela']

        resultado_itens = Interpretador.abstrair_valor_linha(self, itens)
        if not resultado_itens[0]: return resultado_itens

        self.dic_variaveis[variavel][0][int(resultado_posicao[1]) - 1] = [resultado_itens[1], resultado_itens[2]]
        return [True, None, 'vazio', 'fazerNada']

    # ========== FUNÇÔES GRANDES ======================= #

    def funcao_declarar_listas(self, variavel, itens):
        #Interpretador.log(self, "__funcao_declarar_listas")

        if itens == '' or variavel == '':
            return [False,self.msg("variavel_posicao_nao_informada"), 'string', 'exibirNaTela']

        variavel = variavel.strip()

        teste =Interpretador.analisa_padrao_variavel(self, variavel)
        testa =Interpretador.verifica_se_tem(self, itens, ', ')

        if not teste[0]: return teste

        if testa != []:
            listaItens = []
            anterior = 0

            for valorItem in testa:
                if len(itens[anterior: valorItem[0]]) > 0:
                    listaItens.append(itens[anterior: valorItem[0]])

                anterior = valorItem[1]

            if len(itens[anterior:]) > 0:
                listaItens.append(itens[anterior:])

            listaItensDeclarar = []

            for item in listaItens:
                obterValor =Interpretador.abstrair_valor_linha(self, item)

                if obterValor[0] == False:
                    return [obterValor[0], obterValor[1], obterValor[2], 'exibirNaTela']

                listaItensDeclarar.append([obterValor[1], obterValor[2]])

            self.dic_variaveis[variavel] = [listaItensDeclarar, 'lista']
            return [True, None, 'vazio', 'fazerNada']

        else:
            obterValor =Interpretador.abstrair_valor_linha(self, itens)
            if obterValor[0] == False:
                return [obterValor[0], obterValor[1], obterValor[2], 'exibirNaTela']

            lista = []
            lista.append([obterValor[1], obterValor[2]])

            self.dic_variaveis[variavel] = [lista, 'lista']
            return [True, None, 'vazio', 'fazerNada']

    def funcao_declarar_funcao(self, nomeDaFuncao, parametros=None):
        #Interpretador.log(self, "__funcao_declarar_funcao: nomeDaFuncao = '{}', parametros = '{}'".format(nomeDaFuncao, parametros))

        if parametros is not None:
            if parametros.strip() == "":
                parametros = None

        # Se o nome da função não está no padrão
        teste =Interpretador.analisa_padrao_variavel(self, nomeDaFuncao)
        if not teste[0]:
            return teste

        # Se não tem parâmetros
        if parametros is None:
            self.dic_funcoes[nomeDaFuncao] = {'parametros': None, 'bloco': 'bloco'}

            return [True, True, 'booleano', 'declararFuncao', nomeDaFuncao]

        # Verifica se tem mais de um parâmetro
        testa =Interpretador.verifica_se_tem(self, parametros, ', ')

        # Tem mais de um parametro
        if testa != []:
            listaParametros = []
            anterior = 0

            for valorItem in testa:
                if parametros[anterior: valorItem[0]]:
                    listaParametros.append(parametros[anterior: valorItem[0]])

                anterior = valorItem[1]

            if len(parametros[anterior:]) > 0:
                listaParametros.append(parametros[anterior:])

            listaFinalDeParametros = []
            for parametro in listaParametros:
                listaFinalDeParametros.append(parametro.strip())

                teste =Interpretador.analisa_padrao_variavel(self, parametro.strip())
                if not teste[0]: return teste

            # Adicionar Função
            self.dic_funcoes[nomeDaFuncao] = {'parametros': listaFinalDeParametros, 'bloco': 'bloco'}

        # Não multiplos parâmetros
        else:

            # Verifica se o parâmetro está no padrão
            teste =Interpretador.analisa_padrao_variavel(self, parametros)
            if not teste[0]:
                return teste

            # Adicionar Função
            self.dic_funcoes[nomeDaFuncao] = {'parametros': [parametros], 'bloco': 'bloco'}

        funcao_em_analise = nomeDaFuncao
        return [True, True, 'booleano', 'declararFuncao', funcao_em_analise]

    def funcao_executar_funcao(self, nomeDaFuncao, parametros=None):
        #Interpretador.log(self, "__funcao_executar_funcao: nomeDaFuncao = '{}', parametros='{}'".format(nomeDaFuncao, parametros))

        if parametros is not None:
            if parametros.strip() == "":
                parametros = None
            
        try:
            self.dic_funcoes[nomeDaFuncao]
        except Exception as erro:
            return [False, self.msg("funcao_nao_existe").format(nomeDaFuncao), 'string', 'exibirNaTela']

        # Se não veio parâmetros
        if parametros is None:
            # Se a função tem parâmetros, mas não foi informando nenhum
            if self.dic_funcoes[nomeDaFuncao]['parametros'] != None:
                return [False,self.msg("funcao_nao_passou_parametros").format(nomeDaFuncao, len(
                    self.dic_funcoes[nomeDaFuncao]['parametros'])), 'string', 'exibirNaTela']

            # Executa o bloco de instrução da função
            resultadoOrquestrador = Interpretador.orquestrador_interpretador_(self, self.dic_funcoes[nomeDaFuncao]['bloco'])

            # Se deu erro
            if not resultadoOrquestrador[0]:
                return [resultadoOrquestrador[0], resultadoOrquestrador[1], resultadoOrquestrador[2], 'exibirNaTela']
            return [True, None, 'vazio', 'fazerNada']

        # Verifica se tem virgulas separando os parâmetros
        testa = Interpretador.verifica_se_tem(self, parametros, ',')

        # Se tinha multiplos parâmetros
        if testa != []:
            anterior = 0
            listaParametros = []

            # Anda pelos parâmetros
            for valorItem in testa:

                # Obtem os parâmetros
                if len(parametros[anterior:valorItem[0]]) > 0:
                    listaParametros.append(parametros[anterior: valorItem[0]])
                    anterior = valorItem[1]

            if len(parametros[anterior:]) > 0:
                listaParametros.append(parametros[anterior:])

            listaFinalDeParametros = []

            # Anda pelos parâmetros
            for parametro in listaParametros:
                listaFinalDeParametros.append(parametro.strip())

            # Foi informando parâmetros, mas a função não tem parâmetros
            if self.dic_funcoes[nomeDaFuncao]['parametros'] is None:
                return [False,self.msg("funcao_informou_mais_parametros").format(nomeDaFuncao), 'string', 'exibirNaTela']

            # Se a quantidade de itens for a mesma dessa funcao
            if len(self.dic_funcoes[nomeDaFuncao]['parametros']) == len(listaFinalDeParametros):

                for parametroDeclarar in range(len(self.dic_funcoes[nomeDaFuncao]['parametros'])):
                    resultado = Interpretador.funcao_realizar_atribu(self, self.dic_funcoes[nomeDaFuncao]['parametros'][
                        parametroDeclarar], listaFinalDeParametros[parametroDeclarar])

                    if resultado[0] == False:
                        return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
            else:
                return [False,self.msg("funcao_tem_parametros_divergentes").format(
                    nomeDaFuncao,
                    len(self.dic_funcoes[nomeDaFuncao]['parametros']),
                    len(listaFinalDeParametros)),
                    'string', 'fazerNada']


        # Se não vieram parâmetros
        elif parametros is not None:

            # Foi informando parâmetros, mas a função não tem parâmetros
            if self.dic_funcoes[nomeDaFuncao]['parametros'] is None:
                return [False,self.msg("funcao_informou_mais_parametros").format(nomeDaFuncao), 'string', 'exibirNaTela']


            if len(self.dic_funcoes[nomeDaFuncao]['parametros']) == 1:
                resultado =Interpretador.funcao_realizar_atribu(self, self.dic_funcoes[nomeDaFuncao]['parametros'][0], parametros)

                if not resultado[0]:
                    return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
            else:
                 return [False,self.msg("funcao_passou_um_parametros").format(nomeDaFuncao, len(self.dic_funcoes[nomeDaFuncao]['parametros'])), 'string', 'exibirNaTela']

        resultadoOrquestrador = Interpretador.orquestrador_interpretador_(self, self.dic_funcoes[nomeDaFuncao]['bloco'])

        if not resultadoOrquestrador[0]:
            return [resultadoOrquestrador[0], resultadoOrquestrador[1], resultadoOrquestrador[2], 'exibirNaTela']

        if resultadoOrquestrador[3] != 'retornarOrquestrador':
            # Sem retorno
            return [True, "", 'vazio', 'fazerNada']
        else:
            return [True, resultadoOrquestrador[1], resultadoOrquestrador[2], 'fazerNada']

    def filtrar_comando(self, linha, comando, substituicao):
        #Interpretador.log(self, "filtrar_comando")

        for comando in self.dic_comandos[comando]["comando"]:
            linha = linha.replace(comando[0], substituicao)

        return linha

    def funcao_testar_condicao(self, linha):
        #Interpretador.log(self, "__funcao_testar_condicao")

        linha = Interpretador.filtrar_comando(self, linha, "logico_maior_igual", ' >= ')
        linha = Interpretador.filtrar_comando(self, linha, "logico_menor_igual", ' <= ')
        linha = Interpretador.filtrar_comando(self, linha, "logico_diferente", ' != ')
        linha = Interpretador.filtrar_comando(self, linha, "logico_maior", ' > ')
        linha = Interpretador.filtrar_comando(self, linha, "logico_menor", ' < ')
        linha = Interpretador.filtrar_comando(self, linha, "logico_igual", ' == ')
        linha = Interpretador.filtrar_comando(self, linha, "logico_e", '  and  ')
        linha = Interpretador.filtrar_comando(self, linha, "logico_ou", '  or  ')

        linha = ' ' + str(linha) + ' '
        simbolosEspeciais = ['>=', '<=', '!=', '>', '<', '==', '(', ')', ' and ', ' or ', ' tiver ']
        qtd_simbolos_especiais = 0

        # Deixando todos os itens especiais com espaço em relação aos valores
        for item in simbolosEspeciais:

            # Se tiver o simbolo especial na linha, some +1
            if item in linha:
                qtd_simbolos_especiais += 1

                # Adiciona espaço para cada simbolos
                linha = linha.replace(item, '  {}  '.format(item))

        # Coreção de bugs ao usar o recurso de deixar espaços
        linha = linha.replace('* *', '**')
        linha = linha.replace('> =', '>=')
        linha = linha.replace('< =', '<=')
        linha = linha.replace('! =', '!=')

        linha = linha.replace('   tiver   ', ' tiver ')

        linha = linha.strip()
        simbolosArrumados = [' >= ', ' <= ', ' != ', ' > ', ' < ', ' == ', ' ( ', ' ) ', ' and ', ' or ']

        # Marcar os simbolos para correta captura do regex
        for simbolo in range(len(simbolosArrumados)):
            linha = linha.replace(
                simbolosArrumados[simbolo], '_._' + simbolosArrumados[simbolo] + '_._')

        linha = linha.replace('_._ < _._ =', '_._ <= _._')
        linha = linha.replace('_._ > _._ =', '_._ >= _._')

        # Usando Regex para isolar os simbolos
        anterior = 0
        final = ''

        for item in finditer("_\\._[^_]*_\\._", linha):

            # Abstrai um valor qual
            resultado = Interpretador.abstrair_valor_linha(self, linha[anterior:item.start()])

            if resultado[0] is False:
                return resultado

            saida = resultado[1]

            if resultado[2] == 'string':
                saida = '"' + resultado[1] + '"'

            # Reover marcadores de simbolos
            final += str(saida) + linha[item.start() + 3:item.end() - 3]

            anterior = item.end()

        boolTemTiverLista = False
        resultado = Interpretador.tiver_valor_lista(self, linha[anterior:].strip())

        if not resultado[0]:
            return resultado

        if resultado[2] == 'booleano':

            if resultado[1] == 'sim':
                final += ' True '
                boolTemTiverLista = True

            elif resultado[1] == 'nao':
                final += ' False '
                boolTemTiverLista = True

        if not boolTemTiverLista:

            resultado =Interpretador.abstrair_valor_linha(self, linha[anterior:])
            if not resultado[0]:
                return resultado

            saida = resultado[1]
            if resultado[2] == 'string':
                saida = '"' + resultado[1] + '"'

            final += str(saida)

        # Tente fazer a condição com isso
        try:
            resutadoFinal = eval(final)

        except Exception as erro:
            return [False, "{} |{}|".format(self.msg("nao_possivel_fazer_condicao"), final),
                    'string', 'exibirNaTela']

        else:
            return [True, resutadoFinal, 'booleano', 'declararCondicional']
