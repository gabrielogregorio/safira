from json import load

def abrir_arquivo(filename):
    try:
        arquivo = open(filename,'r', encoding='utf8')
        text = arquivo.read()
        arquivo.close()

    except Exception as erro:
        # Texto, erro
        return [None, str(erro)]
    else:
        # Texto, erro
        return [text, None]

def carregar_json(arquivo):

    with open(arquivo, encoding='utf8') as json_file:
        dic_json = load(json_file)

    return dic_json

def atualiza_configuracoes_temas():
    dicionario_sub_comandos = None
    dicionario_comandos = None
    dicionario_design = None
    cor_da_sintaxe = None

    # CARREGAMENTO DOS COMANDOS DA LINGUAGEM
    try:
        with open('configuracoes/comandos.json', encoding='utf8') as json_file:
            dicionario_comandos = load(json_file)
    except Exception as e1:
        print('Erro ao carregar o arquivo \'configuracoes/comandos.json\':',e1)

    # CARREGAMENTO DOS COMANDOS DENTRO DOS COMANDOS
    try:
        with open('configuracoes/subcomandos.json', encoding='utf8') as json_file:
            dicionario_sub_comandos = load(json_file)
    except Exception as e2:
        print('Erro ao carregar o arquivo \'configuracoes/subcomandos.json\':',e2)

    # BUSCA PELAS CONFIGURAÇÕES DO PROGRAMA
    try:

        with open('configuracoes/configuracoes.json', encoding='utf8') as json_file:
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
        print('Erro ao carregar o arquivo \'configuracoes/configuracoes.json\':',e1)

    return [dicionario_sub_comandos, dicionario_comandos, dicionario_design, cor_da_sintaxe]
