
    def inicializar_interpretador(self, tipo_execucao: str):
        """inicia uma instância do interpretador informando um código

        Args:
        tipo_execucao = "debug", "parar", "direto"

        Returns:
            None:
        """

        print("Inicializador do orquestrador iniciado")

        if self.interpretador_status == 'iniciado' or tipo_execucao == 'parar':
            # Para o interpretador
            try:
                self.instancia.aconteceu_erro = True

                if self.interpretador_finalizado:
                    # FINALIZAÇÃO COMPLETA
                    # Delete a instância
                    del self.instancia

                    # Insere mensagem de finalização
                    self.cont_lin1.linha_analise = 0
                    self.cont_lin1.desenhar_linhas()

                    self.bt_playP.configure(image=self.icone_play_stop)
                    print("############### FIM ############")
                    self.interpretador_status = 'parado'

            except Exception as erro:
                print("Instância inexistente")

            return 0

        elif self.interpretador_status == 'parado':
            self.interpretador_status = 'iniciado'
            self.interpretador_finalizado = False

            # Configura o icone de parar
            self.bt_playP.configure(image=self.icone_stop)
            self.bt_playP.update()
            
            # Carregar o console
            if tipo_execucao == 'debug':
                Interface.iniciar_terminal_debug(self)
                bool_ignorar_todos_breakpoints = False
            else:
                Interface.iniciar_terminal_direto(self)

                # A principio, ignore todos os breakpoint
                bool_ignorar_todos_breakpoints = True


            # Limpar o terminal
            self.tx_terminal.delete('1.0', END)
            self.tx_terminal.update()

            # Atualizar os elementos da interface
            self.tela.update()
            self.tx_editor_codigo.update()
            self.tx_terminal.update()

            # Linha que o interpretador está executando
            self.linha_analise = None

            # Obter o código
            linhas = self.tx_editor_codigo.get('1.0', END)[0:-1]

            # Adicionar marcação do número da linha
            linhas = Interface.colocar_linhas_codigo(self, linhas)

            # Obter o diretório base
            diretorio_base = self.dic_abas[self.num_aba_focada]["arquivoSalvo"]["link"]

            # Obter apenas o diretório
            diretorio_base = re.sub('([^\\/]{1,})$', '', diretorio_base)

            # Criar uma instância do interpretador
            self.instancia = Interpretador(
                self.bool_logs,
                self.dic_abas[self.num_aba_focada]["lst_breakpoints"],
                bool_ignorar_todos_breakpoints,
                diretorio_base,
                self.dicLetras,
                self.dic_comandos,
                self.idioma,
                dic_regex_compilado=None, re_comandos=self.re_comandos)

            # Remover os comentárioos
            linhas = self.instancia.cortar_comentarios(linhas)

            # Marcar o inicio do interpretador
            inicio = time()

            # iniciar um thread do interpretador
            t = Thread(target=lambda codigoPrograma=linhas: self.instancia.orquestrador_interpretador_(codigoPrograma))
            t.start()

            # Referenciar o terminal
            tx_terminal = self.tx_terminal
            valor_antigo = 0
            p_cor_num = 0

            # Enquanto o interpretador não iniciar
            while self.instancia.numero_threads_ativos != 0 or not self.instancia.boo_orquestrador_iniciado:

                try:
                    # Atualize a interface
                    self.tela.update()
                    self.tx_editor_codigo.update()
                    self.tx_terminal.update()
                except:

                    # Se alguma coisa foi fechada, finalize o interpretador
                    self.instancia.aconteceu_erro = True
                    break

                if tipo_execucao == 'debug':
                    # Marca que chegou até a linha
                    linha_analise = int(self.instancia.num_linha)
                    self.cont_lin1.linha_analise = linha_analise
                    self.cont_lin1.desenhar_linhas() 
                    self.tx_editor_codigo.update()
                    self.tela.update()


                acao = ""
                # Obtem uma instrução do interpretador
                acao = self.instancia.controle_interpretador

                # Se existe uma ação
                if acao != "":
                    valores = None
                    valores = re.search(self.regex_interpretador, acao)

                    # Se a instrução é de exibição na tela
                    if valores is not None:            

                        # Obter instrução
                        # Numero da 
                        instrucao = valores.group(1)
                        linha = valores.group(4)
                        cor = valores.group(3)

                        if instrucao == 'nessaLinha':
                            self.instancia.controle_interpretador = ""

                            try:

                                # Insere o texto e libera o interpretador
                                inicio_cor = float(self.tx_terminal.index("end-1line lineend"))
                                self.tx_terminal.insert(END, linha)

                                # Se era para exibir com alguma cor especial
                                if cor != "":
                                    # Adiciona a cor
                                    fim_cor = float(self.tx_terminal.index("end-1line lineend"))
                                    self.tx_terminal.tag_add("palavra"+str(p_cor_num), inicio_cor, fim_cor)
                                    self.tx_terminal.tag_config("palavra"+str(p_cor_num), foreground=cor)

                                    # Marca onde a cor foi inserida
                                    p_cor_num += 1
                                self.tx_terminal.see('end')


                            except:
                                self.instancia.aconteceu_erro = True
                                break
                        elif instrucao == 'mostreLinha':
                            self.instancia.controle_interpretador = ""

                            try:
                                # Insere  texto
                                inicio_cor = float(self.tx_terminal.index("end-1line lineend"))
                                self.tx_terminal.insert(END, linha + '\n')

                                # Se era para exibir em uma cor
                                if cor != "":

                                    # Exibe nesta cor
                                    fim_cor = float(self.tx_terminal.index("end-1line lineend"))
                                    self.tx_terminal.tag_add("palavra"+str(p_cor_num), inicio_cor, fim_cor)
                                    self.tx_terminal.tag_config("palavra"+str(p_cor_num), foreground=cor)
                                    p_cor_num += 1

                                self.tx_terminal.see('end')

                            except:
                                self.instancia.aconteceu_erro = True
                                break
         

                    elif acao == ':input:':
                        # Obtem como está o código agora
                        textoOriginal = len(self.tx_terminal.get(1.0, END))

                        # Espera o usuário pressionar enter
                        self.esperar_pressionar_enter = True
                        while self.esperar_pressionar_enter:

                            try:
                                self.tela.update()
                                self.tx_editor_codigo.update()
                                self.tx_terminal.update()
                            except:
                                self.instancia.aconteceu_erro = True
                                break

                        # Marca que já foi pressionado enter
                        self.esperar_pressionar_enter = False

                        # Obtem o novo texto com o que o usuário digitou
                        digitado = self.tx_terminal.get(1.0, END)
                        digitado = digitado[textoOriginal - 1:-2]

                        # Atribui o texto
                        self.instancia.texto_digitado = digitado.replace("\n", "")

                        # Libera o interpretador
                        self.instancia.controle_interpretador = ""

                    elif acao == 'limpar_tela':
                        self.instancia.controle_interpretador = ""

                        # Limpa o terminal
                        try:
                            self.tx_terminal.delete('1.0', END)

                            # Atualiza o interpretador para continuar
                            self.instancia.controle_interpretador = ""
                        except Exception as erro:
                            self.instancia.aconteceu_erro = True
                            break


                    elif acao == 'aguardando_breakpoint':
                            # Aguarda o breakpoint ser liberado

                            try:
                                # Marca que chegou até a linha
                                linha_analise = int(self.instancia.num_linha)

                                self.cont_lin1.linha_analise = linha_analise
                                self.cont_lin1.desenhar_linhas() 
                                self.tx_editor_codigo.update()
                                self.tela.update()

                                
                                # Enquanto o breakpoint estiver preso
                                self.libera_breakpoint = False

                                # Enquanto o breakpoint não for liberado
                                while not self.libera_breakpoint:

                                    # Atualiza a tela
                                    self.tx_terminal.update()
                                    self.tx_editor_codigo.update()
                                    self.tela.update()

                                    if self.instancia.aconteceu_erro:
                                        break

                                # Libera o interpretador
                                self.instancia.controle_interpretador = ""

                                # Deixa breakpoint liberado
                                self.libera_breakpoint = False


                            except Exception as erro:
                                self.instancia.aconteceu_erro = True
                                break
                    else:
                        print("Instrução do Interpretador não é reconhecida => '{}'".format(acao))

            if self.instancia.aconteceu_erro:
                # Se o erro foi avisado
                if self.instancia.erro_alertado is True:

                    # Se não foi interrompido
                    if self.instancia.mensagem_erro != "Interrompido":

                        # Se não foi erro ao iniciar
                        if self.instancia.mensagem_erro != "Erro ao iniciar o Interpretador":

                            # Mostre uma mensagem complementar na tela
                            Interface.mostrar_mensagem_de_erro(self, self.instancia.mensagem_erro, self.instancia.dir_script_aju_erro, self.instancia.linha_que_deu_erro)

            else:
                try:
                    self.tx_terminal.insert(END, self.interface_idioma["script_finalizado"][self.idioma].format(time() - inicio))
                    self.tx_terminal.see("end")

                except Exception as erro:
                    print('Impossível exibir mensagem de finalização, erro: '+str(erro))

            self.interpretador_finalizado = True

            # Em modo que não seja debug, finalize o interpretador
            if tipo_execucao == 'continua' or not self.instancia.aconteceu_erro:
                Interface.inicializar_interpretador(self, tipo_execucao = 'parar')

            return 0

    def colocar_linhas_codigo(self, linhas: str) -> str:
        """Adiciona [[numero_linha] no inicio de todas as linhas]

        Args:
            linhas (str): [O código qualquer ]

        Returns:
            str: [O código com o [numero_linha] em todas as linhas]
        """

        nova_linha = ''
        lista = linhas.split('\n')
        for linha in range(len(lista)):
            nova_linha += '[{}]{}\n'.format(str(linha + 1), lista[linha])

        return nova_linha

    def liberar_breakpoint_ou_inicicar(self, tipo_execucao):

        print(self.interpretador_status)

        if self.interpretador_status == 'parado':
            Interface.inicializar_interpretador(self, tipo_execucao='debug')
        else:
            self.libera_breakpoint = True