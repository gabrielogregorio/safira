import subprocess

#output = subprocess.run(["./analisador_de_codigo"], stdout = subprocess.PIPE,
#                        universal_newlines = True).stdout
codigo = "if 1 == 1 else 2 == 2\n if 2 == 2"
output = subprocess.run(["analisador_de_codigo", codigo], stdout = subprocess.PIPE,
                        universal_newlines = True).stdout

posicoes = []
for linha in codigo.split('\n'):
    posicoes.append(len(linha))

print(posicoes)

opcoes = output.split(';')
for opcao in opcoes:
    if opcao.strip() == '': continue

    i, f, cor = opcao.split('.')
    lin = 0
    for x in posicoes:
        lin += 1
        subtract = 0# sum(posicoes[0:lin])
        print(subtract)
        if x >= int(i):
            print('{}.{}, {}.{}, {}'.format( lin, int(i)-subtract, lin, int(f)-subtract, cor)) 

