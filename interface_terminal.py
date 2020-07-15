#!/usr/bin/python3.8

from threading import Thread
from libs.interpretador import Interpretador
from time import sleep 
from os import system, name 

import libs.funcoes as funcoes
import sys


def clear(): 
    # Windows 
    if name == 'nt': 
        system('cls') 
  
    # Mac e Linux
    else: 
        system('clear') 
global esperar_pressionar_enter
esperar_pressionar_enter = False

def iniciar(linhas, tx_terminal=None):
    global esperar_pressionar_enter
    dic_comandos, dic_designRemover, cor_do_comando = funcoes.atualiza_configuracoes_temas()

    dicLetras = {}
    for k, v in dic_comandos.items():
        dicLetras[k] = []
        for valor in v["comando"]:
            valor = valor[0].strip()

            if valor != "":
                valor = valor.lower()

                if valor[0] not in dicLetras[k]:
                    dicLetras[k].append(  valor[0] )

    bool_logs = False
    bool_ignorar_todos_breakpoints = True
    diretorio_base = '/'


    nova_linha = ''
    lista = linhas.split('\n')

    for linha in range(len(lista)):
        nova_linha += '[{}]{}\n'.format( str(linha + 1), lista[linha] )

    instancia = Interpretador(bool_logs, [], bool_ignorar_todos_breakpoints, diretorio_base, dicLetras, dic_comandos)
    t = Thread(target=lambda codigoPrograma = nova_linha: instancia.orquestrador_interpretador_(codigoPrograma))
    t.start()

    while instancia.numero_threads_ativos != 0 or not instancia.boo_orquestrador_iniciado:
        if tx_terminal is not None:
            tela.update()
            tx_terminal.update()

        acao = instancia.controle_interpretador
        if acao != "":

            if acao.startswith(':nessaLinha:'):
                
                if tx_terminal is None:
                    print(acao[len(':nessaLinha:') : ], end="")
                else:                                   
                    tx_terminal.insert(END, acao[len(':nessaLinha:') : ])
                
                instancia.controle_interpretador = ""

            elif acao.startswith(':mostreLinha:'):
                if tx_terminal is None:
                    print(acao[len(':mostreLinha:') : ])
                else:
                    tx_terminal.insert(END, acao[len(':mostreLinha:') : ] + '\n')

                instancia.controle_interpretador = ""


            elif acao == ':input:':

                if tx_terminal is None:
                    instancia.texto_digitado = input()

                else:
                    textoOriginal = len(tx_terminal.get(1.0, END))
                    global esperar_pressionar_enter

                    esperar_pressionar_enter = True
                    while esperar_pressionar_enter:
                        tx_terminal.update()
                        tx_codfc.update()
                        tela.update()

                    digitado = tx_terminal.get(1.0, END)
                    digitado = digitado[textoOriginal - 1:-2]

                    esperar_pressionar_enter = False
                
                instancia.texto_digitado = digitado.replace("\n", "")
                instancia.controle_interpretador = ""


            elif acao == 'limpar_tela':
                if tx_terminal is None:
                    clear()
                else:
                    tx_terminal.delete('1.0', END)
                instancia.controle_interpretador = ""

            elif acao == 'aguardando_breakpoint':
                print("função indisponível")
            else:
                print("INFORMAÇÂO NAO MAPEADA")

    if instancia.aconteceu_erro:
        if tx_terminal is None:
            print("linha erro ", instancia.linha_que_deu_erro)
            print("scrit help ", instancia.dir_script_aju_erro)
            print("mensa erro ", instancia.mensagem_erro)
        else:
            alerta_erro = 'Erro na linha {}, mensagem: {}, script de ajuda: {}'.format(
                instancia.linha_que_deu_erro,
                instancia.mensagem_erro,
                instancia.dir_script_aju_erro
            )
            tx_terminal.insert(END, alerta_erro)


'''
    n = 1

while n < 10 {
    n = n + 1
    print n
}
'''








def altera_status_enter(event=None):
    global esperar_pressionar_enter
    esperar_pressionar_enter = False


from tkinter import *

tela = Tk()

tx_codfc = Text(tela)
tx_codfc.grid(row=1, column=1, sticky=NSEW)

tx_terminal = Text(tela)
tx_terminal.bind("<Return>", altera_status_enter)
tx_terminal.grid(row=1, column=2, sticky=NSEW)

bt = Button(tela, text="iniciar", command=lambda event=None: iniciar(tx_codfc.get('1.0', END), tx_terminal))
bt.grid()

tela.mainloop()


#iniciar(t)