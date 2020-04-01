#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Futuro
[ ] Copiar código na Wiki na área de transferência
[X] Analise de comandos por posição
[ ] Controle em linhas, mostre na linha 12 para gráficos
[ ] lista posto na posicao i ate a posicao 3 no passo de 2


Ambiente:
[X] Windows 10, Ubuntu 19.10, Kali Linux
[X] Sublime text 3
[X] color Schema = Dracula
[X] Theme = Darkmatter
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
from random import randint
from time import sleep
from time import time
from json import load
from os.path import abspath
from os import listdir
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
__last_update__ = '31/03/2020'
__version__     = '0.1'

global arquivo_aberto_atualmente
global bool_tela_em_fullscreen
global aconteceu_erro
global lista_titulos_frames
global fr_help
global numeros_thread_interpretador
global altura_widget
global tx_terminal
global tx_codificacao

global numero_log
global esperar_pressionar_enter
global dic_funcoes
global dic_variaveis
global lb_linhas
global dic_design
global cor_do_comando
global top_janela_terminal
global erro_alertado
global posCorrente
global posAbsuluta
global boo_orquestrador_iniciado

numeros_thread_interpretador = 0
esperar_pressionar_enter = False
arquivo_aberto_atualmente = {'link': None,'texto': None}
bool_tela_em_fullscreen = False
lista_titulos_frames = []
aconteceu_erro = False
dic_variaveis = {}
dic_funcoes = {}
posAbsuluta = 0
posCorrente = 0
numero_log = 1
path = abspath(getcwd())

dic_comandos, dic_design, cor_do_comando = atualiza_configuracoes_temas()

def salvarArquivoComoDialog(event = None):
    global arquivo_aberto_atualmente

    arquivo = filedialog.asksaveasfile(mode='w',
        defaultextension=".fyn",
        title = "Selecione o script",
        filetypes = (("Meus scripts", "*.fyn"), ("all files", "*.*")))

    lnk_arquivo_salvar = str(arquivo.name)

    if arquivo is None:
        return None

    arquivo.close()

    text2save = str(tx_codificacao.get(1.0, END))

    try:

        arquivo = open(lnk_arquivo_salvar, 'w', encoding='utf8')
        arquivo.write(text2save[0:-1])
        arquivo.close()

    except Exception as erro:
        messagebox.showinfo('Erro', 'Erro ao salvar programa, erro: {}'.format(erro))
        log(" Erro ao salvar o arquivo, erro: {}".format(erro))

    else:
        arquivo_aberto_atualmente['link'] = arquivo.name
        arquivo_aberto_atualmente['texto'] = text2save
        return arquivo.name

def salvarArquivo(event=None):
    '''
    Salva um arquivo que já está aberto
    '''

    global arquivo_aberto_atualmente

    if arquivo_aberto_atualmente['link'] == None:
        salvarArquivoComoDialog()

    else:
        programaCodigo = tx_codificacao.get(1.0, END)

        if arquivo_aberto_atualmente['texto'] != programaCodigo:
            try:
                arquivo = open(arquivo_aberto_atualmente['link'], 'w', encoding='utf8')
                arquivo.write(programaCodigo[0:-1])
                arquivo.close()

            except Exception as erro:
                messagebox.showinfo('Erro', 'Não foi possível salvar essa versão do código, erro: {}'.format(erro))
                log(" Não foi possível salvar essa versão do código")
            else:
                arquivo_aberto_atualmente['texto'] = programaCodigo
        else:
            log(" Programa não sofreu modificações para ser salvo novamente....")

def abrirArquivoDialog(event=None):
    global arquivo_aberto_atualmente

    ftypes = [('Scripts fyn', '*.fyn'), ('Todos os arquivos', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    filename = dlg.show()

    if filename != ():
        log(' Arquivo "{}" escolhido'.format(filename))
        arquivo = abrir_arquivo(filename)

        if arquivo[0] != None:
            tx_codificacao.delete(1.0, END)
            tx_codificacao.insert(END, arquivo[0])

        else:
            messagebox.showinfo("ops","Aconteceu um erro ao abrir o arquivo" + arquivo[1])

        coordena_coloracao(None, fazer = 'nada')

        arquivo_aberto_atualmente['link'] = filename
        arquivo_aberto_atualmente['texto'] = arquivo[0]
    else:
        log(' Nenhum arquivo escolhido')

def abrirArquivo(link):
    global arquivo_aberto_atualmente

    log(' Abrindo arquivo "{}" escolhido'.format(link))

    arquivo = abrir_arquivo(link)

    if arquivo[0] != None:
        tx_codificacao.delete(1.0, END)
        tx_codificacao.insert(END, arquivo[0])

        coordena_coloracao(None, fazer = 'nada')

        arquivo_aberto_atualmente['link'] = link
        arquivo_aberto_atualmente['texto'] = arquivo[0]

    else:
        if "\'utf-8' codec can\'t decode byte" in arquivo[1]:
            messagebox.showinfo("Erro de codificação", "Por favor, converta seu arquivo para a codificação UTF-8. Não foi possível abrir o arquivo: \"{}\", erro: \"{}\"".format(link, arquivo[1]))
        else:
            messagebox.showinfo('Erro', 'Aconteceu um erro ao tentar abrir o script: {}, erro: {}'.format(link, arquivo[1]))

        print('Arquivo não selecionado')

def realiza_coloracao(palavra, linha, valor1, valor2, cor):
    """
        Realiza a coloracao de uma unica palavra
    """

    linha1 = '{}.{}'.format(linha , valor1)
    linha2 = '{}.{}'.format(linha , valor2)

    tx_codificacao.tag_add(palavra, linha1 , linha2)
    tx_codificacao.tag_config(palavra, foreground = cor)

def realiza_coloracao_erro(palavra, valor1, valor2, cor='red', linhaErro = None):
    """
        Colore uma linha de erro no terminal
    """

    global tx_terminal
    global tx_codificacao
    global erro_alertado

    linha = tx_terminal.get(1.0, END)
    linha = len(linha.split('\n')) - 1

    linha1 = '{}.{}'.format(linha, valor1)
    linha2 = '{}.{}'.format(linha, valor2)

    tx_terminal.tag_add(palavra, linha1 , linha2)
    tx_terminal.tag_config(palavra, foreground = cor)

    if linhaErro != None:

        lista = tx_codificacao.get(1.0, END).split("\n")
        
        palavra = "**_erro_alertado_**"
        linha1 = str(linhaErro) + ".0"
        linha2 = str(linhaErro) + "." + str(len(lista[int(linhaErro) - 1]))

        tx_codificacao.tag_add(palavra, linha1 , linha2)
        tx_codificacao.tag_config(palavra, background = "#dd3344")

    erro_alertado = True

def analisa_coloracao(palavra, cor, lista):
    """
        Realiza a coloração seguindo instruções
    """

    global tx_codificacao

    cor = cor['foreground']
    tx_codificacao.tag_delete(palavra)

    palavra_comando = palavra.replace('+', '\\+')
    palavra_comando = palavra_comando.replace('/', '\\/')
    palavra_comando = palavra_comando.replace('*', '\\*')


    for linha in range(len(lista)):

        if palavra == "numerico":
            for valor in finditer(
                '(^|\\s|\\,)([0-9\\.]\\s*){1,}($|\\s|\\,)', lista[linha]):
                realiza_coloracao(
                    str(palavra), str(linha+1), valor.start(), valor.end(), cor)

        elif palavra == "comentario":
            for valor in finditer('(#|\\/\\/).*$', lista[linha]):
                realiza_coloracao(
                    str(palavra), str(linha+1), valor.start(), valor.end(), cor)

            # Comentário longo /**/
            for valor in finditer('(\\/\\*[^\\*\\/]*\\*\\/)', lista[linha]):
                realiza_coloracao(
                    str(palavra+'longa'), str(linha+1), valor.start(), valor.end(), cor)

        elif palavra == '"':
            for valor in finditer("""\"[^"]*\"""", lista[linha]):
                realiza_coloracao(
                    str(palavra), str(linha+1), valor.start(), valor.end(), cor)

        else:
            palavra_comando = palavra_comando.replace(' ','\\s*')
            for valor in finditer('(^|\\s){}(\\s|$)'.format(palavra_comando), lista[linha]):
                realiza_coloracao(
                    str(palavra), str(linha+1), valor.start(), valor.end(), cor)

def define_coloracao(chave_comando, chave_cor, lista):
    for comando in dic_comandos[ chave_comando ]:
        analisa_coloracao(comando[0].strip(), cor_do_comando[ chave_cor ], lista)

def coordena_coloracao(event = None, fazer = 'tudo'):
    """
        Coordena a coloração de todos os comandos
    """

    
    global cor_do_comando
    global tx_codificacao

    configuracoes(ev = None)

    if event != None: # não modifica o código
        if event.keysym in ('Down','Up','Left','Right'):
            return 0

    try:

        #if fazer == 'tudo':
        #    th = Thread(target=obterPosicaoDoCursor)
        #    th.start()

        lista = tx_codificacao.get(1.0, END).lower().split('\n')

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

        tx_codificacao.update()

    except Exception as erro:
        print("Erro ao atualizar coloracao", erro)

def log(mensagem):
    global numero_log
    #numero_log += 1

    #print(str(numero_log) + '-' + mensagem)

def inicializador_orquestrador_interpretador(event = None):
    """
        Inicicaliza o orquestrador que analisa blocos de código
    """
    global numeros_thread_interpretador
    global aconteceu_erro
    global tx_codificacao
    global dic_variaveis
    global erro_alertado
    global dic_funcoes
    global esperar_pressionar_enter
    global boo_orquestrador_iniciado

    inicio = time()

    if numeros_thread_interpretador != 0:
        messagebox.showinfo('Problemas',"Já existe um programa sendo executado!")
        return 0

    numeros_thread_interpretador = 0
    aconteceu_erro = False
    erro_alertado = False
    esperar_pressionar_enter = False
    dic_variaveis = {}
    dic_funcoes = {}

    inicializador_terminal()
    tx_terminal.delete('1.0', END)

    linhas = tx_codificacao.get('1.0', END)
    nova_linha = ''

    lista = linhas.split('\n')
    for linha in range(len(lista)):
        nova_linha += '[{}]{}\n'.format(str(linha + 1), lista[linha])
    
    linhas = nova_linha

    logs = '> '

    boo_orquestrador_iniciado = False

    t = Thread(target=lambda codigoPrograma = linhas, logs = logs: orquestrador_interpretador(codigoPrograma, logs))
    t.start()

    while numeros_thread_interpretador != 0 or not boo_orquestrador_iniciado:
        tela.update()

    try:
        tx_terminal.insert(END, '\nScript finalizado em {:.3} segundos'.format(time() - inicio))
        tx_terminal.see("end")
 
    except Exception as erro:
        log(logs + 'Impossível exibir mensagem de finalização, erro: '+ str(erro))

def orq_erro(mensagem, linhaAnalise):
    global aconteceu_erro
    global erro_alertado

    aconteceu_erro = True

    if not erro_alertado:
        tx_terminal.insert(END, "\n" + "[" + linhaAnalise + "]" + mensagem)
        realiza_coloracao_erro('codigoErro', valor1=0, valor2=len(mensagem)+1, cor='#ffabab', linhaErro = linhaAnalise )

def orq_exibir_tela(lst_retorno_ultimo_comando):
    global tx_terminal

    if ":nessaLinha:" in str(lst_retorno_ultimo_comando[1]):
        tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1][len(":nessaLinha:"):]))
    else:
        tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1])+'\n')
    tx_terminal.see("end")

def orquestrador_interpretador(txt_codigo, logs):
    logs = '  ' + logs
    log(logs + '<orquestrador_interpretador>:' + txt_codigo)

    global numeros_thread_interpretador
    global aconteceu_erro
    global dic_funcoes
    global boo_orquestrador_iniciado

    numeros_thread_interpretador += 1
    boo_orquestrador_iniciado = True

    int_tamanho_codigo = len(txt_codigo)

    bool_comentario_longo = False
    bool_salvar_bloco = False
    bool_comentario = False
    bool_texto = False

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

                lst_analisa = interpretador(str_linha, logs)

                if lst_analisa[0][3] == 'linhaVazia':
                    str_linha = ""
                else:
                    lst_ultimo_ret = lst_analisa
                    linhaComCodigoQueFoiExecutado = str_linha
                    linhaAnalise = lst_ultimo_ret[1]
                    lst_ultimo_ret = lst_ultimo_ret[0]

                    # SE DEU ERRO
                    if lst_ultimo_ret[0] == False:

                        if lst_ultimo_ret[1] == 'indisponibilidade_terminal':
                            numeros_thread_interpretador -= 1
                            return [True, 'Orquestrador Finalizado', 'string']

                        orq_erro(lst_ultimo_ret[1], linhaAnalise)
                        numeros_thread_interpretador -= 1
                        return lst_ultimo_ret

                    if lst_ultimo_ret[3] == 'exibirNaTela':
                        orq_exibir_tela(lst_ultimo_ret)

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
            log(logs + '!<Analisa bloco salvo>:"' + str_bloco + '"')

            bool_salvar_bloco = False

            if lst_ultimo_ret[3] == 'declararLoop':

                # Enquanto a condição for verdadeira
                while lst_ultimo_ret[1] and not aconteceu_erro:

                    lst_resultado_execucao = orquestrador_interpretador(
                        str_bloco[1:].strip(), logs)

                    if lst_resultado_execucao[0] == False:
                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            numeros_thread_interpretador -= 1
                            return [True, 'Orquestrador Finalizado', 'string']

                        orq_erro(lst_resultado_execucao[1], "xx")
                        numeros_thread_interpretador -= 1
                        return lst_resultado_execucao

                    # Testa novamente a condição do loo
                    lst_ultimo_ret = interpretador(linhaComCodigoQueFoiExecutado, logs)
                    linhaAnalise = lst_ultimo_ret[1]
                    lst_ultimo_ret = lst_ultimo_ret[0]

                    if lst_ultimo_ret[0] == False:

                        if lst_ultimo_ret[1] == 'indisponibilidade_terminal':
                                numeros_thread_interpretador -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                        orq_erro(lst_ultimo_ret[1], linhaAnalise)
                        numeros_thread_interpretador -= 1
                        return lst_ultimo_ret

            elif lst_ultimo_ret[3] == "declararLoopRepetir":
                lst_ultimo_ret[3] = 'fazerNada'

                for valor in range(0, lst_ultimo_ret[1]):
                    lst_resultado_execucao = orquestrador_interpretador(
                        str_bloco[1:].strip(), logs)

                    if lst_resultado_execucao[0] == False:
                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            numeros_thread_interpretador -= 1
                            return [True, 'Orquestrador Finalizado', 'string']

                        orq_erro(lst_resultado_execucao[1], "xx2")
                        numeros_thread_interpretador -= 1
                        return lst_resultado_execucao

                lst_ultimo_ret[1] = 0
                lst_ultimo_ret = [True, False, 'booleano']

            elif lst_ultimo_ret[3] == "declararFuncao":
                lst_ultimo_ret[3] = "fazerNada"
                dic_funcoes[lst_ultimo_ret[4]] = [dic_funcoes[lst_ultimo_ret[4]][0], str_bloco[1:].strip()]


            elif lst_ultimo_ret[3] == 'declararCondicional':
                if lst_ultimo_ret[1] == True:

                    lst_resultado_execucao = orquestrador_interpretador(str_bloco[1:].strip(), logs)

                    if lst_resultado_execucao[0] == False:
                        if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                            numeros_thread_interpretador -= 1
                            return [True, 'Orquestrador Finalizado', 'string']

                        orq_erro(lst_resultado_execucao[1], "xx3")
                        numeros_thread_interpretador -= 1
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
        lst_ultimo_ret = interpretador(str_linha, logs)
        linhaComCodigoQueFoiExecutado = str_linha
        linhaAnalise = lst_ultimo_ret[1]
        lst_ultimo_ret = lst_ultimo_ret[0]

        if lst_ultimo_ret[0] == False:
            if lst_ultimo_ret[1] == 'indisponibilidade_terminal':
                numeros_thread_interpretador -= 1
                return [True, 'Orquestrador Finalizado', 'string']

            orq_erro(lst_ultimo_ret[1], linhaAnalise)
            numeros_thread_interpretador -= 1
            return lst_ultimo_ret

        if lst_ultimo_ret[3] == 'exibirNaTela':
            orq_exibir_tela(lst_ultimo_ret)

    # Aviso de erros de profundidade
    if int_profundidade > 0:
        numeros_thread_interpretador -= 1
        return [False, None, 'vazia']

    elif int_profundidade < 0:
        numeros_thread_interpretador -= 1
        return [False, None, 'vazia']

    numeros_thread_interpretador -= 1
    return [True, 'Orquestrador Finalizado', 'string']

def analisa_instrucao(comando, texto, grupos_analisar):

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

def interpretador(linha, logs):
    global tx_terminal
    global aconteceu_erro
    try:
        tx_terminal.get(1.0, 1.1)
    except:
        return [[False, 'indisponibilidade_terminal', 'string','exibirNaTela'], "1"]

    logs = '  ' + logs
    log(logs + '<interpretador>:"' + linha + '"')

    if aconteceu_erro:
        return [[False, 'Erro ao iniciar o Interpretador', 'string','exibirNaTela'], "1"]

    linha = linha.replace('\n', '')
    linha = linha.strip()

    # Se for uma linha vazia
    if linha == '':
        return [[True, None, 'vazio','linhaVazia'], "1"]

    else:
        num_linha = "0"
        posicoes = finditer(r'^(\[\d*\])', linha)

        # Obter o número da linha
        for uma_posicao in posicoes:
            num_linha = linha[1 : uma_posicao.end()-1]
            linha = linha[uma_posicao.end() : ]
            linha = linha.strip()
            break

        # Se a linha continuar vazia
        if linha == '':
            return [[True, None, 'vazio','linhaVazia'],"1"]

        analisa = analisa_instrucao('^(<limpatela>)$', linha, grupos_analisar = [1])
        if analisa != False:
            return [funcao_limpar_tela(logs), num_linha]

        analisa = analisa_instrucao('^(<mostreNessa>)(.*)$', linha, grupos_analisar = [2])
        if analisa != False:
            return [funcao_exibir_na_linha(analisa[0], logs), num_linha]

        analisa = analisa_instrucao('^(<mostre>)(.*)$', linha, grupos_analisar = [2])
        if analisa != False:
            return [funcao_exibir(analisa[0], logs), num_linha]

        analisa = analisa_instrucao('^(<se>)(.*)$', linha, grupos_analisar = [2])
        if analisa != False:
            return [funcao_condicional(analisa[0], logs), num_linha]

        analisa = analisa_instrucao('^(<enquanto>)(.*)$', linha, grupos_analisar = [2])
        if analisa != False:
            return [funcao_loops_enquanto(analisa[0], logs), num_linha]

        analisa = analisa_instrucao('^(<aguarde>)(.*)(<esperaEm>)$', linha, grupos_analisar = [2,3])
        if analisa != False:
            return [funcao_tempo(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<repita>)(.*)(<repitaVezes>)$', linha, grupos_analisar = [2])
        if analisa != False:
            return [funcao_repetir(analisa[0], logs), num_linha]

        analisa = analisa_instrucao('^(<incremente>)(.*)(<incrementeDecremente>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [incremente_em(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<decremente>)(.*)(<incrementeDecremente>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [decremente_em(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<funcoes>)(.*)(<recebeParametros>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_declarar_funcao(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<declaraListas>)(.*)(<listaNaPosicao>)(.*)(<recebeDeclaraListas>)(.*)$', linha, grupos_analisar = [2, 4, 6])
        if analisa != False:
            return [funcao_adicione_na_lista_na_posicao(analisa[0], analisa[1], analisa[2], logs), num_linha]

        analisa = analisa_instrucao('^(<declaraListas>)(.*)(<listaCom>)(.*)(<listaPosicoesCom>)$', linha, grupos_analisar = [2,4])
        if analisa != False:
            return [funcao_declarar_listas_posicoes(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<declaraListas>)(.*)(<recebeDeclaraListas>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_declarar_listas(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<RemoverItensListas>)(.*)(<RemoverItensListasInterno>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_remover_itens_na_lista(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<adicionarItensListas>)(.*)(<addItensListaInternoPosicao>)(.*)(<addItensListaInternoPosicaoFinaliza>)(.*)$', linha, grupos_analisar = [2, 4, 6])
        if analisa != False:
            return [funcao_adicionar_itens_na_lista_posicao(analisa[0], analisa[1], analisa[2], logs), num_linha]

        analisa = analisa_instrucao('^(<adicionarItensListas>)(.*)(<addItensListaInternoFinal>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_adicionar_itens_na_lista(analisa[0], analisa[1], logs), num_linha]
            
        analisa = analisa_instrucao('^(<adicionarItensListas>)(.*)(<addItensListaInternoInicio>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_adicionar_itens_na_lista_inicio(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<adicionarItensListas>)(.*)(<addItensListaInterno>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_adicionar_itens_na_lista(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_numero_aleatorio(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_obter_valor_lista(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<digitado>)$', linha, grupos_analisar = [1])
        if analisa != False:
            return [funcao_digitado(analisa[0], logs), num_linha]

        analisa = analisa_instrucao('^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha, grupos_analisar = [2, 4])
        if analisa != False:
            return [funcao_tiver_na_lista(analisa[0],analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(<tamanhoDaLista>)(.*)$', linha, grupos_analisar = [2])
        if analisa != False:
            return [funcao_tamanho_da_lista(analisa[0], logs), num_linha]

        analisa = analisa_instrucao('^(\\s*[a-zA-Z\\_]*)(<declaraVariaveis>)(.*)$', linha, grupos_analisar = [1, 3])
        if analisa != False:
            return [funcao_fazer_atribuicao(analisa[0], analisa[1], logs), num_linha]

        analisa = analisa_instrucao('^(.*)(<passandoParametros>)(.*)$', linha, grupos_analisar = [1,3])
        if analisa != False:
            return [funcao_executar_funcoes(analisa[0],analisa[1], logs), num_linha]

        return [[False, "Um comando desconhecido foi localizado: '{}'".format(linha), 'string','exibirNaTela'], num_linha]
    return [[True, None, 'vazio', 'fazerNada'], num_linha]

def incremente_em(valor, variavel, logs):
    return incremente_decremente(valor, variavel, logs, 'incremente')

def decremente_em(valor, variavel, logs):
    return incremente_decremente(valor, variavel, logs, 'decremente')

def incremente_decremente(valor, variavel, logs, acao):
    logs = '  ' + logs
    log(logs + 'decremente:' + valor+str(variavel))

    teste_existencia = obter_valor_variavel(variavel, logs)
    if teste_existencia[0] == False:
        return teste_existencia

    if teste_existencia[2] != 'float':
        return [False, "A variável \"{}\" não é numérica!".format(variavel), 'string', 'exibirNaTela']

    teste_valor = abstrair_valor_linha(valor, logs)
    if teste_valor[0] == False:
        return teste_valor

    if teste_valor[2] != 'float':
        return [False, "O valor de \"{}\" não é numérico!".format(teste_valor[1]), 'string', 'exibirNaTela']

    if acao == "incremente":
        dic_variaveis[variavel][0] = dic_variaveis[variavel][0] + teste_valor[1]
    else:
        dic_variaveis[variavel][0] = dic_variaveis[variavel][0] - teste_valor[1]

    return [True, True, "booleano", "fazerNada"]

def verifica_se_tem(linha, a_buscar, logs):
    logs = '  ' + logs

    analisar = True
    lista = []

    for caractere in range(len(linha)):
        if linha[caractere] == '"' and analisar == True:
            analisar = False

        elif linha[caractere] == '"' and analisar == False:
            analisar = True

        # Se estiver disponivel para analisar
        if analisar:

            # Se o comando não estourar o limite
            if len(linha) >= caractere + len(a_buscar):

                if linha[caractere : caractere + len(a_buscar) ] == a_buscar:
                    lista.append([caractere, caractere + len(a_buscar) ])

    return lista

def funcao_adicione_na_lista_na_posicao(variavelLista, posicao, valor, logs):
    logs = '  ' + logs
    log(logs + '<funcao_adicione_lista> "{}"'.format(variavelLista))

    if variavelLista == '' or posicao == '' or valor == '':
        return [ False, 'Necessário comando separador como " no meio da lista de "', 'string',' exibirNaTela']

    teste_existencia = obter_valor_variavel(variavelLista, logs)
    if teste_existencia[0] == False:
        return teste_existencia

    if teste_existencia[2] != 'lista':
        return[False, 'A variável "{}" não é uma lista.'.format(variavelLista), 'string']

    testePosicao = abstrair_valor_linha(posicao, logs)

    if testePosicao[0] == False:
        return testePosicao

    if testePosicao[2] != 'float':
        return [False, 'O valor da posição precisa ser numérico',' string', 'exibirNaTela']

    posicao = int(testePosicao[1])

    teste_valor = abstrair_valor_linha(valor, logs)
    if teste_valor[0] == False:
        return teste_valor

    if posicao - 1 > len(dic_variaveis[variavelLista][0]):
        return [False, 'A posição está acima do tamanho da lista', 'string', 'exibirNaTela']

    if posicao < 1 :
        return [False, 'A posição está abaixo do tamanho da lista', 'string', 'exibirNaTela']

    dic_variaveis[variavelLista][0].insert(posicao - 1, [teste_valor[1], teste_valor[2]])
    return [ True, True, 'booleano', 'fazerNada' ]

def obter_valor_lista(linha, logs):
    logs = '  ' + logs
    log(logs + 'obter_valor_lista: "{}"'.format(linha))

    teste = obter_valor_variavel(linha, logs)

    if teste[0] == False:
        return teste

    if teste[2] != 'lista':
        return[False, 'A variável "{}" não é uma lista.'.format(linha), 'string']

    return teste

def funcao_obter_valor_lista(variavel, posicao, logs):
    logs = '  ' + logs
    log(logs + 'Função Valor de lista: "{}", subcomandos: "{}"'.format(variavel, posicao))

    if variavel == '' or posicao == '':
        return [ False, 'Sem variavel passada','string','exibirNaTela']

    busca = abstrair_valor_linha(posicao, logs)
    if busca[0] == False:
        return [busca[0], busca[1], busca[2], 'exibirNaTela']

    try:
        posicao = int(busca[1])
    except:
        return [False, '\'{}\' não é um valor númerico'.format(busca[1]),'string', 'exibirNaTela']

    teste = obter_valor_lista(variavel, logs)
    if teste[0] == False:
        return [teste[0], teste[1], teste[2], 'exibirNaTela']

    resultado = teste[1]

    if len(resultado) < posicao or posicao < 1:
        return [False, 'Posição \'{}\' está fora do escopo da lista {}'.format(posicao, resultado), 'exibirNaTela']

    return [True, resultado[posicao-1][0], resultado[posicao-1][1], 'exibirNaTela']

def funcao_tiver_na_lista(valor, variavel, logs):
    global dic_variaveis
    

    logs = '  ' + logs
    log(logs + 'Função tiver na lista: "{}"'.format(valor))

    if variavel == '' or valor == '':
        return [False, 'É necessário passar um comando de referência, para indicar o que é valor e o que é variável', 'exibirNaTela']

    teste = obter_valor_variavel(variavel, logs)

    if teste[0] == False:
        return [teste[0], teste[1], teste[2], 'exibirNaTela']

    if teste[2] != 'lista':
        return[False, 'A variável "{}" não é uma lista.'.format(linha), 'string', 'exibirNaTela']

    resultado = abstrair_valor_linha(valor, logs)
    if resultado[0] == False:
        return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

    if [resultado[1], resultado[2]] in dic_variaveis[variavel][0]:
        return [True, True, 'booleano', 'fazerNada']

    else:
        return [True, False, 'booleano', 'fazerNada']

def funcao_tamanho_da_lista(linha, logs):
    global dic_variaveis

    logs = '  ' + logs
    log(logs + 'Função obter o tamanho da lista: "{}"'.format(linha))

    linha = linha.strip()

    teste = obter_valor_lista(linha, logs)
    if teste[0] == False:
        return [teste[0], teste[1], teste[2], 'exibirNaTela']

    try:
        return [True, len(dic_variaveis[linha][0]), 'float', 'fazerNada']

    except Exception as erro:
        return [True, 'Erro ao obter o tamanho da lista. Erro: {}'.format(erro), 'string', 'exibirNaTela']

def funcao_remover_itens_na_lista(valor, variavel, logs):
    global dic_variaveis
    

    logs = '  ' + logs
    log(logs + 'Função remover itens da lista: "{}"'.format(valor))

    if variavel == '' or valor == '':
        return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Remova 1 a lista de nomes ', 'exibirNaTela']

    # Analisa se lista foi decarada e se é lista
    teste = obter_valor_lista(variavel, logs)
    if teste[0] == False:
        return [teste[0], teste[1], teste[2], 'exibirNaTela']

    resultado = abstrair_valor_linha(valor, logs)

    if resultado[0] == False:
        return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

    try:
        dic_variaveis[variavel][0].remove([resultado[1], resultado[2]])

    except Exception as erro:
        return [ False, '"{}" Não está na lista "{}"!'.format(resultado[1], variavel), 'string', 'exibirNaTela']

    return [True, None, 'vazio', 'fazerNada']

def funcao_adicionar_itens_na_lista(valor, variavel, logs):
    global dic_variaveis
    

    logs = '  ' + logs
    log(logs + 'Função remover itens da lista: "{}"'.format(valor))

    if variavel == '' or valor == '':
        return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Adicione 1 a lista de nomes ', 'exibirNaTela']

    # Analisa se lista foi decarada e se é lista
    teste_variavel = obter_valor_lista(variavel, logs)
    teste_valor = abstrair_valor_linha(valor, logs)

    if teste_variavel[0] == False:
        return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

    if teste_valor[0] == False:
        return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

    try:
        dic_variaveis[variavel][0].append([teste_valor[1], teste_valor[2]])

    except Exception as erro:
        return [ False, '"{}" Não está na lista "{}"!'.format(teste_valor[1], variavel), 'string', 'exibirNaTela']

    return [True, None, 'vazio', 'fazerNada']

def funcao_adicionar_itens_na_lista_inicio(valor, variavel, logs):
    global dic_variaveis
    

    logs = '  ' + logs
    log(logs + 'Função remover itens da lista: "{}"'.format(valor))

    if variavel == '' or valor == '':
        return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Adicione 1 a lista de nomes ', 'exibirNaTela']

    # Analisa se lista foi decarada e se é lista
    teste_variavel = obter_valor_lista(variavel, logs)
    teste_valor = abstrair_valor_linha(valor, logs)

    if teste_variavel[0] == False:
        return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

    if teste_valor[0] == False:
        return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

    try:
        dic_variaveis[variavel][0].insert(0, [teste_valor[1], teste_valor[2]])

    except Exception as erro:
        return [ False, '"{}" Não foi possivel inserir o elemento na posição inicial"{}"!'.format(teste_valor[1], variavel), 'string', 'exibirNaTela']

    return [True, None, 'vazio', 'fazerNada']

def funcao_adicionar_itens_na_lista_posicao(valor, posicao, variavel, logs):
    global dic_variaveis
    

    logs = '  ' + logs
    log(logs + 'Função remover itens da lista: "{}"'.format(valor))

    if variavel == '' or valor == '':
        return [False, '2 É necessário passar um comando de referência, para indicar o que é valor e o que é variável. Como " Adicione 1 a lista de nomes ', 'exibirNaTela']

    # Analisa se lista foi decarada e se é lista
    teste_variavel = obter_valor_lista(variavel, logs)
    teste_valor = abstrair_valor_linha(valor, logs)
    teste_posicao = abstrair_valor_linha(posicao, logs)

    if teste_variavel[0] == False:
        return [teste_variavel[0], teste_variavel[1], teste_variavel[2], 'exibirNaTela']

    if teste_valor[0] == False:
        return [teste_valor[0], teste_valor[1], teste_valor[2], 'exibirNaTela']

    if teste_posicao[0] == False:
        return [teste_posicao[0], teste_posicao[1], teste_posicao[2], 'exibirNaTela']

    if teste_posicao[2] != 'float':
        return [False, 'A variável posição não é numérica', 'string', 'exibirNaTela']

    posicao = int(teste_posicao[1])

    if posicao - 1 > len(dic_variaveis[variavel][0]):
        return [False, 'A posição está acima do tamanho da lista', 'string', 'exibirNaTela']

    if posicao < 1 :
        return [False, 'A posição está abaixo do tamanho da lista', 'string', 'exibirNaTela']

    dic_variaveis[variavel][0].insert(posicao - 1, [teste_valor[1], teste_valor[2]])
    return [ True, True, 'booleano', 'fazerNada' ]

def funcao_declarar_listas_posicoes(variavel, posicoes, logs):
    # nomes com 5 posicoes"
    global dic_variaveis
    logs = '  ' + logs
    log(logs + 'Função declarar listas posicoes: "{}"'.format(variavel))

    # Se a variável estier fora de padrao
    teste = analisa_padrao_variavel(logs, variavel, 'Lista ')
    if teste[1] != True:
        return [False, teste[1], teste[2], 'exibirNaTela']

    resultado = abstrair_valor_linha(posicoes, logs)
    if resultado[0] == False:
        return resultado

    if resultado[2] != 'float':
        return [False, 'O valor da posição não é numérico', 'string', 'exibirNaTela']

    listaItensDeclarar = []
    for posicao in range(int(posicoes)):
        listaItensDeclarar.append(['', 'string'])

    dic_variaveis[variavel] = [listaItensDeclarar, 'lista']
    return [True, None, 'vazio', 'fazerNada']

def funcao_declarar_listas(variavel,itens , logs):
    global dic_variaveis
    logs = '  ' + logs
    log(logs + 'Função declarar listas: "{}"'.format(variavel + str(itens) ))

    if itens == '' or variavel == '':
        return [False, 'É necessário um comando de atribuição ao declar uma lista!', 'string', 'exibirNaTela']

    variavel = variavel.strip()

    teste = analisa_padrao_variavel(logs,variavel,'Lista ')
    if teste[1] != True:
        return [False, teste[1], teste[2], 'exibirNaTela']

    testa = verifica_se_tem(itens, ', ', logs)

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
            obterValor = abstrair_valor_linha(item, logs)

            if obterValor[0] == False:
                return [obterValor[0], obterValor[1], obterValor[2], 'exibirNaTela']

            listaItensDeclarar.append([obterValor[1], obterValor[2]])

        dic_variaveis[variavel] = [listaItensDeclarar, 'lista']
        return [True, None, 'vazio', 'fazerNada']

    else:
        obterValor = abstrair_valor_linha(itens, logs)
        if obterValor[0] == False:
            return [obterValor[0], obterValor[1], obterValor[2], 'exibirNaTela']
        lista = []
        lista.append([obterValor[1], obterValor[2]])

        dic_variaveis[variavel] = [lista, 'lista']
        return [True, None, 'vazio', 'fazerNada']

def pressionou_enter(event=None):
    global esperar_pressionar_enter
    if esperar_pressionar_enter:
        esperar_pressionar_enter = False

def funcao_digitado(linha, logs):
    global tx_terminal
    global esperar_pressionar_enter
    global aconteceu_erro

    logs = '  ' + logs
    log(logs + 'Função digitado: "{}"'.format(linha))

    textoOriginal = len(tx_terminal.get(1.0, END))

    esperar_pressionar_enter = True

    # FICAR PRESO NO LOOP ATÉ QUE O USUÁRIO PRESSIONE ENTER
    while esperar_pressionar_enter:
        sleep(0.1)
        if aconteceu_erro:
            return [False, "Interrompido","string","exibirNaTela"]

        else:
            tx_terminal.update()

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

def funcao_limpar_tela(logs):
    global tx_terminal

    logs = '  ' + logs
    log(logs + 'Limpatela ativado!')

    tx_terminal.delete(1.0, END)
    return [True, None, 'vazio','fazerNada']

def funcao_repetir(linha, logs):
    logs = '  ' + logs
    log(logs + 'funcao repetir: "{}"'.format(linha))

    linha = linha.replace('vezes', '')
    linha = linha.replace('vez', '')

    linha = linha.strip()

    linha = abstrair_valor_linha(linha, logs)

    if linha[0] == False:
        return [linha[0], linha[1], linha[2], 'exibirNaTela']

    if linha[2] != 'float':
        return[False, 'Você precisa passar um número inteiro para usar a função repetir: "{}"'.format(linha), 'string', 'exibirNaTela']

    try:
        int(linha[1])
    except:
        return [False, "Para usar a função repetir, você precisa passar um número inteiro. Você passou '{}'".format(linha[1]), 'string', 'exibirNaTela']
    else:
        funcao_repita = int(linha[1])
      
        return [True, funcao_repita, 'float', 'declararLoopRepetir']

def funcao_numero_aleatorio(num1, num2, logs):
    """
        numero aleatório entre 10 e 20
    """

    logs = '  ' + logs
    log(logs + 'funcao aleatório: {}'.format(num1))

    # Obtendo ambos os valores
    num1 = abstrair_valor_linha(num1, logs)
    num2 = abstrair_valor_linha(num2, logs)

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

def funcao_executar_funcoes(nomeDaFuncao, parametros, logs):
    """
        calcMedia passando parametros nota1, nota2
    """

    global dic_funcoes

    try:
        dic_funcoes[nomeDaFuncao]
    except:
        return [False, "A função '{}' não existe".format(nomeDaFuncao), 'string', 'exibirNaTela']

    testa = verifica_se_tem(parametros, ', ', logs)
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
        if len(dic_funcoes[nomeDaFuncao][0]) == len(listaFinalDeParametros):

            for parametroDeclarar in range(len(dic_funcoes[nomeDaFuncao][0])):
                resultado = funcao_fazer_atribuicao(dic_funcoes[nomeDaFuncao][0][parametroDeclarar], listaFinalDeParametros[parametroDeclarar], logs)

                if resultado[0] == False:
                    return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
        else:
            return [False, "A função '{}' tem {} parametros, 2mas você passou {} parametros!".format(nomeDaFuncao, len(dic_funcoes[nomeDaFuncao][0]), len(listaFinalDeParametros)), 'string', 'fazerNada']

    # Se tiver só um parametro
    elif parametros != None:

        if len(dic_funcoes[nomeDaFuncao][0]) == 1:
            resultado = funcao_fazer_atribuicao(dic_funcoes[nomeDaFuncao][0], parametros, logs)

            if resultado[0] == False:
                return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']
        else:
            return [False, "A função '{}' tem {} parametros, mas você passou 1 parametro!".format(nomeDaFuncao, len(dic_funcoes[nomeDaFuncao][0])), 'string', 'exibirNaTela']

    resultadoOrquestrador = orquestrador_interpretador( dic_funcoes[nomeDaFuncao][1], logs)

    if resultadoOrquestrador[0] == False:
        return [resultadoOrquestrador[0], resultadoOrquestrador[1], resultadoOrquestrador[2], 'exibirNaTela']

    return [True, None, 'vazio', 'fazerNada']

def funcao_declarar_funcao(nomeDaFuncao, parametros, logs):
    """
        FUNCAO CALCULAMEDIA RECEBE PARAMENTOS NOTA1, NOTA2
    """

    global dic_funcoes

    logs = '  ' + logs
    log(logs + 'Declarar funcoes: {}'.format(nomeDaFuncao + str(parametros)))

    teste = analisa_padrao_variavel(logs, nomeDaFuncao,'Função')

    if teste[1] != True:
        return [False, teste[1], teste[2], 'exibirNaTela']

    testa = verifica_se_tem(parametros, ', ', logs)
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

            teste = analisa_padrao_variavel(logs,parametro.strip(),'Parametro ')
            if teste[1] != True:
                return [False, teste[1], teste[2], 'exibirNaTela']

        dic_funcoes[nomeDaFuncao] = [listaFinalDeParametros, 'bloco']

    else:
        teste = analisa_padrao_variavel(logs,parametros,'Parametro ')
        if teste[1] != True:
            return [False, teste[1], teste[2], 'exibirNaTela']

        dic_funcoes[nomeDaFuncao] = [parametros, 'bloco']

    funcao_em_analise = nomeDaFuncao
    return [True, True, 'booleano', 'declararFuncao',funcao_em_analise]

def funcao_exibir(linha, logs):
    logs = '  ' + logs
    log(logs + 'funcao exibição: {}'.format(linha))

    codigo = linha.strip()
    resultado = abstrair_valor_linha(codigo, logs)
    if resultado[0] == False:
        return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

    ''' | sucesso | saida | tipoSaida | ordem | '''
    return [resultado[0],resultado[1], resultado[2],'exibirNaTela']

def funcao_exibir_na_linha(linha, logs):
    logs = '  ' + logs
    log(logs + 'Função exibir nessa linha ativada'.format(linha))

    linha = linha.strip()
    resultado = abstrair_valor_linha(linha, logs)

    if resultado[0] == False:
        return resultado

    return [ resultado[0], ':nessaLinha:' + str(resultado[1]), resultado[2], 'exibirNaTela' ]

def funcao_tempo(tempo, tipo_espera, logs):

    logs = '  ' + logs
    log(logs + 'Função tempo: {}'.format(tempo))

    resultado = abstrair_valor_linha(tempo, logs)
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

def obter_valor_string(string, logs):

    logs = '  ' + logs
    log(logs + 'Obter valor de uma string: {}'.format(string))

    valorFinal = ''
    anterior = 0

    for valor in finditer("""\"[^"]*\"""", string):

        abstrair = abstrair_valor_linha(
            string[anterior:valor.start()], logs)
        if abstrair[0] == False:
            return abstrair

        valorFinal = valorFinal + str(
            abstrair[1]) + string[valor.start()+1:valor.end()-1]
        anterior = valor.end()

    abstrair = abstrair_valor_linha(string[anterior:], logs)
    if abstrair[0] == False:
        return abstrair

    valorFinal = valorFinal + str(abstrair[1])

    return [True, valorFinal, 'string']

def localiza_transforma_variavel(linha, logs):
    logs = '  ' + logs
    log(logs + 'Encontrar e transformar dic_variaveis: {}'.format(linha))

    anterior = 0
    normalizacao = 0
    linha_base = linha
    tipos_obtidos = []

    for valor in finditer(' ', linha_base):
        palavra = linha[anterior : valor.start() + normalizacao]

        if palavra.isalnum() and palavra[0].isalpha():

            variavelDessaVez = abstrair_valor_linha(palavra, logs)

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

def fazer_contas(linha, logs):
    """
        A string deve estar crua
    """
    logs = '  ' + logs
    log(logs + 'Fazer contas: {}'.format(linha))

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
        # Não mude esse texto
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
    linha = localiza_transforma_variavel(linha, logs)
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

def obter_valor_variavel(variavel, logs):
    logs = '  ' + logs
    log(logs + 'Obter valor da variável: "{}"'.format(variavel))

    global dic_variaveis
    
    variavel = variavel.strip()

    variavel = variavel.replace('\n', '')

    try:
        dic_variaveis[variavel]
    except:
        return [False, "Você precisa definir a variável '{}'".format(variavel), 'string', 'fazerNada']
    else:
        return [True, dic_variaveis[variavel][0], dic_variaveis[variavel][1], 'fazerNada']

def comandos_uso_geral(possivelVariavel, logs):
    logs = '  ' + logs
    log(logs + 'comandos_uso_geral: >{}<'.format(possivelVariavel))

    possivelVariavel = str(possivelVariavel).strip()

    analisa = analisa_instrucao('^(<digitado>)$', possivelVariavel, grupos_analisar = [1])
    if analisa != False:
        return funcao_digitado(analisa[0], logs)

    analisa = analisa_instrucao('^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$',  possivelVariavel, grupos_analisar = [2, 4])
    if analisa != False:
        return funcao_numero_aleatorio(analisa[0], analisa[1], logs)

    analisa = analisa_instrucao('^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', possivelVariavel, grupos_analisar = [2, 4])
    if analisa != False:
        return funcao_obter_valor_lista(analisa[0], analisa[1], logs)

    analisa = analisa_instrucao('^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', possivelVariavel, grupos_analisar = [2, 4])
    if analisa != False:
        return funcao_tiver_na_lista(analisa[0],analisa[1], logs)

    analisa = analisa_instrucao('^(<tamanhoDaLista>)(.*)$', possivelVariavel, grupos_analisar = [2])
    if analisa != False:
        return funcao_tamanho_da_lista(analisa[0], logs)

    return [True, None, 'vazio']

# Os valores aqui ainda estão crus, como: mostre "oi", 2 + 2
def abstrair_valor_linha(possivelVariavel, logs):
    logs = '  ' + logs
    log(logs + 'Abstrar valor de uma linha inteira com possivelVariavel: "{}"'.format(possivelVariavel))
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

    # Se tiver virgulas entre os valores
    testa = verifica_se_tem(possivelVariavel, ",", logs)
    if testa != []:

        listaLinhas = [ possivelVariavel[ : testa[0][0] ],  possivelVariavel[testa[0][1] : ]]
        listaValores = ''
        for linha in listaLinhas:
            valor = abstrair_valor_linha(linha, logs)
            if valor[0] == False:
                return valor

            listaValores += str(valor[1])

        return [True, listaValores, "string"]

    if possivelVariavel == '':
        return [True, possivelVariavel, 'string']

    resultado = fazer_contas(possivelVariavel, logs)
    if resultado[0] == True:
        return resultado

    resultado = comandos_uso_geral(possivelVariavel, logs)

    if resultado[0] == True and resultado[1] != None:
        return resultado

    # Era um digitado ou aleatório, mas deu errado
    elif resultado[0] == False:
        return resultado

    testa = verifica_se_tem(possivelVariavel, '"', logs)
    if testa != []:
        return obter_valor_string(possivelVariavel, logs)

    try:
        float(possivelVariavel)
    except:
        #print("DESNECESSÁRIO?")
        return obter_valor_variavel(possivelVariavel, logs)
    else:
        return [True, float(possivelVariavel), 'float']

def analisa_padrao_variavel(logs,variavelAnalise, msg):
    # ANALISE ESSE NEGÓCIO DIREITO MEU FI
    variavel = variavelAnalise
    logs = '  ' + logs

    variavel = variavel.replace('_','a')
    variavel = variavel.lower()

    if not variavel[0].isalpha():
        return [True, msg + ' devem começar obrigatóriamente com uma letra: \'{}\' não se encaixa nessa regra'.format(variavelAnalise), 'sring']

    if not variavel.isalnum():
        return [True, msg + ' devem conter apenas letras, números ou _: \'{}\' não se encaixa nessa regra'.format(variavelAnalise), 'sring']

    return [True,True,'booleano']

def funcao_fazer_atribuicao(variavel, valor, logs):
    global dic_variaveis

    logs = '  ' + logs
    log(logs + 'Função atribuição: {}'.format(variavel + str(valor)))

    if variavel == '' or valor == '':
        return [False, 'É necessario cum comando de atribuição', 'string', 'exibirNaTela']

    teste = analisa_padrao_variavel(logs,variavel,'Variáveis')
    if teste[1] != True:
        return [False, teste[1], teste[2], 'exibirNaTela']

    valor = valor.replace('\n', '')
    valor = valor.strip()

    resultado = abstrair_valor_linha(valor, logs)
    if resultado[0] == False:
        return resultado

    if resultado[0] == True:
        dic_variaveis[variavel] = [resultado[1], resultado[2]]

        return [True, None, 'vazio', 'fazerNada']

    return [ resultado[0], resultado[1], resultado[2], 'fazerNada']

def funcao_loops_enquanto(linha, logs):
    logs = '  ' + logs
    log(logs + 'Função loops enquanto: {}'.format(linha))

    resultado = funcao_condicional(linha, logs)

    return [resultado[0], resultado[1], resultado[2], 'declararLoop']

def tiver_valor_lista(linha, logs):
    linha = linha.strip()
    logs = '  ' + logs
    log(logs + 'Função condicional: {}'.format(linha))

    analisa = analisa_instrucao('^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha, grupos_analisar = [2, 4])
    if analisa != False:
        return funcao_tiver_na_lista(analisa[0],analisa[1], logs)

    return [True,None,'booleano']

def funcao_condicional(linha, logs):
    ''' 3 for maior que 20 ou 5 for menor que 1 '''
    logs = '  ' + logs
    log(logs + 'Função condicional: {}'.format(linha))

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

        # Marque os sinais especiais
        linha = linha.replace(
            simbolosArrumados[simbolo],'_._' + simbolosArrumados[simbolo] + '_._')

    linha = linha.replace('_._ < _._ =','_._ <= _._')
    linha = linha.replace('_._ > _._ =','_._ >= _._')

    # Usando Regex para isolar os simbolos
    anterior = 0
    final = ''

    # Obter os valores fora dos simbolos marcados
    for item in finditer("_\\._[^_]*_\\._", linha):

        # Abstrai um valor qual
        resultado = abstrair_valor_linha(
            linha[anterior:item.start()],logs)

        if resultado[0] == False:
            return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

        saida = resultado[1]

        # Marcar strings
        if resultado[2] == 'string':
            saida = '"' + resultado[1] + '"'

        # Reover marcadores de simbolos
        final += str(saida) + linha[item.start() + 3:item.end() - 3]

        anterior = item.end()

    boolTemTiverLista = False
    resultado = tiver_valor_lista(linha[anterior:].strip(), logs)

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

        resultado = abstrair_valor_linha(linha[anterior:], logs)
        if resultado[0] == False:
            return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

        # Obter ultima string
        saida = resultado[1]
        if resultado[2] == 'string':
            saida = '"' + resultado[1] + '"'

        # Finalizar nova linha
        final += str(saida)

    # Tente fazer a condição com isso
    try:
        resutadoFinal = eval(final)

    except Exception as erro:
        return [False, "Não foi possivel realizar a condicao |{}|".format(final), 'string', 'exibirNaTela']

    else:
        return [True, resutadoFinal, 'booleano', 'declararCondicional']

def modoFullScreen(event=None):
    global bool_tela_em_fullscreen

    if bool_tela_em_fullscreen:
        bool_tela_em_fullscreen = False

    else:
        bool_tela_em_fullscreen = True

    tela.attributes("-fullscreen", bool_tela_em_fullscreen)

def on_closing(event=None):
    global top_janela_terminal
    global aconteceu_erro
    global numeros_thread_interpretador

    aconteceu_erro = True

    while numeros_thread_interpretador != 0:
        tela.update()
        sleep(0.1)

    top_janela_terminal.destroy()

def inicializador_terminal():
    global tx_terminal
    global top_janela_terminal

    top_janela_terminal = Toplevel(tela)
    #top_janela_terminal.protocol("WM_DELETE_WINDOW", on_closing)
    top_janela_terminal.grid_columnconfigure(1, weight=1)
    top_janela_terminal.rowconfigure(1, weight=1)
    top_janela_terminal.geometry("720x450+150+150")

    tx_terminal = Text(top_janela_terminal)
    try:
        # Se ainda não estava carregado
        tx_terminal.configure(dic_design["tx_terminal"])
    except Exception as erro:
        print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

    tx_terminal.bind('<Return>', lambda event:pressionou_enter(event))
    tx_terminal.focus_force()
    tx_terminal.grid(row=1, column=1, sticky=NSEW)

def atualizarListaDeScripts():
    for file in listdir('scripts/'):
        if len(file) > 5:
            if file[-3:] == 'fyn':
                menu_arquivo_cascate.add_command(
                    label=file, command= lambda link = file: abrirArquivo(
                        'scripts/' + str(link)))

def atualizarListaTemas():
    for file in listdir('temas/'):
        if len(file) > 11:
            if file[-10:] == 'theme.json':
                menu_interface_cascate_temas.add_command(
                    label=file,
                    command= lambda link = file: atualizaInterface(
                        'tema', str(link)))

def atualizarListasintaxe():
    for file in listdir('temas/'):
        if len(file) > 13:
            if file[-12:] == 'sintaxe.json':
                menu_interface_cascate_sintaxe.add_command(
                    label=file,
                    command= lambda link = file: atualizaInterface(
                        'sintaxe', str(link)) )

def atualizarListasfontes():
    fontes=list(font.families())
    fontes.sort()
    for fonte in fontes:
        menu_interface_cascate_fontes.add_command(
            label=fonte)

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
    global tx_codificacao
    
    
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
    tx_codificacao.update()

def atualiza_design_interface():
    try:
        # Menus Superiores
        menu_interface_cascate_sintaxe.configure(dic_design["cor_menu"])
        menu_interface_cascate_temas.configure(dic_design["cor_menu"])
        menu_interface_cascate_fontes.configure(dic_design["cor_menu"])
        menu_arquivo_cascate.configure(dic_design["cor_menu"])
        menu_ferramentas.configure(dic_design["cor_menu"])
        menu_interface.configure(dic_design["cor_menu"])
        menu_localizar.configure(dic_design["cor_menu"])
        menu_executar.configure(dic_design["cor_menu"])
        menu_arquivo.configure(dic_design["cor_menu"])
        menu_editar.configure(dic_design["cor_menu"])
        menu_barra.configure(dic_design["cor_menu"])
        menu_ajuda.configure(dic_design["cor_menu"])
        menu_sobre.configure(dic_design["cor_menu"])
        menu_barra.configure(dic_design["cor_menu"])

        # Onde o usuário codifica
        tx_codificacao.configure(dic_design["tx_codificacao"])
        scrollbar_text.configure(dic_design['scrollbar_text'])

        # Opções com os botões
        fr_opcoes_rapidas.configure(dic_design["fr_opcoes_rapidas"])

        # Botões
        lb_linhas.configure(dic_design["lb_linhas"])
        bt_salva.configure(dic_design["dicBtnMenus"])
        bt_corrige.configure(dic_design["dicBtnMenus"])
        bt_break.configure(dic_design["dicBtnMenus"])
        bt_play.configure(dic_design["dicBtnMenus"])
        bt_play_break_point.configure(dic_design["dicBtnMenus"])
        bt_desfazer.configure(dic_design["dicBtnMenus"])
        bt_redesfazer.configure(dic_design["dicBtnMenus"])
        bt_comentar.configure(dic_design["dicBtnMenus"])
        bt_idioma.configure(dic_design["dicBtnMenus"])
        bt_ajuda.configure(dic_design["dicBtnMenus"])
        bt_pesquisar.configure(dic_design["dicBtnMenus"])
        bt_atena.configure(dic_design["dicBtnMenus"])

    except Exception as erro:
        print('Erro ao atualizar o design da interface, erro: ',erro)

def configuracoes(ev):
    global altura_widget
    global lb_linhas
    global posCorrente
    global posAbsuluta

    if ev != None:
        altura_widget = int( ev.height / 24 )

    qtdLinhas = tx_codificacao.get(1.0, 'end').count('\n')
    #print('Quantidade para : ' + str(qtdLinhas))
    #print('Atualizadoo para: ' + str(altura_widget))

    ate = qtdLinhas + 1
    inicio = 1

    add_linha = ''
    for linha in range(inicio, ate):
        add_linha = add_linha +  "  " + str(linha) + '\n'

    lb_linhas.config(state=NORMAL)
    lb_linhas.delete(1.0, END)
    lb_linhas.insert(1.0, add_linha[:-1])

    #print('------------------')
    #print('altura:',altura_widget)
    #print('posAbs:',posAbsuluta)
    #print('posCor:',posCorrente)
    #print('------------------')

    lb_linhas.config(state=DISABLED)

def obterPosicaoDoCursor(event=None):

    numPosicao = str(tx_codificacao.index(INSERT))
    #posCorrente = int(float(tx_codificacao.index(CURRENT)))

    if '.' not in numPosicao:
        numPosicao = numPosicao + '.0'

    # Obter linha e coluna
    linha, coluna = numPosicao.split('.')

    palavra = ""
    aconteceuEspaco = False

    # Obter o código sendo digitado
    for valor in range(0, int(coluna)):
        letra = tx_codificacao.get('{}.{}'.format( int(linha), int(coluna) - valor - 1 ))

        palavra = letra + palavra

        # Se chegar no incio da linha, ou se não for alfabético e sejá aconteceu algo diferente de espaço
        if ( ( letra == "\n" or not letra.isalpha() ) and aconteceuEspaco):
            break

        # Se for alfabético
        if letra.isalpha():

            # Libera para interromper novamente
            aconteceuEspaco = True

    # Carregar a tela de ajuda
    tela_ajuda(palavra.strip())

def tela_ajuda(pesquisa):
    global fr_help
    global lista_titulos_frames

    # Remover todos os botões
    for item in lista_titulos_frames:
        item[0].destroy()
        item[1].destroy()
        item[2].destroy()

    # Limpar as listas
    lista_titulos_frames = []

    # Carregar os dados
    json_ajuda = carregar_json('configuracoes/menu_ajuda.json')

    # Criar os botões na tela
    contador = 2
    for k, v in json_ajuda.items():

        titulo = json_ajuda[k]['titulo']
        descricao = json_ajuda[k]['descricao']
        exemplo = json_ajuda[k]['exemplo']
        link = json_ajuda[k]['link']
        chave = json_ajuda[k]['chave']

        if ( ( pesquisa in titulo.lower() ) or ( pesquisa in chave.lower())) == False:
            continue

        # MENU COM A OPÇÂO
        fr_help_comando = Frame(fr_help, pady=10, padx=0, bg="#fefefe", highlightbackground="#ababab", highlightthickness= 2)

        # TEXTO DO MENU DE AJUDA
        lb_help_texto_comando = Label(fr_help_comando, text=titulo, bg="#fefefe", font=("", 12), width = 25, anchor="w")

        # DESCRICAO DO MENU DE AJUDA
        lb_help_desc_comando = Label(fr_help_comando,wraplength=200,justify="left", text=exemplo, bg="#fefefe", font=("", 10), width = 25, anchor="w")

        fr_help_comando.grid(row=contador, column=1, sticky=NSEW)
        lb_help_texto_comando.grid(row=1, column=1, sticky=W)
        lb_help_desc_comando.grid(row=2, column=1, sticky=NSEW)

        lista_titulos_frames.append([fr_help_comando, lb_help_texto_comando, lb_help_desc_comando])

        contador += 1

tela = Tk()
tela.title('Linguagem feynman')
tela.configure(bg='#393944')
tela.rowconfigure(2, weight=1)
tela.geometry("1100x600")
tela.grid_columnconfigure(1, weight=1)
#tela.attributes('-fullscreen', True)
tela.bind('<F11>', lambda event: modoFullScreen(event))
tela.bind('<F5>', lambda event: inicializador_orquestrador_interpretador(event))
tela.bind('<Control-s>', lambda event: salvarArquivo(event))
tela.bind('<Control-o>', lambda event: abrirArquivoDialog(event))
tela.bind('<Control-S>', lambda event: salvarArquivoComoDialog(event))

try:
    imgicon = PhotoImage(file='icone.png')
    tela.call('wm', 'iconphoto',tela._w, imgicon)

except:
    pass

menu_barra = Menu(tela, tearoff = False)
tela.config(menu=menu_barra)

menu_ferramentas = Menu(menu_barra, tearoff = False)
menu_interface = Menu(menu_barra, tearoff = False)
menu_localizar = Menu(menu_barra, tearoff = False)
menu_executar = Menu(menu_barra, tearoff = False)
menu_arquivo = Menu(menu_barra, tearoff = False)
menu_editar = Menu(menu_barra, tearoff = False)
menu_ajuda = Menu(menu_barra, tearoff = False)
menu_sobre = Menu(menu_barra, tearoff = False)
menu_desenvolvedor = Menu(menu_barra, tearoff = False)

menu_barra.add_cascade(label='  Arquivo'   , menu=menu_arquivo)
menu_barra.add_cascade(label='  Executar'  , menu=menu_executar)
menu_barra.add_cascade(label='  Localizar' , menu=menu_localizar)
menu_barra.add_cascade(label='  Interface' , menu=menu_interface)
menu_barra.add_cascade(label='  Ajuda'     , menu=menu_ajuda)
menu_barra.add_cascade(label='  sobre'     , menu=menu_sobre)
menu_barra.add_cascade(label='  Dev'       , menu=menu_desenvolvedor)

# ARQUIVO
menu_arquivo_cascate = Menu(menu_arquivo, tearoff = False)
menu_arquivo.add_command(label='  Abrir arquivo (Ctrl+O)', command=abrirArquivoDialog)
menu_arquivo.add_command(label='  Nova Guia (Ctrl-N)')
menu_arquivo.add_command(label='  Abrir pasta')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='  Recentes')
menu_arquivo.add_cascade(label='  Exemplos', menu=menu_arquivo_cascate)
atualizarListaDeScripts()

menu_arquivo.add_separator()
menu_arquivo.add_command(label='  Salvar (Ctrl-S)', command=salvarArquivo)
menu_arquivo.add_command(label='  Salvar Como (Ctrl-Shift-S)', command=salvarArquivoComoDialog)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='  imprimir (Ctrl-P)')
menu_arquivo.add_command(label='  Exportar (Ctrl-E)')
menu_arquivo.add_command(label='  Enviar por e-mail ')

# COMANDOS DE EXECUTAR
menu_executar.add_command(label='  Executar Tudo (F5)', command=inicializador_orquestrador_interpretador)
menu_executar.add_command(label='  Executar linha (F6)')
menu_executar.add_command(label='  Executar até breakpoint (F7)')
menu_executar.add_command(label='  Executar com delay (F8)')
menu_executar.add_command(label='  Parar execução (F9)')
menu_executar.add_command(label='  Inserir breakpoint (F10)')
menu_localizar.add_command(label='  Localizar (CTRL + F)')
menu_localizar.add_command(label='  Substituir (CTRL + R)')
menu_ferramentas.add_command(label='  corrigir identação')
menu_ferramentas.add_command(label='  Numero de espaços para o tab')

menu_interface_cascate_temas = Menu(menu_interface, tearoff = False)
menu_interface.add_cascade(label='  Temas', menu=menu_interface_cascate_temas)
atualizarListaTemas()

menu_interface_cascate_sintaxe = Menu(menu_interface, tearoff = False)
menu_interface.add_cascade(label='  sintaxe', menu=menu_interface_cascate_sintaxe)
atualizarListasintaxe()

menu_interface_cascate_fontes = Menu(menu_interface, tearoff = False)
menu_interface.add_cascade(label='  fontes', menu=menu_interface_cascate_fontes)
atualizarListasfontes()

menu_ajuda.add_command(label='  Ajuda (F1)', command = lambda event = None: webbrowser.open(path + "/tutorial/index.html"))
menu_ajuda.add_command(label='  Comandos Disponíveis', command = lambda event = None: webbrowser.open(path + "/tutorial/index.html"))
menu_ajuda.add_command(label='  Comunidade', command = lambda event = None: webbrowser.open("https://feynmancode.blogspot.com/p/comunidade.html"))
menu_sobre.add_command(label='  Projeto', command= lambda event = None: webbrowser.open("http://feynmancode.blogspot.com/"))

menu_desenvolvedor.add_command(label='  Logs')

# OPÇÕES RÁPIDAS
fr_opcoes_rapidas = Frame(tela)
fr_opcoes_rapidas.grid(row = 1, column =1, sticky=NSEW, columnspan=2)
icon_salva = PhotoImage(file='imagens/icon_salvar.png')
icon_corrige = PhotoImage(file='imagens/icon_arrumar.png')
icon_break = PhotoImage(file='imagens/icon_parar.png')
icon_play = PhotoImage(file='imagens/icon_play.png')
icon_play_break_point = PhotoImage(file='imagens/icon_play_breakpoint.png')
icon_desfazer = PhotoImage(file='imagens/left.png')
icon_redesfazer = PhotoImage(file='imagens/right.png')
icon_comentar = PhotoImage(file='imagens/icon_comentario.png')
icon_idioma = PhotoImage(file='imagens/icon_idioma.png')
icon_ajuda = PhotoImage(file='imagens/icon_duvida.png')
icon_pesquisar = PhotoImage(file='imagens/icon_pesquisa.png')
icon_atena = PhotoImage(file='imagens/icon_atena.png')

icon_salva = icon_salva.subsample(4,4)
icon_corrige = icon_corrige.subsample(4,4)
icon_break = icon_break.subsample(4,4)
icon_play = icon_play.subsample(4,4)
icon_play_break_point = icon_play_break_point.subsample(4,4)
icon_desfazer = icon_desfazer.subsample(4,4)
icon_redesfazer = icon_redesfazer.subsample(4,4)
icon_comentar = icon_comentar.subsample(4,4)
icon_idioma = icon_idioma.subsample(4,4)
icon_ajuda = icon_ajuda.subsample(4,4)
icon_pesquisar = icon_pesquisar.subsample(4, 4)
icon_atena = icon_atena.subsample(4,4)

bt_salva = Button(fr_opcoes_rapidas, image=icon_salva, relief = RAISED)
bt_corrige = Button(fr_opcoes_rapidas, image=icon_corrige, relief = RAISED)
bt_break = Button(fr_opcoes_rapidas, image=icon_break, relief = RAISED)
bt_play = Button(fr_opcoes_rapidas, image=icon_play, relief = RAISED, command = inicializador_orquestrador_interpretador)
bt_play_break_point = Button(fr_opcoes_rapidas, image=icon_play_break_point, relief = RAISED, command = inicializador_orquestrador_interpretador)
bt_desfazer = Button(fr_opcoes_rapidas, image=icon_desfazer, relief = RAISED)
bt_redesfazer = Button(fr_opcoes_rapidas, image=icon_redesfazer, relief = RAISED)
bt_comentar = Button(fr_opcoes_rapidas, image=icon_comentar, relief = RAISED)
bt_idioma = Button(fr_opcoes_rapidas, image=icon_idioma, relief = RAISED)
bt_ajuda = Button(fr_opcoes_rapidas, image=icon_ajuda, relief = RAISED)
bt_pesquisar = Button(fr_opcoes_rapidas, image=icon_pesquisar, relief = RAISED)
bt_atena = Button(fr_opcoes_rapidas, image=icon_atena, relief = RAISED)

bt_salva.grid(row=1,column=1)
bt_corrige.grid(row=1,column=2)
bt_break.grid(row=1,column=3)
bt_play.grid(row=1,column=4)
bt_play_break_point.grid(row=1,column=5)
bt_desfazer.grid(row=1,column=6)
bt_redesfazer.grid(row=1, column=7)
bt_comentar.grid(row=1, column=8)
bt_idioma.grid(row=1, column=9)
bt_ajuda.grid(row=1, column=10)
bt_pesquisar.grid(row=1, column=11)
bt_atena.grid(row=1, column=12)

# INTERFACE GERAL
fr_principal = Frame(tela, bg='#393944')
fr_principal.grid_columnconfigure(2, weight=1)
fr_principal.rowconfigure(1, weight=1)
fr_principal.grid(row=2, column=1, sticky=NSEW)

# CONTADOR DE LINHAS
lb_linhas = Text(fr_principal, width = 5)
lb_linhas.config(state = DISABLED, border = 0, highlightthickness=0)
lb_linhas.grid(row=1, column=1, sticky=NSEW)

# TELA DE CODIFICAÇÃO
tx_codificacao = Text(fr_principal)

scrollbar_text = Scrollbar(fr_principal, relief = FLAT)

tx_codificacao['yscrollcommand'] = scrollbar_text.set
scrollbar_text.config(command = tx_codificacao.yview)

tx_codificacao.focus_force()
#tx_codificacao.bind('<Configure>', configuracoes )
tx_codificacao.bind('<KeyRelease>', coordena_coloracao)
tx_codificacao.grid(row=1, column=2, sticky=NSEW)
scrollbar_text.grid(row=1, column=3, sticky=NSEW)

# TELA DE AJUDA
fr_help = Frame(fr_principal, width = 25, bg="#ababab", padx=0, pady=0)
fr_help.grid(row=1, column=4, sticky=NSEW)

# TELA PESQUISA
tx_pesquisa = Entry(fr_help, font=("", 13),  fg="#676767")
tx_pesquisa.bind('<KeyRelease>', lambda event = None: tela_ajuda(tx_pesquisa.get()))
tx_pesquisa.grid(row=0, column=1, sticky = NSEW)

atualiza_design_interface()

#abrirArquivo('programa_teste.fyn')

tela_ajuda("")

tela.mainloop()

