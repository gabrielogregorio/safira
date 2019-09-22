s = """ 
mostre 21 
mostre 24.14 
escreva 3 
mostre 4 
mostre 5 
print 6 
exiba 7 

"""

exibicao = ['mostre','mostre nessa tela','exiba','exiba nessa tela','escreva na tela', 'escreva', 'print']
programa = s.split('\n')

string = False

def mostre(parametro):
    print(parametro)

for linha in range( len( programa ) ):
  continuacoes = 0
  if string == False:
    metodo = ''
  parametro = ''
  for caracter in range( len( programa[linha] ) ):

    # método localizado
    for itens in exibicao:

      if programa[linha][caracter : caracter + len(itens)] == itens:
        continuacoes = len(itens)
        metodo = 'mostre'

    if continuacoes > 0:
      continuacoes -= 1
      continue

    # Abstrair numero
    if (programa[linha][caracter] == ' ') and string==True:
      string = False

    if programa[linha][caracter].isnumeric():
      string = True

    if string == True:
      parametro += programa[linha][caracter]
      continue

  if metodo == 'mostre':
    if string == True:
      print('deixe um espaço no final da linha {}'.format(linha))
      break
    mostre(parametro)



