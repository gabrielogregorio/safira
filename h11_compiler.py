a = open('programa.ec','r')
s = a.read() + ' '
a.close()

global programa
global p

programa = ''
p = 0

# Não aconteceu nada
global aconteceu
# sim ou não | evento
aconteceu = [False,'']

def substitui(valor,por):
    global aconteceu
    global p
    global programa
    if valor == s[p:p+len(valor)]:
        programa += por
        p += len(valor)
        aconteceu = [True,por]

def troca():
    # atribuição
    substitui('vale','=')
    substitui('recebe','=')

    # loop
    substitui('enquanto','while')

    # comparação
    substitui('for diferente de','!=')
    substitui('for menor que','<')
    substitui('for maior que','>')
    substitui('for igual a','==')

    # usos do print
    substitui('exiba','print(')
    substitui('mostre','print(')

    # SE NÂO TEM QUE SER ANTES DO SE
    substitui('senao','else: ')
    substitui('se ','if ')

while p < len(s):
    # troca valores
    troca()

    # se não aconteceu nada
    if aconteceu[0] == False:
        programa += s[p]
        p += 1

    elif aconteceu[1] == 'print(':
       inicio = s[ p : p+s[p:].find('\n')+1]
       inicio = inicio.replace('\n',')\n')
       s = s[:p] + inicio + s[p+s[p:].find('\n')+1:]

    elif aconteceu[1] == 'if ' or aconteceu[1] == 'while':
       inicio = s[ p : p+s[p:].find('\n')+1]
       inicio = inicio.replace('\n',':\n')
       s = s[:p] + inicio + s[p+s[p:].find('\n')+1:]

    # resete os acontecimentos
    aconteceu[0] = False

f = open('script.py','w')
f.write(programa)
f.close()

import os
os.system('python script.py')
#print(programa)
