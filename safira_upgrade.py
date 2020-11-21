from AtualizarSafira import Upgrade
import os
from datetime import datetime
from tkinter import messagebox

from threading import Thread

from tkinter import Frame
from tkinter import Label
from tkinter import Label
from tkinter import NSEW, EW, Text, END
from tkinter import Tk
from time import sleep

from tkinter import Toplevel, FLAT
from tkinter import Label, Scrollbar
from tkinter import Frame, NE
from tkinter import Button
from tkinter import GROOVE, GROOVE, NSEW
from tkinter import PhotoImage
from tkinter import Tk
import util.funcoes as funcoes 
from design import Design 

VERSAO_ATUAL = {"versao": 0.29}

class Updgrade():
    def __init__(self, frame, design, idioma, interface_idioma, icon):
        #frame.withdraw()

        self.icon = icon
        self.idioma = idioma
        self.interface_idioma = interface_idioma
        self.design = design
        self.frame = frame
        self.linha = 2
        self.icone = None
        self.fr_ic_versao = None
        self.frb = None
        self.fr1 = None
        self.fr2 = None
        self.fr_bts = None
        self.fr3 = None

        self.tx_logs = None
        self.bt_voltar = None
        self.bt_atualizar = None

        data = str(datetime.now()).split('.')[0]
        data = data.replace(' ', '-')
        data = data.replace(':', '-')

        # Destino dos Downloads e Backups
        dest_download = os.path.join(os.getcwd(), 'AtualizarSafira')
        dest_backup = os.path.join(os.getcwd(), 'backups' , data)

        self.up = Upgrade.Upgrade(dest_download, dest_backup)
        dic_versoes = self.up.obter_informacoes_versao()

        if dic_versoes.get('erro'):
            print(dic_versoes['erro'])
            self.frame.destroy()
            messagebox.showinfo("Erro ao buscar versões", "Aconteceu um erro quando a Safira tentou buscar as versões disponíveis. Este foi o erro: {}".format(dic_versoes['erro']))
        else:
            nova = max(dic_versoes.keys())
            if float(VERSAO_ATUAL["versao"]) < float(nova):
                print('A versão {} disponível, deseja atualizar?'.format(nova))


    def thread_baixar_versao(self, versao):
        th = Thread(target=lambda v=versao: self.baixar_versao(v))
        th.start()

    def log(self, msg):
        print(msg)
        self.tx_logs.insert(END, msg + '\n')

    def baixar_versao(self, versao):
        self.tx_logs.delete(1.0, END)
        self.fr_bts.destroy()

        self.log("Tentando baixar a versão {}".format(versao))

        atualizar = self.up.baixar_versao(versao)
        sucesso, msg, arquivo = atualizar

        # Baixou com sucesso
        if sucesso:
            self.log(msg)
            self.log("Extraindo versão na pasta: {}".format(self.up.dest_download))

            # Extraiu com sucesso
            sucesso, msg = self.up.extrair_versao(arquivo)
            if sucesso:
                self.log(msg)
                self.log("Fazendo Backup da versão atual")


                # Backup da versão atual
                sucesso_bkup, msg_bpk = self.up.fazer_backup_versao()
                if sucesso_bkup:
                    self.log(msg_bpk)
                    self.log("Sobrescrevendo a versão atual")

                    # Atualizar a versão
                    pp, msg_atualizar = self.atualizar_arquivos(versao)
                    if sucesso_atualizar:
                        print(msg_atualizar)
                        print("Versão atualizada com sucesso, feche tudo e tente novamente para usar a Safira")
                       

                    else:
                        print("******** ERRO ********")
                        print(msg_atualizar)

                        print("Tentando Restaurar a versão!")
                        sucesso_restaurar, msg_restaurar = self.restaurar_versao()

                        print(sucesso_restaurar[1])
                else:
                    self.log(msg_bpk)
            else:
                self.log(msg)
        else:
            self.log(msg)

    def fechar_janela(self, inst):
        inst.withdraw()
        inst.destroy()

if __name__ == '__main__':
    master = Tk()
    master.rowconfigure(1, weight=1)
    master.grid_columnconfigure(1, weight=1)
    #master.overrideredirect(1)

    design = Design()
    design.update_design_dic()

    # Configurações da IDE
    arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

    # Idioma que a safira está configurada
    idioma = arquivo_configuracoes['idioma']
    interface_idioma = funcoes.carregar_json("configuracoes/interface.json")

    icon = PhotoImage(file='imagens/icone.png')
    fr = Frame(master, width=100, height=100, bg='blue')
    fr.grid(row=1, column=1, sticky=NSEW)
    fr.grid_columnconfigure(1, weight=1)


    _ = Updgrade(fr, design, idioma, interface_idioma, icon)

    #idioma = Idioma()
    

    master.mainloop()
