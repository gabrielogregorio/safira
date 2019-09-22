# funções básicas
class funcao():
    def abrir_arquivo(filename):
        try:
            arquivo = open(filename,'r',encoding='utf8')
            text = arquivo.read()
            arquivo.close()

        except Exception as erro:
            print('Aconteceu um erro ao abrir o arquivo {}. \n\nErro:'.format(filename,erro))
            return None

        else:
            print('Arquivo aberto com sucesso')
            return text

