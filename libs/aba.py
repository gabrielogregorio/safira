import libs.funcoes as funcoes

from tkinter import N
from tkinter import NSEW
from tkinter import Frame
from tkinter import Button
from tkinter import FLAT, PhotoImage
from tkinter import END, Tk


class Aba():
    def __init__(self):
        self.tela = None
        pass

    def atualizar_coloracao_aba(self):
        self.colorir_codigo.aba_focada = self.aba_focada
        self.colorir_codigo.historico_coloracao[self.aba_focada] = []
        self.colorir_codigo.coordena_coloracao(None, tx_codfc = self.tx_codfc)

    def atualiza_texto_tela(self, num_aba):

        self.tx_codfc.delete(1.0, END)
        self.tx_codfc.insert(END, str(self.dic_abas[num_aba]["arquivoAtual"]["texto"])[0:-1])

        nome_arquivo = self.dic_abas[num_aba]["arquivoSalvo"]["link"].split("/")
        nome_arquivo = str(nome_arquivo[-1])

        if nome_arquivo.strip() == "":
            nome_arquivo = " " * 14

        self.dic_abas[num_aba]["listaAbas"][2].configure(text=nome_arquivo)

        for x in range(0, 3):
            self.dic_abas[num_aba]["listaAbas"][x].update()

        Aba.atualizar_coloracao_aba(self)

    def configurar_cor_aba(self, dic_cor_abas, bg_padrao, dic_cor_botao, dic_cor_marcador):
        self.dic_abas[self.aba_focada]["listaAbas"][3].configure(dic_cor_botao)
        self.dic_abas[self.aba_focada]["listaAbas"][3].update()
        self.dic_abas[self.aba_focada]["listaAbas"][2].configure(dic_cor_abas, activebackground = bg_padrao)
        self.dic_abas[self.aba_focada]["listaAbas"][2].update()
        self.dic_abas[self.aba_focada]["listaAbas"][1].configure(dic_cor_marcador)
        self.dic_abas[self.aba_focada]["listaAbas"][1].update()
        self.dic_abas[self.aba_focada]["listaAbas"][0].configure(background = bg_padrao)
        self.dic_abas[self.aba_focada]["listaAbas"][0].update()

    def fecha_aba(self, bt_fechar):
        bool_era_focado = False

        dic_cor_abas = self.dic_design["dic_cor_abas"]
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:

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
                    self.dic_abas[chave]["listaAbas"][3].update()
                    self.dic_abas[chave]["listaAbas"][3].grid_forget()
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
                dic_cor_botao = self.dic_design["dic_cor_abas_focada_botao"]
                dic_cor_marcador = self.dic_design["dic_cor_marcador_focado"]
                self.aba_focada = chave
                self.dic_abas[chave]["foco"] =True

                Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
                Aba.atualiza_texto_tela(self, chave)

                self.lst_historico_abas_focadas.append(chave)
                Aba.atualizar_coloracao_aba(self)
                return 0

    def atualiza_aba_foco(self, num_aba):
        if num_aba == self.aba_focada:
            return 0

        dic_cor_finao = self.dic_design["dic_cor_abas_nao_focada"]
        dic_cor_botao = self.dic_design["dic_cor_abas_nao_focada_botao"]
        dic_cor_marcador = self.dic_design["dic_cor_marcador_nao_focado"]
        Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)

        self.dic_abas[self.aba_focada]["foco"] = False

        dic_cor_finao = self.dic_design["dic_cor_abas_focada"]
        dic_cor_botao = self.dic_design["dic_cor_abas_focada_botao"]
        dic_cor_marcador = self.dic_design["dic_cor_marcador_focado"] 

        self.aba_focada = num_aba
        self.dic_abas[num_aba]["foco"] = True

        self.lst_historico_abas_focadas.append(num_aba)

        Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
        Aba.atualiza_texto_tela(self, num_aba)

        self.colorir_codigo.aba_focada = self.aba_focada
        self.colorir_codigo.historico_coloracao[self.aba_focada] = []
        self.colorir_codigo.coordena_coloracao(None, tx_codfc = self.tx_codfc)

    def nova_aba(self, event=None):

        posicao_adicionar = 0 # Adicionar na posição 0

        if len(self.dic_abas) != 0:
            dic_cor_finao = self.dic_design["dic_cor_abas_nao_focada"] 
            dic_cor_botao = self.dic_design["dic_cor_abas_nao_focada_botao"] 
            dic_cor_marcador = self.dic_design["dic_cor_marcador_nao_focado"] 

            Aba.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
            posicao_adicionar = max(self.dic_abas.keys()) + 1

        self.dic_abas[ posicao_adicionar ] = funcoes.carregar_json("configuracoes/guia.json")

        dic_cor_finao = self.dic_design["dic_cor_abas_focada"] 
        dic_cor_botao = self.dic_design["dic_cor_abas_focada_botao"]
        dic_cor_marcador = self.dic_design["dic_cor_marcador_focado"] 

        fr_uma_aba = Frame(self.fr_abas, background=dic_cor_finao["background"])

        fr_marcador = Frame(fr_uma_aba, dic_cor_marcador)
        lb_aba = Button(fr_uma_aba, dic_cor_finao, text="              ", border=0, highlightthickness=0)
        bt_fechar = Button(fr_uma_aba, dic_cor_botao, text="x ", relief=FLAT, border=0, highlightthickness=0)

        lb_aba.bind('<ButtonPress>', lambda event=None, num_aba = posicao_adicionar: Aba.atualiza_aba_foco(self, num_aba) )
        bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: Aba.fecha_aba(self, bt_fechar) )

        bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: Aba.muda_cor_fecha_botao(self, bt_fechar))
        bt_fechar.bind("<Leave>", lambda event=None, padrao=dic_cor_botao["foreground"], bt_fechar=bt_fechar: Aba.volta_cor_fecha_botao(self, padrao, bt_fechar))

        fr_uma_aba.rowconfigure(1, weight=1)
             
        fr_uma_aba.grid(row=1, column=posicao_adicionar + 2, sticky=N)
        fr_marcador.grid(row=0, column=1,columnspan=2, sticky=NSEW)
        lb_aba.grid(row=1, column=1, sticky=NSEW)
        bt_fechar.grid(row=1, column=2)

        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_uma_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_marcador)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(lb_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(bt_fechar)

        self.aba_focada = posicao_adicionar
        Aba.atualiza_texto_tela(self, self.aba_focada)

    def muda_cor_fecha_botao(self, bt_fechar):
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:
                self.dic_abas[chave]["listaAbas"][3].configure(self.dic_design["dic_cor_abas_botao_fechar_focada"])
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    def volta_cor_fecha_botao(self, padrao, bt_fechar):
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:
                self.dic_abas[chave]["listaAbas"][3].configure(foreground=padrao)
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    def renderizar_abas_inicio(self):
        """
            Usado apenas no inicio do programa *****1 VEZ*****
        """
        for num_aba, dados_aba in self.dic_abas.items():
 
            # Coloração da aba
            if dados_aba["foco"]:
                self.aba_focada = num_aba
                dic_cor_marcador = self.dic_design["dic_cor_marcador_focado"] 
                dic_cor_finao = self.dic_design["dic_cor_abas_focada"]
                dic_cor_botao = self.dic_design["dic_cor_abas_focada_botao"]
            else:
                dic_cor_marcador = self.dic_design["dic_cor_marcador_nao_focado"] 
                dic_cor_finao = self.dic_design["dic_cor_abas_nao_focada"]
                dic_cor_botao = self.dic_design["dic_cor_abas_nao_focada_botao"]

            fr_uma_aba = Frame(self.fr_abas, background = dic_cor_finao["background"])
            fr_uma_aba.rowconfigure(1, weight=1)

            nome_arquivo = str(dados_aba["arquivoSalvo"]["link"]).split("/")
            nome_arquivo = str(nome_arquivo[-1])

            txt_btn = "x "

            if nome_arquivo.strip() == "":
                nome_arquivo = "            "
            else:
                nome_arquivo = " " + nome_arquivo

            fr_marcador = Frame(fr_uma_aba, dic_cor_marcador, padx=100, bd=10)
            lb_aba = Button(fr_uma_aba, dic_cor_finao, text=nome_arquivo, border=0, highlightthickness=0)
            bt_fechar = Button(fr_uma_aba, dic_cor_botao, text=txt_btn, relief=FLAT, border=0, highlightthickness=0)

            bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: Aba.muda_cor_fecha_botao(self, bt_fechar))
            bt_fechar.bind("<Leave>", lambda event=None, padrao=dic_cor_botao["foreground"], bt_fechar=bt_fechar: Aba.volta_cor_fecha_botao(self, padrao, bt_fechar))

            lb_aba.bind('<ButtonPress>', lambda event=None, num_aba = num_aba: Aba.atualiza_aba_foco(self, num_aba) )
            bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: Aba.fecha_aba(self, bt_fechar))

            fr_uma_aba.update()
            fr_marcador.update()
            lb_aba.update()
            bt_fechar.update()

            fr_uma_aba.grid(row=1, column=num_aba + 2, sticky=N)
            fr_marcador.grid(row=0, column=1,columnspan=2, sticky=NSEW)
            lb_aba.grid(row=1, column=1, sticky=NSEW)
            bt_fechar.grid(row=1, column=2)

            self.dic_abas[num_aba]["listaAbas"].append(fr_uma_aba)
            self.dic_abas[num_aba]["listaAbas"].append(fr_marcador)
            self.dic_abas[num_aba]["listaAbas"].append(lb_aba)
            self.dic_abas[num_aba]["listaAbas"].append(bt_fechar)
