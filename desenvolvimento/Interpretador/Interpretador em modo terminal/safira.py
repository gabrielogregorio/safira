from time import sleep
from threading import Thread
from os import system, name, path
import sys
from interpretador import Interpretador
import funcoes as funcoes
import os

import re
LST_BREAKPOINTS = []
BOOL_IGNORAR_TODOS_BREAKPOINTS = True
ESPERAR_PRESSIONAR_ENTER = False


class Console:
    def __init__(self, bool_logs, idioma):
        self.bool_logs = bool_logs
        self.diretorio_base = os.getcwd() + "/"
        self.dicLetras = {}
        self.dic_comandos = funcoes.carregar_json('comandos.json')

        self.idioma = idioma
        self.tx_terminal = None

        self.esperar_pressionar_enter = ESPERAR_PRESSIONAR_ENTER
        self.lst_breakpoints = LST_BREAKPOINTS
        self.bool_ignorar_todos_breakpoints = BOOL_IGNORAR_TODOS_BREAKPOINTS

    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def gerar_dicionario_letras(self):
        self.dicLetras = {}
        for k, v in self.dic_comandos.items():
            self.dicLetras[k] = []
            for valor in v["comando"]:
                valor = valor[0].strip()

                if valor == "":
                    self.dicLetras[k].append(valor)
                else:
                    valor = valor.lower()

                    if valor[0] not in self.dicLetras[k]:
                        self.dicLetras[k].append(valor[0])

    def marcar_linhas(self, linhas):
        # Marcando as linhas com um número, [numero da linha]
        lista = linhas.split('\n')
        nova_linha = ''
        for linha in range(len(lista)):
            nova_linha += '[{}]{}\n'.format(str(linha+1), lista[linha])
        return nova_linha

    def iniciar(self, linhas, tx_terminal=None):
        self.tx_terminal = tx_terminal
        # Obter o comandos
        Console.gerar_dicionario_letras(self)

        # Marcar número de cada linha
        nova_linha = Console.marcar_linhas(self, linhas)

        # Instãncia do terminal
        self.instancia = Interpretador(self.bool_logs, self.lst_breakpoints, self.bool_ignorar_todos_breakpoints, self.diretorio_base, self.dicLetras, self.dic_comandos, self.idioma)

        # Remove comentários
        nova_linha = self.instancia.cortar_comentarios(nova_linha)

        # Inicia o interpretador
        t = Thread(target=lambda codigoPrograma=nova_linha: self.instancia.orquestrador_interpretador_(codigoPrograma))
        t.start()

        # Executa as intruções do interpretador
        # Enquanto não finalizar ou o interpretador não ser iniciado
        valor_antigo = 0
        tx_terminal = self.tx_terminal
        p_cor_num = 0
        while self.instancia.numero_threads_ativos != 0 or not self.instancia.boo_orquestrador_iniciado:
            if tx_terminal is not None:

                try:
                    self.tela.update()
                    self.tx_editor_codigo.update()
                    self.tx_terminal.update()
                except:
                    self.instancia.aconteceu_erro = True
                    break


            acao = self.instancia.controle_interpretador

            if acao != "":

                regex = r"^\:(.*?)\:(.*?)\:(.*?)\:(.*)"
                valores = None
                valores = re.search(regex, acao)
                cor = ""
                instrucao = ""

                if valores is not None:            
                    instrucao = valores.group(1)
                    cor = valores.group(3)
                    linha = valores.group(4)

                if instrucao == 'nessaLinha':

                    if self.tx_terminal is None:
                        print(linha, end="")
                    else:

                        try:
                            self.tx_terminal.update()
                        except:
                            self.instancia.aconteceu_erro = True
                            break

                        inicio_cor = float(self.tx_terminal.index("end-1line lineend"))
                        self.tx_terminal.insert(END, linha)
    
                        if cor != "":
                            fim_cor = float(self.tx_terminal.index("end-1line lineend"))

                            self.tx_terminal.tag_add("palavra"+str(p_cor_num), inicio_cor, fim_cor)
                            self.tx_terminal.tag_config("palavra"+str(p_cor_num), foreground=cor)
                            p_cor_num += 1
                        self.tx_terminal.update()

                    self.instancia.controle_interpretador = ""

                elif instrucao == 'mostreLinha':

                    if self.tx_terminal is None:
                        print(linha)
                    else:

                        try:
                            self.tx_terminal.update()
                        except:
                            self.instancia.aconteceu_erro = True
                            break
 
                        inicio_cor = float(self.tx_terminal.index("end-1line lineend"))

                        self.tx_terminal.insert(END, linha + '\n')
                        self.tx_terminal.update()

                        if cor != "":
                            fim_cor = float(self.tx_terminal.index("end-1line lineend"))
                            self.tx_terminal.tag_add("palavra"+str(p_cor_num), inicio_cor, fim_cor)
                            self.tx_terminal.tag_config("palavra"+str(p_cor_num), foreground=cor)
                            p_cor_num += 1
                        self.tx_terminal.update()

                    self.instancia.controle_interpretador = ""




                elif acao == ':input:':

                    if self.tx_terminal is None:
                        digitado = input()

                    else:
                        textoOriginal = len(self.tx_terminal.get(1.0, END))

                        # Espera o usuário pressionar enter
                        self.esperar_pressionar_enter = True
                        while self.esperar_pressionar_enter:

                            # Atualiza a interface
                            self.tx_editor_codigo.update()
                            self.tela.update()

                            try:
                                self.tx_terminal.update()
                            except:
                                self.instancia.aconteceu_erro = True
                                break

                        if not self.instancia.aconteceu_erro:
                            digitado = self.tx_terminal.get(1.0, END)
                            digitado = digitado[textoOriginal - 1:-2]

                            self.esperar_pressionar_enter = False
                        else:
                            break

                    self.instancia.texto_digitado = digitado.replace("\n", "")
                    self.instancia.controle_interpretador = ""

                elif acao == 'limpar_tela':

                    # Limpar a interface ou o terminal
                    if self.tx_terminal is None:
                        clear()
                    else:
                        try:
                            self.tx_terminal.delete('1.0', END)
                        except Exception as erro:
                            self.instancia.aconteceu_erro = True
                            break

                        

                    # Atualiza o interpretador para continuar
                    self.instancia.controle_interpretador = ""

                elif acao == 'aguardando_breakpoint':
                    # Modo debug
                    if tipo_exec == 'debug':
                        try:
                            self.linha_analise = int(self.instancia.num_linha)
                            if self.linha_analise != valor_antigo:
                                valor_antigo = self.linha_analise
                                self.cont_lin.linha_analise = self.linha_analise
                                self.cont_lin.desenhar_linhas()
                                self.tela.update()
                                self.tx_editor_codigo.update()
                        except Exception as erro:
                            print("Erro update", erro)

                    libera_breakpoint = False
                    while not libera_breakpoint:
                        self.tx_terminal.update()
                        self.tx_editor_codigo.update()
                        self.tela.update()

                    libera_breakpoint = False

                    self.instancia.controle_interpretador = ""
                else:
                    print("Instrução do Interpretador não é reconhecida => '{}'".format(acao))


        if self.instancia.aconteceu_erro:
            if tx_terminal is None:
                print("Erro : ", self.instancia.mensagem_erro)
                print("Linha: ", self.instancia.linha_que_deu_erro)

            else:
                # Se o erro foi avisado
                if self.instancia.erro_alertado is True:
                    if self.instancia.mensagem_erro != "Interrompido":
                        if self.instancia.mensagem_erro != "Erro ao iniciar o Interpretador":
                            Interface.mostrar_mensagem_de_erro(self, self.instancia.mensagem_erro, self.instancia.dir_script_aju_erro, self.instancia.linha_que_deu_erro)

        del self.instancia

bool_logs = False
idioma = "pt-br"

a = open(sys.argv[1], 'r')
t = a.read()
a.close()

i = Console(bool_logs, idioma)
i.iniciar(t)
