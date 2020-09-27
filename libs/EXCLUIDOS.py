
            ##################################################################
            #                       SISTEMA OPERACIONAL                      #
            ##################################################################

            #if caractere_inicio in self.dicLetras["obter_diretorio"]:
            #    instrucao_analise = Interpretador.analisa_instrucao(self, '^(<obter_diretorio>)$', linha)
            #    if instrucao_analise[0]: return [Interpretador.funcao_obter_diretorio_atual(self), self.num_linha, ""]

            #if caractere_inicio in self.dicLetras["mova"]:
            #    instrucao_analise = Interpretador.analisa_instrucao(self, '^(<mova>)(.*)(<mova_para>)(.*)(<mova_para_opcional>)$', linha)
            #    if instrucao_analise[0]: return [Interpretador.funcao_mover_arquivo(self, instrucao_analise[1][2], instrucao_analise[1][4] ), self.num_linha, ""]

            #if caractere_inicio in self.dicLetras["copie"]:
            #    instrucao_analise = Interpretador.analisa_instrucao(self, '^(<copie>)(.*)(<copie_para>)(.*)(<copie_para_opcional>)$', linha)
            #    if instrucao_analise[0]: return [Interpretador.funcao_copiar_arquivo(self, instrucao_analise[1][2], instrucao_analise[1][4] ), self.num_linha, ""]


        #instrucao_analise = Interpretador.analisa_instrucao(self, '^(.*)(<for_vazio>)$', possivelVariavel)
        #if instrucao_analise[0]: return Interpretador.funcao_for_vazio(self, instrucao_analise[1][1])

        ##################################################################
        #                       SISTEMA OPERACIONAL                      #
        ##################################################################

        if caractere_inicio in self.dicLetras["obter_diretorio"]:
            instrucao_analise = Interpretador.analisa_instrucao(self, '^(<obter_diretorio>)$', possivelVariavel)
            if instrucao_analise[0]: return Interpretador.funcao_obter_diretorio_atual(self)


        ##################################################################
        #                             ARQUIVOS                           #
        ##################################################################
        #if caractere_inicio in self.dicLetras["lista_arquivos_diretorio"]:
        #    instrucao_analise = Interpretador.analisa_instrucao(self, '^(<lista_arquivos_diretorio>)(.*)(<lista_arquivos_diretorio_final>)$', possivelVariavel)
        #    if instrucao_analise[0]: return Interpretador.funcao_listar_arquivos(self, instrucao_analise[1][2])




  "esta_contido_apenas_visualizacao":{
    "comando":[
      [" in ","en-us"]
    ],
    "cor":"logico"
  },

    # Funções do Sistema Operacional
    def funcao_obter_diretorio_atual(self):
        Interpretador.log(self, "__funcao_obter_diretorio_atual")

        return [True, os.getcwd() , 'string', 'fazerNada']



  "obter_diretorio":{
    "comando":[
      ["del directorio de trabajo actual", "es"],
      ["ele diretorio de trabalho atual", "es"],
      ["the current working directory", "en-us"],
      ["o diretorio de trabalho atual", "pt-br"],
      ["directorio de trabajo actual", "es"],
      ["diretorio de trabalho atual", "pt-br"],
      ["current working directory", "en-us"],
      ["o diretorio de trabalho", "pt-br"],
      ["take the current path ", "en-us"],
      ["the current directory", "en-us"],
      ["the current folder", "en-us"],
      ["el directorio actual", "es"],
      ["o diretorio atual", "pt-br"],
      ["o diretorio atual", "pt-br"],
      ["la carpeta actual", "es"],
      ["a pasta atual", "pt-br"]
          ],
    "cor":"lista"
  },








  "lista_arquivos_diretorio":{
    "comando":[
      ["una lista de todos los archivos en el directorio ", "es"],
      ["uma lista com todos os arquivos do diretorio ", "pt-br"],
      ["lista com todos os arquivos do diretorio ", "pt-br"],
      ["una lista de archivos en el directorio ", "es"],
      ["una lista con archivos del directorio ", "es"],
      ["lista com arquivos do diretorio ", "pt-br"],
      ["lista de arquivos do diretorio ", "pt-br"],
      ["a list of all files in the ", "en-us"],
      ["os arquivos do diretorio ", "pt-br"],
      ["archivos del directorio ", "es"],
      ["list with files from the ", "en-us"],
      ["arquivos do diretorio ", "pt-br"],
      ["list of files in the ", "en-us"],
      ["files from the ", "en-us"]
    ],
    "cor":"lista"
  },

  "lista_arquivos_diretorio_final":{
    "comando":[
      [" directory", "en-us"],
      ["", "all"]
    ],
    "cor":"lista"
  },





  "copie":{
    "comando":[
      ["copie el archivo ","es"],
      ["copia o arquivo ","pt-br"],
      ["copy the file ","en-us"],
      ["copia ","pt-br"],
      ["copie ","es"],
      ["copy ","en-us"]
    ],
    "cor":"lista"
  },
  "copie_para":{
    "comando":[
      [" to the directory ","en-us"],
      [" en el directorio ","es"],
      [" para o diretorio ","pt-br"],
      [" al directorio ","es"],
      [" to the folder ","en-us"],
      [" para a pasta ","pt-br"],
      [" a la carpeta ","es"],
      [" to the ","en-us"],
      [" para ","pt-br"],
      [" to ","en-us"],
      [" a ","es"]
    ],
    "cor":"lista"
  },
  "copie_para_opcional":{
    "comando":[
      [" directory","en-us"],
      [" folder","en-us"],
      ["","all"]
    ],
    "cor":"lista"
  },

 
  "for_vazio":{
    "comando":[
      [" for vazio","pt-br"],
      [" is empty","en-us"],
      [" esta vacio","es"]
        ],
    "cor":"condicionais"
  },




    def funcao_for_vazio(self, valor):
        teste_valor = Interpretador.abstrair_valor_linha(self, valor)
        if not teste_valor[0]:
            return teste_valor

        if teste_valor[1] == "":
            return [True, True, "booleano", "fazerNada"]
        return [True, False, "booleano", "fazerNada"]







  "for_vazio":{
    "comando":[
      [" for vazio","pt-br"],
      [" is empty","en-us"],
      [" esta vacio","es"]
        ],
    "cor":"condicionais"
  },






  "mova":{
    "comando":[
      ["mueva el archivo ","es"],
      ["mova o arquivo ","pt-br"],
      ["move the ","en-us"],
      ["mova ","pt-br"],
      ["mueve ","es"],
      ["move ","en-us"]
        ],
    "cor":"lista"
  },
  "mova_para":{
    "comando":[
      [" para o diretorio ", "pt-br"],
      [" al directorio ", "en-us"],
      [" para a pasta ", "pt-br"],
      [" a la carpeta ", "es"],
      [" file to the ", "en-us"],
      [" file to ", "en-us"],
      [" to the ", "en-us"],
      [" para ", "pt-br"],
      [" to ", "en-us"]
        ],
    "cor":"lista"
  },
  "mova_para_opcional":{
    "comando":[
      [" directory","en-us"],
      [" folder","en-us"],
      ["","all"]
    ],
    "cor":"lista"
  },




    def funcao_mover_arquivo(self, arquivo, objetivo):
        Interpretador.log(self, "__funcao_mover_arquivo")

        # Abstrair o valor do arquivo e do objetivo
        teste_arquivo = Interpretador.testar_existencia(self, arquivo)
        if not teste_arquivo[0]: return teste_arquivo

        teste_objetivo = Interpretador.testar_existencia(self, objetivo)
        if not teste_objetivo[0]: return teste_objetivo

        try:
            shutil.move(teste_arquivo[1], teste_objetivo[1])
        except Exception as erro:
            #if  'already exists' in erro:
            return [False, self.msg("erro_mover_arquivo").format(teste_arquivo[1], teste_objetivo[1], erro), 'string', 'fazerNada']

        return [True, True , 'booleano', 'fazerNada']

    def funcao_copiar_arquivo(self, arquivo, objetivo):
        Interpretador.log(self, "__funcao_copiar_arquivo")

        # Abstrair o valor do arquivo e do objetivo
        teste_arquivo = Interpretador.testar_existencia(self, arquivo)
        if not teste_arquivo[0]: return teste_arquivo

        teste_objetivo = Interpretador.testar_existencia(self, objetivo)
        if not teste_objetivo[0]: return teste_objetivo

        try:
            shutil.copy(teste_arquivo[1], teste_objetivo[1])
        except Exception as erro:
            #if  'already exists' in erro:
            return [False, self.msg("erro_copiar_arquivo").format(teste_arquivo[1], teste_objetivo[1], erro), 'string', 'fazerNada']

        return [True, True , 'booleano', 'fazerNada']


  "abra_um_arquivo":{
    "comando":[
      ["abra o arquivo ","pt-br"],
      ["abra a imagem ","pt-br"],
      ["abra a foto ","pt-br"]
    ],
    "cor":"lista"
  },
  "abra_um_arquivo_no":{
    "comando":[
      [" no ","pt-br"]
    ],
    "cor":"lista"
  },


  ,

  "crie_um_diretorio":{
    "comando":[
      ["crie uma pasta com o nome de ", "pt-br"],
      ["crie um diretorio com o nome ", "pt-br"],
      ["crie um diretorio chamado ", "pt-br"],
      ["crie uma pasta com o nome ", "pt-br"],
      ["crie uma pasta chamada ", "pt-br"],
      ["create a folder called ", "en-us"],
      ["create a folder named ", "en-us"],
      ["crear un directorio ", "es"],
      ["criar um diretorio ", "pt-br"],
      ["crear una carpeta ", "es"],
      ["crie o diretorio ", "pt-br"],
      ["crie uma pasta ", "pt-br"],
      ["crie a pasta ", "pt-br"],
      ["create the ", "en-us"],
      ["create a ", "en-us"]
      
          ],
    "cor":"lista"
  },
  "crie_um_diretorio_sub":{
    "comando":[
      [" directory","en-us"],
      [" folder","en-us"],
      ["","all"]
    ],
    "cor":"lista"
  }


  #ARRUMAR O ESTA CONTIDO
Ver se um arquivo termina com uma extensao








### FUTURO
### n recebe os arquivos do diretório "/home" que terminam com ".pdf"

Apagar um diretório

limpar arquivo
limpe o arquivo "log.txt"

crie uma pasta com o nome
crie uma pasta chamada
create a folder called
create a folder named
crear la carpeta
cree la carpeta 
crie a pasta
create the

dentro de la carpeta
folder inside the
en el directorio
dentro da pasta
folder in the
en la carpeta
no diretorio
na pasta
in the 

directory
folder

Liste todos os arquivos do diretório
Criar um diretório 
Apagar um diretório


PRECISA DE ERRO AO NAO FECHAR BLOCOS
BUGO DO ENTAO ANTES DE {, exemplo. entao{ da erro
ARREDONDAMENTO
dividido pelo
dividido por
Suporte a comentários com //