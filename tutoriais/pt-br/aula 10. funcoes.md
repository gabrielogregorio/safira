## Conceito de Funções  
Cria um bloco de código com um nome que pode ser
executado em qualquer parte do código através da palavra atribuida


## Usando Funções Simples
```
# Criando uma função
funcao mostraArvore
{
    mostre "    *    "
    mostre "   ***   "
    mostre "  *****  "
    mostre " ******* "
    mostre "    *    "
}

# Chamando a função
mostraArvore
```

## Usando Funções Com parâmetros
```
# Você também pode criar uma função com parâmetros
funcao calculaMedia recebe parametros nota1, nota2
{
    # Retorna o valor para quem chamou a função
    retorne (nota1 + nota2) / 2
}

# A variável final agora terá o valor retornado
nota_final vale calculaMedia passando parametros 9.8, 7.5
```

## Variações da Declaração de uma Funções
```
function mostraSobrenome {}
funcao mostraSobrenome {}
funcion mostraSobrenome {}
def mostraSobrenome {}
```
