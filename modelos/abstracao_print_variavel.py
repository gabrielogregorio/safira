s = """ 
mostre Biscoito 
exiba Nasa 
"""

NOVO_VARIAVEIS = {'Biscoito':14,'Nasa':'Agencia Espacial'}
exibicao = ['mostre','mostre nessa tela','exiba','exiba nessa tela','escreva na tela', 'escreva', 'print']
programa = s.split('\n')

string = False
NOVA_metodo_localizado = False
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
        NOVA_metodo_localizado = True

    if continuacoes > 0:
      continuacoes -= 1
      continue

    # Abstrair numero
    if (programa[linha][caracter] == ' ') and string==True:
      string = False

    if programa[linha][caracter].isalnum() and NOVA_metodo_localizado:
      string = True

    if string == True:
      parametro += programa[linha][caracter]
      continue

  if metodo == 'mostre':
    if string == True:
      print('deixe um espaço no final da linha {}'.format(linha))
      break

    try:
      if NOVO_VARIAVEIS[parametro.strip()]:
        pass
    except:
      print('Você esqueceu de dizer quanto vale a variável {}'.format(parametro.strip()))
    else:
      mostre(  NOVO_VARIAVEIS[parametro.strip()]  )



