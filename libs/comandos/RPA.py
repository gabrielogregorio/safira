class RPA():
    def __init__(self):
        """
        Biblioteca de RPA
        """
        pass

    def funcao_abrir_arquivo(self, nome_arquivo, nome_software):

        nome_arquivo =Run.abstrair_valor_linha(self, nome_arquivo)
        nome_software =Run.abstrair_valor_linha(self, nome_software)

        if not nome_arquivo[0]: return nome_arquivo
        if not nome_software[0]: return nome_software
        
        if nome_arquivo[2] != "string":
            return [False, "O nome do arquivo precisa ser um texto", 'string', ' exibirNaTela'] 

        if nome_software[2] != "string":
            return [False, "O nome do software precisa ser um texto", 'string', ' exibirNaTela'] 

        texto = system("{} \"{}\" ".format(nome_software[1], nome_arquivo[1] ))

        return [True, texto, "string", "exibirNaTela"]


    def funcao_tirar_print_salvar_como(self, nome_imagem):
        nome_imagem =Run.abstrair_valor_linha(self, nome_imagem)

        if not nome_imagem[0]: return nome_imagem

        if nome_imagem[2] != "string":
            return [False, "O nome da imagem precisa ser um texto", 'string', ' exibirNaTela'] 

        try:
            import pyautogui
            pyautogui.screenshot(nome_imagem[1])

        except Exception as e:
            return [False, "Erro com a execução da função, erro 1 '{}'".format(e), "string", 'exibirNaTela']

        else:
            return [True, True, "booleano", "fazerNada"]

    def thread_tempo_espera(self, tempo):
        self.esperando_tempo = True
        sleep(tempo)
        self.esperando_tempo = False




    def funcao_a_imagem_aparecer_por_minuto(self, imagem, tempo):
        tempo =Run.abstrair_valor_linha(self, tempo)
        if not tempo[0]: return tempo

        if tempo[2] != 'float':
            return [False, "A variável tempo precisa ser numérica", 'string', ' exibirNaTela'] 

        # Minutos em segundos
        return funcao_a_imagem_aparecer_por(self, imagem, tempo[1]*60)

    def funcao_a_imagem_aparecer_por(self, imagem, tempo):
        #Run.log(self, 'funcao funcao_a_imagem_aparecer_por {}'.format(imagem))

        imagem =Run.abstrair_valor_linha(self, imagem)
        tempo =Run.abstrair_valor_linha(self, tempo)

        if not imagem[0]: return imagem
        if not tempo[0]: return tempo

        if imagem[2] != "string":
            return [False, "A imagem precisa ser um texto", 'string', ' exibirNaTela']

        if tempo[2] != "float":
            return [False, "A variável tempo precisa ser numérico", 'string', ' exibirNaTela']

        self.esperando_tempo = True
        threading.Thread(target=lambda this=self, tempo=tempo:Run.thread_tempo_espera(self, tempo))

        try:
            import pyautogui

            posicoes = None
            while posicoes is None:
                posicoes = pyautogui.locateCenterOnScreen(imagem[1], confidence=0.8, grayscale=True)

                if posicoes is not None:
                    return [True, True, "booleano", "fazerNada"]

                if not self.esperando_tempo:
                    return [True, False, "booleano", "fazerNada"]

        except Exception as e:
            return [False, "Erro com a execução da função, erro 1 '{}'".format(e), "string", 'exibirNaTela']

        else:
            return [True, teste, "booleano", "fazerNada"]

    # ************************* FIM RPA ************************************#

