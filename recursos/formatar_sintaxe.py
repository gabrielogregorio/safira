class Formatar():
    """Recebe um código sem formatação e retorna ele formatado em relação aos espaços

    ============= Entrada: =============
    if 1 == 1 {
      mostre 1
        if 2 == 2 {
           mostre "Olá"             
           }         
     }

    =============== Saída ==============
    if 1 == 1 {
        mostre 1        
        if 2 == 2 {     
            mostre "Olá"
        }
    }

    """
    def __init__(self, codigo:str):
        """carregamento do texto

        Args:
            codigo (str): Código do programa
        """
        self.codigo = codigo

    def formatar(self):
        novo_codigo = ""  # Código Formatado
        espaco = '' # Espaço para ajudar na formatação

        # Separação das linhas por \n
        linhas = self.codigo.split('\n')

        # Loop pelas linhas
        for linha in linhas:
            linha = linha.strip()

            # Se encontrar um {, é para aumentar 4 espaços
            inicio_aumento = False

            if '{' in linha:
                inicio_aumento = True
                novo_codigo = novo_codigo +'\n'+ espaco + linha
                espaco = espaco + '    '
                continue

            if '}' in linha:
                # Remoção de 4 espaços
                if len(espaco) == 4 or espaco == '':
                    espaco = ''
                else:
                    espaco = espaco[0:-4]

            if not inicio_aumento:
                novo_codigo = novo_codigo +'\n'+ espaco + linha

        return novo_codigo[1:]

if __name__ == '__main__':
    codigo = '''sss
        if 1 == 1 {
        mostre 1
            if 2 == 2 {
            mostre "Olá"             
        }         
        }'''

    f = Formatar(codigo)
    print(f.formatar())