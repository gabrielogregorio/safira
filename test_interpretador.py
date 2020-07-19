#!/usr/bin/python3.8

from threading import Thread
from libs.interpretador import Interpretador
from time import sleep 
from os import system, name 

import libs.funcoes as funcoes
import sys

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


instancia = Interpretador(bool_logs, [], bool_ignorar_todos_breakpoints, diretorio_base, dicLetras, dic_comandos)

def test_condicao():
    assert instancia.funcao_testar_condicao("2 for igual a 2") == [True, True, 'booleano', 'declararCondicional']

def test_verifica_se_tem():
	assert instancia.verifica_se_tem(linha = "nome, idade", a_buscar = ",") == [[4, 5]]

def test_funcao_realizar_atribu():
	assert instancia.funcao_realizar_atribu(variavel="nome", valor="10 *2") == [True, None, 'vazio', 'fazerNada']

def test_obter_valor_variavel():
	assert instancia.obter_valor_variavel(variavel="nome") == [True, 20, 'float', 'fazerNada']

def test_funcao_esperar_n_tempo():
	assert instancia.funcao_esperar_n_tempo(tempo="2", tipo_espera="s") == [True, None, 'vazio', 'fazerNada']

def test_fazer_contas():
	assert instancia.fazer_contas(linha="2 + 2 / 2") == [True, 3.0, 'float']

def test_funcao_loops_enquantox():
	assert instancia.funcao_loops_enquantox(linha="2 for maior que 2") == [True, False, 'booleano', 'declararLoop']

def test_funcao_repetir_n_vezes():
	assert instancia.funcao_repetir_n_vezes(linha="20 vezes") == [True, 20, 'float', 'declararLoopRepetir']

def test_funcao_senao_se():
	assert instancia.funcao_senao_se(condicao="2 for menor que 1") == [True, False, 'booleano', 'declararSenaoSe']

def test_funcao_exibir_outra_ln():
	assert instancia.funcao_exibir_outra_ln(linha="10, \"ola mundo\"") == [True, '10.0ola mundo', 'string', 'exibirNaTela']

def test_funcao_exibir_mesma_ln():
	assert instancia.funcao_exibir_mesma_ln(linha="123+1") == [True, ':nessaLinha:124', 'float', 'exibirNaTela']

def test_funcao_arquivo_existe():
	assert instancia.funcao_arquivo_existe(nome_arquivo='"teste.safira" ') == [True, False, 'booleano', 'fazerNada']

def test_funcao_arquivo_nao_existe():
	assert instancia.funcao_arquivo_nao_existe(nome_arquivo='"teste.safira"') == [True, True, 'booleano', 'fazerNada']

def test_funcao_criar_arquivo():
	assert instancia.funcao_criar_arquivo(nome_arquivo='"teste.safira"') == [True, '', 'vazio', 'fazerNada']

def test_funcao_ler_arquivo():
	assert instancia.funcao_ler_arquivo(nome_arquivo='"teste.safira"') == [True, '', 'string', 'fazerNada']

def test_funcao_sobrescrever_arquivo():
	assert instancia.funcao_sobrescrever_arquivo(texto='"mostre 1\n"' , nome_arquivo='"teste.safira"') == [True, True, 'booleano', 'fazerNada']

def test_funcao_adicionar_arquivo():
	assert instancia.funcao_adicionar_arquivo(texto='"mostre 2 "', nome_arquivo='"teste.safira"') == [True, True, 'booleano', 'fazerNada']

def test_funcao_excluir_arquivo():
	assert instancia.funcao_excluir_arquivo(nome_arquivo='"teste.safira"') == [True, '', 'vazio', 'fazerNada']

def test_funcao_loop_para_cada_():
	assert instancia.funcao_loop_para_cada_(variavel="x", inicio="10", fim="20") == [True, ['x', 10, 20, 1], 'lista', 'declararLoopParaCada']

#print(instancia.obter_valor_lista(linha))
#print(instancia.funcao_retornar_lista(variavel))
#print(instancia.funcao_otamanho_da_lst(variavel))
#print(instancia.funcao_ovalor_digitado(linha))
#print(instancia.obter_valor_string(string))
#print(instancia.localiza_transforma_variavel(linha))
#print(instancia.abstrair_valor_linha(possivelVariavel))
#print(instancia.funcao_importe(biblioteca))
#print(instancia.funcao_tipo_variavel(variavel))
#print(instancia.funcao_incremente_vari(valor, variavel))
#print(instancia.funcao_decremente_vari(valor, variavel))
#print(instancia.incremente_decremente(valor, variavel, acao))
#print(instancia.teste_generico_lista(variavel, valor))
#print(instancia.funcao_rem_itns_na_lst(valor, variavel))
#print(instancia.funcao_add_itns_na_lst(valor, variavel))
#print(instancia.funcao_add_itns_lst_in(valor, variavel))
#print(instancia.funcao_add_itns_lst_ps(valor, posicao, variavel))
#print(instancia.tiver_valor_lista(linha))
#print(instancia.funcao_add_lst_na_posi(variavelLista, posicao, valor))
#print(instancia.funcao_obter_valor_lst(variavel, posicao))
#print(instancia.funcao_tiver_valor_lst(valor, variavel))
#print(instancia.funcao_dec_lst_posicoe(variavel, posicoes))
#print(instancia.funcao_numer_aleatorio(num1, num2))
#print(instancia.funcao_declarar_listas(variavel, itens))
#print(instancia.funcao_declarar_funcao(nomeDaFuncao, parametros=None))
#print(instancia.funcao_executar_funcao(nomeDaFuncao, parametros=None))