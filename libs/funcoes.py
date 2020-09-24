from json import load, loads


def abrir_arquivo(filename):
    try:
        arquivo = open(filename, 'r', encoding='utf8')
        text = arquivo.read()
        arquivo.close()

    except Exception as erro:
        return [None, str(erro)]

    return [text, None]

def salvar_arquivo(arquivo, texto):
    arquivo = open(arquivo, 'w', encoding='utf8')
    arquivo.write(texto)
    arquivo.close()

def carregar_json(arquivo):
    with open(arquivo, encoding='utf8') as json_file:
        dic_json = load(json_file)
    return dic_json

def transformar_em_json(texto):
    return loads(texto)

def atualiza_configuracoes_temas():
    dicionario_comandos = carregar_json('libs/comandos.json')
    config = carregar_json('configuracoes/configuracoes.json')
    cor_da_sintaxe = carregar_json('temas/{}'.format(config["sintaxe"]))

    return [dicionario_comandos, cor_da_sintaxe]
