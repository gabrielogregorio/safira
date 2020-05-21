__author__      = 'Gabriel Gregório da Silva'
__email__       = 'gabriel.gregorio.1@outlook.com'
__project__     = 'Combratec'
__github__      = 'https://github.com/Combratec/'
__description__ = 'Interpretador de comandos'
__status__      = 'Desenvolvimento'
__version__     = '0.1'

from re import findall, finditer
from tkinter import END, DISABLED, NORMAL
from random import randint
from time import sleep
import libs.funcoes as funcoes
from json import load
import threading
import os.path
import os

#from libs.interpretador import Interpretador

class Run():
    def __init__(self, terminal, tx_codficac, bool_logs, lst_breakpoints, bool_ignorar_todos_breakpoints):

        self.aconteceu_erro = False
        self.erro_alertado = False
        self.ignorar_erros = False
        self.esperar_pressionar_enter = False
        self.dic_variaveis = {}
        self.dic_funcoes = {}
        self.boo_orquestrador_iniciado = False
        self.tx_terminal = terminal
        self.numero_threads = 0
        self.bool_logs = bool_logs
        self.tx_codficac = tx_codficac
        self.dic_comandos = funcoes.carregar_json('configuracoes/comandos.json')
        self.lst_breakpoints = lst_breakpoints
        self.bool_break_point_liberado = None
        self.bool_ignorar_todos_breakpoints = bool_ignorar_todos_breakpoints
        self.idioma = "pt-br"
        self.rgx_padrao_variavel = '[a-zA-Z0-9\\_]*'
        self.valor_tecla_pressionada = ""
        self.num_linha = "0"
        self.txt_ultima_msg_erro = ""
        self.esperando_tempo = False
        self.dir_script_aju_erro = ""

        with open('configuracoes/mensagens.json', encoding='utf8') as json_file:
            self.mensagens = load(json_file)

    def pressionou_enter(self, event=None):
        if self.esperar_pressionar_enter:
            self.esperar_pressionar_enter = False

    def capturar_tecla(self, tecla_pressionada):
        self.valor_tecla_pressionada = tecla_pressionada

    def aguardar_liberacao_breakPoint(self):
        self.bool_break_point_liberado = False
        while not self.bool_break_point_liberado and not self.bool_ignorar_todos_breakpoints:
            self.tx_codficac.update()

    def realiza_coloracao_erro(self, palavra, valor1, valor2, cor='red', linhaErro = None):
        """
            Colore uma linha de erro no terminal
        """

        linha = self.tx_terminal.get(1.0, END)
        linha = len(linha.split('\n')) - 1

        linha1 = '{}.{}'.format(linha, valor1)
        linha2 = '{}.{}'.format(linha, valor2)

        self.tx_terminal.tag_add(palavra, linha1 , linha2)
        self.tx_terminal.tag_config(palavra, foreground = cor)

        if linhaErro is not None:

            lista = self.tx_codficac.get(1.0, END).split("\n")

            palavra = "codigoErro"
            linha1 = str(linhaErro) + ".0"
            linha2 = str(linhaErro) + "." + str(len(lista[int(linhaErro) - 1]))

            self.tx_codficac.tag_add(palavra, linha1 , linha2)
            self.tx_codficac.tag_config(palavra, background = "#572929")

        self.erro_alertado = True

    def log(self, msg_log):
        if self.bool_logs:
            print(msg_log)

    def orq_erro(self, msg_log, linhaAnalise, dir_script_erro):
        if self.ignorar_erros:
            return "Ignorar Erro"

        self.aconteceu_erro = True

        if msg_log not in ["Erro ao iniciar o Interpretador", "indisponibilidade_terminal", "Interrompido"]:
            if not self.erro_alertado:

                self.txt_ultima_msg_erro = msg_log
                self.dir_script_aju_erro = dir_script_erro

                mensagem_erro = "\n[{}] {}".format(linhaAnalise, msg_log)
                self.tx_terminal.config(state=NORMAL)
                self.tx_terminal.insert(END, mensagem_erro)
                Run.realiza_coloracao_erro(self, 'codigoErro', valor1=0, valor2=len(mensagem_erro)+1, cor='#ffabab', linhaErro = linhaAnalise )

    def orq_exibir_tela(self, lst_retorno_ultimo_comando):
        try:
            self.tx_terminal.config(state=NORMAL)
            if ":nessaLinha:" in str(lst_retorno_ultimo_comando[1]):
                self.tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1][len(":nessaLinha:"):]))
            else:
                self.tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1])+'\n')

            self.tx_terminal.see("end")
            self.tx_terminal.update()
            self.tx_terminal.config(state=DISABLED)

        except Exception as erro:
            return [[False, "indisponibilidade_terminal", 'string','exibirNaTela'], "1"]


    def orquestrador_interpretador(self, txt_codigo):
        Run.log(self, '<orquestrador_interpretador>:' + txt_codigo)

        self.numero_threads += 1 # Aumenta os Thread
        self.boo_orquestrador_iniciado = True # Indica que já está contando os Thread

        int_tamanho_codigo = len(txt_codigo)
        bool_achou_comentario_longo = False
        bool_salvar_bloco = False
        bool_achou_comentario = False
        bool_achou_string = False
        bool_execucao_deu_erro_temporario = False

        str_bloco_salvo = ""
        txt_linha_comando = ""
        txt_caractere = ""
        historico_fluxo_de_dados = []
        bool_ultimo_teste = False

        int_profundidade_bloco = 0
        for num_txt_caractere, txt_caractere in enumerate(txt_codigo):
            txt_dois_caracteres = txt_codigo[num_txt_caractere : num_txt_caractere + 2]

            # Ignorar tudo entre /**/
            if txt_dois_caracteres == '/*' and not bool_achou_string and not bool_achou_comentario:
                bool_achou_comentario_longo = True
                continue

            if bool_achou_comentario_longo and txt_codigo[num_txt_caractere - 2:num_txt_caractere] == '*/':
                bool_achou_comentario_longo = False

            if bool_achou_comentario_longo:
                continue


            # Ignorar comentário #
            if( txt_caractere == '#' or txt_dois_caracteres == '//') and not bool_achou_string:
                bool_achou_comentario = True

            if bool_achou_comentario and txt_caractere == "\n":
                bool_achou_comentario = False

            elif bool_achou_comentario:
                continue


            # Executar o comando de uma linha
            # Se chegar no fim da linha ou iniciar um bloco e um bloco não estiver sendo salvo e nem estiver em uma string
            if ( txt_caractere == "\n" or txt_caractere == "{" and not bool_salvar_bloco and not bool_achou_string ):

                # Se tiver alguma coisa na linha 
                if len(txt_linha_comando.strip()) > 0:

                    # Remoção de lixo
                    txt_linha_comando = txt_linha_comando.replace("\n","").strip()

                    lst_analisa = Run.interpretador(self, txt_linha_comando)

                    if lst_analisa[0][3] == 'linhaVazia': # A linha estava em branco
                        txt_linha_comando = ""

                    else:
                        lst_ultimo_teste = lst_analisa
                        txt_comando_testado = txt_linha_comando
                        num_linha_analisada = lst_ultimo_teste[1]
                        arq_script_erro = lst_ultimo_teste[2]
                        lst_ultimo_teste = lst_ultimo_teste[0]

                        if lst_ultimo_teste[0] == False: # Seu erro

                            self.numero_threads -= 1
                            if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]
    
                            Run.orq_erro(self, lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                            return lst_ultimo_teste

                        if lst_ultimo_teste[3] == 'exibirNaTela':
                            Run.orq_exibir_tela(self, lst_ultimo_teste)

                        if lst_ultimo_teste[3] in ['fazerNada', 'exibirNaTela']: # Adiciona no fluxo de dados
                            historico_fluxo_de_dados.append('acaoDiversa')


                        txt_linha_comando = ""

                        if txt_caractere == "\n" and lst_ultimo_teste[3] == 'fazerNada':
                            continue




            # Quando começar uma string
            if txt_caractere == '"' and not bool_achou_string and not bool_salvar_bloco:
                bool_achou_string = True

            elif txt_caractere == '"' and bool_achou_string and not bool_salvar_bloco:
                bool_achou_string = False


            # Quando começar um bloco
            if txt_caractere == "{" and not bool_achou_string:
                int_profundidade_bloco += 1
                bool_salvar_bloco = True

            elif txt_caractere == "}" and not bool_achou_string:
                int_profundidade_bloco -= 1




            # Quando finalizar um bloco
            if txt_caractere == "}" and not bool_achou_string and int_profundidade_bloco == 0:
                Run.log(self, '!<Analisa bloco salvo>:"' + str_bloco_salvo + '"')

                bool_salvar_bloco = False

                if lst_ultimo_teste[3] == 'declararLoop':
                    historico_fluxo_de_dados.append('declararLoop') # Encaixa Loop

                    # Enquanto a condição for verdadeira
                    while lst_ultimo_teste[1] and not self.aconteceu_erro:

                        # Executar o bloco completo
                        lst_resultado_execucao = Run.orquestrador_interpretador(self, 
                            str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            self.numero_threads -= 1
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)

                            return lst_resultado_execucao

                        # Testar novamente a condição do loop
                        lst_ultimo_teste = Run.interpretador(self, txt_comando_testado)

                        num_linha_analisada = lst_ultimo_teste[1]
                        arq_script_erro = lst_ultimo_teste[2]
                        lst_ultimo_teste = lst_ultimo_teste[0]

                        
                        if lst_ultimo_teste[0] == False:

                            self.numero_threads -= 1
                            if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                            return lst_ultimo_teste

                elif lst_ultimo_teste[3] == "declararLoopRepetir":
                    historico_fluxo_de_dados.append('declararLoopRepetir') # Encaixa Loop

                    lst_ultimo_teste[3] = 'fazerNada'

                    for valor in range(0, lst_ultimo_teste[1]):
                        lst_resultado_execucao = Run.orquestrador_interpretador(self, 
                            str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads -= 1
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

                        criar_variavel = Run.funcao_realizar_atribu(self, lst_ultimo_teste[1][0], str(valor))
                        if criar_variavel[0] == False:
                            self.numero_threads -= 1
                            return criar_variavel

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, 
                            str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads -= 1
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

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)

                            self.numero_threads -= 1
                            return lst_resultado_execucao
                    else:
                        bool_ultimo_teste == False

                # É um senao se e o teste
                elif lst_ultimo_teste[3] == 'declararSenaoSe':

                    if len(historico_fluxo_de_dados) == 0:
                        Run.orq_erro(self, "Você precisa definir uma condição, para testar o senão", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir uma condição, para testar o senão", 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'declararCondicional':
                        Run.orq_erro(self, "Você precisa definir uma condição, para testar o senão", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir uma condição, para testar o senão", 'string', "fazerNada"]

                    # Condição se ou senão anterior era falsa
                    if bool_ultimo_teste == False:

                        # Teste senão é verdadeiro
                        if lst_ultimo_teste[1]:
                            bool_ultimo_teste = True # Condição agora foi executada

                            lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                            if lst_resultado_execucao[0] == False:

                                if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                    self.numero_threads -= 1
                                    return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                                Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                                self.numero_threads -= 1
                                return lst_resultado_execucao

                # É um senao se e o teste
                elif lst_ultimo_teste[3] == 'declararSenao':

                    if len(historico_fluxo_de_dados) == 0:
                        Run.orq_erro(self, "Você precisa definir uma condição, para testar o senão", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir uma condição, para testar o senão", 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'declararCondicional':
                        Run.orq_erro(self, "Você precisa definir uma condição, para testar o senão", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir uma condição, para testar o senão", 'string', "fazerNada"]

                    # Condição se ou senão anterior era falsa
                    if bool_ultimo_teste == False:
                        bool_ultimo_teste = True # Condição agora foi executada
                        lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads -= 1
                            return lst_resultado_execucao




                # É tente algo
                elif lst_ultimo_teste[3] == 'tenteAlgo':
                    self.ignorar_erros = True
                    historico_fluxo_de_dados.append("tenteAlgo")

                    lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                    bool_execucao_deu_erro_temporario = False

                    if lst_resultado_execucao[0] == False:
                        bool_execucao_deu_erro_temporario = True

                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            self.numero_threads -= 1
                            return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                        print("Erro ignorado => " + str(lst_resultado_execucao))

                        lst_resultado_execucao = [True, "", "linhaVazia", "fazerNada"]

                    self.ignorar_erros = False



                elif lst_ultimo_teste[3] == 'seDerErro':

                    if len(historico_fluxo_de_dados) == 0:
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se der erro", 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se der erro", 'string', "fazerNada"]

                    # Teste deu erro
                    if bool_execucao_deu_erro_temporario:

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[3] == 'seNaoErro':

                    if len(historico_fluxo_de_dados) == 0:
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se não der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se não der erro", 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se não der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se não der erro", 'string', "fazerNada"]

                    # Teste deu erro
                    if bool_execucao_deu_erro_temporario == False:

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads -= 1
                            return lst_resultado_execucao


                elif lst_ultimo_teste[3] == 'seDerErro':

                    if len(historico_fluxo_de_dados) == 0:
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se der erro", 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se der erro", 'string', "fazerNada"]

                    # Teste deu erro
                    if bool_execucao_deu_erro_temporario:

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                        if lst_resultado_execucao[0] == False:

                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                            Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                            self.numero_threads -= 1
                            return lst_resultado_execucao

                elif lst_ultimo_teste[3] == 'emQualquerCaso':

                    if len(historico_fluxo_de_dados) == 0:
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se não der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se não der erro", 'string', "fazerNada"]

                    if historico_fluxo_de_dados[-1] != 'tenteAlgo':
                        Run.orq_erro(self, "Você precisa definir um tente, para testar o se não der erro", "1", "")
                        self.numero_threads -= 1
                        return [False, "Você precisa definir um tente, para testar o se não der erro", 'string', "fazerNada"]


                    lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco_salvo[1:].strip())

                    if lst_resultado_execucao[0] == False:

                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            self.numero_threads -= 1
                            return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                        Run.orq_erro(self, lst_resultado_execucao[1], num_linha_analisada, arq_script_erro)
                        self.numero_threads -= 1
                        return lst_resultado_execucao

                str_bloco_salvo = ""
                continue

            # Se for para salvar bloco, salve o txt_caractere
            if bool_salvar_bloco:
                str_bloco_salvo += txt_caractere

            # Armazene os comandos
            elif not bool_achou_comentario:
                txt_linha_comando += txt_caractere

        # Se chegar no final do código e tiver comando para analisar
        if len(txt_linha_comando.strip()) > 0 and int_tamanho_codigo -1 == num_txt_caractere:

            txt_linha_comando = txt_linha_comando.replace("\n","").strip()
            lst_ultimo_teste = Run.interpretador(self, txt_linha_comando)

            txt_comando_testado = txt_linha_comando
            num_linha_analisada = lst_ultimo_teste[1]
            arq_script_erro = lst_ultimo_teste[2]
            lst_ultimo_teste = lst_ultimo_teste[0]

            if lst_ultimo_teste[0] == False:

                self.numero_threads -= 1
                if lst_ultimo_teste[1] == 'indisponibilidade_terminal':
                    return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

                Run.orq_erro(self, lst_ultimo_teste[1], num_linha_analisada, arq_script_erro)
                return lst_ultimo_teste

            if lst_ultimo_teste[3] == 'exibirNaTela': Run.orq_exibir_tela(self, lst_ultimo_teste)

        # Aviso de erros de profundidade
        self.numero_threads -= 1
        if int_profundidade_bloco > 0:
            return [False, "Você usou mais { do que o normal", 'string', "fazerNada"]

        elif int_profundidade_bloco < 0:
            return [False, "Você precisa de fechar uma {", 'string', "fazerNada"]

        return [True, 'Orquestrador Finalizado', 'string', "fazerNada"]

    def analisa_instrucao(self, comando, texto):
        re_comandos = "(\\<[a-zA-Z\\_]*\\>)"
        re_groups = findall(re_comandos, comando)
        if re_groups == None:
            return [False]

        dic_options = {}
        # Anda pelos grupos <se>, <esperar>
        for grupo in re_groups:

            # Anda pelos comandos no dicionários, [se], [if]...
            for n_comando in range(0, len( self.dic_comandos[grupo[1:-1]]["comando"] )):

                # Obtem um comando. se, if
                txt_comando_analisar = self.dic_comandos[ grupo[1:-1] ]["comando"][n_comando][0]

                # Substitui o grupo pelo comando. <se>, if
                comando_analise = comando.replace(grupo, txt_comando_analisar)
                try:
                    dic_options[grupo] = dic_options[grupo] +"|" + str(txt_comando_analisar)
                except Exception as err:
                    dic_options[grupo] = txt_comando_analisar

        for k,v in dic_options.items():
            v_add = v.replace(' ','\\s{1,}')

            comando = comando.replace(k, v_add )

        # o ? evita a gulidisse do .*, ele pode remover um passando parametros e considerar só o parametros, por exemplo
        comando = comando.replace('(.*)','(\\"[^\\"]*\\"|.*?)')

        # Marca o padrão de variável
        comando = comando.replace('__var__', '({})'.format(self.rgx_padrao_variavel))

        # Aplicar no texto
        re_texto = findall(comando, texto)

        if re_texto == []: return [False, 0]
        if str(type(re_texto[0])) == "<class 'str'>": lista_itens = [re_texto[0]]
        else: lista_itens = list(re_texto[0]) # Remover indexação a partir do zero
            
        lista_itens.insert(0, "")
        return [True, [saida.strip() for saida in lista_itens]]

    def interpretador(self, linha):
        Run.log(self, 'Interpretador iniciado')

        try:
            self.tx_terminal.get(1.0, 1.1)
        except:
            return [[False, 'indisponibilidade_terminal', 'string','exibirNaTela'], "1", ""]

        if self.aconteceu_erro:
            return [[False, 'Erro ao iniciar o Interpretador', 'string','exibirNaTela'], "1", ""]

        linha = linha.replace('\n', '')
        linha = linha.strip()

        # Se for uma linha vazia
        if linha == '':
            return [ [True, None, 'vazio','linhaVazia'], "1", "" ]

        else:
            self.num_linha = "0"
            posicoes = finditer(r'^(\[\d*\])', linha)

            # Obter o número da linha
            for uma_posicao in posicoes:
                self.num_linha = linha[1 : uma_posicao.end()-1]
                linha = linha[uma_posicao.end() : ]
                linha = linha.strip()
                break

            # Se estiver em um breakpoint, aguarde.
            if int(self.num_linha) in self.lst_breakpoints:
                Run.aguardar_liberacao_breakPoint(self)
            if self.aconteceu_erro:
                return [[False, 'Erro ao iniciar o Interpretador', 'string','exibirNaTela'], "1", ""]


            if linha == '':
                return [[True, None, 'vazio','linhaVazia'], "1", ""]

            analisa000 = Run.analisa_instrucao(self, '^(<limpatela>)$', linha)
            analisa001 = Run.analisa_instrucao(self, '^(<mostreNessa>)(.*)$', linha)
            analisa002 = Run.analisa_instrucao(self, '^(<mostre>)(.*)$', linha)
            analisa004 = Run.analisa_instrucao(self, '^(<enquanto>)(.*)$', linha)
            analisa005 = Run.analisa_instrucao(self, '^(<aguarde>)(.*)(<esperaEm>)$', linha)
            analisa006 = Run.analisa_instrucao(self, '^(<repita>)(.*)(<repitaVezes>)$', linha)
            analisa007 = Run.analisa_instrucao(self, '^(<incremente>)(.*)(<incrementeDecremente>)(.*)$', linha)
            analisa008 = Run.analisa_instrucao(self, '^(<decremente>)(.*)(<incrementeDecremente>)(.*)$', linha)
            analisa009 = Run.analisa_instrucao(self, '^(<funcoes>)(.*)(<recebeParametros>)(.*)$', linha)
            analisa010 = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaNaPosicao>)(.*)(<recebeDeclaraListas>)(.*)$', linha)
            analisa011 = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaCom>)(.*)(<listaPosicoesCom>)$', linha)
            analisa012 = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<recebeDeclaraListas>)(.*)$', linha)
            analisa013 = Run.analisa_instrucao(self, '^(<RemoverItensListas>)(.*)(<RemoverItensListasInterno>)(.*)$', linha)
            analisa014 = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoPosicao>)(.*)(<addItensListaInternoPosicaoFinaliza>)(.*)$', linha)
            analisa015 = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoFinal>)(.*)$', linha)
            analisa016 = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoInicio>)(.*)$', linha)
            analisa017 = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInterno>)(.*)$', linha)
            analisa018 = Run.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', linha)
            analisa019 = Run.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', linha)
            analisa020 = Run.analisa_instrucao(self, '^(<digitado>)$', linha)
            analisa021 = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha)
            analisa022 = Run.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', linha)
            analisa023 = Run.analisa_instrucao(self, '^(\\s*[a-zA-Z\\_0-9]*)(<declaraVariaveis>)(.*)$', linha)
            analisa024 = Run.analisa_instrucao(self, '^(.*)(<passandoParametros>)(.*)$', linha)
            analisa025 = Run.analisa_instrucao(self, '^(<para_cada>)__var__(<para_cada_de>)(.*)(<para_cada_ate>)(.*)$', linha)
            analisa026 = Run.analisa_instrucao(self, '^(<ler_tecla_por>)(.*)(<esperaEm>)$', linha)
            analisa026 = Run.analisa_instrucao(self, '^(<ler_tecla_por>)(.*)(<esperaEm>)$', linha)
            analisa027 = Run.analisa_instrucao(self, '^(<crie_arquivo>)(.*)$', linha)
            analisa028 = Run.analisa_instrucao(self, '^(<delete_arquivo>)(.*)$', linha)

            analisa042 = Run.analisa_instrucao(self, '^(<arquivo_existe>)(.*)(<arquivo_existe_nao_sub_existe>)$', linha)
            analisa029 = Run.analisa_instrucao(self, '^(<arquivo_existe>)(.*)(<arquivo_existe_sub_existe>)$', linha)

            analisa030 = Run.analisa_instrucao(self, '^(<adicione_texto_arquivo>)(.*)(<adicione_texto_arquivo_sub>)(.*)$', linha)
            analisa031 = Run.analisa_instrucao(self, '^(<sobrescreva_texto_arquivo>)(.*)(<sobrescreva_texto_arquivo_sub>)(.*)(<sobrescreva_texto_arquivo_sub_sub>)$', linha)
            analisa032 = Run.analisa_instrucao(self, '^(<leia_arquivo>)(.*)$', linha)
            analisa033 = Run.analisa_instrucao(self, '^(<tipo_variavel>)(.*)$', linha)
            analisa034 = Run.analisa_instrucao(self, '^(<a_imagem_aparecer>)(.*)(<a_imagem_aparecer_interno>)(.*)(<a_imagem_aparecer_interno_segundos>)$', linha)
            analisa035 = Run.analisa_instrucao(self, '^(<se_nao_se>)(.*)$', linha)
            analisa036 = Run.analisa_instrucao(self, '^(<se_nao>)$', linha)

            analisa037 = Run.analisa_instrucao(self, '^(<tente>)$', linha)
            analisa038 = Run.analisa_instrucao(self, '^(<se_der_erro>)$', linha)
            analisa039 = Run.analisa_instrucao(self, '^(<senao_der_erro>)$', linha)
            analisa040 = Run.analisa_instrucao(self, '^(<em_qualquer_caso>)$', linha)
            analisa003 = Run.analisa_instrucao(self, '^(<se>)(.*)$', linha)
            analisa041 = Run.analisa_instrucao(self, '^(<importe>)(.*)$', linha)

            analisa043 = Run.analisa_instrucao(self, '^(<funcoes>)(\s*[\w*\_]*\s*)$', linha)
            analisa044 = Run.analisa_instrucao(self, '^\s*[a-z\_]*\s*$', linha)



            if analisa000[0]: return [ Run.funcao_limpar_o_termin(self), self.num_linha , "limpaTela.fyn"]
            if analisa001[0]: return [ Run.funcao_exibir_mesma_ln(self, analisa001[1][2]), self.num_linha, "exibiçãoNaTela.fyn"]
            if analisa002[0]: return [ Run.funcao_exibir_outra_ln(self, analisa002[1][2]), self.num_linha, "exibiçãoNaTela.fyn" ]
            if analisa004[0]: return [ Run.funcao_loops_enquantox(self, analisa004[1][2]), self.num_linha, "enquanto.fyn"]
            if analisa005[0]: return [ Run.funcao_esperar_n_tempo(self, analisa005[1][2],  analisa005[1][3]), self.num_linha, "esperar.fyn"]
            if analisa006[0]: return [ Run.funcao_repetir_n_vezes(self, analisa006[1][2]), self.num_linha, "repetir.fyn" ]
            if analisa007[0]: return [ Run.funcao_incremente_vari(self, analisa007[1][2],  analisa007[1][4]), self.num_linha, "" ]
            if analisa008[0]: return [ Run.funcao_decremente_vari(self, analisa008[1][2],  analisa008[1][4]), self.num_linha, "" ]
            if analisa043[0]: return [ Run.funcao_declarar_funcao(self, analisa043[1][2] ), self.num_linha, "funcoes.fyn" ]
            if analisa009[0]: return [ Run.funcao_declarar_funcao(self, analisa009[1][2],  analisa009[1][4]), self.num_linha, "funcoes.fyn" ]
            if analisa010[0]: return [ Run.funcao_add_lst_na_posi(self, analisa010[1][2],  analisa010[1][4],  analisa010[1][6]),  self.num_linha, "" ]
            if analisa011[0]: return [ Run.funcao_dec_lst_posicoe(self, analisa011[1][2],  analisa011[1][4]), self.num_linha, "" ]
            if analisa012[0]: return [ Run.funcao_declarar_listas(self, analisa012[1][2],  analisa012[1][4]), self.num_linha, "listas.fyn" ]
            if analisa013[0]: return [ Run.funcao_rem_itns_na_lst(self, analisa013[1][2],  analisa013[1][4]), self.num_linha, "listas.fyn" ]
            if analisa014[0]: return [ Run.funcao_add_itns_lst_ps(self, analisa014[1][2],  analisa014[1][4],  analisa014[1][6]),  self.num_linha, "listas.fyn" ]
            if analisa015[0]: return [ Run.funcao_add_itns_na_lst(self, analisa015[1][2],  analisa015[1][4]), self.num_linha, "listas.fyn" ]
            if analisa016[0]: return [ Run.funcao_add_itns_lst_in(self, analisa016[1][2],  analisa016[1][4]), self.num_linha, "listas.fyn" ]
            if analisa017[0]: return [ Run.funcao_add_itns_na_lst(self, analisa017[1][2],  analisa017[1][4]), self.num_linha, "listas.fyn" ]
            if analisa018[0]: return [ Run.funcao_numer_aleatorio(self, analisa018[1][2],  analisa018[1][4]), self.num_linha, "aleatorio.fyn" ]
            if analisa019[0]: return [ Run.funcao_obter_valor_lst(self, analisa019[1][2],  analisa019[1][4]), self.num_linha, "" ]
            if analisa020[0]: return [ Run.funcao_ovalor_digitado(self, analisa020[1][1]), self.num_linha, "tudo_entradas.fyn" ]
            if analisa021[0]: return [ Run.funcao_tiver_valor_lst(self, analisa021[1][2],  analisa021[1][4]), self.num_linha, "se tiver.fyn" ]
            if analisa022[0]: return [ Run.funcao_otamanho_da_lst(self, analisa022[1][2]), self.num_linha, "" ]
            if analisa023[0]: return [ Run.funcao_realizar_atribu(self, analisa023[1][1],  analisa023[1][3]), self.num_linha, "atribuicoes.fyn" ]
            if analisa024[0]: return [ Run.funcao_executar_funcao(self, analisa024[1][1],  analisa024[1][3]), self.num_linha, "funcoes.fyn" ]
            if analisa025[0]: return [ Run.funcao_loop_para_cada_(self, analisa025[1][2],  analisa025[1][4], analisa025[1][6]), self.num_linha, "" ]
            if analisa026[0]: return [ Run.funcao_ler_tecla_por_s(self, analisa026[1][2]), self.num_linha, "" ]
            if analisa027[0]: return [ Run.funcao_criar_arquivo(self, analisa027[1][2]), self.num_linha, "" ]
            if analisa028[0]: return [ Run.funcao_excluir_arquivo(self, analisa028[1][2]), self.num_linha, "" ]


            if analisa042[0]: return [ Run.funcao_arquivo_nao_existe(self, analisa042[1][2]), self.num_linha, "" ]
            if analisa029[0]: return [ Run.funcao_arquivo_existe(self, analisa029[1][2]), self.num_linha, "" ]
            if analisa030[0]: return [ Run.funcao_adicionar_arquivo(self, analisa030[1][2], analisa030[1][4]), self.num_linha, "" ]
            if analisa031[0]: return [ Run.funcao_sobrescrever_arquivo(self, analisa031[1][2], analisa031[1][4]), self.num_linha, "" ]
            if analisa032[0]: return [ Run.funcao_ler_arquivo(self, analisa032[1][2]), self.num_linha, "" ]
            if analisa033[0]: return [ Run.funcao_tipo_variavel(self, analisa033[1][2]), self.num_linha, "" ]
            if analisa034[0]: return [ Run.funcao_a_imagem_aparecer_por(self, analisa034[1][2], analisa034[1][4]), self.num_linha, "" ]
            if analisa035[0]: return [ Run.funcao_senao_se(self, analisa035[1][2]), self.num_linha, "" ]
            if analisa036[0]: return [ Run.funcao_senao(self), self.num_linha, "" ]

            if analisa037[0]: return [ Run.funcao_tente(self), self.num_linha, "" ]
            if analisa038[0]: return [ Run.funcao_se_der_erro(self), self.num_linha, "" ]
            if analisa039[0]: return [ Run.funcao_senao_der_erro(self), self.num_linha, "" ]
            if analisa040[0]: return [ Run.funcao_em_qualquer_caso(self), self.num_linha, "" ]
            if analisa003[0]: return [ Run.funcao_testar_condicao(self, analisa003[1][2]), self.num_linha, "condicionais.fyn" ]
            if analisa041[0]: return [ Run.funcao_importe(self, analisa041[1][2]), self.num_linha, "" ]

            if analisa044[0]: return [ Run.funcao_executar_funcao(self, analisa044[1][1]), self.num_linha, "funcoes.fyn" ]


            return [ [False, "{}'{}'".format( Run.msg_idioma(self, 'comando_desconhecido'), linha), 'string','exibirNaTela'], self.num_linha, "" ]
        return [ [True, None, 'vazio', 'fazerNada'], self.num_linha, "" ]


    def funcao_importe(self, biblioteca):
        Run.log(self, 'funcao_importe:')

        # Tenta abrir o texto da biblioteca
        teste = funcoes.abrir_arquivo(str(biblioteca.lower()) + str(".fyn"))
        if teste[0] == None:
            return [False, "Erro ao abrir a biblioteca {}, erro {}".format(biblioteca, teste[1]), "string", "fazerNada"]

        # Carrega a biblioteca
        resultadoOrquestrador = Run.orquestrador_interpretador(self, teste[0])

        if resultadoOrquestrador[0] == False:
            return resultadoOrquestrador

        return [True, None, 'vazio', 'fazerNada']

    def funcao_tente(self):
        Run.log(self, 'funcao_tente:')
        return [True, True, 'string', 'tenteAlgo']

    def funcao_se_der_erro(self):
        Run.log(self, 'funcao_se_der_erro:')
        return [True, True, 'string', 'seDerErro']

    def funcao_senao_der_erro(self):
        Run.log(self, 'funcao_senao_der_erro:')
        return [True, True, 'string', 'seNaoErro']

    def funcao_em_qualquer_caso(self):
        Run.log(self, 'funcao_em_qualquer_caso:')
        return [True, True, 'string', 'emQualquerCaso']



    def funcao_senao(self):
        Run.log(self, 'funcao_senao:')
        return [True, True, 'string', 'declararSenao']

    def funcao_senao_se(self, condicao):
        Run.log(self, 'funcao_senao_se: {}'.format(condicao))
        resultado = Run.funcao_testar_condicao(self, condicao)
        return [resultado[0], resultado[1], resultado[2], 'declararSenaoSe']


    def comandos_uso_geral(self, possivelVariavel):
        Run.log(self, 'comandos_uso_geral: {}'.format(possivelVariavel))

        possivelVariavel = str(possivelVariavel).strip()

        analisa018 = Run.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$',  possivelVariavel)
        analisa019 = Run.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', possivelVariavel)
        analisa020 = Run.analisa_instrucao(self, '^(<digitado>)$', possivelVariavel)
        analisa021 = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', possivelVariavel)
        analisa022 = Run.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', possivelVariavel)
        analisa026 = Run.analisa_instrucao(self, '^(<ler_tecla_por>)(.*)(<esperaEm>)$', possivelVariavel)
        analisa029 = Run.analisa_instrucao(self, '^(<arquivo_existe>)(.*)(<arquivo_existe_sub_existe>)$', possivelVariavel)
        analisa032 = Run.analisa_instrucao(self, '^(<leia_arquivo>)(.*)$', possivelVariavel)
        analisa033 = Run.analisa_instrucao(self, '^(<tipo_variavel>)(.*)$', possivelVariavel)
        analisa034 = Run.analisa_instrucao(self, '^(<a_imagem_aparecer>)(.*)(<a_imagem_aparecer_interno>)(.*)(<a_imagem_aparecer_interno_segundos>)$', possivelVariavel)

        if analisa018[0]: return Run.funcao_numer_aleatorio(self, analisa018[1][2], analisa018[1][4])
        if analisa019[0]: return Run.funcao_obter_valor_lst(self, analisa019[1][2], analisa019[1][4])
        if analisa020[0]: return Run.funcao_ovalor_digitado(self, analisa020[1][1])
        if analisa021[0]: return Run.funcao_tiver_valor_lst(self, analisa021[1][2],analisa021[1][4])
        if analisa022[0]: return Run.funcao_otamanho_da_lst(self, analisa022[1][2])
        if analisa026[0]: return Run.funcao_ler_tecla_por_s(self, analisa026[1][2])
        if analisa029[0]: return Run.funcao_arquivo_existe(self, analisa029[1][2])
        if analisa032[0]: return Run.funcao_ler_arquivo(self, analisa032[1][2])
        if analisa033[0]: return Run.funcao_tipo_variavel(self, analisa033[1][2])
        if analisa034[0]: return Run.funcao_a_imagem_aparecer_por(self, analisa034[1][2], analisa034[1][4])

        return [True, None, 'vazio']



    def thread_tempo_espera(self, tempo):
        self.esperando_tempo = True

        sleep(tempo)

        self.esperando_tempo = False

    def funcao_a_imagem_aparecer_por(self, imagem, tempo):
        Run.log(self, 'funcao funcao_a_imagem_aparecer_por {}'.format(imagem))

        imagem = Run.abstrair_valor_linha(self, imagem)
        tempo = Run.abstrair_valor_linha(self, tempo)

        if not imagem[0]: return imagem
        if not tempo[0]: return tempo

        if imagem[2] != "string":
            return [ False,"A imagem precisa ser um texto", 'string',' exibirNaTela']

        if tempo[2] != "float":
            return [ False,"A variável tempo precisa ser numérico", 'string',' exibirNaTela']

        self.esperando_tempo = True
        threading.Thread(target=lambda this = self, tempo = tempo: Run.thread_tempo_espera(self, tempo))

        try:
            import pyautogui

            posicoes = None
            while posicoes is None:
                posicoes = pyautogui.locateCenterOnScreen(imagem[1], confidence = 0.8, grayscale=True)

                if posicoes is not None:
                    return [True, True, "booleano", "fazerNada"]

                if not self.esperando_tempo:
                    return [True, False, "booleano", "fazerNada"]

        except Exception as e:
            return [False, "Erro com a execução da função, erro 1 '{}'".format(e), "string",'exibirNaTela']

        else:
            return [True, teste, "booleano", "fazerNada"]

    def funcao_tipo_variavel(self, variavel):
        Run.log(self, 'funcao funcao_tipo_variavel: {}'.format(variavel))

        resultado = Run.abstrair_valor_linha(self, variavel)
        if not resultado[0]: return resultado

        resultado[1] = str(resultado[1]).replace("\\n","\n")
        # Retornando o tipo
        return [resultado[0], resultado[2], resultado[2],'exibirNaTela']

    def funcao_ler_arquivo(self, nome_arquivo):

        teste_valor_arquivo = Run.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor_arquivo[0] == False: return teste_valor_arquivo

        if teste_valor_arquivo[1] == "":
            return [ False,"Você precisa informar o nome de um arquivo", 'string',' exibirNaTela']


        nome_arquivo = str(teste_valor_arquivo[1])

        if os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "r")
                texto = f.read()
                f.close()

            except Exception as e:
                return [ False,"Erro ao abrir o arquivo \"{}\", erro \"{}\"".format(arquivo, e), 'string',' exibirNaTela']

            else:
                return [True, str(texto), "string", "fazerNada"]

            return [True, True, "booleano", "fazerNada"]


        return [ False,"O arquivo \"{}\" não existe!".format(nome_arquivo), 'string',' exibirNaTela']



    def funcao_sobrescrever_arquivo(self, texto, nome_arquivo):

        teste_valor_arquivo = Run.abstrair_valor_linha(self, nome_arquivo)
        teste_valor_texto = Run.abstrair_valor_linha(self, texto)

        if teste_valor_arquivo[0] == False: return teste_valor_arquivo
        if teste_valor_texto[0] == False: return teste_valor_texto

        if teste_valor_arquivo[1] == "":
            return [ False,"Você precisa informar o nome de um arquivo", 'string',' exibirNaTela']


        nome_arquivo = str(teste_valor_arquivo[1])
        texto = str(teste_valor_texto[1])
        texto = texto.replace("\\n","\n")

        if os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "w", encoding = "utf8")
                f.write(texto)
                f.close()

            except Exception as e:
                return [ False,"Erro ao adicionar o texto \"{}\" no arquivo \"{}\". Erro \"{}\"".format(texto, arquivo, e), 'string',' exibirNaTela']

            return [True, True, "booleano", "fazerNada"]

        return [ False,"O arquivo \"{}\" não existe!".format(nome_arquivo), 'string',' exibirNaTela']


    def funcao_adicionar_arquivo(self, texto, nome_arquivo):

        teste_valor_arquivo = Run.abstrair_valor_linha(self, nome_arquivo)
        teste_valor_texto = Run.abstrair_valor_linha(self, texto)

        if teste_valor_arquivo[0] == False: return teste_valor_arquivo
        if teste_valor_texto[0] == False: return teste_valor_texto

        if teste_valor_arquivo[1] == "":
            return [ False,"Você precisa informar o nome de um arquivo", 'string',' exibirNaTela']


        nome_arquivo = str(teste_valor_arquivo[1])
        texto = str(teste_valor_texto[1])
        texto = texto.replace("\\n","\n")

        if os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "a", encoding = "utf8")
                f.write(texto)
                f.close()
            except Exception as e:
                return [ False,"Erro ao adicionar o texto \"{}\" no arquivo \"{}\". Erro \"{}\"".format(texto, arquivo, e), 'string',' exibirNaTela']

            return [True, True, "booleano", "fazerNada"]


        return [ False,"O arquivo \"{}\" não existe!".format(nome_arquivo), 'string',' exibirNaTela']

    def funcao_arquivo_existe(self, nome_arquivo):
        if nome_arquivo == "":
            return [ False,"Você precisa informar o nome de um arquivo", 'string',' exibirNaTela']

        teste_valor = Run.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])

        if os.path.exists(nome_arquivo):
            return [True, True, "booleano", "fazerNada"]

        else:
            return [True, False, "booleano", "fazerNada"]

    def funcao_arquivo_nao_existe(self, nome_arquivo):
        if nome_arquivo == "":
            return [ False,"Você precisa informar o nome de um arquivo", 'string',' exibirNaTela']

        teste_valor = Run.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])

        if os.path.exists(nome_arquivo):
            return [True, False, "booleano", "fazerNada"]

        else:
            return [True, True, "booleano", "fazerNada"]


    def funcao_excluir_arquivo(self, nome_arquivo):
        if nome_arquivo == "":
            return [ False,"Você precisa informar o nome de um arquivo", 'string',' exibirNaTela']

        teste_valor = Run.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])

        if os.path.exists(nome_arquivo):
            try:
                os.remove(nome_arquivo)

            except Exception as erro:
                return [ False,"Erro ao deletar o arquivo, erro \"{}\"".format(erro), 'string',' exibirNaTela']

            else:
                return [True, "", "vazio", "fazerNada"]

        else:
            return [ False,"O arquivo \"{}\" não existe".format(nome_arquivo), 'string',' exibirNaTela']

        


    def funcao_criar_arquivo(self, nome_arquivo):
        if nome_arquivo == "":
            return [ False,"Você precisa informar o nome de um arquivo", 'string',' exibirNaTela']

        teste_valor = Run.abstrair_valor_linha(self, nome_arquivo)
        if teste_valor[0] == False: return teste_valor

        nome_arquivo = str(teste_valor[1])

        if not os.path.exists(nome_arquivo):
            try:
                f = open(nome_arquivo, "w", encoding='utf8')
                f.write("")
                f.close()

            except Exception as erro:
                return [ False,"Erro ao criar o arquivo, erro \"{}\"".format(erro), 'string',' exibirNaTela']

        return [True, "", "vazio", "fazerNada"]



    def funcao_ler_tecla_por_s(self, tempo):
        Run.log(self, 'ler tecla por: ' + tempo)
        self.valor_da_tecla_pressionada = ""
  
        sleep(0.1)
        tecla = self.valor_tecla_pressionada
        self.valor_tecla_pressionada = ""

        return [True, str(tecla).lower(), "string", "fazerNada"]

    def msg_variavel_numerica(self, msg, variavel):
        if msg == 'naoNumerico':
            return [False, "A variável '{}' não é numérica!".format(variavel), 'string', 'exibirNaTela']

    def funcao_loop_para_cada_(self, variavel, inicio, fim):

        teste_exist = Run.obter_valor_variavel(self, variavel)
        teste_valorI = Run.abstrair_valor_linha(self, inicio)
        teste_valorF = Run.abstrair_valor_linha(self, fim)

        if teste_valorI[0] == False: return teste_valorI
        if teste_valorF[0] == False: return teste_valorF

        if teste_valorI[2] != 'float': return Run.msg_variavel_numerica(self, 'naoNumerico', teste_valorI[1])
        if teste_valorF[2] != 'float': return Run.msg_variavel_numerica(self, 'naoNumerico', teste_valorF[1])

        # Variável não existe
        if teste_exist[0] == False:
            criar_variavel = Run.funcao_realizar_atribu(self, variavel, '0')

            if not criar_variavel[0]:
                return criar_variavel
        passo = 1
        if (int(teste_valorI[1]) > int(teste_valorF[1])):
            passo = -1
        
        return [True, [variavel, int(teste_valorI[1]), int(teste_valorF[1]), passo], "lista", "declararLoopParaCada"]

    def funcao_incremente_vari(self, valor, variavel):
        return Run.incremente_decremente(self, valor, variavel,  'incremente')

    def funcao_decremente_vari(self, valor, variavel):
        return Run.incremente_decremente(self, valor, variavel, 'decremente')

    def incremente_decremente(self, valor, variavel, acao):
        Run.log(self, 'incremente_decremente:' + valor+str(variavel))

        teste_exist = Run.obter_valor_variavel(self, variavel)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if teste_exist[0] == False: return teste_exist
        if teste_valor[0] == False: return teste_valor

        if teste_exist[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico', variavel)

        if teste_valor[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico', teste_valor[1])

        if acao == "incremente":
            self.dic_variaveis[ variavel ][0] = self.dic_variaveis[ variavel ][0] + teste_valor[1]

        else:
            self.dic_variaveis[ variavel ][0] = self.dic_variaveis[ variavel ][0] - teste_valor[1]

        return [True, True, "booleano", "fazerNada"]

    def msg_idioma(self, chave):
        return self.mensagens[chave][self.idioma]

    def funcao_add_lst_na_posi(self, variavelLista, posicao, valor):
        Run.log(self, 'funcao_add_lst_na_posi:' + str(variavelLista))

        if variavelLista == '' or posicao == '' or valor == '': # Veio sem dados
            return [ False, Run.msg_idioma(self, 'add_lst_posicao_separador'), 'string',' exibirNaTela']

        teste_exist = Run.obter_valor_variavel(self, variavelLista)
        teste_posic = Run.abstrair_valor_linha(self, posicao)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if not teste_exist[0]: return teste_exist
        if not teste_posic[0]: return teste_posic
        if not teste_valor[0]: return teste_valor

        if teste_exist[2] != 'lista':
            return[False, '{} {}'.format(variavelLista, Run.msg_idioma(self, "nao_e_lista")), 'string']

        if teste_posic[2] != 'float':
            return  Run.msg_variavel_numerica(self, 'naoNumerico',  teste_posic[1])

        posicao = int(teste_posic[1])

        # Posição estoura posições da lista
        if posicao - 1 > len(self.dic_variaveis[variavelLista][0]):
            return [False, '{} {}'.format(Run.msg_idioma(self, "posicao_maior_limite_lista"), posicao), 'string', 'exibirNaTela']

        if posicao < 1 :
            return [False, '{} {}'.format(Run.msg_idioma(self, "posicao_menor_limite_lista") ,posicao), 'string', 'exibirNaTela']

        self.dic_variaveis[variavelLista][0].insert(posicao - 1, [teste_valor[1], teste_valor[2]])
        return [ True, True, 'booleano', 'fazerNada' ]

    def obter_valor_lista(self, linha):
        Run.log(self, 'obter_valor_lista ' + str(linha))

        teste = Run.obter_valor_variavel(self, linha)

        if not teste[0]: return teste

        if teste[2] != 'lista':
            return[False, "{} {}".format(linha, Run.msg_idioma(self, "nao_e_lista")), 'string']

        return teste

    def funcao_obter_valor_lst(self, variavel, posicao):
        Run.log(self, 'Função Valor de lista: "{}", subcomandos: "{}"'.format(variavel, posicao))

        if variavel == '' or posicao == '':
            return [ False, Run.msg_idioma(self, "variavel_posicao_nao_informada"),'string','exibirNaTela']

        teste_posicao = Run.abstrair_valor_linha(self, posicao)
        teste_variavel = Run.obter_valor_lista(self, variavel)

        if not teste_posicao[0]:
            return [teste_posicao[0], teste_posicao[1], teste_posicao[2], 'exibirNaTela']

        elif teste_posicao[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  teste_posicao[1]) 

        elif teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        posicao = int(teste_posicao[1])
        resultado = teste_variavel[1]

        if posicao < 1:
            return [False, Run.msg_idioma(self, "posicao_menor_limite_lista"), 'exibirNaTela']

        if len(resultado) < posicao:
            return [False, Run.msg_idioma(self, "posicao_maior_limite_lista"), 'exibirNaTela']

        return [True, resultado[posicao-1][0], resultado[posicao-1][1], 'exibirNaTela']

    def funcao_tiver_valor_lst(self, valor, variavel):
        Run.log(self, "Função tiver na lista: " + valor)

        if variavel == '' or valor == '':
            return [False, Run.msg_idioma(self, "variavel_valor_nao_informado"), 'exibirNaTela']

        teste_variavel = Run.obter_valor_variavel(self, variavel)
        resultado_valor = Run.abstrair_valor_linha(self, valor)

        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if teste_variavel[2] != 'lista':
            return [False, '{} {}'.format(linha, Run.msg_idioma(self, "nao_e_lista")), 'string', 'exibirNaTela']

        if not resultado_valor[0]:
            return [resultado_valor[0], resultado_valor[1], resultado_valor[2], 'exibirNaTela']

        if [resultado_valor[1], resultado_valor[2]] in self.dic_variaveis[variavel][0]:
            return [True, True, 'booleano', 'fazerNada']

        return [True, False, 'booleano', 'fazerNada']

    def funcao_otamanho_da_lst(self, linha):
        Run.log(self, 'Função obter o tamanho da lista: "{}"'.format(linha))

        linha = linha.strip()

        teste = Run.obter_valor_lista(self, linha)
        if not teste[0]:
            return [teste[0], teste[1], teste[2], 'exibirNaTela']

        try:
            return [True, len(self.dic_variaveis[linha][0]), 'float', 'fazerNada']
        except Exception as erro:
            return [True, '{} {}'.format(Run.msg_idioma(self, "erro_obter_tamanho_lista"), erro), 'string', 'exibirNaTela']

    def funcao_rem_itns_na_lst(self, valor, variavel):
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, Run.msg_idioma(self, "variavel_valor_nao_informado"), 'exibirNaTela']

        # analisa[1] se lista foi decarada e se é lista
        teste = Run.obter_valor_lista(self, variavel)
        if not teste[0]:
            return [teste[0], teste[1], teste[2], 'exibirNaTela']

        resultado = Run.abstrair_valor_linha(self, valor)

        if not resultado[0]:
            return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

        try:
            self.dic_variaveis[variavel][0].remove([resultado[1], resultado[2]])
        except Exception as erro:
            return [ False, '"{}" {} "{}"!'.format(resultado[1], Run.msg_idioma(self, "nao_esta_na_lista")  , variavel), 'string', 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']

    def funcao_add_itns_na_lst(self, valor, variavel):
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, Run.msg_idioma(self, "variavel_valor_nao_informado"), 'exibirNaTela']

        teste_variavel = Run.obter_valor_lista(self, variavel)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if not teste_valor[0]:
            return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

        try:
            self.dic_variaveis[variavel][0].append([teste_valor[1], teste_valor[2]])
        except Exception as erro:
            return [ False, '"{}" {} "{}"!'.format(teste_valor[1], Run.msg_idioma(self, "nao_esta_na_lista"), variavel), 'string', 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']

    def funcao_add_itns_lst_in(self, valor, variavel):
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, Run.msg_idioma(self, "variavel_valor_nao_informado"), 'exibirNaTela']

        # analisa[1] se lista foi decarada e se é lista
        teste_variavel = Run.obter_valor_lista(self, variavel)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if not teste_variavel[0]:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if not teste_valor[0]:
            return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

        self.dic_variaveis[variavel][0].insert(0, [teste_valor[1], teste_valor[2]])
        return [True, None, 'vazio', 'fazerNada']

    def funcao_add_itns_lst_ps(self, valor, posicao, variavel):
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Adicione 1 a lista de nomes ', 'exibirNaTela']

        teste_variavel = Run.obter_valor_lista(self, variavel)
        teste_posicao = Run.abstrair_valor_linha(self, posicao)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if not teste_variavel[0]: return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']
        if not teste_valor[0]: return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']
        if not teste_posicao[0]: return [teste_posicao[0], teste_posicao[1], teste_posicao[2], 'exibirNaTela']

        if teste_posicao[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  teste_posicao[1])

        posicao = int(teste_posicao[1])

        if posicao - 1 > len(self.dic_variaveis[variavel][0]):
            return [False, Run.msg_idioma(self, "posicao_maior_limite_lista"), 'string', 'exibirNaTela']

        if posicao < 1 :
            return [False, Run.msg_idioma(self, "posicao_menor_limite_lista"), 'string', 'exibirNaTela']

        self.dic_variaveis[variavel][0].insert(posicao - 1, [teste_valor[1], teste_valor[2]])
        return [ True, True, 'booleano', 'fazerNada' ]

    def funcao_dec_lst_posicoe(self, variavel, posicoes):
        Run.log(self, 'Função declarar listas posicoes: "{}"'.format(variavel))

        teste = Run.analisa_padrao_variavel(self, variavel)
        resultado = Run.abstrair_valor_linha(self, posicoes)

        if not teste[0]: return teste

        if not resultado[0]: return resultado

        if resultado[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  resultado[1]) 

        listaItensDeclarar = []
        for posicao in range(int(posicoes)):
            listaItensDeclarar.append(['', 'string'])

        self.dic_variaveis[variavel] = [listaItensDeclarar, 'lista']
        return [True, None, 'vazio', 'fazerNada']

    def funcao_declarar_listas(self, variavel, itens ):
        Run.log(self, 'Função declarar listas: "{}"'.format(variavel + str(itens) ))

        if itens == '' or variavel == '':
            return [False, Run.msg_idioma(self, "variavel_posicao_nao_informada"), 'string', 'exibirNaTela']

        variavel = variavel.strip()

        teste = Run.analisa_padrao_variavel(self, variavel)
        testa = Run.verifica_se_tem(self, itens, ', ')

        if not teste[0]: return teste

        if testa != []:
            listaItens = []
            anterior = 0

            for valorItem in testa:
                if len(itens[anterior : valorItem[0]]) > 0:
                    listaItens.append( itens[anterior : valorItem[0]] )

                anterior = valorItem[1]

            if len(itens[anterior : ]) > 0:
                listaItens.append( itens[anterior : ] )

            listaItensDeclarar = []

            for item in listaItens:
                obterValor = Run.abstrair_valor_linha(self, item)

                if obterValor[0] == False:
                    return [obterValor[0], obterValor[1], obterValor[2], 'exibirNaTela']

                listaItensDeclarar.append([obterValor[1], obterValor[2]])

            self.dic_variaveis[variavel] = [listaItensDeclarar, 'lista']
            return [True, None, 'vazio', 'fazerNada']

        else:
            obterValor = Run.abstrair_valor_linha(self, itens)
            if obterValor[0] == False:
                return [obterValor[0], obterValor[1], obterValor[2], 'exibirNaTela']
            lista = []
            lista.append([obterValor[1], obterValor[2]])

            self.dic_variaveis[variavel] = [lista, 'lista']
            return [True, None, 'vazio', 'fazerNada']

    def funcao_ovalor_digitado(self, linha):
        Run.log(self, 'Função digitado: "{}"'.format(linha))

        textoOriginal = len(self.tx_terminal.get(1.0, END))

        self.tx_terminal.config(state=NORMAL)

        self.esperar_pressionar_enter = True

        while self.esperar_pressionar_enter:

            try:
                self.tx_terminal.get(1.0, 1.1)

                if self.aconteceu_erro:
                    return [False, "Interrompido","string","exibirNaTela"]
                else:
                    self.tx_terminal.update()

            except:
                return [False, 'indisponibilidade_terminal', 'string','exibirNaTela']

        digitado = self.tx_terminal.get(1.0, END)
        self.tx_terminal.config(state=DISABLED)
        digitado = digitado[textoOriginal-1:-2]
        digitado = digitado.replace("\n","")

        # SE FOR NUMÉRICO
        if 'numero ' in linha:
            try:
                float(digitado)
            except:
                return[False, '{} "{}"'.format(Run.msg_idioma(self, "digitou_caractere"), digitado), 'string', 'fazerNada']
            else:
                return [True, float(digitado), 'float', 'fazerNada']
        else:
            return [True, digitado, 'string', 'fazerNada']

    def funcao_limpar_o_termin(self):
        Run.log(self, 'Limpatela ativado!')
        self.tx_terminal.config(state=NORMAL)
        self.tx_terminal.delete(1.0, END)
        self.tx_terminal.config(state=DISABLED)
        return [True, None, 'vazio','fazerNada']

    def funcao_repetir_n_vezes(self, linha):
        Run.log(self, "funcao repetir: '{}'".format(linha))

        linha = linha.replace('vezes', '')
        linha = linha.replace('vez', '')
        linha = linha.strip()
        linha = Run.abstrair_valor_linha(self, linha)

        if not linha[0]: return [linha[0], linha[1], linha[2], 'exibirNaTela']

        if linha[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  linha[1]) 

        try:
            int(linha[1])
        except:
            return [False, '{} "{}"'.format(Run.msg_idioma(self, "repetir_nao_informou_inteiro"), linha[1]), 'string', 'exibirNaTela']
        else:
            funcao_repita = int(linha[1])
            return [True, funcao_repita, 'float', 'declararLoopRepetir']

    def funcao_numer_aleatorio(self, num1, num2):
        Run.log(self,  'funcao aleatório: {}'.format(num1))

        num1 = Run.abstrair_valor_linha(self, num1)
        num2 = Run.abstrair_valor_linha(self, num2)

        if not num1[0]: return num1
        if not num2[0]: return num2

        try:
            int(num1[1])
        except:
            return [False, Run.msg_idioma(self, "aleatorio_valor1_nao_numerico"), 'string', 'exibirNaTela']

        try:
            int(num2[1])
        except:
            return [False, Run.msg_idioma(self, "aleatorio_valor2_nao_numerico"), 'string', 'exibirNaTela']

        n1 = int(num1[1])
        n2 = int(num2[1])

        if n1 == n2:
            return [False, Run.msg_idioma(self, "aleatorio_valor1_igual_valo2"), 'string', 'exibirNaTela']

        elif n1 > n2:
            return [False, Run.msg_idioma(self, "aleatorio_valor1_maior_valo2"), 'string', 'exibirNaTela']

        return [True, randint(n1, n2), 'float', 'fazerNada']

















    def funcao_declarar_funcao(self, nomeDaFuncao, parametros=None):
        Run.log(self, 'funcao_declarar_funcao. Nome: {}, Parametros: {}'.format(nomeDaFuncao, parametros))

        # Se o nome da função não está no padrão
        teste = Run.analisa_padrao_variavel(self, nomeDaFuncao)
        if not teste[0]:
            return teste

        # Se não tem parâmetros
        if parametros is None:
            self.dic_funcoes[nomeDaFuncao] = {'parametros':None, 'bloco':'bloco'}

            return [True, True, 'booleano', 'declararFuncao', nomeDaFuncao]


        # Verifica se tem mais de um parâmetro
        testa = Run.verifica_se_tem(self, parametros, ', ')

        # Tem mais de um parametro
        if testa != []:
            listaParametros = []
            anterior = 0

            for valorItem in testa:
                if parametros[anterior : valorItem[0]]:
                    listaParametros.append(parametros[ anterior : valorItem[0]])
                anterior = valorItem[1]

            if len( parametros[anterior : ]) > 0:
                listaParametros.append(parametros[ anterior : ])

            listaFinalDeParametros = []
            for parametro in listaParametros:
                listaFinalDeParametros.append(parametro.strip())

                teste = Run.analisa_padrao_variavel(self, parametro.strip())
                if not teste[0]: return teste

            # Adicionar Função
            self.dic_funcoes[nomeDaFuncao] = {'parametros':listaFinalDeParametros, 'bloco':'bloco'}

        # Não multiplos parâmetros
        else:

            # Verifica se o parâmetro está no padrão
            teste = Run.analisa_padrao_variavel(self, parametros)
            if not teste[0]:
                return teste

            # Adicionar Função
            self.dic_funcoes[nomeDaFuncao] = {'parametros':[parametros], 'bloco':'bloco'}

        funcao_em_analise = nomeDaFuncao
        return [True, True, 'booleano', 'declararFuncao',funcao_em_analise]





    def funcao_executar_funcao(self, nomeDaFuncao, parametros = None):
        try:
            self.dic_funcoes[nomeDaFuncao]
        except:
            return [False, Run.msg_idioma(self, "funcao_nao_existe").format(nomeDaFuncao), 'string', 'exibirNaTela']

        # Se não veio parâmetros
        if parametros is None:

            # Se a função tem parâmetros
            if self.dic_funcoes[nomeDaFuncao]['parametros'] != None:
                return [False, Run.msg_idioma(self, "funcao_nao_passou_parametros").format( nomeDaFuncao,  len(self.dic_funcoes[nomeDaFuncao]['parametros'])), 'string', 'exibirNaTela']

            resultadoOrquestrador = Run.orquestrador_interpretador(self, self.dic_funcoes[nomeDaFuncao]['bloco'])

            if not resultadoOrquestrador[0]:
                return [resultadoOrquestrador[0], resultadoOrquestrador[1], resultadoOrquestrador[2], 'exibirNaTela']
            return [True, None, 'vazio', 'fazerNada']


        # Não tem multiplos parâmetros
        testa = Run.verifica_se_tem(self, parametros, ',')
        if testa != []:
            anterior = 0
            listaParametros = []

            # Anda pelos valores
            for valorItem in testa:

                # Obtem os parâmetros
                if len(parametros[anterior : valorItem[0]]) > 0:
                    listaParametros.append( parametros[anterior : valorItem[0]] )
                    anterior = valorItem[1]

            if len(parametros[anterior : ]) > 0:
                listaParametros.append( parametros[anterior : ] )

            listaFinalDeParametros = []

            # Anda pelos parâmetros
            for parametro in listaParametros:
                listaFinalDeParametros.append(parametro.strip())

            # Se a quantidade de itens for a mesma dessa funcao
            if len(self.dic_funcoes[nomeDaFuncao]['parametros']) == len(listaFinalDeParametros):

                for parametroDeclarar in range(len(self.dic_funcoes[nomeDaFuncao]['parametros'])):
                    resultado = Run.funcao_realizar_atribu(self, self.dic_funcoes[nomeDaFuncao]['parametros'][parametroDeclarar], listaFinalDeParametros[parametroDeclarar])

                    if resultado[0] == False:
                        return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
            else:
                return [False, Run.msg_idioma(self, "funcao_tem_parametros_divergentes").format(nomeDaFuncao, len(self.dic_funcoes[nomeDaFuncao]['parametros']), len(listaFinalDeParametros)), 'string', 'fazerNada']

        elif parametros is not None:

            if len(self.dic_funcoes[nomeDaFuncao]['parametros']) == 1:
                resultado = Run.funcao_realizar_atribu(self, self.dic_funcoes[nomeDaFuncao]['parametros'], parametros)

                if not resultado[0]: return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
            else:
                return [False, Run.msg_idioma(self, "funcao_passou_um_parametros").format(nomeDaFuncao, len(self.dic_funcoes[nomeDaFuncao]['parametros'])), 'string', 'exibirNaTela']

        resultadoOrquestrador = Run.orquestrador_interpretador(self, self.dic_funcoes[nomeDaFuncao]['bloco'])

        if not resultadoOrquestrador[0]:
            return [resultadoOrquestrador[0], resultadoOrquestrador[1], resultadoOrquestrador[2], 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']



































    def funcao_exibir_outra_ln(self, linha):
        Run.log(self, 'funcao exibição: {}'.format(linha))

        resultado = Run.abstrair_valor_linha(self, linha)
        if not resultado[0]: return resultado

        resultado[1] = str(resultado[1]).replace("\\n","\n")
        return [resultado[0], resultado[1], resultado[2],'exibirNaTela']

    def funcao_exibir_mesma_ln(self, linha):
        Run.log(self, 'Função exibir nessa linha ativada'.format(linha))

        resultado = Run.abstrair_valor_linha(self, linha)
        if not resultado[0]: return resultado

        resultado[1] = str(resultado[1]).replace("\\n","\n")
        return [ resultado[0], ':nessaLinha:' + str(resultado[1]), resultado[2], 'exibirNaTela' ]

    def funcao_esperar_n_tempo(self, tempo, tipo_espera):
        Run.log(self, 'Função tempo: {}'.format(tempo))

        resultado = Run.abstrair_valor_linha(self, tempo)
        if not resultado[0]: return resultado

        if tipo_espera == "segundos" or tipo_espera == "s" or tipo_espera == "segundo":
            sleep(resultado[1])

        elif tipo_espera == "milisegundos" or tipo_espera == "ms" or tipo_espera == "milisegundo":
            sleep(resultado[1]/1000)

        return [True, None, 'vazio', 'fazerNada']

    def obter_valor_string(self, string):
        Run.log(self, 'Obter valor de uma string: {}'.format(string))

        valorFinal = ''
        anterior = 0

        for valor in finditer("""\"[^"]*\"""", string):

            abstrair = Run.abstrair_valor_linha(self, 
                string[anterior:valor.start()])

            if not abstrair[0]: return abstrair

            valorFinal = valorFinal + str( abstrair[1] ) + string[ valor.start()+1:valor.end() -1 ]
            anterior = valor.end()

        abstrair = Run.abstrair_valor_linha(self, string[anterior:])
        if not abstrair[0]: return abstrair

        valorFinal = valorFinal + str(abstrair[1])

        return [True, valorFinal, 'string']

    def localiza_transforma_variavel(self, linha):
        Run.log(self, 'localiza_transforma_variavel: {}'.format(linha))

        anterior = 0
        normalizacao = 0
        linha_base = linha
        tipos_obtidos = []

        for valor in finditer(' ', linha_base):
            palavra = linha[anterior : valor.start() + normalizacao]

            if palavra.isalnum() and palavra[0].isalpha():

                variavelDessaVez = Run.abstrair_valor_linha(self, palavra)

                if not variavelDessaVez[0]: return variavelDessaVez

                tipos_obtidos.append(variavelDessaVez[2])
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
        Run.log(self, 'Fazer contas: {}'.format(linha))

        # Do maior para o menor
        linha = linha.replace(' multiplicado por ', ' * ')
        linha = linha.replace(' dividido por ', ' / ')
        linha = linha.replace(' multiplique ', ' * ')
        linha = linha.replace(' elevado por ', ' ** ')
        linha = linha.replace(' elevado a ', ' ** ')
        linha = linha.replace(' elevado ', ' ** ')
        linha = linha.replace(' divide ', ' / ')
        linha = linha.replace(' mais ', ' + ')
        linha = linha.replace(' menos ', ' - ')
        linha = linha.replace('true', 'True')
        linha = linha.replace('verdadeiro', 'True')
        linha = linha.replace('verdadeira', 'True')
        linha = linha.replace('verdade', 'True')
        linha = linha.replace('false', 'False')
        linha = linha.replace('falso', 'False')
        linha = linha.replace('mentira', 'False')

        if '"' in linha: return [False, "Isso é uma string", 'string']

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
            return [False, "Não foi possivel realizar a conta, porque não tem nenhum valor aqui. ", 'string']

        # Correção de caracteres
        linha = linha.replace('*  *', '**')
        linha = linha.replace('< =', '<=')
        linha = linha.replace('> =', '>=')
        linha = linha.replace("! =", '!=')

        # Abstrai o valor de todas as variáveis
        linha = Run.localiza_transforma_variavel(self, linha)
        if not linha[0]: return linha

        # Se sobrou texto
        for caractere in linha[1]:
            if str(caractere).isalpha():
                return [False, Run.msg_idioma(self, "nao_possivel_conta_string") + str(linha[1]), 'string']

        # Tente fazer uma conta com isso
        try:
            resutadoFinal = eval(linha[1])
        except Exception as erro:
            return [False, "{} |{}|".format(Run.msg_idioma(self, "nao_possivel_fazer_conta"), linha[1]), 'string']
        else:
            return [True, resutadoFinal, 'float']

    def obter_valor_variavel(self, variavel):
        Run.log(self, 'Obter valor da variável: "{}"'.format(variavel))
        variavel = variavel.strip()
        variavel = variavel.replace('\n', '')

        try:
            self.dic_variaveis[variavel]
        except:
            return [False, "{} '{}'".format(Run.msg_idioma(self, "voce_precisa_definir_variavel"), variavel), 'string', 'fazerNada']
        else:
            return [True, self.dic_variaveis[variavel][0], self.dic_variaveis[variavel][1], 'fazerNada']


    def abstrair_valor_linha(self, possivelVariavel):
        Run.log(self, "Abstrar valor de uma linha inteira com possivelVariavel: '{}'".format(possivelVariavel))

        possivelVariavel = str(possivelVariavel).strip()

        if possivelVariavel.lower() in ['true', 'verdadeiro', 'verdadeira', 'verdade']:
            return [True, 'True', 'booleano']

        if possivelVariavel.lower() in ['false','falso', 'mentira']:
            return [True, 'False', 'booleano']

        if possivelVariavel == '':
            return [True, possivelVariavel, 'string']

        # Caso existam contas entre strings ( Formatação )
        if possivelVariavel[0] == ',':
            possivelVariavel = possivelVariavel[1:]

        # Caso existam contas entre strings ( Formatação )
        if len(possivelVariavel) > 1:

            if possivelVariavel[-1] == ',':
                possivelVariavel = possivelVariavel[0:len(possivelVariavel)-1]

        possivelVariavel = possivelVariavel.strip()

        testa = Run.verifica_se_tem(self, possivelVariavel, ",")
        if testa != []:

            listaLinhas = [ possivelVariavel[ : testa[0][0] ],  possivelVariavel[testa[0][1] : ]]
            listaValores = ''
            for linha in listaLinhas:
                valor = Run.abstrair_valor_linha(self, linha)

                if not valor[0]: return valor

                listaValores += str(valor[1])

            return [True, listaValores, "string"]

        if possivelVariavel[-1] == '"' and possivelVariavel[0] == '"':
            return [True, possivelVariavel[1:-1], 'string']

        if possivelVariavel == '':
            return [True, possivelVariavel, 'string']

        resultado = Run.fazer_contas(self, possivelVariavel)
        if resultado[0]: return resultado

        resultado = Run.comandos_uso_geral(self, possivelVariavel)

        if resultado[0] and resultado[1] != None:
            return resultado

        elif not resultado[0]: return resultado

        testa = Run.verifica_se_tem(self, possivelVariavel, '"')
        if testa != []:
            return Run.obter_valor_string(self, possivelVariavel)

        try:
            float(possivelVariavel)
        except:
            return Run.obter_valor_variavel(self, possivelVariavel)
        else:
            return [True, float(possivelVariavel), 'float']

    def analisa_padrao_variavel(self, variavel):
        variavel = str(variavel)

        variavel = variavel.replace("_","") # _ também é valido

        if not variavel[0].isalpha():
            return [False, Run.msg_idioma(self, "variaveis_comecar_por_letra"), "string", 'exibirNaTela']

        if not variavel.isalnum():
            return [False, Run.msg_idioma(self, "variaveis_devem_conter"), 'string', 'exibirNaTela']

        return [True,True,'booleano']

    def funcao_realizar_atribu(self, variavel, valor):
        Run.log(self, 'Função atribuição: {}'.format(variavel + str(valor)))

        if variavel == '' or valor == '':
            return [False, Run.msg_idioma(self, "variavel_valor_nao_informado"), 'string', 'exibirNaTela']

        teste_padrao = Run.analisa_padrao_variavel(self, variavel)
        if not teste_padrao[0]:
            return teste_padrao

        valor = valor.replace('\n', '')
        valor = valor.strip()

        resultado = Run.abstrair_valor_linha(self, valor)
        if not resultado[0]: return resultado

        if resultado[0]:
            self.dic_variaveis[variavel] = [resultado[1], resultado[2]]
            return [True, None, 'vazio', 'fazerNada']

        return [ resultado[0], resultado[1], resultado[2], 'fazerNada']

    def funcao_loops_enquantox(self, linha):
        Run.log(self, 'Função loops enquanto: {}'.format(linha))
        resultado = Run.funcao_testar_condicao(self, linha)
        return [resultado[0], resultado[1], resultado[2], 'declararLoop']

    def tiver_valor_lista(self, linha):
        Run.log(self, 'Função condicional: {}'.format(linha))

        linha = linha.strip()

        analisa021 = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha)
        if analisa021[0]:
            return Run.funcao_tiver_valor_lst(self, analisa021[1][2],analisa021[1][4])

        return [True,None,'booleano']

    def verifica_se_tem(self, linha, a_buscar):
        analisar = True
        lista = []

        for caractere in range(len(linha)):
            if linha[caractere] == '"' and analisar == True:
                analisar = False

            elif linha[caractere] == '"' and analisar == False:
                analisar = True

            if analisar:
                if len(linha) >= caractere + len(a_buscar):

                    if linha[caractere : caractere + len(a_buscar) ] == a_buscar:
                        lista.append([caractere, caractere + len(a_buscar) ])

        return lista

    def funcao_testar_condicao(self, linha):
        Run.log(self, 'Função condicional: {}'.format(linha))

        # Padronização geral
        linha = linha.replace(' for maior ou igual a ', ' >= ')
        linha = linha.replace(' for menor ou igual a ', ' <= ')
        linha = linha.replace(' for diferente de ', ' != ')
        linha = linha.replace(' for maior que ', ' > ')
        linha = linha.replace(' for menor que ', ' < ')
        linha = linha.replace(' for igual a ', ' == ')
        linha = linha.replace(' e ' , '  and  ')
        linha = linha.replace(' && ', '  and  ')
        linha = linha.replace(' ou ', '  or  ')
        linha = linha.replace(' || ', '  or  ')

        # Adicionando um espaço
        linha = ' ' + str(linha) + ' '

        # Todos os caracteres especiais de
        simbolosEspeciais = ['>=', '<=', '!=', '>', '<', '==', '(', ')',' and ', ' or ',' tiver ']

        qtd_simbolos_especiais = 0

        # Deixando todos os itens especiais com espaço em relação aos valores
        for item in simbolosEspeciais:

            # Se tiver o simbolo especial na linha, some +1
            if item in linha:

                qtd_simbolos_especiais += 1

                # Adiciona espaço para cada simbolos
                linha = linha.replace(item, '  {}  '.format(item))

        # Se não tiver nenhuma operação a fazer
        #if qtd_simbolos_especiais == 0:
        #    return [False, Run.msg_idioma(self, "condicao_nao_possui_condicao"), 'string', 'exibirNaTela']

        # Coreção de bugs ao usar o recurso de deixar espaços
        linha = linha.replace('* *', '**')
        linha = linha.replace('> =', '>=')
        linha = linha.replace('< =', '<=')
        linha = linha.replace('! =', '!=')
        linha = linha.replace('   tiver   ',' tiver ')

        linha = linha.strip()
        simbolosArrumados = [' >= ', ' <= ', ' != ', ' > ', ' < ', ' == ', ' ( ', ' ) ',' and ', ' or ']

        # Marcar os simbolos para correta captura do regex
        for simbolo in range(len(simbolosArrumados)):

            linha = linha.replace(
                simbolosArrumados[simbolo],'_._' + simbolosArrumados[simbolo] + '_._')

        linha = linha.replace('_._ < _._ =','_._ <= _._')
        linha = linha.replace('_._ > _._ =','_._ >= _._')

        # Usando Regex para isolar os simbolos
        anterior = 0
        final = ''

        for item in finditer("_\\._[^_]*_\\._", linha):

            # Abstrai um valor qual
            resultado = Run.abstrair_valor_linha(self, linha[anterior:item.start()])

            if resultado[0] == False: return resultado

            saida = resultado[1]

            if resultado[2] == 'string':
                saida = '"' + resultado[1] + '"'

            # Reover marcadores de simbolos
            final += str(saida) + linha[item.start() + 3:item.end() - 3]

            anterior = item.end()

        boolTemTiverLista = False
        resultado = Run.tiver_valor_lista(self, linha[anterior:].strip())

        if not resultado[0]: return resultado

        if resultado[2] == 'booleano':

            if resultado[1] == 'sim':
                final += ' True '
                boolTemTiverLista = True

            elif resultado[1] == 'nao':
                final += ' False '
                boolTemTiverLista = True

        if not boolTemTiverLista:

            resultado = Run.abstrair_valor_linha(self, linha[anterior:])
            if not resultado[0]: return resultado

            saida = resultado[1]
            if resultado[2] == 'string':
                saida = '"' + resultado[1] + '"'

            final += str(saida)

        # Tente fazer a condição com isso
        try:
            resutadoFinal = eval(final)

        except Exception as erro:
            return [False, "{} |{}|".format(Run.msg_idioma(self, "nao_possivel_fazer_condicao"), final), 'string', 'exibirNaTela']

        else:
            return [True, resutadoFinal, 'booleano', 'declararCondicional']

