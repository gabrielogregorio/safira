import libs.funcoes as funcoes
from tkinter import N
from tkinter import NSEW
from tkinter import Frame
from tkinter import Button
from tkinter import FLAT
from tkinter import END

class Aba():
    def atualiza_texto_tela(self, num_aba):

        self.tx_codfc.delete(1.0, END)
        self.tx_codfc.insert(END, str(self.dic_abas[num_aba]["arquivoAtual"]["texto"])[0:-1])
        self.colorir_codigo.coordena_coloracao(None, tx_codfc = self.tx_codfc)

        nome_arquivo = self.dic_abas[num_aba]["arquivoSalvo"]["link"].split("/")
        nome_arquivo = str(nome_arquivo[-1])

        if nome_arquivo.strip() == "":
            nome_arquivo = " " * 8

        self.dic_abas[num_aba]["listaAbas"][1].configure(text=nome_arquivo)

        for x in range(0, 3):
            self.dic_abas[num_aba]["listaAbas"][x].update()

    def configurar_cor_aba(self, dic_cor_abas, bg_padrao):
        self.dic_abas[self.aba_focada]["listaAbas"][2].configure(dic_cor_abas, activebackground = bg_padrao)
        self.dic_abas[self.aba_focada]["listaAbas"][2].update()
        self.dic_abas[self.aba_focada]["listaAbas"][1].configure(dic_cor_abas, activebackground = bg_padrao)
        self.dic_abas[self.aba_focada]["listaAbas"][1].update()
        self.dic_abas[self.aba_focada]["listaAbas"][0].configure(background = bg_padrao, height=20)
        self.dic_abas[self.aba_focada]["listaAbas"][0].update()

    def fecha_aba(self, bt_fechar):
        bool_era_focado = False

        dic_cor_abas = self.dic_design["dic_cor_abas"]
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][2] == bt_fechar:

                while chave in self.lst_historico_abas_focadas:
                    self.lst_historico_abas_focadas.remove(chave)

                if len(self.dic_abas) == 1:
                    self.dic_abas[chave]["nome"] =""
                    self.dic_abas[chave]["lst_breakpoints"] = []
                    self.dic_abas[chave]["arquivoSalvo"] = {"link": "","texto": ""}
                    self.dic_abas[chave]["arquivoAtual"] = {"texto": ""}

                    Aba.atualiza_texto_tela(self, chave)
                    self.lst_historico_abas_focadas.append(chave)
                    return 0

                else:
                    self.dic_abas[chave]["listaAbas"][2].update()
                    self.dic_abas[chave]["listaAbas"][2].grid_forget()
                    self.dic_abas[chave]["listaAbas"][1].update()
                    self.dic_abas[chave]["listaAbas"][1].grid_forget()
                    self.dic_abas[chave]["listaAbas"][0].update()
                    self.dic_abas[chave]["listaAbas"][0].grid_forget()

                    if self.dic_abas[chave]["foco"] == True:
                        bool_era_focado = True
                    del self.dic_abas[chave]
                    break

        if bool_era_focado: # Aba fechada era a focada

                try:
                    chave = self.lst_historico_abas_focadas[-1]
                except:
                    for k, valor in self.dic_abas.items():
                        chave = k
                        break
    
                dic_cor_finao = self.dic_design["dic_cor_abas_focada"]
                self.aba_focada = chave
                self.dic_abas[chave]["foco"] =True

                Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"])
                Aba.atualiza_texto_tela(self, chave)

                self.lst_historico_abas_focadas.append(chave)
                return 0

    def atualiza_aba_foco(self, num_aba):
        if num_aba == self.aba_focada:
            return 0

        dic_cor_finao = self.dic_design["dic_cor_abas_nao_focada"]
        Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"])

        self.dic_abas[self.aba_focada]["foco"] = False

        dic_cor_finao = self.dic_design["dic_cor_abas_focada"]
        self.aba_focada = num_aba
        self.dic_abas[num_aba]["foco"] = True

        self.lst_historico_abas_focadas.append(num_aba)

        Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"])
        Aba.atualiza_texto_tela(self, num_aba)

    def nova_aba(self, event=None):

        posicao_adicionar = 0 # Adicionar na posição 0

        if len(self.dic_abas) != 0:
            dic_cor_finao = self.dic_design["dic_cor_abas_nao_focada"] 

            Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"])
            posicao_adicionar = max(self.dic_abas.keys()) + 1

        self.dic_abas[ posicao_adicionar ] = funcoes.carregar_json("configuracoes/guia.json")

        dic_cor_finao = self.dic_design["dic_cor_abas_focada"] 

        fr_uma_aba = Frame(self.fr_abas, height=20, background=dic_cor_finao["background"])
        lb_aba = Button(fr_uma_aba, dic_cor_finao, text="     ", border=0, highlightthickness=0, padx=8, font = ("Lucida Sans", 13))
        bt_fechar = Button(fr_uma_aba, dic_cor_finao, text="x ", relief=FLAT, border=0, highlightthickness=0, font = ("Lucida Sans", 13))

        lb_aba['command'] = lambda num_aba = posicao_adicionar: Aba.atualiza_aba_foco(self, num_aba)
        bt_fechar['command'] = lambda bt_fechar=bt_fechar: Aba.fecha_aba(self, bt_fechar)

        fr_uma_aba.rowconfigure(1, weight=1)
             
        fr_uma_aba.grid(row=1, column=posicao_adicionar + 2, sticky=N)
        lb_aba.grid(row=1, column=1, sticky=NSEW)
        bt_fechar.grid(row=1, column=2)

        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_uma_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(lb_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(bt_fechar)

        self.aba_focada = posicao_adicionar
        Aba.atualiza_texto_tela(self, self.aba_focada)

    def renderizar_abas_inicio(self):
        """
            Usado apenas no inicio do programa *****1 VEZ*****
        """
        for num_aba, dados_aba in self.dic_abas.items():
 
            # Coloração da aba
            if dados_aba["foco"]:
                self.aba_focada = num_aba
                dic_cor_finao = self.dic_design["dic_cor_abas_focada"]
            else:
                dic_cor_finao = self.dic_design["dic_cor_abas_nao_focada"]

            fr_uma_aba = Frame(self.fr_abas, background = dic_cor_finao["background"], height=20)
            fr_uma_aba.rowconfigure(1, weight=1)

            nome_arquivo = str(dados_aba["arquivoSalvo"]["link"]).split("/")
            nome_arquivo = str(nome_arquivo[-1])

            if dados_aba["arquivoSalvo"]["texto"] != dados_aba["arquivoAtual"]["texto"]:
                txt_btn = "* "
            else:
                txt_btn = "x "

            if nome_arquivo.strip() == "":
                nome_arquivo = "      "
            else:
                nome_arquivo = " " + nome_arquivo

            lb_aba = Button(fr_uma_aba, dic_cor_finao, text=nome_arquivo, border=0, highlightthickness=0, padx=8, font = ("Lucida Sans", 13))
            bt_fechar = Button(fr_uma_aba, dic_cor_finao, text=txt_btn, relief=FLAT, border=0, highlightthickness=0, font = ("Lucida Sans", 13))
     
            fr_uma_aba.update()
            lb_aba.update()
            bt_fechar.update()

            fr_uma_aba.grid(row=1, column=num_aba + 2, sticky=N)
            lb_aba.grid(row=1, column=1, sticky=NSEW)
            bt_fechar.grid(row=1, column=2)

            lb_aba['command'] = lambda num_aba = num_aba: Aba.atualiza_aba_foco(self, num_aba)
            bt_fechar['command'] = lambda bt_fechar=bt_fechar: Aba.fecha_aba(self, bt_fechar)

            self.dic_abas[num_aba]["listaAbas"].append(fr_uma_aba)
            self.dic_abas[num_aba]["listaAbas"].append(lb_aba)
            self.dic_abas[num_aba]["listaAbas"].append(bt_fechar)
