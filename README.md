![Imagem](imagens/projeto.gif)

-------


<p align="center">
  Desenvolvimento da linguagem de programação Safira
  <br>
  <a href="https://safiralang.blogspot.com/"><strong>Faça do Download das versões estáveis >> </strong></a>
  <br>
  <br>

</p>

![GitHub estrelas](https://img.shields.io/github/stars/safira-lang/safira-ide)
![GitHub last commit](https://img.shields.io/github/last-commit/safira-lang/safira-ide?style=flat-square)
![GitHub contributors](https://img.shields.io/github/contributors/safira-lang/safira-ide)
![GitHub language count](https://img.shields.io/github/languages/count/safira-lang/safira-ide)
![GitHub repo size](https://img.shields.io/github/repo-size/safira-lang/safira-ide)

# Introdução


A Safira é uma linguagem de programação focada na lógica com o objetivo de amortecer o impacto do primeiro contato com o mundo da programação, oferecendo uma interface simples, intuitiva e uma codificação natural.

Aviso: Uma versão dos outros repositórios estão embutidos neste repositório.

A Safira é focada apenas na estrutura básica e em pequenos scripts, sendo que o principal diferencial dela é aceitar comandos em níveis naturais, como se fosse uma pessoa conversando com outra e comandos em linguagem similar as principais linguagens do mercado.

Nos primeiro contato com a Safira, é recomendado o uso de comandos no idioma nativo, como o português, exemplo:

Se o foco for ensinar linguagem Python para um grupo de pessoas com dificuldade, é recomendado começar com comandos bem simples, como:

    nome vale o que o usuario digitar

    se nome for igual a "Gabriel" entao {
        mostre "Olá Gabriel"
    } 

Posteriormente, é recomendado a variação, mesmo que seja comando por comando, no ritmo do aluno para a seguinte codificação:

    nome = input

    if nome == "Gabriel" {
        print "Olá Gabriel"
    }

Perceba que a Safira está muito mais próximo do Python agora.

Desta forma, a complexidade das linguagens de programação, é reduzida e o conceito é levado mais em conta. 

A safira entende comando em inglês, português, espanhol e de forma similar a outras linguagens do mercado.
 
É assim que fica a codificação de um programa maior na Safira.
![Imagem](imagens/safira.png)


--------------
# Plataforma Base

A IDE final deve ser leve e independente do Python, devendo funcionar no Windows 10.

--------------------------------

# Como iniciar o desenvolvimento
Hoje a safira é feita no Python3.8, tenha ele instalado.
principais plataformas de desenvolvimento é Ubuntu, Linux Mint e Windows por enquanto

#### Crie um ambiente virtuai e ative-o
```shell
python3.8 -m venv .
source ./activate
```

#### Desenvolva os programas
Programe seguinte separando as etapas e fazendo muitos testes

#### Instale biblioteca
Instale as bibliotecas, dentro do ambiente virtual
```shell
python -m pip install requests
```

#### Salve os requisitos
```shell
python -m pip freeze > requeriments.txt
```

-----------------
## Nomes de Widgets

| Nomes de variáveis | Widgets tkinter |
|--------------------|-----------------|
| Button             | bt_             |
| Label              | lb_             |
| Frame              | fr_             |
| Entry              | et_             |
| Text               | tx_             |

-------------------------

## Classes

Classes devem começar com letra maiúscula, e terem type anotations e docstring para documentá-las

```python
class Atualizar:
    """ Essa classe fornece recursos de atualizações """
    def __init__(self, versao:str) -> None:
        pass
```

------------------------

## Funções

todas as letras em **minúscula** e separado por _, usando type anotations e docstrings

```python
def analisar_comando(self, texto: str, pontos: dict={}) -> dict:
    return {'pontos': pontos}

```

-------------

### Outras boas prátcas

```python
    # Recomendado
    if (valor):

    # Nao recomendado
    if (valor == True)



    ### Recomendado
    if (valor is None):

    ### Não recomendado
    if (valor == None)
```

---------------

# Como executar os arquivos do repositório
## 1° forma, versão estável para aprender
Baixe a versão executável, no final da página em **Download**.

1. Baixe o arquivo .zip
2. Extraia-o em alguma pasta
3. Execute a Safira

**Para distribuições Linux, certifique de fornecer as permissões para executar.**

## 2° forma, versão de desenvolvimento
Está é uma versão de desenvolvimento, com bugs e implementações em andamento.

1. clone este repositório  
2. Baixe e instale o Python3.8 (3.7 e 3.6 são aceitos)  
3. Instale os pacotes necessários com o comando abaixo  

  ```shell
    python3.8 -m pip install -r requeriments.txt
  ```
4. Execute o arquivo safiraide.py

A IDE será carregada, e você já pode desenvolver

-------------------------------------

# Como programar em Safira?
Confira os principais comandos aqui: https://safiralang.blogspot.com/p/comandos.html

-------------------------------------

# Como fazer parte do desenvolvimento da safira?
Entre em contato com:
* safira.ide@gmail.com

# Quem pode ajudar no desenvolvimento?
Atualmente precisamos de pessoas que possam dar feedback sobre o projeto, que possam usá-la, de desenvolvedores que possam melhorar o código, tornando o mais escalável, de designs para ajudar no desenvolvimento de interfaces mais bonitas e que sejam úteis para os usuários e de pessoas que possam contribuir de outras formas.

# Quais tecnologias o projeto usa atualmente?
* Python3.8 para todo o projeto por enquanto

#### Interface gráfica
* tkinter como principal biblioteca para a geração das interfaces

#### Interpretador
* expressões regulares para a análise de comandos no interpretador

#### Recursos
* biblioteca requests para a comunicação com a internet

-------------------------

# Download
* [Windows 10](https://safiralang.blogspot.com/p/downloads.html)
* [Linux Mint](https://safiralang.blogspot.com/p/downloads.html)
* [Ubuntu](https://safiralang.blogspot.com/p/downloads.html)

# Outros Links
* [Blog](https://safiralang.blogspot.com/)
* [Facebook](https://www.facebook.com/safiralang/)
