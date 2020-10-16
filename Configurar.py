    def carregar_dicionario_letra(dic_comandos:dict) -> dict:
        """

        """
        dic_letras = {}

        # Anda por todos os comandos
        for k, v in dic_comandos.items():

            # Cria uma lista pela chave de cada comando
            dic_letras[k] = []

            # Para cada subcomando
            for valor in v["comando"]:

                # Pega a primeira letra do subcomando
                valor = valor[0].strip()

                # Adiona no dicionário a primeira letra do comando
                if valor == "":
                    dic_letras[k].append(valor)
                else:
                    valor = valor.lower()

                    if valor[0] not in dic_letras[k]:
                        dic_letras[k].append(valor[0])
        return dic_letras


    def gerar_regex_compilado_interpretador(self) -> None:
        print("Inicializador do orquestrador iniciado")
        diretorio_base = ''
        bool_ignorar_todos_breakpoints = True
        bool_logs = False


        instancia = Interpretador(
            bool_logs,
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"],
            bool_ignorar_todos_breakpoints,
            diretorio_base,
            self.dicLetras,
            self.dic_comandos,
            self.idioma,
            dic_regex_compilado=self.dic_regex_compilado,
            re_comandos = self.re_comandos)

        self.dic_regex_compilado = instancia.dic_regex_compilado
        self.re_comandos = instancia.re_comandos 
        del instancia

