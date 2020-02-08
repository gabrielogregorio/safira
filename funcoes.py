from json import load

def abrir_arquivo(filename):
    try:
        arquivo = open(filename,'r',encoding='utf8')
        text = arquivo.read()
        arquivo.close()

    except Exception as erro:
        print('Aconteceu um erro ao abrir o arquivo: "{}", erro:{}'.format(filename,erro))
        return None

    else:
        print('Arquivo aberto com sucesso')
        return text

def atualiza_configuracoes_temas():
    dicionario_sub_comandos = None
    dicionario_comandos = None
    dicionario_design = None
    cor_da_sintaxe = None

    # CARREGAMENTO DOS COMANDOS DA LINGUAGEM
    try:
        with open('comandos/comandos.json') as json_file:
            dicionario_comandos = load(json_file)
    except Exception as e1:
        print('Erro ao carregar o arquivo \'comandos/comandos.json\':',e1)

    # CARREGAMENTO DOS COMANDOS DENTRO DOS COMANDOS
    try:
        with open('comandos/subcomandos.json') as json_file:
            dicionario_sub_comandos = load(json_file)
    except Exception as e2:
        print('Erro ao carregar o arquivo \'comandos/subcomandos.json\':',e2)

    # BUSCA PELAS CONFIGURAÇÕES DO PROGRAMA
    try:

        with open('configuracoes.json') as json_file:
            arquivoConfigs = load(json_file)

            # BUSCA PELOS TEMAS DA SINTAXE
            try:
                with open(
                    'temas/{}'.format(arquivoConfigs["sintaxe"])) as json_file:
                    cor_da_sintaxe = load(json_file)
            except Exception as e2:
                print('Erro ao carregar o tema da sintaxe:',e2)

            # BUSCA PELOS TEMAS DA INTERFACE
            try:
                with open(
                    'temas/{}'.format(arquivoConfigs["tema"])) as json_file:
                    dicionario_design = load(json_file)
            except Exception as e3:
                print('Erro ao carregar os temas:',e3)

    except Exception as e1:
        print('Erro ao carregar o arquivo \'configuracoes.json\':',e1)

    return [dicionario_sub_comandos, dicionario_comandos, dicionario_design, cor_da_sintaxe]
