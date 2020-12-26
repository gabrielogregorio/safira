possibilidades = [
    #'(sobrescreva_texto_arquivo)(.*)(sobrescreva_texto_arquivo_sub)(.*)(sobrescreva_texto_arquivo_sub_sub)',
    #'(funcoes)(\\s*[\\w*\\_]*\\s*)(recebeParametros_parentese_abre)\\s*(recebeParametros_parentese_fecha)',
    #'(adicionarItensListas)(.*)(listaNaPosicao)(.*)(addItensListaInternoPosicaoFinaliza)(.*)',
    #'(funcoes)(.*)(recebeParametros_parentese_abre)(.*)(recebeParametros_parentese_fecha)',
    #'(substitua)(.*)(substitua_por)(.*)(substitua_na_variavel)(\\s*[A-Z0-9a-z\\_]*\\s*)',
    #'(declaraListasObterPosicao)(.*)(listaNaPosicao)(.*)(declara_variaveis)(.*)',
    #'(declaraListas)(.*)(listaNaPosicao)(.*)(recebeDeclaraListas)(.*)',
    #'(.*)(passando_parametros_abrir)(.*)(passando_parametros_fechar)',
    #'(adicione_texto_arquivo)(.*)(adicione_texto_arquivo_sub)(.*)',
    #'(remover_itens_listas)(.*)(remover_itens_listas_interno)(.*)',
    #'(adicionarItensListas)(.*)(addItensListaInternoInicio)(.*)',
    #'(para_cada)__var__(para_cada_de)(.*)(para_cada_ate)(.*)',
    #'(adicionarItensListas)(.*)(addItensListaInternoFinal)(.*)',
    #'(declaraListas)(.*)(listaCom)(.*)(listaPosicoesCom)',
    #'(adicionarItensListas)(.*)(addItensListaInterno)(.*)',
    #'(declaraListasObterPosicao)(.*)(listaNaPosicao)(.*)',
    #'(arquivo_existe)(.*)(arquivo_existe_nao_sub_existe)',
    #'(percorra_items)(.*)(percorra_items_lista_sub)(.*)',
    #'(arquivo_existe)(.*)(arquivo_existe_sub_existe)',
    #'(declaraListas)(.*)(recebeDeclaraListas)(.*)',
    #'(decremente)(.*)(incremente_decremente)(.*)',
    #'(incremente)(.*)(incremente_decremente)(.*)',
    #'(tiver_lista)(.*)(tiver_interno_lista)(.*)',
    #'([a-zA-Z_0-9]*)(declara_variaveis)(.*)',
    #'(aleatorio)(.*)(aleatorioEntre)(.*)',
    #'(funcoes)(.*)(recebeParametros)(.*)',
    #'(declaraListas)(\\s*[a-zA-Z\\_0-9]*)',
    #'(enquanto)(.*)(enquanto_final)',
    #'(funcoes)(\\s*[\\w*\\_]*\\s*)',
    #'(arquivo_existe_completo)(.*)',
    #'(.*)(passandoParametros)(.*)',
    #'(se_nao_se)(.*)(se_final)',
    #'(repita)(.*)(repitaVezes)',
    #'(aguarde)(.*)(esperaEm)',
    #'(tamanho_da_lista)(.*)',
    #'(delete_arquivo)(.*)',
    #'(se)(.*)(se_final)',
    #'(tipo_variavel)(.*)',
    #'(crie_arquivo)(.*)',
    #'(leia_arquivo)(.*)',
    #'(mostreNessa)(.*)',
    #'(importe)(.*)',
    #'(retorne)(.*)',
    '(interrompa)',
    #'(mostre)(.*)',
    '(limpatela)',
    '(digitado)',
    '(continue)',
    '(se_nao)',
    '(pare)',

    #'(tente)',
    #'(se_der_erro)',
    #'(em_qualquer_caso)',
    #'(senao_der_erro)',

    # EM BAIXO
    #'(\\s*[\\w*\\_]*)(percorrer_lst_str_a_cada)(.*)(percorrer_lst_str_a_cada_subum)(.*)(percorrer_lst_str_a_cada_subdois)(.*)(percorrer_lst_str_a_cada_final)',
    #'(\\s*[\\w*\\_]*)(percorrer_lst_str_ate)(.*)(percorrer_lst_str_ate_sub)(.*)(percorrer_lst_str_ate_final)',
    #'(.*)(passando_parametros_abrir)(.*)(passando_parametros_fechar)',
    #'(declaraListasObterPosicao)(.*)(listaNaPosicao)(.*)',
    #'(arquivo_existe)(.*)(arquivo_existe_nao_sub_existe)',
    #'(arquivo_existe)(.*)(arquivo_existe_sub_existe)',
    #'(tiver_lista)(.*)(tiver_interno_lista)(.*)',
    #'(tiver_lista)(.*)(tiver_interno_lista)(.*)',
    #'(aleatorio)(.*)(aleatorioEntre)(.*)',
    #'(declaraListas)(\\s*[a-zA-Z\\_0-9]*)',
    #'(arquivo_existe_completo)(.*)',
    #'(.*)(passandoParametros)(.*)',
    #'(.*)(formatar_textos)(.*)',
    #'(tamanho_da_lista)(.*)',
    #'(tipo_variavel)(.*)',
    #'(leia_arquivo)(.*)',
    #'(.*)(to_captalize)',
    #'(.*)(na_cor)(.*)',
    #'(.*)(to_upper)',
    #'(.*)(to_lower)',
    '(digitado)'
]

from re import compile, findall

import util.funcoes as funcoes
dic_comandos, cor_do_comando = funcoes.atualiza_configuracoes_temas()
rgx_padrao_variavel = '[a-zA-Z0-9\\_]*'


programa = ""
for pos in possibilidades:
    regex = findall('\\(.*?\\)', pos)
    for _ in list(regex):
        comando = dic_comandos[_[1:-1]]['comando']
        for com in comando:
            print(com[0])
            programa = programa + '\n' + 'print "' + com[0] + '"\n' +  com[0]


with open('testes.safira', 'w', encoding='utf-8') as file:
    file.write(programa)