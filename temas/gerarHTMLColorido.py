# Carregando a sintaxe
from json import load
import re

# Carregando os comandos principais
with open('../comandos/comandos.json') as json_file:
    dicComandos = load(json_file)

with open('../temas/white_sintaxe.json') as json_file:
    Sintaxe = load(json_file)

# Carregando os comandos secundários
with open('../comandos/subcomandos.json') as json_file:
    dicSubComandos = load(json_file)


texto ='''
mostre "teste"    
10 - 2   
'''.lower()

def sintaxe(palavra, cor):

    global texto
    cor = cor['foreground']

    lista = texto.split('\n')

    # Remoção de bugs no regex, deixe ele aqui para eviar um \* \\* \\\* \\\\* no loop
    palavra_comando = palavra.replace('+', '\\+')
    palavra_comando = palavra_comando.replace('/', '\\/')
    palavra_comando = palavra_comando.replace('*', '\\*')

    correcao = 0
    # Ande por todas as linhas do programa
    for linha in range(len(lista)):
        # Se a palavra for apontada como string
        if palavra == '"':
            line = lista[linha]
            for valor in re.finditer("""\"[^"]*\"""", lista[linha]):
                c1 = "<span style=\'fg:{}\'>".format(cor)
                c2 = "</span>"

                line = texto[:valor.start()+1 + correcao] + c1 + texto[valor.start()+1 + correcao : valor.end() + correcao] + c2 + texto[valor.end() : ]

                correcao = correcao + len(c1) + len(c2)

            texto = texto.replace(lista[linha], line)
        # se a palavra foi apontada como numérico
        elif palavra == "numerico":
            line = lista[linha]
            for valor in re.finditer('(\\s|^)([0-9\\.\\, \\s]+)(\\s|$)', lista[linha]):
                c1 = "<span style=\'fg:{}\'>".format(cor)
                c2 = "</span>"

                line = texto[:valor.start()+1 + correcao] + c1 + texto[valor.start()+1 + correcao : valor.end() + correcao] + c2 + texto[valor.end() : ]

                correcao = correcao + len(c1) + len(c2)
            texto = texto.replace(lista[linha], line)

        # Se a palavra foi apontada como comentário
        elif palavra == "comentario":
            for valor in re.finditer('(#|\\/\\/).*$', lista[linha]):
                #print(valor.start(), valor.end(), cor)
                pass

        # Se for uma palavra especial
        else:
            palavra_comando = palavra_comando.replace(' ','\\s*')
            for valor in re.finditer('(^|\\s){}(\\s|$)'.format(palavra_comando), lista[linha]):
                #print(valor.start(), valor.end(), cor)
                pass

# Cores que as palavras vão assumir
def sintaxeDasPalavras():

    # Principais comandos
    for comando in dicComandos['declaraVariaveis']:
        sintaxe(comando.strip(), Sintaxe["atribuicao"])

    for comando in dicComandos['declaraListas']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicComandos['adicionarItensListas']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicComandos['tiverLista']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicComandos['RemoverItensListas']:
        sintaxe(comando.strip(), Sintaxe["logico"])

    for comando in dicComandos['tamanhoDaLista']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicComandos['digitado']:
        sintaxe(comando.strip(), Sintaxe["tempo"])

    for comando in dicComandos['loopsss']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicComandos['repita']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicComandos['se']:
        sintaxe(comando.strip(), Sintaxe["condicionais"])

    for comando in dicComandos['mostre']:
        sintaxe(comando.strip(), Sintaxe["exibicao"])

    for comando in dicComandos['mostreNessa']:
        sintaxe(comando.strip(), Sintaxe["exibicao"])

    for comando in dicComandos['funcoes']:
        sintaxe(comando.strip(), Sintaxe["tempo"])

    for comando in dicComandos['aguarde']:
        sintaxe(comando.strip(), Sintaxe["tempo"])

    for comando in dicComandos['aleatorio']:
        sintaxe(comando.strip(), Sintaxe["tempo"])

    for comando in dicComandos['limpatela']:
        sintaxe(comando.strip(), Sintaxe["tempo"])

    # Comandos internos a cada Comando
    for comando in dicSubComandos['passandoParametros']:
        sintaxe(comando.strip(), Sintaxe["tempo"])

    for comando in dicSubComandos['acesarListas']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicSubComandos['adicionarItensListas']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicSubComandos['RemoverItensListas']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicSubComandos['tiverLista']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicSubComandos['recebeParametros']:
        sintaxe(comando.strip(), Sintaxe["tempo"])

    for comando in dicSubComandos['esperaEm']:
        sintaxe(comando.strip(), Sintaxe["tempo"])
    
    for comando in dicSubComandos['matematica']:
        sintaxe(comando.strip(), Sintaxe["contas"])

    for comando in dicSubComandos['repitaVezes']:
        sintaxe(comando.strip(), Sintaxe["lista"])

    for comando in dicSubComandos['logico']:
        sintaxe(comando.strip(), Sintaxe["logico"])

    # Numero
    sintaxe('numerico'     , Sintaxe["numerico"])

    # String
    sintaxe('"'            , Sintaxe["string"])

    # Comentários
    sintaxe('comentario'   , Sintaxe["comentario"])

sintaxeDasPalavras()
print(texto)