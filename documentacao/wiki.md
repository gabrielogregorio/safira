## Documentação da Safira

**Versão da documentação:** 04/07/2020  
**Versão da Safira:** 0.25  
**Idioma:** Português-Brasil  



## Tópicos
- [Introdução](#Introdução)  
- [palavras Frequentes](#Introdução)  
- [Interface gráfica](#Introdução)  
- [Sintaxe](#Introdução)  
- [Exibindo algo na tela](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Declarando variáveis](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Testando condições](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Fazendo Loops](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Esperando por um tempo](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Manipulando Textos](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Criando e manipulando listas](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Sorteando um número](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Lendo o teclado](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Criando Funções](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Criando e manipulando arquivos](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Controlando o sistema operacional](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
- [Trabalhando com datas](#Introdução)  
  - [Conceito](#Introdução)  
  - [Usando na prática](#Introdução)  
  - [Variações](#Introdução)  
  


## Introdução

A Safira é uma linguagem de programação focada na naturalidade, na prática, você consegue programar usando palavras como se estivesse conversando com outra pessoa. A Safira também consegue trabalhar em um nível mais direto.

## Palavras Interessantes!  
- **Programa:** É o Texto que você escreveu, são suas ordens ao computador
- **Script:** É um arquivo com o programa que vocẽ escreveu. Normalmente eles terminal com ".safira"
- **Algorítimo:** É o programa que você escreveu, ou mais especificamente, a sua solução

-----
## **Introdução do Menu**
O menu da safira contém informações e recrusos de acesso arápido para otimizar  seu tempo na programação

## **Menu Arquivo**    
#### Abrir Arquivo    
Abre um script safira, você pode informar 

#### Nova Aba  
Abre uma nova Aba para você escrever outro código safira

#### Salvar  
Salva suas modificações no Script

#### Salvar Como  
Salva o script com um novo nome, como uma cópia

-------------

## **Menu Executar**  
#### Executar Tudo  
Inicia e executa o código Safira até o final sem paradas

#### Executar Linha por Linha  
Inicia e executa linha por linha da safira, parando a cada linha que é executada e você autoriza a safira a executar a proxima linha

#### Executar Até BreakPoint  
Inicia e Executa até um ponto de parada (breakpoint)

#### Inserir BreakPoint  
Insere um ponto de parada, se a safira for executa no modo Executar até breakpoint, a safira irá executar o código até essa linha, parando nela.

> Aviso: A Safira não lê linhas que contém apenas comentários.

---------------

## **Exemplos**  
Contém vários exemplos de código em Safira, você 

---------------
    
## **Interface**   
#### Temas  
Contem Cores diferntes para a interface

#### Interface  
Contem cores 

---------

## Ajuda Sobre  


----------------
# **Menu de acesso rápido**   
## Interface
(img)[]


## Salvar  
Salva suas modificações no Script  

## Executar Tudo  
Inicia e executa o código Safira até o final sem paradas  

## Executar Até BreakPoint  
Inicia e Executa até um ponto de parada (breakpoint)  

## Inserir ou remover um BreakPoint  
Insere um ponto de parada, se a safira for executa no modo Executar até breakpoint, a safira irá executar o código até essa linha, parando nela.  
Clique em uma linha e aperte no item od breakpoint  

## Executar Linha por Linha   
Inicia e executa linha por linha da safira, parando a cada linha que é executada e você autoriza a safira a executar a proxima linha  

## Marca ou desmarca breakponts em todas as linhas  
Ao clicar nessa linhas, todas as linhas terão ou um breakpoint ou serão removidas
##?
Abre um menu de ajuda   

## BR  
Idioma da Safira, é nesta opção que você escolhe o idioma que a Safira irá trabalhar. Para que todas as alterações sejam aplicadas, você terá que terá que fechar a Safira e abrir novamente  

> Aviso: A Safira não lê linhas que contém apenas comentários, ou seja, não insira breakpoints em linhas sem comentários





-----------
# **Safira**



## Conceito de Exibiçao  
Esse comando serve para mostrar alguma coisa na tela
Para escrever um texto qualquer, coloqueo texto entre Aspas, exemplo:
"Isso é um texto"

## Usando Exibiçao
```
mostre "Olá mundo"
mostre "Isso é um texto qualquer"
mostre 10
```

## Variações da Exibiçao
Se você quiser exibir um texto e um número por exemplo, você pode usar a virgula, desta forma:
```
mostre "A soma de 2 + 2 é ", 4
```

Você também pode fazer contas
```
mostre 10 + 5
mostre "A soma de 10 + 5 é ", 2 + 5
```

Além do mostre, você pode usar todos esses comandos para fazer a mesma coisa:
```
mostre "Olá, tudo bem?"
imprima "Olá, tudo bem?"
escreva "Olá, tudo bem?"
escreval "Olá, tudo bem?"
exiba "Olá, tudo bem?"
show "Olá, tudo bem?"
write "Olá, tudo bem?"
printf "Olá, tudo bem?"
println "Olá, tudo bem?"
mostrar "Olá, tudo bem?"
escribe"Olá, tudo bem?"
```

-------------------


## Conceito de Variáveis  
Variáveis são palavras que tem um valor que pode variar associado a elas.

## Usando Variáveis
```
nome vale "Safira"
numero vale 10

mostre nome
mostre numero

# Neste exemplo de cima, a variável nome tem o valor de "gabriel", um txto e a variável numero tem o valor numérico de 10.

```

## Variações da Variáveis

```
nome has the value of "safira"
nome tem o valor do "safira"
nome tem o valor de "safira"
nome receives "safira"
nome receive "safira"
nome vale "safira"
nome tiene el valor "safira"
nome tem o valor "safira"
nome obtiene "safira"
nome := "safira"
nome equals "safira"
nome recebe "safira"
nome worth "safira"
nome <- "safira"
nome = "safira"
```

## Conceito de condições  
Este comando testa se uma ou mais condições são verdadeiras, a primeira condição que for verdadeira, será executada, as demais serão ignoradas, mesmo que também sejam verdadeiras.


## Usando condições

```
sinal = "Vermelho"

se 1 for igual a 1 entao
{
    mostre "A condição é verdadeira"
}
senao se 2 for diferente de 10 ou sinal for igual a "Vermelho"
{
    mostre "Essa condição é verdadeira e a de cima é falsa"
}
senao 
{
    mostre "Nenhuma das condições são verdadeiras"
}

```  

O "senao se" e o "senao" não são obrigatórios, você pode usa-los ou não.
O "senao" sempre deve ser o ultimo teste

## Variações da condições 
Todas as condições podem começar pelos seguintes comandos

```
# quando
# caso
# se
# if
# si
```

## Variações dos testes das condições 
```
for maior ou igual a 
es mayor o igual a 
is greater than or equal to 
>= 

 
for diferente de 
es diferente de 
is different from 
!= 
 
for igual a 
es igual a 
is equal to 
== 

for maior que 
es mayor que 
is greater than 
> 

for menor que
es menos que 
is less than
< 

true
truth
verdadeiro
verdadeira
verdade
cierto
verdad

false
falso
mentira

for menor ou igual a 
es menor o igual que 
is less than or equal a 
<= 

```

## Variações dos multiplos testes das condições 
Em uma condição, você pode fazer vários testes, usando os seguintes separados.
## Se uma condição for verdadeira ou se a outa for
```
se 1 for maior que 2 ou 2 for menor que 1
# ou 
# or 
# o 
# ||
```

```
and 
e 
y 
&& 
```

## Variações do então no final dos testes
Se você quiser, você pode colocar um dos seguintes comandos no final do seu código:
```
entao faca isso
entonces cuchillo
entao faca
then knife
cuchillo
entonces
entao
knife
then
faca
```

---------------------
## Conceito de Loops Enquanto  
## Usando Loops Enquanto  
## Variações da Loops Enquanto  

## Conceito de Loops Para cada
## Usando Loops Para cada  
## Variações da Loops Para cada  

## Conceito de delay  
## Usando delay
## Variações da delay

## Conceito de Manipulando Textos  
## Usando Manipulando Textos  
## Variações da Manipulando Textos

## Conceito de Listas  
## Usando Listas
## Variações da Listas






------------

## Conceito de Sorteando um número  
Este comand sorteia um número aleatório, os valores informandos podem ser numéricos diretamente ou variáveis.

## Usando Sorteando um número
```
numeroSorteado = um numero aleatorio entre 10 e 20
mostre numeroSorteado
```

## Considerações do comando
Os valores também pode ser variávies, exemplo:

```
numero1 vale 2
um numero aleatorio entre numero1 e 10
```

Uma variável também pode receber um numeró aleatorio, exemplo:
```
nomero_soteado vale um numero aleatorio entre 2 e 10
```


## Variações da Sorteando um número
```
um numero aleatorio entre 2 e 10
pense em um numero aleatorio entre 2 e 20
numero aleatorio entre 2 e 10
un numero aleatorio entre 2 e 10
numero aleatorio entre 2 e 10
a random number between 2 and 10
random number between 2 y 10
```

----------------------

## Conceito de Lendo o teclado  
Recebe um valor que o usuario digitar
Se o comando não contiver a palavrá "número" (em seus respectivos idiomas), O valor será considerado texto


## Usando Lendo o teclado
```
mostre nessa linha "Digite seu nome: "
nome vale o que o usuario digitar

mostre nessa linha "Digite sua idade: "
idade = o numero que o usuario digitar

mostre nome, " sua idade é ", idade
```

## Variações da Lendo o teclado

```
o numero que o usuario digitar
numero que o usuario digitar
o numero que for digitado
numero que for digitado
o que o usuario digitar
que o usuario digitar
o que for digitado
que for digitado
numero digitado
digitado
entrada
el numero que ingresa el usuario
numero que escribe el usuario
el numero que se ingresa
numero que está escrito
lo que escribe el usuario
el usuario a escribir
lo que sea que esté escrito
eso está escrito
numero escrito
mecanografiado
the number that the user enters
number that the user types
the number that is entered
number that is typed
what the user types
the user to type
whatever is typed
that is typed
typed number
input
typed
```

------------------------

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

## Variações da Declaração de recebendo paramaetros
```
funcao mostraDobro recebe parametros numero {}
funcao mostraDobro receives parameters numero {}
funcao mostraDobro recibe parametros numero {}
funcao mostraDobro(numero) {}
funcao mostraDobro(numero): {}
```

## Variações de Chamando uma função
O modo mais básico é digitar o nome de uma função, mas se caso ela tiver parâmetros, você terá que usar uma destas formas

```
mostraDobro passando parametros25
mostraDobro passing parameters 25
mostraDobro passing parameter 25
mostraDobro parameters 25
mostraDobro parametros de paso 25
mostraDobro parametro de paso 25
mostraDobro parametros 25
mostraDobro pasando los 25
mostraDobro passing 25
mostraDobro passando parametro 25
mostraDobro parametros 25
mostraDobro passando 25
mostraDobro parametro 25
mostraDobro 25
mostraDobro parameter 25
mostraDobro parametro 25
mostraDobro 25
mostraDobro(25)
```






----------------------------

## Conceito de manipulando arquivos  
Comandos para criar arquivos, adicionar texto, ler texto e excluir arquivos

## Usando manipulando arquivos

## Criando arquivos
```
# Criar um arquivo chamado "arquivo.txt"
crie o arquivo "arquivo.txt"
```

## Inserindo texto nos arquivos
```
# Adiciona u mtexto no final do arquivo
adicione "Texto qualquer" no arquivo "arquivo.txt"

# Sobrescreve todo o texto do arquivo por um novo texto
sobrescreva "Iai, tudo bem amigo" no arquivo "arquivo.txt"
```


## Obtendo o texto de arquivos
```
# Obtém o conteudo de um arquivo
conteudo = leia o texto do arquivo "arquivo.txt"
mostre conteudo
```

## Verificando se um arquivo existe
```
# Verificar se um arquivo existe ou não
se o arquivo "arquivoQUeNaoExiste.txt" nao existe
{
    mostre "Esse arquivo não existe"
}
senao se o arquivo "arquivoQUeNaoExiste.txt" existe
{
    mostre "Esse arquivo existe"
}


```

## Excluindo um arquivo
```
# Excluindo um arquivo
se o arquivo "arquivo.txt" existe
{
    mostre "Esse arquivo Existe e será removido"
    delete o arquivo "arquivo.txt"
}
```

## Variações da criação de arquivos
```
crie o arquivo "ola mundo.txt"
create the file "ola mundo.txt"
crea el archivo "ola mundo.txt"
```


## Variações da Adição de texto
```
escreva "ola mundo" no arquivo "log.txt"
adicione "ola mundo" no arquivo "log.txt"
write "ola mundo" in the file "log.txt"
add "ola mundo" to the "log.txt"
escriba "ola mundo" en el archivo "log.txt"
agregue "ola mundo" al archivo "log.txt"
```

## Variações da Substituição de texto
```
sobrescreva "ola" no arquivo "log.txt"
sobrescrever "ola" no arquivo "log.txt"
overwrite "ola" in the "log.txt"
overwrite "ola" in the "log.txt" file
sobrescriba "ola" en el archivo "log.txt"
```

## Variações da Leitura de texto
```
leia o texto do arquivo "log.txt"
get the text from the file "log.txt"
obtenha o texto do arquivo "log.txt"
read the text of the file "log.txt"
obtener el texto del archivo "log.txt"
lea el texto del archivo "log.txt"
leia o arquivo "log.txt"
read the file "log.txt"
lea el archivo "log.txt"
```

## Variações da Verificação se um arquivo existe
```
o arquivo "log.txt" nao existe
the file "log.txt" not exists
el archivo "log.txt" nao existe

o arquivo "log.txt" existe
the file "log.txt" exists
el archivo "log.txt" existe
```
## Variações da Excluir um arquivo
```
delete o arquivo "log.txt"
remova o arquivo "log.txt"
exclua o arquivo "log.txt"
delete the file "log.txt"
eliminar el archivo "log.txt"
```

--------------------------


## Conceito de Controlando o sistema operacional  
## Usando Controlando o sistema operacional
## Variações da Controlando o sistema operacional





## Conceito de Exidatasbiçao  
## Usando datas
## Variações da datas

