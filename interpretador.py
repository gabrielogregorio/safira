from re import findall, finditer
from tkinter import END
from random import randint
import funcoes

class Run():
    def __init__(self, terminal, tx_codficac, bool_logs = False):
        self.aconteceu_erro = False
        self.erro_alertado = False
        self.esperar_pressionar_enter = False
        self.dic_variaveis = {}
        self.dic_funcoes = {}
        self.boo_orquestrador_iniciado = False
        self.tx_terminal = terminal
        self.numero_threads = 0
        self.bool_logs = bool_logs
        self.tx_codficac = tx_codficac
        self.dic_comandos = funcoes.carregar_json('configuracoes/comandos.json')


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

        if linhaErro != None:

            lista = self.tx_codficac.get(1.0, END).split("\n")
            
            palavra = "**_erro_alertado_**"
            linha1 = str(linhaErro) + ".0"
            linha2 = str(linhaErro) + "." + str(len(lista[int(linhaErro) - 1]))

            self.tx_codficac.tag_add(palavra, linha1 , linha2)
            self.tx_codficac.tag_config(palavra, background = "#dd3344")

        self.erro_alertado = True

    def log(self, mensagem):
        if self.bool_logs:
            print(mensagem)

    def orq_erro(self, mensagem, linhaAnalise):
        self.aconteceu_erro = True

        if not self.erro_alertado:
            self.tx_terminal.insert(END, "\n[{}] {}".format(linhaAnalise, mensagem))
            Run.realiza_coloracao_erro(self, 'codigoErro', valor1=0, valor2=len(mensagem)+1, cor='#ffabab', linhaErro = linhaAnalise )

    def orq_exibir_tela(self, lst_retorno_ultimo_comando):
        
        try:
            if ":nessaLinha:" in str(lst_retorno_ultimo_comando[1]):
                self.tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1][len(":nessaLinha:"):]))
            else:
                self.tx_terminal.insert(END, str(lst_retorno_ultimo_comando[1])+'\n')

            self.tx_terminal.see("end")

        except Exception as erro:
            print('ERRO:', erro)
            return [[False, 'indisponibilidade_terminal', 'string','exibirNaTela'], "1"]

    def orquestrador_interpretador(self, txt_codigo):        
        Run.log(self, '<orquestrador_interpretador>:' + txt_codigo)

        self.boo_orquestrador_iniciado = True
        self.numero_threads += 1

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
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_ultimo_ret[1], linhaAnalise)
                            self.numero_threads -= 1
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
                Run.log(self, '!<Analisa bloco salvo>:"' + str_bloco + '"')

                bool_salvar_bloco = False

                if lst_ultimo_ret[3] == 'declararLoop':

                    # Enquanto a condição for verdadeira
                    while lst_ultimo_ret[1] and not self.aconteceu_erro:

                        lst_resultado_execucao = Run.orquestrador_interpretador(self, 
                            str_bloco[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_resultado_execucao[1], linhaAnalise)
                            self.numero_threads -= 1
                            return lst_resultado_execucao

                        # Testa novamente a condição do loo
                        lst_ultimo_ret = Run.interpretador(self, comando_testado)
                        linhaAnalise = lst_ultimo_ret[1]
                        lst_ultimo_ret = lst_ultimo_ret[0]

                        if lst_ultimo_ret[0] == False:

                            if lst_ultimo_ret[1] == 'indisponibilidade_terminal':
                                    self.numero_threads -= 1
                                    return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_ultimo_ret[1], linhaAnalise)
                            self.numero_threads -= 1
                            return lst_ultimo_ret

                elif lst_ultimo_ret[3] == "declararLoopRepetir":
                    lst_ultimo_ret[3] = 'fazerNada'

                    for valor in range(0, lst_ultimo_ret[1]):
                        lst_resultado_execucao = Run.orquestrador_interpretador(self, 
                            str_bloco[1:].strip())

                        if lst_resultado_execucao[0] == False:
                            if lst_resultado_execucao[1] == 'indisponibilidade_terminal':
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_resultado_execucao[1], linhaAnalise)
                            self.numero_threads -= 1
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
                                self.numero_threads -= 1
                                return [True, 'Orquestrador Finalizado', 'string']

                            Run.orq_erro(self, lst_resultado_execucao[1], linhaAnalise)
                            self.numero_threads -= 1
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
                    self.numero_threads -= 1
                    return [True, 'Orquestrador Finalizado', 'string']

                Run.orq_erro(self, lst_ultimo_ret[1], linhaAnalise)
                self.numero_threads -= 1
                return lst_ultimo_ret

            if lst_ultimo_ret[3] == 'exibirNaTela':
                Run.orq_exibir_tela(self, lst_ultimo_ret)

        # Aviso de erros de profundidade
        if int_profundidade > 0:
            self.numero_threads -= 1
            return [False, None, 'vazia']

        elif int_profundidade < 0:
            self.numero_threads -= 1
            return [False, None, 'vazia']

        self.numero_threads -= 1
        return [True, 'Orquestrador Finalizado', 'string']

    def analisa_instrucao(self, comando, texto):
        re_comandos = "(\\<[a-zA-Z]*\\>)"
        re_groups = findall(re_comandos, comando)
        if re_groups == None:
            return False

        dic_options = {}
       
        # Anda pelos grupos <se>, <esperar>
        for grupo in re_groups:

            # Anda pelos comandos no dicionários, [se], [if]...
            for n_comando in range(0, len(self.dic_comandos[ grupo[1:-1] ])):

                # Obtem um comando. se, if
                txt_comando_analisar = self.dic_comandos[ grupo[1:-1] ][n_comando][0]

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

        # Para remover a indexação a partir do zero
        lista_itens = list(re_texto[0])
        lista_itens.insert(0, "")

        return lista_itens

    def interpretador(self, linha):
        Run.log(self, 'Interpretador iniciado')

        try:
            self.tx_terminal.get(1.0, 1.1)
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
 



            analisa = Run.analisa_instrucao(self, '^(<limpatela>)$', linha)
            if analisa: return [ Run.funcao_limpar_tela(self, ), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<mostreNessa>)(.*)$', linha)
            if analisa: return [ Run.funcao_exibir_na_linha(self, analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<mostre>)(.*)$', linha)
            if analisa: return [ Run.funcao_exibir(self, analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<se>)(.*)$', linha)
            if analisa: return [ Run.funcao_condicional(self, analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<enquanto>)(.*)$', linha)
            if analisa: return [ Run.funcao_loops_enquanto(self, analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<aguarde>)(.*)(<esperaEm>)$', linha)
            if analisa: return [ Run.funcao_tempo(self, analisa[2], analisa[3]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<repita>)(.*)(<repitaVezes>)$', linha)
            if analisa: return [ Run.funcao_repetir(self, analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<incremente>)(.*)(<incrementeDecremente>)(.*)$', linha)
            if analisa: return [ Run.incremente_em(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<decremente>)(.*)(<incrementeDecremente>)(.*)$', linha)
            if analisa: return [ Run.decremente_em(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<funcoes>)(.*)(<recebeParametros>)(.*)$', linha)
            if analisa: return [ Run.funcao_declarar_funcao(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaNaPosicao>)(.*)(<recebeDeclaraListas>)(.*)$', linha)
            if analisa: return [ Run.funcao_adicione_na_lista_na_posicao(self, analisa[2], analisa[4], analisa[6]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<listaCom>)(.*)(<listaPosicoesCom>)$', linha)
            if analisa: return [ Run.funcao_declarar_listas_posicoes(self, analisa[2], analisa[4]), num_linha ]
 
            analisa = Run.analisa_instrucao(self, '^(<declaraListas>)(.*)(<recebeDeclaraListas>)(.*)$', linha)
            if analisa: return [ Run.funcao_declarar_listas(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<RemoverItensListas>)(.*)(<RemoverItensListasInterno>)(.*)$', linha)
            if analisa: return [ Run.funcao_remover_itens_na_lista(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoPosicao>)(.*)(<addItensListaInternoPosicaoFinaliza>)(.*)$', linha)
            if analisa: return [ Run.funcao_adicionar_itens_na_lista_posicao(self, analisa[2], analisa[4], analisa[6]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoFinal>)(.*)$', linha)
            if analisa: return [ Run.funcao_adicionar_itens_na_lista(self, analisa[2], analisa[4]), num_linha ]
                
            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInternoInicio>)(.*)$', linha)
            if analisa: return [ Run.funcao_adicionar_itens_na_lista_inicio(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<adicionarItensListas>)(.*)(<addItensListaInterno>)(.*)$', linha)
            if analisa: return [ Run.funcao_adicionar_itens_na_lista(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$', linha)
            if analisa: return [ Run.funcao_numero_aleatorio(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', linha)
            if analisa: return [ Run.funcao_obter_valor_lista(self, analisa[2], analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<digitado>)$', linha)
            if analisa: return [ Run.funcao_digitado(self, analisa[1]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha)
            if analisa: return [ Run.funcao_tiver_na_lista(self, analisa[2],analisa[4]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', linha)
            if analisa:return [ Run.funcao_tamanho_da_lista(self, analisa[2]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(\\s*[a-zA-Z\\_]*)(<declaraVariaveis>)(.*)$', linha)
            if analisa: return [ Run.funcao_fazer_atribuicao(self, analisa[1], analisa[3]), num_linha ]

            analisa = Run.analisa_instrucao(self, '^(.*)(<passandoParametros>)(.*)$', linha)
            if analisa: return [ Run.funcao_executar_funcoes(self, analisa[1],analisa[3]), num_linha ]

            return [ [False, "Um comando desconhecido foi localizado: '{}'".format(linha), 'string','exibirNaTela'], num_linha ]
        return [ [True, None, 'vazio', 'fazerNada'], num_linha ]

    def comandos_uso_geral(self, possivelVariavel):
        Run.log(self, 'comandos_uso_geral: {}'.format(possivelVariavel))

        possivelVariavel = str(possivelVariavel).strip()

        analisa = Run.analisa_instrucao(self, '^(<digitado>)$', possivelVariavel)
        if analisa: return Run.funcao_digitado(self, analisa[1])

        analisa = Run.analisa_instrucao(self, '^(<aleatorio>)(.*)(<aleatorioEntre>)(.*)$',  possivelVariavel)
        if analisa: return Run.funcao_numero_aleatorio(self, analisa[2], analisa[4])

        analisa = Run.analisa_instrucao(self, '^(<declaraListasObterPosicao>)(.*)(<listaNaPosicao>)(.*)$', possivelVariavel)
        if analisa: return Run.funcao_obter_valor_lista(self, analisa[2], analisa[4])

        analisa = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', possivelVariavel)
        if analisa: return Run.funcao_tiver_na_lista(self, analisa[2],analisa[4])

        analisa = Run.analisa_instrucao(self, '^(<tamanhoDaLista>)(.*)$', possivelVariavel)
        if analisa: return Run.funcao_tamanho_da_lista(self, analisa[2])

        return [True, None, 'vazio']

    def incremente_em(self, valor, variavel):
        return Run.incremente_decremente(self, valor, variavel,  'incremente')

    def decremente_em(self, valor, variavel):
        return Run.incremente_decremente(self, valor, variavel, 'decremente')

    def msg_variavel_numerica(self, msg, variavel):
        if msg == 'naoNumerico':
            return [False, "A variável '{}' não é numérica!".format(variavel), 'string', 'exibirNaTela']

    def incremente_decremente(self, valor, variavel, acao):
        Run.log(self, 'decremente:' + valor+str(variavel))

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
        Run.log(self, 'funcao_adicione_na_lista_na_posicao:' + str(variavelLista))

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
        Run.log(self, 'obter_valor_lista ' + str(linha))

        teste = Run.obter_valor_variavel(self, linha)

        if teste[0] == False:
            return teste

        if teste[2] != 'lista':
            return[False, "A variável '{}' não é uma lista.".format(linha), 'string']

        return teste

    def funcao_obter_valor_lista(self, variavel, posicao):
        Run.log(self, 'Função Valor de lista: "{}", subcomandos: "{}"'.format(variavel, posicao))

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
        Run.log(self, "Função tiver na lista: " + valor)

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
        Run.log(self, 'Função obter o tamanho da lista: "{}"'.format(linha))

        linha = linha.strip()

        teste = Run.obter_valor_lista(self, linha)
        if teste[0] == False:
            return [teste[0], teste[1], teste[2], 'exibirNaTela']

        try:
            return [True, len(self.dic_variaveis[linha][0]), 'float', 'fazerNada']

        except Exception as erro:
            return [True, 'Erro ao obter o tamanho da lista. Erro: {}'.format(erro), 'string', 'exibirNaTela']

    def funcao_remover_itens_na_lista(self, valor, variavel):
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

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
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

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
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

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
        Run.log(self, 'Função remover itens da lista: "{}"'.format(valor))

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
        Run.log(self, 'Função declarar listas posicoes: "{}"'.format(variavel))

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
        Run.log(self, 'Função declarar listas: "{}"'.format(variavel + str(itens) ))

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
        Run.log(self, 'Função digitado: "{}"'.format(linha))

        textoOriginal = len(self.tx_terminal.get(1.0, END))

        self.esperar_pressionar_enter = True

        while self.esperar_pressionar_enter:

            try:
                self.tx_terminal.get(1.0, 1.1)

                if self.aconteceu_erro: return [False, "Interrompido","string","exibirNaTela"]
                else: self.tx_terminal.update()

            except:
                return [False, 'indisponibilidade_terminal', 'string','exibirNaTela']

        digitado = self.tx_terminal.get(1.0, END)
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
        Run.log(self, 'Limpatela ativado!')

        self.tx_terminal.delete(1.0, END)
        return [True, None, 'vazio','fazerNada']

    def funcao_repetir(self, linha):
        Run.log(self, "funcao repetir: '{}'".format(linha))

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
        Run.log(self,  'funcao aleatório: {}'.format(num1))

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
        Run.log(self, 'Declarar funcoes: {}'.format(nomeDaFuncao + str(parametros)))

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
        Run.log(self, 'funcao exibição: {}'.format(linha))

        codigo = linha.strip()
        resultado = Run.abstrair_valor_linha(self, codigo)

        if resultado[0] == False:
            return [resultado[0], resultado[1], resultado[2], 'exibirNaTela']

        return [resultado[0],resultado[1], resultado[2],'exibirNaTela']

    def funcao_exibir_na_linha(self, linha):
        Run.log(self, 'Função exibir nessa linha ativada'.format(linha))

        linha = linha.strip()
        resultado = Run.abstrair_valor_linha(self, linha)

        if resultado[0] == False:
            return resultado

        return [ resultado[0], ':nessaLinha:' + str(resultado[1]), resultado[2], 'exibirNaTela' ]

    def funcao_tempo(self, tempo, tipo_espera):
        Run.log(self, 'Função tempo: {}'.format(tempo))

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
        Run.log(self, 'Obter valor de uma string: {}'.format(string))

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
        Run.log(self, 'Encontrar e transformar dic_variaveis: {}'.format(linha))

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
        Run.log(self, 'Obter valor da variável: "{}"'.format(variavel))
        
        variavel = variavel.strip()
        variavel = variavel.replace('\n', '')

        try:
            self.dic_variaveis[variavel]
        except:
            return [False, "Você precisa definir a variável '{}'".format(variavel), 'string', 'fazerNada']
        else:
            return [True, self.dic_variaveis[variavel][0], self.dic_variaveis[variavel][1], 'fazerNada']


    def abstrair_valor_linha(self, possivelVariavel):
        Run.log(self, "Abstrar valor de uma linha inteira com possivelVariavel: '{}'".format(possivelVariavel))

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
        Run.log(self, 'Função atribuição: {}'.format(variavel + str(valor)))

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
        Run.log(self, 'Função loops enquanto: {}'.format(linha))

        resultado = Run.funcao_condicional(self, linha)
        return [resultado[0], resultado[1], resultado[2], 'declararLoop']

    def tiver_valor_lista(self, linha):
        Run.log(self, 'Função condicional: {}'.format(linha))

        linha = linha.strip()

        analisa = Run.analisa_instrucao(self, '^(<tiverLista>)(.*)(<tiverInternoLista>)(.*)$', linha)
        if analisa != False:
            return Run.funcao_tiver_na_lista(self, analisa[2],analisa[4])

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

