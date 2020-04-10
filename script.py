#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Futuro
    [ ] Copiar código na Wiki na área de transferência
    [ ] lista posto na posicao i ate a posicao 3 no passo de 2


    Ambiente:
    Windows 10, Ubuntu 19.10, Kali Linux
    Sublime text 3
    color Schema = Dracula
    Theme = Darkmatter
"""

from tkinter.font import nametofont
from threading import Thread
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import DISABLED
from tkinter import Toplevel
from tkinter import CURRENT
from tkinter import INSERT
from tkinter import Button
from tkinter import NORMAL
from tkinter import RAISED
from tkinter import SUNKEN
from tkinter import Frame
from tkinter import Label
from tkinter import FLAT
from tkinter import Menu
from tkinter import NSEW
from tkinter import Text
from tkinter import font
from tkinter import END
from tkinter import Tk
from funcoes import *
from time import sleep
from time import time
from json import load
from random import randint
from os import listdir
from os.path import abspath
from os import getcwd
from re import finditer
from re import findall
from tkinter import N, S, E, W, Entry
import webbrowser

__author__      = 'Gabriel Gregório da Silva'
__email__       = 'gabriel.gregorio.1@outlook.com'
__project__     = 'Combratec'
__github__      = 'https://github.com/Combratec/'
__description__ = 'Linguagem de programação focada em lógica'
__status__      = 'Desenvolvimento'
__date__        = '01/08/2019'
__last_update__ = '05/04/2020'
__version__     = '0.1'

global dic_info_arquivo
global bool_tela_em_fullscreen
global aconteceu_erro
global lst_titulos_frames
global fr_ajuda
global numero_threads
global altura_widget
global tx_terminal
global tx_codficac
global dic_funcoes
global dic_variaveis
global lb_linhs
global dic_design
global cor_do_comando
global top_janela_terminal
global erro_alertado
global posCorrente
global bool_logs
global posAbsuluta
global boo_orquestrador_iniciado

numero_threads = 0
bool_tela_em_fullscreen = False
lst_titulos_frames = []
bool_logs = True
aconteceu_erro = False
dic_info_arquivo = {'link': None,'texto': None}
dic_variaveis = {}
dic_funcoes = {}
posAbsuluta = 0
posCorrente = 0
path = abspath(getcwd())

class Run():
    def __init__(self):
        self.aconteceu_erro = False
        self.erro_alertado = False
        self.esperar_pressionar_enter = False
        self.dic_variaveis = {}
        self.dic_funcoes = {}

    def orq_erro(self, mensagem, linhaAnalise):
        self.aconteceu_erro = True

        if not self.erro_alertado:
            tx_terminal.insert(END, "\n" + "[" + linhaAnalise + "] " + mensagem)
            realiza_coloracao_erro('codigoErro', valor1=0, valor2=len(mensagem)+1, cor='#ffabab', linhaErro = linhaAnalise )

    def orq_exibir_tela(self, lst_retorno_ultimo_comando):
        global tx_terminal
        
        try:
            if ":nessaLinha:" in str(lst_retorno_ultimo_comando[1]):
                tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1][len(":nessaLinha:"):]))
            else:
                tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1])+'\n')

            tx_terminal.see("end")

        except Exception as erro:
            print('ERRO:', erro)
            return [[False, 'indisponibilidade_terminal', 'string','exibirNaTela'], "1"]

    def orquestrador_interpretador(self, txt_codigo):
        global numero_threads
        global boo_orquestrador_iniciado

        
        log('<orquestrador_interpretador>:' + txt_codigo)

        int_tamanho_codigo = len(txt_codigo)
        boo_orquestrador_iniciado = True
        bool_comentario_longo = False
        bool_salvar_bloco = False
        bool_comentario = False
        bool_texto = False
        numero_threads += 1

        str_bloco = ""
        str_linha = ""
        caractere = ""

        int_profundidade = 0
        for int_cont, caractere in enumerate(txt_codigo):
            
            dois_caracteres = txt_codigo[int_cont : int_cont + 2]

            # Ignorar tudo entre /**/
            if dois_caracteres == '/*' and not bool_texto and not bool_comentario:
                bool_comentario_longo = True
                continue

            if bool_comentario_longo and txt_codigo[int_cont - 2:int_cont] == '*/':
                bool_comentario_longo = False
              
            if bool_comentario_longo:
                continue

            # Ignorar comentário
            if( caractere == '#' or dois_caracteres == '//') and not bool_texto:
                bool_comentario = True

            if bool_comentario and caractere == "\n":
                bool_comentario = False

            elif bool_comentario:
                continue

            # Se chegar no fim da linha ou iniciar um bloco
            if ( caractere == "\n" or ( caractere == "{" and not bool_comentario) ) and not bool_salvar_bloco and not bool_texto :

                if len(str_linha.strip()) > 0:
                    str_linha = str_linha.replace("\n","").strip()

                    lst_analisa = Run.interpretador(self, str_linha)

                    if lst_analisa[0][3] == 'linhaVazia':
                        str_linha = ""

                    else:
                        lst_ultimo_ret = lst_analisa
                        comando_testado = str_linha
                        linhaAnalise = lst_ultimo_ret[1]
                        lst_ultimo_ret = lst_ultimo_ret[0]

                        if lst_ultimo_ret[0] == False:

                            if lst_ultimo_ret[1] == 'indisponibilidade_terminal':
                                numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_ultimo_ret[1], linhaAnalise)
                            numero_threads -= 1
                            return lst_ultimo_ret

                        if lst_ultimo_ret[3] == 'exibirNaTela':
                            Run.orq_exibir_tela(self, lst_ultimo_ret)

                        str_linha = ""

                        if caractere == "\n" and lst_ultimo_ret[3] == 'fazerNada':
                            continue

            # Quando começar uma string
            if caractere == '"' and not bool_texto and not bool_comentario and not bool_salvar_bloco:
                bool_texto = True

            elif caractere == '"' and bool_texto and not bool_comentario and not bool_salvar_bloco:
                bool_texto = False

            # Quando começar um bloco
            if caractere == "{" and not bool_texto and not bool_comentario:
                int_profundidade += 1
                bool_salvar_bloco = True

            elif caractere == "}" and not bool_texto and not bool_comentario:
                int_profundidade -= 1

            # Quando finalizar um bloco
            if caractere == "}" and not bool_texto and not bool_comentario and int_profundidade == 0:
                log('!<Analisa bloco salvo>:"' + str_bloco + '"')

                bool_salvar_bloco = False

                if lst_ultimo_ret[3] == 'declararLoop':

                    # Enquanto a condição for verdadeira
                    while lst_ultimo_ret[1] and not self.aconteceu_erro:

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, 
                            str_bloco[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_resultado_execucao[1], linhaAnalise)
                            numero_threads -= 1
                            return lst_resultado_execucao

                        # Testa novamente a condição do loo
                        lst_ultimo_ret = Run.interpretador(self, comando_testado)
                        linhaAnalise = lst_ultimo_ret[1]
                        lst_ultimo_ret = lst_ultimo_ret[0]

                        if lst_ultimo_ret[0] == False:

                            if lst_ultimo_ret[1] == 'indisponibilidade_terminal':
                                    numero_threads -= 1
                                    return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_ultimo_ret[1], linhaAnalise)
                            numero_threads -= 1
                            return lst_ultimo_ret

                elif lst_ultimo_ret[3] == "declararLoopRepetir":
                    lst_ultimo_ret[3] = 'fazerNada'

                    for valor in range(0, lst_ultimo_ret[1]):
                        lst_resultado_execucao = Run.orquestrador_interpretador(self, 
                            str_bloco[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_resultado_execucao[1], linhaAnalise)
                            numero_threads -= 1
                            return lst_resultado_execucao

                    lst_ultimo_ret[1] = 0
                    lst_ultimo_ret = [True, False, 'booleano']

                elif lst_ultimo_ret[3] == "declararFuncao":
                    lst_ultimo_ret[3] = "fazerNada"
                    self.dic_funcoes[lst_ultimo_ret[4]] = [self.dic_funcoes[lst_ultimo_ret[4]][0], str_bloco[1:].strip()]

                elif lst_ultimo_ret[3] == 'declararCondicional':
                    if lst_ultimo_ret[1] == True:

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, str_bloco[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_resultado_execucao[1], linhaAnalise)
                            numero_threads -= 1
                            return lst_resultado_execucao

                str_bloco = ""
                continue

            # Se for para salvar bloco, salve o caractere
            if bool_salvar_bloco:
                str_bloco += caractere

            # Armazene os comandos
            elif not bool_comentario:
                str_linha += caractere

        # Se chegar no final do código e tiver comando para analisar
        if len(str_linha.strip()) > 0 and int_tamanho_codigo -1 == int_cont:

            str_linha = str_linha.replace("\n","").strip()
            lst_ultimo_ret = Run.interpretador(self, str_linha)
            comando_testado = str_linha
            linhaAnalise = lst_ultimo_ret[1]
            lst_ultimo_ret = lst_ultimo_ret[0]

            if lst_ultimo_ret[0] == False:
                if lst_ultimo_ret[1] == 'indisponibilidade_terminal':
                    numero_threads -= 1
                    return [True, 'Orquestrador Finalizado', 'string']

                Run.orq_erro(self, lst_ultimo_ret[1], linhaAnalise)
                numero_threads -= 1
                return lst_ultimo_ret

            if lst_ultimo_ret[3] == 'exibirNaTela':
                Run.orq_exibir_tela(self, lst_ultimo_ret)

        # Aviso de erros de profundidade
        if int_profundidade > 0:
            numero_threads -= 1
            return [False, None, 'vazia']

        elif int_profundidade < 0:
            numero_threads -= 1
            return [False, None, 'vazia']

        numero_threads -= 1
        return [True, 'Orquestrador Finalizado', 'string']

    def analisa_instrucao(self, comando, texto, grupos_analisar):

        re_comandos = "(\\<[a-zA-Z]*\\>)"
        re_groups = findall(re_comandos, comando)
        if re_groups == None:
            return False

        dic_options = {}
       
        # Anda pelos grupos <se>, <esperar>
        for grupo in re_groups:

            # Anda pelos comandos no dicionários, [se], [if]...
            for n_comando in range(0, len(dic_comandos[ grupo[1:-1] ])):

                # Obtem um comando. se, if
                txt_comando_analisar = dic_comandos[ grupo[1:-1] ][n_comando][0]

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

        # Aplicar no texto
        re_texto = findall(comando, texto)
        if re_texto == []:
            return False

        re_texto= re_texto[0]
        lst_retorno = []
        for n_grupo in grupos_analisar:
            lst_retorno.append(re_texto[n_grupo-1].strip())

        return lst_retorno

    def interpretador(self, linha):
        log('Interpretador iniciado')
        global tx_terminal

        try:
            tx_terminal.get(1.0, 1.1)
        except:
            return [[False, 'indisponibilidade_terminal', 'string','exibirNaTela'], "1"]

        if self.aconteceu_erro:
            return [[False, 'Erro ao iniciar o Interpretador', 'string','exibirNaTela'], "1"]

        linha = linha.replace('\n', '')
        linha = linha.strip()

        # Se for uma linha vazia
        if linha == '': return [ [True, None, 'vazio','linhaVazia'], "1" ]

        else:
            num_linha = "0"
            posicoes = finditer(r'^(\[\d*\])', linha)

            # Obter o número da linha
            for uma_posicao in posicoes:
                num_linha = linha[1 : uma_posicao.end()-1]
                linha = linha[uma_posicao.end() : ]
                linha = linha.strip()
                break

            if linha == '':
                return [[True, None, 'vazio','linhaVazia'], "1"]

            analisa = Run.analisa_instrucao(self, '^(<limpatela>)$', linha, grupos_analisar = [1])
            if analisa: return [ Run.funcao_limpar_tela(self, ), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<mostreNessa>)(.*)$', linha, grupos_analisar = [2])
            if analisa: return [ Run.funcao_exibir_na_linha(self, analisa[0]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<mostre>)(.*)$', linha, grupos_analisar = [2])
            if analisa: return [ Run.funcao_exibir(self, analisa[0]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<se>)(.*)$', linha, grupos_analisar = [2])
            if analisa: return [ Run.funcao_condicional(self, analisa[0]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<enquanto>)(.*)$', linha, grupos_analisar = [2])
            if analisa: return [ Run.funcao_loops_enquanto(self, analisa[0]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<aguarde>)(.*)(<esperaEm>)$', linha, grupos_analisar = [2,3])
            if analisa: return [ Run.funcao_tempo(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<repita>)(.*)(<repitaVezes>)$', linha, grupos_analisar = [2])
            if analisa: return [ Run.funcao_repetir(self, analisa[0]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<incremente>)(.*)(<incrementeDecremente>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.incremente_em(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<decremente>)(.*)(<incrementeDecremente>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.decremente_em(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<funcoes>)(.*)(<recebeParametros>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_declarar_funcao(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaNaPosicao>)(.*)(<recebeDeclaraListas>)(.*)$', linha, grupos_analisar = [2, 4, 6])
            if analisa: return [ Run.funcao_adicione_na_lista_na_posicao(self, analisa[0], analisa[1], analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaCom>)(.*)(<listaPosicoesCom>)$', linha, grupos_analisar = [2,4])
            if analisa: return [ Run.funcao_declarar_listas_posicoes(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<recebeDeclaraListas>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_declarar_listas(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<RemoverItensListas>)(.*)(<RemoverItensListasInterno>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_remover_itens_na_lista(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoPosicao>)(.*)(<addItensListaInternoPosicaoFinaliza>)(.*)$', linha, grupos_analisar = [2, 4, 6])
            if analisa: return [ Run.funcao_adicionar_itens_na_lista_posicao(self, analisa[0], analisa[1], analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoFinal>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_adicionar_itens_na_lista(self, analisa[0], analisa[1]), num_linha ]
                
            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoInicio>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_adicionar_itens_na_lista_inicio(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInterno>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_adicionar_itens_na_lista(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_numero_aleatorio(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_obter_valor_lista(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<digitado>)$', linha, grupos_analisar = [1])
            if analisa: return [ Run.funcao_digitado(self, analisa[0]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha, grupos_analisar = [2, 4])
            if analisa: return [ Run.funcao_tiver_na_lista(self, analisa[0],analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', linha, grupos_analisar = [2])
            if analisa:return [ Run.funcao_tamanho_da_lista(self, analisa[0]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(\\s*[a-zA-Z\\_]*)(<declaraVariaveis>)(.*)$', linha, grupos_analisar = [1, 3])
            if analisa: return [ Run.funcao_fazer_atribuicao(self, analisa[0], analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(.*)(<passandoParametros>)(.*)$', linha, grupos_analisar = [1,3])
            if analisa: return [ Run.funcao_executar_funcoes(self, analisa[0],analisa[1]), num_linha ]

            return [ [False, "Um comando desconhecido foi localizado: '{}'".format(linha), 'string','exibirNaTela'], num_linha ]
        return [ [True, None, 'vazio', 'fazerNada'], num_linha ]

    def comandos_uso_geral(self, possivelVariavel):
        log('comandos_uso_geral: {}'.format(possivelVariavel))

        possivelVariavel = str(possivelVariavel).strip()

        analisa = Run.analisa_instrucao(self, '^(<digitado>)$', possivelVariavel, grupos_analisar = [1])
        if analisa: return Run.funcao_digitado(self, analisa[0])

        analisa = Run.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$',  possivelVariavel, grupos_analisar = [2, 4])
        if analisa: return Run.funcao_numero_aleatorio(self, analisa[0], analisa[1])

        analisa = Run.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', possivelVariavel, grupos_analisar = [2, 4])
        if analisa: return Run.funcao_obter_valor_lista(self, analisa[0], analisa[1])

        analisa = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', possivelVariavel, grupos_analisar = [2, 4])
        if analisa: return Run.funcao_tiver_na_lista(self, analisa[0],analisa[1])

        analisa = Run.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', possivelVariavel, grupos_analisar = [2])
        if analisa: return Run.funcao_tamanho_da_lista(self, analisa[0])

        return [True, None, 'vazio']

    def incremente_em(self, valor, variavel):
        return Run.incremente_decremente(self, valor, variavel,  'incremente')

    def decremente_em(self, valor, variavel):
        return Run.incremente_decremente(self, valor, variavel, 'decremente')

    def msg_variavel_numerica(self, msg, variavel):
        if msg == 'naoNumerico':
            return [False, "A variável '{}' não é numérica!".format(variavel), 'string', 'exibirNaTela']

    def incremente_decremente(self, valor, variavel, acao):
        log('decremente:' + valor+str(variavel))

        teste_existencia = Run.obter_valor_variavel(self, variavel)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if teste_existencia[0] == False:
            return teste_existencia

        if teste_valor[0] == False:
            return teste_valor

        if teste_existencia[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico', variavel)

        if teste_valor[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico', teste_valor[1])

        if acao == "incremente":
            self.dic_variaveis[ variavel ][0] = self.dic_variaveis[ variavel ][0] + teste_valor[1]

        else:
            self.dic_variaveis[ variavel ][0] = self.dic_variaveis[ variavel ][0] - teste_valor[1]

        return [True, True, "booleano", "fazerNada"]

    def funcao_adicione_na_lista_na_posicao(self, variavelLista, posicao, valor):
        log('funcao_adicione_na_lista_na_posicao:' + str(variavelLista))

        if variavelLista == '' or posicao == '' or valor == '': # Veio sem dados
            return [ False, 'Necessário comando separador como " no meio da lista de "', 'string',' exibirNaTela']

        teste_existencia = Run.obter_valor_variavel(self, variavelLista)
        testePosicao = Run.abstrair_valor_linha(self, posicao)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if teste_existencia[0] == False:
            return teste_existencia

        if testePosicao[0] == False:
            return testePosicao

        if teste_valor[0] == False:
            return teste_valor

        if teste_existencia[2] != 'lista':
            return[False, 'A variável "{}" não é uma lista.'.format(variavelLista), 'string']

        if testePosicao[2] != 'float':
            return  Run.msg_variavel_numerica(self, 'naoNumerico',  testePosicao[1])

        posicao = int(testePosicao[1])

        # Posição estoura posições da lista
        if posicao - 1 > len(self.dic_variaveis[variavelLista][0]):
            return [False, 'A posição está acima do tamanho da lista', 'string', 'exibirNaTela']

        if posicao < 1 :
            return [False, 'A posição está abaixo do tamanho da lista', 'string', 'exibirNaTela']


        self.dic_variaveis[variavelLista][0].insert(posicao - 1, [teste_valor[1], teste_valor[2]])
        return [ True, True, 'booleano', 'fazerNada' ]

    def obter_valor_lista(self, linha):
        log('obter_valor_lista ' + str(linha))

        teste = Run.obter_valor_variavel(self, linha)

        if teste[0] == False:
            return teste

        if teste[2] != 'lista':
            return[False, "A variável '{}' não é uma lista.".format(linha), 'string']

        return teste

    def funcao_obter_valor_lista(self, variavel, posicao):
        log('Função Valor de lista: "{}", subcomandos: "{}"'.format(variavel, posicao))

        if variavel == '' or posicao == '':
            return [ False, 'Sem variavel passada','string','exibirNaTela']

        teste_posicao = Run.abstrair_valor_linha(self, posicao)
        teste_variavel = Run.obter_valor_lista(self, variavel)

        if teste_posicao[0] == False:
            return [teste_posicao[0], teste_posicao[1], teste_posicao[2], 'exibirNaTela']

        elif teste_posicao[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  teste_posicao[1]) 

        elif teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        posicao = int(teste_posicao[1])
        resultado = teste_variavel[1]

        if len(resultado) < posicao or posicao < 1:
            return [False, "Posição '{}' está fora do escopo da lista {}".format(posicao, resultado), 'exibirNaTela']

        return [True, resultado[posicao-1][0], resultado[posicao-1][1], 'exibirNaTela']

    def funcao_tiver_na_lista(self, valor, variavel):
        log("Função tiver na lista: " + valor)

        if variavel == '' or valor == '':
            return [False, 'É necessário passar um comando de referência, para indicar o que é valor e o que é variável', 'exibirNaTela']

        teste_variavel = Run.obter_valor_variavel(self, variavel)
        resultado_valor = Run.abstrair_valor_linha(self, valor)

        if teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if teste_variavel[2] != 'lista':
            return [False, 'A variável "{}" não é uma lista.'.format(linha), 'string', 'exibirNaTela']

        if resultado_valor[0] == False:
            return [resultado_valor[0], resultado_valor[1], resultado_valor[2], 'exibirNaTela']

        if [resultado_valor[1], resultado_valor[2]] in self.dic_variaveis[variavel][0]:
            return [True, True, 'booleano', 'fazerNada']

        return [True, False, 'booleano', 'fazerNada']

    def funcao_tamanho_da_lista(self, linha):
        log('Função obter o tamanho da lista: "{}"'.format(linha))

        linha = linha.strip()

        teste = Run.obter_valor_lista(self, linha)
        if teste[0] == False:
            return [teste[0], teste[1], teste[2], 'exibirNaTela']

        try:
            return [True, len(self.dic_variaveis[linha][0]), 'float', 'fazerNada']

        except Exception as erro:
            return [True, 'Erro ao obter o tamanho da lista. Erro: {}'.format(erro), 'string', 'exibirNaTela']

    def funcao_remover_itens_na_lista(self, valor, variavel):
        log('Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Remova 1 a lista de nomes ', 'exibirNaTela']

        # Analisa se lista foi decarada e se é lista
        teste = Run.obter_valor_lista(self, variavel)
        if teste[0] == False:
            return [teste[0], teste[1], teste[2], 'exibirNaTela']

        resultado = Run.abstrair_valor_linha(self, valor)

        if resultado[0] == False:
            return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

        try:
            self.dic_variaveis[variavel][0].remove([resultado[1], resultado[2]])

        except Exception as erro:
            return [ False, '"{}" Não está na lista "{}"!'.format(resultado[1], variavel), 'string', 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']

    def funcao_adicionar_itens_na_lista(self, valor, variavel):
        log('Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Adicione 1 a lista de nomes ', 'exibirNaTela']

        # Analisa se lista foi decarada e se é lista
        teste_variavel = Run.obter_valor_lista(self, variavel)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if teste_valor[0] == False:
            return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

        try:
            self.dic_variaveis[variavel][0].append([teste_valor[1], teste_valor[2]])

        except Exception as erro:
            return [ False, "'{}'' Não está na lista '{}'!".format(teste_valor[1], variavel), 'string', 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']

    def funcao_adicionar_itens_na_lista_inicio(self, valor, variavel):
        log('Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Adicione 1 a lista de nomes ', 'exibirNaTela']

        # Analisa se lista foi decarada e se é lista
        teste_variavel = Run.obter_valor_lista(self, variavel)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if teste_valor[0] == False:
            return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

        try:
            self.dic_variaveis[variavel][0].insert(0, [teste_valor[1], teste_valor[2]])

        except Exception as erro:
            return [ False, '"{}" Não foi possivel inserir o elemento na posição inicial"{}"!'.format(teste_valor[1], variavel), 'string', 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']

    def funcao_adicionar_itens_na_lista_posicao(self, valor, posicao, variavel):
        log('Função remover itens da lista: "{}"'.format(valor))

        if variavel == '' or valor == '':
            return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Adicione 1 a lista de nomes ', 'exibirNaTela']

        teste_variavel = Run.obter_valor_lista(self, variavel)
        teste_posicao = Run.abstrair_valor_linha(self, posicao)
        teste_valor = Run.abstrair_valor_linha(self, valor)

        if teste_variavel[0] == False:
            return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

        if teste_valor[0] == False:
            return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

        if teste_posicao[0] == False:
            return [teste_posicao[0], teste_posicao[1], teste_posicao[2], 'exibirNaTela']

        if teste_posicao[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  teste_posicao[1])

        posicao = int(teste_posicao[1])

        if posicao - 1 > len(self.dic_variaveis[variavel][0]):
            return [False, 'A posição está acima do tamanho da lista', 'string', 'exibirNaTela']

        if posicao < 1 :
            return [False, 'A posição está abaixo do tamanho da lista', 'string', 'exibirNaTela']

        self.dic_variaveis[variavel][0].insert(posicao - 1, [teste_valor[1], teste_valor[2]])
        return [ True, True, 'booleano', 'fazerNada' ]

    def funcao_declarar_listas_posicoes(self, variavel, posicoes):
        log('Função declarar listas posicoes: "{}"'.format(variavel))

        teste = Run.analisa_padrao_variavel(self, variavel, 'Lista ')
        resultado = Run.abstrair_valor_linha(self, posicoes)

        if teste[1] != True:
            return [False, teste[1], teste[2], 'exibirNaTela']

        if resultado[0] == False:
            return resultado

        if resultado[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  resultado[1]) 

        listaItensDeclarar = []
        for posicao in range(int(posicoes)):
            listaItensDeclarar.append(['', 'string'])

        self.dic_variaveis[variavel] = [listaItensDeclarar, 'lista']
        return [True, None, 'vazio', 'fazerNada']

    def funcao_declarar_listas(self, variavel, itens ):
        log('Função declarar listas: "{}"'.format(variavel + str(itens) ))

        if itens == '' or variavel == '':
            return [False, 'É necessário um comando de atribuição ao declar uma lista!', 'string', 'exibirNaTela']

        variavel = variavel.strip()

        teste = Run.analisa_padrao_variavel(self, variavel,'Lista ')
        testa = Run.verifica_se_tem(self, itens, ', ')

        if teste[1] != True:
            return [False, teste[1], teste[2], 'exibirNaTela']

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

    def pressionou_enter(self, event=None):
        if self.esperar_pressionar_enter:
            self.esperar_pressionar_enter = False

    def funcao_digitado(self, linha):
        log('Função digitado: "{}"'.format(linha))

        global tx_terminal

        textoOriginal = len(tx_terminal.get(1.0, END))

        self.esperar_pressionar_enter = True

        while self.esperar_pressionar_enter:

            try:
                tx_terminal.get(1.0, 1.1)

                if self.aconteceu_erro: return [False, "Interrompido","string","exibirNaTela"]
                else: tx_terminal.update()

            except:
                return [False, 'indisponibilidade_terminal', 'string','exibirNaTela']

        digitado = tx_terminal.get(1.0, END)
        digitado = digitado[textoOriginal-1:-2]

        # SE FOR NUMÉRICO
        if ' numero ' in linha:
            try:
                float(digitado)
            except:
                return[False, "Você disse que queria digitar um número, mas digitou um texto '{}'".format(digitado), 'string', 'fazerNada']
            else:
                return [True, float(digitado), 'float', 'fazerNada']
        else:
            return [True, digitado, 'string', 'fazerNada']

    def funcao_limpar_tela(self):
        log('Limpatela ativado!')

        global tx_terminal

        tx_terminal.delete(1.0, END)
        return [True, None, 'vazio','fazerNada']

    def funcao_repetir(self, linha):
        log("funcao repetir: '{}'".format(linha))

        linha = linha.replace('vezes', '')
        linha = linha.replace('vez', '')
        linha = linha.strip()
        linha = Run.abstrair_valor_linha(self, linha)

        if linha[0] == False:
            return [linha[0], linha[1], linha[2], 'exibirNaTela']

        if linha[2] != 'float':
            return Run.msg_variavel_numerica(self, 'naoNumerico',  linha[1]) 

        try:
            int(linha[1])
        except:
            return [False, "Para usar a função repetir, você precisa passar um número inteiro. Você passou '{}'".format(linha[1]), 'string', 'exibirNaTela']
        else:
            funcao_repita = int(linha[1])
          
            return [True, funcao_repita, 'float', 'declararLoopRepetir']

    def funcao_numero_aleatorio(self, num1, num2):
        log( 'funcao aleatório: {}'.format(num1))

        num1 = Run.abstrair_valor_linha(self, num1)
        num2 = Run.abstrair_valor_linha(self, num2)

        if num1[0] == False:
            return [num1[0], num1[1], num1[2], 'exibirNaTela']

        if num2[0] == False:
            return [num2[0], num2[1], num2[2], 'exibirNaTela']

        try:
            int(num1[1])
        except:
            return [False, "O valor 1 não é numérico", 'string', 'exibirNaTela']

        try:
            int(num2[1])
        except:
            return [False, "O valor 2 não é numérico", 'string', 'exibirNaTela']

        n1 = int(num1[1])
        n2 = int(num2[1])

        if n1 == n2:
            return [False, "O valor 1 e o valor 2 da função aleatório tem que ser diferentes", 'string', 'exibirNaTela']

        elif n1 > n2:
            return [False, "O valor 1 é maior que o valor 2, o valor 1 tem que ser maior", 'string', 'exibirNaTela']

        return [True, randint(n1, n2), 'float', 'fazerNada']

    def funcao_executar_funcoes(self, nomeDaFuncao, parametros):

        try:
            self.dic_funcoes[nomeDaFuncao]

        except:
            return [False, "A função '{}' não existe".format(nomeDaFuncao), 'string', 'exibirNaTela']

        testa = Run.verifica_se_tem(self, parametros, ', ')
        if testa != []:
            anterior = 0
            listaDeParametros = []

            for valorItem in testa:
                if len(parametros[anterior : valorItem[0]]) > 0:
                    listaDeParametros.append( parametros[anterior : valorItem[0]] )
                    anterior = valorItem[1]

            if len(parametros[anterior : ]) > 0:
                listaDeParametros.append( parametros[anterior : ] )

            listaFinalDeParametros = []

            for parametro in listaDeParametros:
                listaFinalDeParametros.append(parametro.strip())

            # Se tiver a mesma quantiade de parametros
            if len(self.dic_funcoes[nomeDaFuncao][0]) == len(listaFinalDeParametros):

                for parametroDeclarar in range(len(self.dic_funcoes[nomeDaFuncao][0])):
                    resultado = Run.funcao_fazer_atribuicao(self, self.dic_funcoes[nomeDaFuncao][0][parametroDeclarar], listaFinalDeParametros[parametroDeclarar])

                    if resultado[0] == False:
                        return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
            else:
                return [False, "A função '{}' tem {} parametros, 2mas você passou {} parametros!".format(nomeDaFuncao, len(dic_funcoes[nomeDaFuncao][0]), len(listaFinalDeParametros)), 'string', 'fazerNada']

        elif parametros != None:

            if len(self.dic_funcoes[nomeDaFuncao][0]) == 1:
                resultado = Run.funcao_fazer_atribuicao(self, self.dic_funcoes[nomeDaFuncao][0], parametros)

                if resultado[0] == False:
                    return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
            else:
                return [False, "A função '{}' tem {} parametros, mas você passou 1 parametro!".format(nomeDaFuncao, len(dic_funcoes[nomeDaFuncao][0])), 'string', 'exibirNaTela']

        resultadoOrquestrador = Run.orquestrador_interpretador(self, self.dic_funcoes[nomeDaFuncao][1])

        if resultadoOrquestrador[0] == False:
            return [resultadoOrquestrador[0], resultadoOrquestrador[1], resultadoOrquestrador[2], 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']

    def funcao_declarar_funcao(self, nomeDaFuncao, parametros):
        log('Declarar funcoes: {}'.format(nomeDaFuncao + str(parametros)))

        teste = Run.analisa_padrao_variavel(self, nomeDaFuncao,'Função')
        testa = Run.verifica_se_tem(self, parametros, ', ')

        if teste[1] != True:
            return [False, teste[1], teste[2], 'exibirNaTela']

        if testa != []:
            listaDeParametros = []
            anterior = 0

            for valorItem in testa:
                if parametros[anterior : valorItem[0]]:
                    listaDeParametros.append(parametros[ anterior : valorItem[0]])
                anterior = valorItem[1]

            if len( parametros[anterior : ]) > 0:
                listaDeParametros.append(parametros[ anterior : ])

            listaFinalDeParametros = []
            for parametro in listaDeParametros:
                listaFinalDeParametros.append(parametro.strip())

                teste = Run.analisa_padrao_variavel(self, parametro.strip(),'Parametro ')
                if teste[1] != True:
                    return [False, teste[1], teste[2], 'exibirNaTela']

            self.dic_funcoes[nomeDaFuncao] = [listaFinalDeParametros, 'bloco']

        else:
            teste = Run.analisa_padrao_variavel(self, parametros,'Parametro ')
            if teste[1] != True:
                return [False, teste[1], teste[2], 'exibirNaTela']

            self.dic_funcoes[nomeDaFuncao] = [parametros, 'bloco']

        funcao_em_analise = nomeDaFuncao
        return [True, True, 'booleano', 'declararFuncao',funcao_em_analise]

    def funcao_exibir(self, linha):
        log('funcao exibição: {}'.format(linha))

        codigo = linha.strip()
        resultado = Run.abstrair_valor_linha(self, codigo)

        if resultado[0] == False:
            return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

        return [resultado[0],resultado[1], resultado[2],'exibirNaTela']

    def funcao_exibir_na_linha(self, linha):
        log('Função exibir nessa linha ativada'.format(linha))

        linha = linha.strip()
        resultado = Run.abstrair_valor_linha(self, linha)

        if resultado[0] == False:
            return resultado

        return [ resultado[0], ':nessaLinha:' + str(resultado[1]), resultado[2], 'exibirNaTela' ]

    def funcao_tempo(self, tempo, tipo_espera):
        log('Função tempo: {}'.format(tempo))

        resultado = Run.abstrair_valor_linha(self, tempo)
        if resultado != False:

            if tipo_espera == "segundos" or tipo_espera == "s" or tipo_espera == "segundo":
                sleep(resultado[1])
                return [True, None, 'vazio', 'fazerNada']

            elif tipo_espera == "milisegundos" or tipo_espera == "ms" or tipo_espera == "milisegundo":
                sleep(resultado[1]/1000)
                return [True, None, 'vazio', 'fazerNada']

        else:
            return [False, 'Erro ao obter um valor no tempo', 'string', 'exibirNaTela']

        return [True, None, 'vazio', 'fazerNada']

    def obter_valor_string(self, string):
        log('Obter valor de uma string: {}'.format(string))

        valorFinal = ''
        anterior = 0

        for valor in finditer("""\"[^"]*\"""", string):

            abstrair = Run.abstrair_valor_linha(self, 
                string[anterior:valor.start()])
            if abstrair[0] == False:
                return abstrair

            valorFinal = valorFinal + str( abstrair[1] ) + string[ valor.start()+1:valor.end() -1 ]
            anterior = valor.end()

        abstrair = Run.abstrair_valor_linha(self, string[anterior:])
        if abstrair[0] == False:
            return abstrair

        valorFinal = valorFinal + str(abstrair[1])

        return [True, valorFinal, 'string']

    def localiza_transforma_variavel(self, linha):
        log('Encontrar e transformar dic_variaveis: {}'.format(linha))

        anterior = 0
        normalizacao = 0
        linha_base = linha
        tipos_obtidos = []

        for valor in finditer(' ', linha_base):
            palavra = linha[anterior : valor.start() + normalizacao]

            if palavra.isalnum() and palavra[0].isalpha():

                variavelDessaVez = Run.abstrair_valor_linha(self, palavra)

                if variavelDessaVez[0] == False:
                    return variavelDessaVez

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
        log('Fazer contas: {}'.format(linha))

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

        if '"' in linha:
            return [False, "Isso é uma string", 'string']

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
        if linha[0] == False:
            return linha

        # Se sobrou texto
        for caractere in linha[1]:
            if str(caractere).isalpha():
                return [False, 'não é possível fazer contas com strings: ' + str(linha[1]), 'string']

        # Tente fazer uma conta com isso
        try:
            resutadoFinal = eval(linha[1])

        except Exception as erro:
            return [False, "Não foi possivel realizar a conta |{}|".format(linha[1]), 'string']

        else:
            return [True, resutadoFinal, 'float']

    def obter_valor_variavel(self, variavel):
        log('Obter valor da variável: "{}"'.format(variavel))
        
        variavel = variavel.strip()
        variavel = variavel.replace('\n', '')

        try:
            self.dic_variaveis[variavel]
        except:
            return [False, "Você precisa definir a variável '{}'".format(variavel), 'string', 'fazerNada']
        else:
            return [True, self.dic_variaveis[variavel][0], self.dic_variaveis[variavel][1], 'fazerNada']


    def abstrair_valor_linha(self, possivelVariavel):
        log("Abstrar valor de uma linha inteira com possivelVariavel: '{}'".format(possivelVariavel))

        possivelVariavel = str(possivelVariavel).strip()

        if possivelVariavel == 'True':
            return [True, 'True', 'booleano']

        if possivelVariavel == 'False':
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

                if valor[0] == False:
                    return valor

                listaValores += str(valor[1])

            return [True, listaValores, "string"]

        if possivelVariavel[-1] == '"' and possivelVariavel[0] == '"':
            return [True, possivelVariavel[1:-1], 'string']

        if possivelVariavel == '':
            return [True, possivelVariavel, 'string']

        resultado = Run.fazer_contas(self, possivelVariavel)
        if resultado[0] == True:
            return resultado

        resultado = Run.comandos_uso_geral(self, possivelVariavel)

        if resultado[0] == True and resultado[1] != None:
            return resultado

        elif resultado[0] == False:
            return resultado

        testa = Run.verifica_se_tem(self, possivelVariavel, '"')
        if testa != []:
            return Run.obter_valor_string(self, possivelVariavel)

        try:
            float(possivelVariavel)
        except:
            return Run.obter_valor_variavel(self, possivelVariavel)
        else:
            return [True, float(possivelVariavel), 'float']

    def analisa_padrao_variavel(self, variavelAnalise, msg):
        variavel = variavelAnalise

        variavel = variavel.replace('_','a')
        variavel = variavel.lower()

        if not variavel[0].isalpha():
            return [True, msg + ' devem começar obrigatóriamente com uma letra: \'{}\' não se encaixa nessa regra'.format(variavelAnalise), 'sring']

        if not variavel.isalnum():
            return [True, msg + ' devem conter apenas letras, números ou _: \'{}\' não se encaixa nessa regra'.format(variavelAnalise), 'sring']

        return [True,True,'booleano']

    def funcao_fazer_atribuicao(self, variavel, valor):
        log('Função atribuição: {}'.format(variavel + str(valor)))

        if variavel == '' or valor == '':
            return [False, 'É necessario cum comando de atribuição', 'string', 'exibirNaTela']

        teste = Run.analisa_padrao_variavel(self, variavel,'Variáveis')
        if teste[1] != True:
            return [False, teste[1], teste[2], 'exibirNaTela']

        valor = valor.replace('\n', '')
        valor = valor.strip()

        resultado = Run.abstrair_valor_linha(self, valor)
        if resultado[0] == False:
            return resultado

        if resultado[0] == True:
            self.dic_variaveis[variavel] = [resultado[1], resultado[2]]

            return [True, None, 'vazio', 'fazerNada']

        return [ resultado[0], resultado[1], resultado[2], 'fazerNada']

    def funcao_loops_enquanto(self, linha):
        log('Função loops enquanto: {}'.format(linha))

        resultado = Run.funcao_condicional(self, linha)
        return [resultado[0], resultado[1], resultado[2], 'declararLoop']

    def tiver_valor_lista(self, linha):
        log('Função condicional: {}'.format(linha))

        linha = linha.strip()

        analisa = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return Run.funcao_tiver_na_lista(self, analisa[0],analisa[1])

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

    def funcao_condicional(self, linha):
        log('Função condicional: {}'.format(linha))

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
        if qtd_simbolos_especiais == 0:
            return [False, "Não foi possivel realizar a condição por que não tem nenhum simbolo condicional", 'string', 'exibirNaTela']

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
            resultado = Run.abstrair_valor_linha(self, 
                linha[anterior:item.start()])

            if resultado[0] == False:
                return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

            saida = resultado[1]

            if resultado[2] == 'string':
                saida = '"' + resultado[1] + '"'

            # Reover marcadores de simbolos
            final += str(saida) + linha[item.start() + 3:item.end() - 3]

            anterior = item.end()

        boolTemTiverLista = False
        resultado = Run.tiver_valor_lista(self, linha[anterior:].strip())

        if resultado[0] == False:
            return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

        if resultado[2] == 'booleano':

            if resultado[1] == 'sim':
                final += ' True '
                boolTemTiverLista = True

            elif resultado[1] == 'nao':
                final += ' False '
                boolTemTiverLista = True

        if not boolTemTiverLista:

            resultado = Run.abstrair_valor_linha(self, linha[anterior:])
            if resultado[0] == False:
                return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

            saida = resultado[1]
            if resultado[2] == 'string':
                saida = '"' + resultado[1] + '"'

            final += str(saida)

        # Tente fazer a condição com isso
        try:
            resutadoFinal = eval(final)

        except Exception as erro:
            return [False, "Não foi possivel realizar a condicao |{}|".format(final), 'string', 'exibirNaTela']

        else:
            return [True, resutadoFinal, 'booleano', 'declararCondicional']


dic_comandos, dic_design, cor_do_comando = atualiza_configuracoes_temas()

def salvar_arquivo_como_dialog(event = None):
    global dic_info_arquivo

    arq = filedialog.asksaveasfile(mode='w',
                                   defaultextension=".fyn",
                                   title = "Selecione o script",
                                   filetypes = (("Meus scripts", "*.fyn"), ("all files", "*.*"))
    )

    lnk_arquivo_salvar = str(arq.name)

    if arq is None:
        return None

    arq.close()

    text2save = str(tx_codficac.get(1.0, END))
    try:
        arq = open(lnk_arquivo_salvar, 'w', encoding='utf8')
        arq.write(text2save[0:-1])
        arq.close()

    except Exception as erro:
        messagebox.showinfo('Erro', 'Erro ao salvar programa, erro: {}'.format(erro))

    else:
        dic_info_arquivo['link'] = arq.name
        dic_info_arquivo['texto'] = text2save

        return arq.name

def salvar_arquivo(event=None):
    """
    Salva um arquivo que já está aberto
    """

    global dic_info_arquivo

    if dic_info_arquivo['link'] == None:
        salvar_arquivo_como_dialog()

    else:
        programaCodigo = tx_codficac.get(1.0, END)

        if dic_info_arquivo['texto'] == programaCodigo:
            log(" Programa não sofreu modificações para ser salvo novamente....")

        else:
            try:
                salvar_arquivo(arquivo = dic_info_arquivo['link'], texto = programaCodigo[0:-1])

            except Exception as erro:
                messagebox.showinfo('Erro', 'Não foi possível salvar essa versão do código, erro: {}'.format(erro))

            else:
                dic_info_arquivo['texto'] = programaCodigo

def salvar_arquivo_dialog(event=None):
    global dic_info_arquivo

    arq_tips = [('Scripts fyn', '*.fyn'), ('Todos os arquivos', '*')]
    arq_dial = filedialog.Open(filetypes = arq_tips)
    arq_nome = arq_dial.show()

    if arq_nome == ():
        log(' Nenhum arquivo escolhido')

    else:
        log(' Arquivo "{}" escolhido'.format(arq_nome))
        arq_txts = abrir_arquivo(arq_nome)

        if arq_txts[0] != None:
            tx_codficac.delete(1.0, END)
            tx_codficac.insert(END, arq_txts[0])

        else:
            messagebox.showinfo("ops","Aconteceu um erro ao abrir o arquivo" + arq_txts[1])

        coordena_coloracao(None, fazer = 'nada')

        dic_info_arquivo['link'] = arq_nome
        dic_info_arquivo['texto'] = arq_txts[0]

def abrirArquivo(link):
    global dic_info_arquivo

    log(' Abrindo arquivo "{}" escolhido'.format(link))

    arq = abrir_arquivo(link)

    if arq[0] != None:
        tx_codficac.delete(1.0, END)
        tx_codficac.insert(END, arq[0])

        coordena_coloracao(None, fazer = 'nada')

        dic_info_arquivo['link'] = link
        dic_info_arquivo['texto'] = arq[0]

    else:
        if "\'utf-8' codec can\'t decode byte" in arq[1]:
            messagebox.showinfo("Erro de codificação", "Por favor, converta seu arquivo para a codificação UTF-8. Não foi possível abrir o arquivo: \"{}\", erro: \"{}\"".format(link, arq[1]))
        else:
            messagebox.showinfo('Erro', 'Aconteceu um erro ao tentar abrir o script: {}, erro: {}'.format(link, arq[1]))

        print('Arquivo não selecionado')

def realiza_coloracao(palavra, linha, valor1, valor2, cor):
    """
        Realiza a coloracao de uma unica palavra
    """
    linha1 = '{}.{}'.format(linha , valor1)
    linha2 = '{}.{}'.format(linha , valor2)

    tx_codficac.tag_add(palavra, linha1 , linha2)
    tx_codficac.tag_config(palavra, foreground = cor)

def realiza_coloracao_erro(palavra, valor1, valor2, cor='red', linhaErro = None):
    """
        Colore uma linha de erro no terminal
    """
    global tx_terminal
    global tx_codficac
    global erro_alertado

    linha = tx_terminal.get(1.0, END)
    linha = len(linha.split('\n')) - 1

    linha1 = '{}.{}'.format(linha, valor1)
    linha2 = '{}.{}'.format(linha, valor2)

    tx_terminal.tag_add(palavra, linha1 , linha2)
    tx_terminal.tag_config(palavra, foreground = cor)

    if linhaErro != None:

        lista = tx_codficac.get(1.0, END).split("\n")
        
        palavra = "**_erro_alertado_**"
        linha1 = str(linhaErro) + ".0"
        linha2 = str(linhaErro) + "." + str(len(lista[int(linhaErro) - 1]))

        tx_codficac.tag_add(palavra, linha1 , linha2)
        tx_codficac.tag_config(palavra, background = "#dd3344")

    erro_alertado = True

def marcar_coloracao(regex, lista, linha, palavra, cor):
    for valor in finditer(regex, lista[linha]):
        realiza_coloracao(str(palavra), str(linha + 1), valor.start(), valor.end(), cor)

def define_coloracao(chave_comando, chave_cor, lista):
    for comando in dic_comandos[ chave_comando ]:
        analisa_coloracao(comando[0].strip(), cor_do_comando[ chave_cor ], lista)

def analisa_coloracao(palavra, cor, lista):
    """
        Realiza a coloração seguindo instruções
    """

    global tx_codficac

    cor = cor['foreground']
    tx_codficac.tag_delete(palavra)

    palavra_comando = palavra.replace('+', '\\+')
    palavra_comando = palavra_comando.replace('/', '\\/')
    palavra_comando = palavra_comando.replace('*', '\\*')

    for linha in range(len(lista)):

        if palavra == "numerico":
            marcar_coloracao('(^|\\s|\\,)([0-9\\.]\\s*){1,}($|\\s|\\,)', lista, linha, palavra, cor)

        elif palavra == "comentario":
            marcar_coloracao('(#|\\/\\/).*$', lista, linha, palavra, cor)
            marcar_coloracao('(\\/\\*[^\\*\\/]*\\*\\/)', lista, linha, palavra + "longo", cor)

        elif palavra == '"':
            marcar_coloracao("""\"[^"]*\"""", lista, linha, palavra, cor)

        else:
            palavra_comando = palavra_comando.replace(' ','\\s*')
            marcar_coloracao('(^|\\s){}(\\s|$)'.format(palavra_comando), lista, linha, palavra, cor)

def coordena_coloracao(event = None, fazer = 'tudo'):
    """
        Coordena a coloração de todos os comandos
    """
    
    global cor_do_comando
    global tx_codficac

    configuracoes(ev = None)

    if event != None: # não modifica o código
        if event.keysym in ('Down','Up','Left','Right'):
            return 0

    try:
        lista = tx_codficac.get(1.0, END).lower().split('\n')

        define_coloracao('addItensListaInternoPosicaoFinaliza', "lista", lista)
        define_coloracao('addItensListaInternoFinal', "lista", lista)
        define_coloracao('addItensListaInternoPosicao', "lista", lista)
        define_coloracao('addItensListaInternoInicio', "lista", lista)
        define_coloracao('declaraListasObterPosicao', "lista", lista)
        define_coloracao('RemoverItensListasInterno', "lista", lista)
        define_coloracao('declaraVariaveis', "atribuicao", lista)
        define_coloracao('passandoParametros', "tempo", lista)
        define_coloracao('RemoverItensListas', "lista", lista)
        define_coloracao('incrementeDecremente', "tempo", lista)
        define_coloracao('recebeDeclaraListas', "lista", lista)
        define_coloracao('tiverInternoLista', "lista", lista)
        define_coloracao('aleatorioEntre', "lista", lista)
        define_coloracao('listaPosicoesCom', "lista", lista)
        define_coloracao('listaNaPosicao', "lista", lista)
        define_coloracao('listaCom', "lista", lista)
        define_coloracao('declaraListas', "lista", lista)
        define_coloracao('adicionarItensListas', "lista", lista)
        define_coloracao('tamanhoDaLista', "lista", lista)
        define_coloracao('digitado', "tempo", lista)
        define_coloracao('enquanto', "lista", lista)
        define_coloracao('mostreNessa', "exibicao", lista)
        define_coloracao('funcoes', "tempo", lista)
        define_coloracao('aguarde', "tempo", lista)
        define_coloracao('aleatorio', "tempo", lista)
        define_coloracao('limpatela', "tempo", lista)
        define_coloracao('incremente', "tempo", lista)
        define_coloracao('decremente', "logico", lista)
        define_coloracao('tiverLista', "lista", lista)
        define_coloracao('recebeParametros', "tempo", lista)
        define_coloracao('esperaEm', "tempo", lista)
        define_coloracao('matematica', "contas", lista)
        define_coloracao('repitaVezes', "lista", lista)
        define_coloracao('logico', "logico", lista)
        define_coloracao('repita', "lista", lista)
        define_coloracao('mostre', "exibicao", lista)
        define_coloracao('se', "condicionais", lista)

        analisa_coloracao('numerico'     , cor_do_comando["numerico"], lista)
        analisa_coloracao('comentario'   , cor_do_comando["comentario"], lista)
        analisa_coloracao('"'            , cor_do_comando["string"], lista)

        tx_codficac.update()

    except Exception as erro:
        print("Erro ao atualizar coloracao", erro)

def log(mensagem):
    global bool_logs

    if bool_logs:
        print(mensagem)

global instancia
def inicializa_orquestrador(event = None):
    """
        Inicicaliza o orquestrador que analisa blocos de código
    """

    log("\n Orquestrador iniciado")
    global numero_threads
    global tx_codficac
    global instancia
    global boo_orquestrador_iniciado

    inicio = time()

    if numero_threads != 0:
        messagebox.showinfo('Problemas',"Já existe um programa sendo executado!")
        return 0

    numero_threads = 0
    inicializador_terminal()
    
    tx_terminal.delete('1.0', END)

    linhas = tx_codficac.get('1.0', END)
    nova_linha = ''

    lista = linhas.split('\n')
    for linha in range(len(lista)):
        nova_linha += '[{}]{}\n'.format(str(linha + 1), lista[linha])
    
    linhas = nova_linha

    boo_orquestrador_iniciado = False

    instancia = Run()
    t = Thread(target=lambda codigoPrograma = linhas: instancia.orquestrador_interpretador(codigoPrograma))
    t.start()

    while numero_threads != 0 or not boo_orquestrador_iniciado:
        tela.update()

    del instancia

    try:
        tx_terminal.insert(END, '\nScript finalizado em {:.3} segundos'.format(time() - inicio))
        tx_terminal.see("end")
 
    except Exception as erro:
        log('Impossível exibir mensagem de finalização, erro: '+ str(erro))

def modoFullScreen(event=None):
    global bool_tela_em_fullscreen

    if bool_tela_em_fullscreen:
        bool_tela_em_fullscreen = False

    else:
        bool_tela_em_fullscreen = True

    tela.attributes("-fullscreen", bool_tela_em_fullscreen)

def ativar_logs(event=None):
    global bool_logs

    if bool_logs:
        bool_logs = False

    else:
        bool_logs = True

def inicializador_terminal():
    global tx_terminal
    global top_janela_terminal
    global instancia

    top_janela_terminal = Toplevel(tela)
    top_janela_terminal.grid_columnconfigure(1, weight=1)
    top_janela_terminal.rowconfigure(1, weight=1)
    top_janela_terminal.geometry("720x450+150+150")

    tx_terminal = Text(top_janela_terminal)
    try:
        # Se ainda não estava carregado
        tx_terminal.configure(dic_design["tx_terminal"])
    except Exception as erro:
        print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

    tx_terminal.bind('<Return>', lambda event:instancia.pressionou_enter(event))
    tx_terminal.focus_force()
    tx_terminal.grid(row=1, column=1, sticky=NSEW)

def atualizarListaDeScripts():
    for file in listdir('scripts/'):
        if len(file) > 5:
            if file[-3:] == 'fyn':
                funcao = lambda link = file: abrirArquivo('scripts/' + str(link))
                mn_arq_casct.add_command(label=file, command = funcao)
 
def atualizarListaTemas():
    for file in listdir('temas/'):
        if len(file) > 11:
            if file[-10:] == 'theme.json':
                funcao = lambda link = file: atualizaInterface('tema', str(link))
                mn_intfc_casct_temas.add_command(label=file, command=funcao)

def atualizarListasintaxe():
    for file in listdir('temas/'):
        if len(file) > 13:
            if file[-12:] == 'sintaxe.json':
                funcao = lambda link = file: atualizaInterface('sintaxe', str(link))
                mn_intfc_casct_sintx.add_command(label=file, command=funcao)

def atualizarListasfontes():
    fontes=list(font.families())
    fontes.sort()

    for fonte in fontes:
        mn_intfc_casct_fonts.add_command(label=fonte)

def arquivoConfiguracao(chave, novo = None):
    if novo == None:

        with open('configuracoes/configuracoes.json') as json_file:
            configArquivoJson = load(json_file)
            retorno = configArquivoJson[chave]

        return retorno

    elif novo != None:

        with open('configuracoes/configuracoes.json') as json_file:
            configArquivoJson = load(json_file)

            configArquivoJson[chave] = novo
            configArquivoJson = str(configArquivoJson).replace('\'','\"')

        file = open('configuracoes/configuracoes.json','w')
        file.write(str(configArquivoJson))
        file.close()

def atualizaInterface(chave, novo):
    global tela
    global tx_codficac
    global dic_design
    global cor_do_comando

    try:
        arquivoConfiguracao(chave, novo)

    except Exception as e:
        return [None,'Erro ao atualizar o arquivo \'configuracoes/configuracoes.json\'. Sem esse arquivo, não é possível atualizar os temas']

    dic_comandos, dic_design, cor_do_comando = atualiza_configuracoes_temas()

    try:
        atualiza_design_interface()
        coordena_coloracao(None, fazer = 'nada')
    except Exception as erro:
        print('ERRO: ', erro)
    else:
        print('Temas atualizados')

    tela.update()
    tx_codficac.update()

def atualiza_design_interface():

    try:
        mn_intfc_casct_sintx.configure(dic_design["cor_menu"])
        mn_intfc_casct_temas.configure(dic_design["cor_menu"])
        mn_intfc_casct_fonts.configure(dic_design["cor_menu"])
        mn_arq_casct.configure(dic_design["cor_menu"])
        mn_ferrm.configure(dic_design["cor_menu"])
        mn_intfc.configure(dic_design["cor_menu"])
        mn_loclz.configure(dic_design["cor_menu"])
        mn_exect.configure(dic_design["cor_menu"])
        mn_arqui.configure(dic_design["cor_menu"])
        mn_edita.configure(dic_design["cor_menu"])
        mn_barra.configure(dic_design["cor_menu"])
        mn_ajuda.configure(dic_design["cor_menu"])
        mn_sobre.configure(dic_design["cor_menu"])
        mn_barra.configure(dic_design["cor_menu"])
        mn_devel.configure(dic_design["cor_menu"])
        lb_linhs.configure(dic_design["lb_linhas"])
        bt_salva.configure(dic_design["dicBtnMenus"])
        bt_ident.configure(dic_design["dicBtnMenus"])
        bt_break.configure(dic_design["dicBtnMenus"])
        bt_playP.configure(dic_design["dicBtnMenus"])
        bt_breaP.configure(dic_design["dicBtnMenus"])
        bt_desfz.configure(dic_design["dicBtnMenus"])
        bt_redsf.configure(dic_design["dicBtnMenus"])
        bt_comme.configure(dic_design["dicBtnMenus"])
        bt_idiom.configure(dic_design["dicBtnMenus"])
        bt_ajuda.configure(dic_design["dicBtnMenus"])
        bt_pesqu.configure(dic_design["dicBtnMenus"])
        bt_atena.configure(dic_design["dicBtnMenus"])
        tx_pesqu.configure(dic_design["tx_pesqu"])
        fr_ajuda.configure(dic_design["fr_ajuda"])
        fr_princ.configure(dic_design["fr_princ"])

        tela.configure(dic_design["tela"])

        tx_codficac.configure(dic_design["tx_codificacao"])
        sb_codfc.configure(dic_design['scrollbar_text'])

        fr_opc_rapidas.configure(dic_design["fr_opcoes_rapidas"])

    except Exception as erro:
        print('Erro ao atualizar o design da interface, erro: ',erro)

def configuracoes(ev):
    print('configuracoes')

    global altura_widget
    global lb_linhs
    global posCorrente
    global posAbsuluta

    if ev != None:
        altura_widget = int( ev.height / 24 )

    qtdLinhas = tx_codficac.get(1.0, 'end').count('\n')
    #print('Quantidade para : ' + str(qtdLinhas))
    #print('Atualizadoo para: ' + str(altura_widget))

    ate = qtdLinhas + 1
    inicio = 1

    add_linha = ''
    for linha in range(inicio, ate):
        add_linha = add_linha +  "  " + str(linha) + '\n'

    lb_linhs.config(state=NORMAL)
    lb_linhs.delete(1.0, END)
    lb_linhs.insert(1.0, add_linha[:-1])

    lb_linhs.config(state=DISABLED)

def obterPosicaoDoCursor(event=None):
    global altura_widget
    global lb_linhs
    global tx_codficac

    numPosicao = str(tx_codficac.index(INSERT))
    posCorrente = int(float(tx_codficac.index(CURRENT)))

    print('linha que o cursor está : ', numPosicao)
    print('posicao do cursor: ', posCorrente)
    print('altura: ', altura_widget)

    if posCorrente - altura_widget <= 0:
        return 0

    add_linha = ''
    for linha in range(posCorrente - altura_widget, posCorrente):
        add_linha = add_linha +  "  " + str(linha) + '\n'

    lb_linhs.config(state=NORMAL)
    lb_linhs.delete(1.0, END)
    lb_linhs.insert(1.0, add_linha[:-1])
    lb_linhs.config(state=DISABLED)

def tela_ajuda(pesquisa):
    global fr_ajuda
    global lst_titulos_frames

    # Remover todos os botões
    for item in lst_titulos_frames:
        item[0].destroy()
        item[1].destroy()
        item[2].destroy()

    lst_titulos_frames = []

    json_ajuda = carregar_json('configuracoes/menu_ajuda.json')

    contador_frames = 2
    for k, v in json_ajuda.items(): # Cria os itens na tela

        descricao = json_ajuda[k]['descricao']
        exemplo = json_ajuda[k]['exemplo']
        titulo = json_ajuda[k]['titulo']
        chave = json_ajuda[k]['chave']
        link = json_ajuda[k]['link']

        if pesquisa in titulo.lower() or pesquisa in chave.lower() == False:
            continue

        # MENU
        fr_ajuda_comando = Frame(fr_ajuda) 
        lb_ajuda_texto_c = Label(fr_ajuda_comando, text=titulo)
        lb_ajuda_descr_c = Label(fr_ajuda_comando, text=exemplo)

        fr_ajuda_comando.configure(dic_design["fr_ajuda_comando"])
        lb_ajuda_texto_c.configure(dic_design["lb_ajuda_texto_c"])
        lb_ajuda_descr_c.configure(dic_design["lb_ajuda_descr_c"])

        fr_ajuda_comando.grid(row=contador_frames, column=1, sticky=NSEW)
        lb_ajuda_texto_c.grid(row=1, column=1, sticky=W)
        lb_ajuda_descr_c.grid(row=2, column=1, sticky=NSEW)

        lst_titulos_frames.append([fr_ajuda_comando, lb_ajuda_texto_c, lb_ajuda_descr_c])

        contador_frames += 1

# tela.attributes('-fullscreen', True)

tela = Tk()
tela.title('Combratec - Linguagem feynman')
tela.rowconfigure(2, weight=1)
tela.geometry("1100x600")
tela.grid_columnconfigure(1, weight=1)

tela.bind('<F11>', lambda event: modoFullScreen(event))
tela.bind('<F5>', lambda event: inicializa_orquestrador(event))
tela.bind('<Control-s>', lambda event: salvar_arquivo(event))
tela.bind('<Control-o>', lambda event: salvar_arquivo_dialog(event))
tela.bind('<Control-S>', lambda event: salvar_arquivo_como_dialog(event))

try:
    imgicon = PhotoImage(file='icone.png')
    tela.call('wm', 'iconphoto', tela._w, imgicon)

except Exception as erro:
    print('Erro ao carregar icone do app:', erro)

mn_barra = Menu(tela, tearoff = False)
tela.config(menu=mn_barra)

mn_ferrm = Menu(mn_barra, tearoff = False)
mn_intfc = Menu(mn_barra, tearoff = False)
mn_loclz = Menu(mn_barra, tearoff = False)
mn_exect = Menu(mn_barra, tearoff = False)
mn_arqui = Menu(mn_barra, tearoff = False)
mn_edita = Menu(mn_barra, tearoff = False)
mn_ajuda = Menu(mn_barra, tearoff = False)
mn_sobre = Menu(mn_barra, tearoff = False)
mn_devel = Menu(mn_barra, tearoff = False)

mn_barra.add_cascade(label='  Arquivo'    , menu=mn_arqui)
mn_barra.add_cascade(label='  Executar'   , menu=mn_exect)
mn_barra.add_cascade(label='  Localizar'  , menu=mn_loclz)
mn_barra.add_cascade(label='  Interface'  , menu=mn_intfc)
mn_barra.add_cascade(label='  Ajuda'      , menu=mn_ajuda)
mn_barra.add_cascade(label='  sobre'      , menu=mn_sobre)
mn_barra.add_cascade(label='  Dev'        , menu=mn_devel)
mn_barra.add_cascade(label='  Ferramentas', menu=mn_ferrm)

mn_arq_casct = Menu(mn_arqui, tearoff = False)
mn_arqui.add_command(label='  Abrir arquivo (Ctrl+O)', command=salvar_arquivo_dialog)
mn_arqui.add_command(label='  Nova Guia (Ctrl-N)')
mn_arqui.add_command(label='  Abrir pasta')
mn_arqui.add_separator()
mn_arqui.add_command(label='  Recentes')
mn_arqui.add_cascade(label='  Exemplos', menu=mn_arq_casct)
atualizarListaDeScripts()

mn_arqui.add_separator()
mn_arqui.add_command(label='  Salvar (Ctrl-S)', command=salvar_arquivo)
mn_arqui.add_command(label='  Salvar Como (Ctrl-Shift-S)', command=salvar_arquivo_como_dialog)
mn_arqui.add_separator()
mn_arqui.add_command(label='  imprimir (Ctrl-P)')
mn_arqui.add_command(label='  Exportar (Ctrl-E)')
mn_arqui.add_command(label='  Enviar por e-mail ')

mn_exect.add_command(label='  Executar Tudo (F5)', command=inicializa_orquestrador)
mn_exect.add_command(label='  Executar linha (F6)')
mn_exect.add_command(label='  Executar até breakpoint (F7)')
mn_exect.add_command(label='  Executar com delay (F8)')
mn_exect.add_command(label='  Parar execução (F9)')
mn_exect.add_command(label='  Inserir breakpoint (F10)')
mn_loclz.add_command(label='  Localizar (CTRL + F)')
mn_loclz.add_command(label='  Substituir (CTRL + R)')
mn_ferrm.add_command(label='  corrigir identação')
mn_ferrm.add_command(label='  Numero de espaços para o tab')

mn_intfc_casct_temas = Menu(mn_intfc, tearoff = False)
mn_intfc.add_cascade(label='  Temas', menu=mn_intfc_casct_temas)

atualizarListaTemas()

mn_intfc_casct_sintx = Menu(mn_intfc, tearoff = False)
mn_intfc.add_cascade(label='  sintaxe', menu=mn_intfc_casct_sintx)

atualizarListasintaxe()

mn_intfc_casct_fonts = Menu(mn_intfc, tearoff = False)
mn_intfc.add_cascade(label='  fontes', menu=mn_intfc_casct_fonts)

atualizarListasfontes()

mn_ajuda.add_command(label='  Ajuda (F1)', command = lambda event = None: webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comandos Disponíveis', command = lambda event = None: webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comunidade', command = lambda event = None: webbrowser.open("https://feynmancode.blogspot.com/p/comunidade.html"))
mn_sobre.add_command(label='  Projeto', command= lambda event = None: webbrowser.open("http://feynmancode.blogspot.com/"))

mn_devel.add_command(label='  Logs', command= lambda event = None: ativar_logs())

fr_opc_rapidas = Frame(tela)
fr_opc_rapidas.grid(row = 1, column =1, sticky=NSEW, columnspan=2)

ic_salva = PhotoImage(file='imagens/ic_salvar.png')
ic_ident = PhotoImage(file='imagens/ic_arrumar.png')
ic_break = PhotoImage(file='imagens/ic_parar.png')
ic_playP = PhotoImage(file='imagens/ic_play.png')
ic_breaP = PhotoImage(file='imagens/ic_play_breakpoint.png')
ic_desfz = PhotoImage(file='imagens/left.png')
ic_redsf = PhotoImage(file='imagens/right.png')
ic_comme = PhotoImage(file='imagens/ic_comentario.png')
ic_idiom = PhotoImage(file='imagens/ic_idioma.png')
ic_ajuda = PhotoImage(file='imagens/ic_duvida.png')
ic_pesqu = PhotoImage(file='imagens/ic_pesquisa.png')
ic_atena = PhotoImage(file='imagens/ic_atena.png')

ic_salva = ic_salva.subsample(4,4)
ic_ident = ic_ident.subsample(4,4)
ic_break = ic_break.subsample(4,4)
ic_playP = ic_playP.subsample(4,4)
ic_breaP = ic_breaP.subsample(4,4)
ic_desfz = ic_desfz.subsample(4,4)
ic_redsf = ic_redsf.subsample(4,4)
ic_comme = ic_comme.subsample(4,4)
ic_idiom = ic_idiom.subsample(4,4)
ic_ajuda = ic_ajuda.subsample(4,4)
ic_pesqu = ic_pesqu.subsample(4,4)
ic_atena = ic_atena.subsample(4,4)

bt_salva = Button(fr_opc_rapidas, image=ic_salva, relief = RAISED)
bt_ident = Button(fr_opc_rapidas, image=ic_ident, relief = RAISED)
bt_break = Button(fr_opc_rapidas, image=ic_break, relief = RAISED)
bt_playP = Button(fr_opc_rapidas, image=ic_playP, relief = RAISED, command = inicializa_orquestrador)
bt_breaP = Button(fr_opc_rapidas, image=ic_breaP, relief = RAISED, command = inicializa_orquestrador)
bt_desfz = Button(fr_opc_rapidas, image=ic_desfz, relief = RAISED)
bt_redsf = Button(fr_opc_rapidas, image=ic_redsf, relief = RAISED)
bt_comme = Button(fr_opc_rapidas, image=ic_comme, relief = RAISED)
bt_idiom = Button(fr_opc_rapidas, image=ic_idiom, relief = RAISED)
bt_ajuda = Button(fr_opc_rapidas, image=ic_ajuda, relief = RAISED)
bt_pesqu = Button(fr_opc_rapidas, image=ic_pesqu, relief = RAISED)
bt_atena = Button(fr_opc_rapidas, image=ic_atena, relief = RAISED)

fr_princ = Frame(tela)
fr_princ.grid_columnconfigure(2, weight=1)
fr_princ.rowconfigure(1, weight=1)

lb_linhs = Text(fr_princ)

tx_codficac = Text(fr_princ)
sb_codfc = Scrollbar(fr_princ, relief = FLAT)
fr_ajuda = Frame(fr_princ)
tx_pesqu = Entry(fr_ajuda)

tx_codficac.focus_force()
lb_linhs.config(state = DISABLED)
tx_codficac['yscrollcommand'] = sb_codfc.set
sb_codfc.config(command = tx_codficac.yview)

tx_codficac.bind('<Configure>', configuracoes )
tx_codficac.bind('<Button>', obterPosicaoDoCursor)
tx_codficac.bind('<KeyRelease>', coordena_coloracao)
tx_pesqu.bind('<KeyRelease>', lambda event = None: tela_ajuda(tx_pesqu.get()))

bt_salva.grid(row=1,column=1)
bt_ident.grid(row=1,column=2)
bt_break.grid(row=1,column=3)
bt_playP.grid(row=1,column=4)
bt_breaP.grid(row=1,column=5)
bt_desfz.grid(row=1,column=6)
bt_redsf.grid(row=1, column=7)
bt_comme.grid(row=1, column=8)
bt_idiom.grid(row=1, column=9)
bt_ajuda.grid(row=1, column=10)
bt_pesqu.grid(row=1, column=11)
bt_atena.grid(row=1, column=12)
fr_princ.grid(row=2, column=1, sticky=NSEW)
lb_linhs.grid(row=1, column=1, sticky=NSEW)
tx_codficac.grid(row=1, column=2, sticky=NSEW)
sb_codfc.grid(row=1, column=3, sticky=NSEW)
fr_ajuda.grid(row=1, column=4, sticky=NSEW)
tx_pesqu.grid(row=0, column=1, sticky=NSEW)

atualiza_design_interface()

tela_ajuda("")
abrirArquivo('programa_teste.fyn')
tela.mainloop()


#abrirArquivo('bug.fyn')


'''
    if '.' not in numPosicao:
        numPosicao = numPosicao + '.0'

    # Obter linha e coluna
    linha, coluna = numPosicao.split('.')

    palavra = ""
    aconteceuEspaco = False

    # Obter o código sendo digitado
    for valor in range(0, int(coluna)):
        letra = tx_codficac.get('{}.{}'.format( int(linha), int(coluna) - valor - 1 ))

        palavra = letra + palavra

        # Se chegar no incio da linha, ou se não for alfabético e sejá aconteceu algo diferente de espaço
        if ( ( letra == "\n" or not letra.isalpha() ) and aconteceuEspaco):
            break

        # Se for alfabético
        if letra.isalpha():

            # Libera para interromper novamente
            aconteceuEspaco = True
'''
