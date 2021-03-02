from tkinter import Toplevel
from tkinter import messagebox
from tkinter import Frame
from tkinter import Button
from tkinter import Message
from tkinter import Label
from tkinter import FLAT
from tkinter import NSEW
from webbrowser import open as webbrowser_open
from threading import Thread
from datetime import datetime
from os import path as os_path
from os import getcwd as os_getcwd
from upgrade import Upgrade

VERSAO_ATUAL = {"versao": 0.35}


class Atualizar():
    def __init__(self):

        # Destino dos Downloads e Backups
        self.__tp_atualizacao = None
        data = str(datetime.now()).split('.')[0]
        data = data.replace(' ', '-')
        data = data.replace(':', '-')

        dest_download = os_path.join(os_getcwd(), 'AtualizarSafira')
        dest_backup = os_path.join(os_getcwd(), 'backups' , data)

        # Instância de Upgrades
        self.__up = Upgrade.Upgrade(dest_download, dest_backup)


    def verificar_atualizacoes(self, primeira_vez=False):
        """Verifica se existe uma versão mais recente disponível """
        try:
            baixada = VERSAO_ATUAL

            # Obter todas as versões
            dic_versoes = self.__up.obter_informacoes_versao()

            if dic_versoes.get('erro'):
                print(dic_versoes['erro'])

                messagebox.showinfo("Erro ao buscar versões", "Aconteceu um erro quando a Safira tentou buscar as versões disponíveis. Este foi o erro: {}".format(dic_versoes['erro']))
            else:
                # Obter ultima versão
                recente = max(dic_versoes.keys())
                if float(VERSAO_ATUAL["versao"]) < float(recente):

                    print('A versão {} disponível, deseja atualizar?'.format(recente))
                    self.__aviso_versao(baixada, recente)

                else:
                    # Não é necessário avisar que está atualizado
                    # Se a interface estiver iniciando
                    if not primeira_vez:
                        self.__aviso_versao_atualizada(baixada)

        except Exception as erro:
            if not primeira_vez:
                messagebox.showinfo("ops", self.interface_idioma["erro_generico"][self.idioma] + str(erro))

    def __aviso_versao(self, baixada, recente):
        """ Aviso, existe uma nova versão disponível """

        self.__tp_atualizacao = Toplevel(self.master, self.design.dic["aviso_versao_top_level"])
        self.__tp_atualizacao.withdraw()
        self.__tp_atualizacao.focus_force()
        self.__tp_atualizacao.resizable(False, False)
        self.__tp_atualizacao.tk.call('wm', 'iconphoto', self.__tp_atualizacao._w, self.icon)
        self.__tp_atualizacao.grid_columnconfigure(1, weight=1)
        self.__tp_atualizacao.title(self.interface_idioma["titulo_aviso_atualizacao"][self.idioma])

        # Objetos da interface
        fr_atualizaca = Frame(self.__tp_atualizacao)
        lb_versao_dev = Label(fr_atualizaca, text=self.interface_idioma["versao_nova_disponivel"][self.idioma])
        lb_versao_tex = Message(fr_atualizaca, text='{}'.format(self.interface_idioma["texto_update_disponivel"][self.idioma]).format(recente))
        fr_botoes = Frame(fr_atualizaca)

        bt_cancela = Button(fr_botoes, text=self.interface_idioma["versao_nao_quero"][self.idioma])
        bt_atualiza = Button(fr_botoes, text=self.interface_idioma["atualizar_agora"][self.idioma])

        # Configurações de desingn
        fr_atualizaca.configure(self.design.dic["aviso_versao_fr_atualizacao"])
        lb_versao_dev.configure(self.design.dic["aviso_versao_lb_dev"])
        lb_versao_tex.configure(self.design.dic["aviso_versao_ms"])
        fr_botoes.configure(self.design.dic["aviso_versao_btn"])
        bt_cancela.configure(self.design.dic["aviso_versao_btn_cancela"], relief=FLAT)
        bt_atualiza.configure(self.design.dic["aviso_versao_btn_atualiza"], relief=FLAT)

        # Eventos
        bt_atualiza.configure(command=lambda rec=recente: self.__aviso_aguarde_instalando(rec))
        bt_cancela.configure(command=lambda event=None: self.__tp_atualizacao.destroy())

        # Posicionamento de itens
        fr_atualizaca.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(2, weight=1)
        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_versao_dev.grid(row=1, column=1)
        lb_versao_tex.grid(row=2, column=1, sticky=NSEW)
        fr_botoes.grid(row=3, column=1, sticky=NSEW)
        bt_cancela.grid(row=1, column=1)
        bt_atualiza.grid(row=1, column=2)

        # Posicionando a tela
        j_width = self.__tp_atualizacao.winfo_reqwidth()
        j_height = self.__tp_atualizacao.winfo_reqheight()
        t_width = self.master.winfo_screenwidth()
        t_heigth = self.master.winfo_screenheight()

        self.__tp_atualizacao.geometry("+{}+{}".format(int(t_width/2)-int(j_width/2), int(t_heigth/2)-int(j_height/2)))
        self.__tp_atualizacao.deiconify()
        self.__tp_atualizacao.update()


    def __aviso_aguarde_instalando(self, recente):
        """ Realizando a atualização """

        if self.__tp_atualizacao is not None:
            self.__tp_atualizacao.destroy()

        self.__tp_atualizacao = Toplevel(None)
        self.__tp_atualizacao.withdraw()
        self.__tp_atualizacao.focus_force()
        self.__tp_atualizacao.resizable(False, False)
        self.__tp_atualizacao.tk.call('wm', 'iconphoto', self.__tp_atualizacao._w, self.icon)
        self.__tp_atualizacao.configure(self.design.dic["aviso_versao_top_level"])
        self.__tp_atualizacao.grid_columnconfigure(1, weight=1)
        self.__tp_atualizacao.title('Atualizando.... Não feche a Safira!')

        fr_atualizaca = Frame(self.__tp_atualizacao)
        lb_versao_dev = Label(fr_atualizaca, text= '{:^30}'.format('Aguarde Atualizando!'))
        lb_versao_tex = Message(fr_atualizaca, text=' '*50, width=200)
        fr_botoes = Frame(fr_atualizaca)
        bt_atualiza = Button(fr_botoes)

        fr_atualizaca.configure(self.design.dic["aviso_versao_fr_atualizacao"])
        lb_versao_dev.configure(self.design.dic["aviso_versao_lb_dev"])
        lb_versao_tex.configure(self.design.dic["aviso_versao_ms"])
        fr_botoes.configure(self.design.dic["aviso_versao_btn"])
        bt_atualiza.configure(self.design.dic["aviso_versao_btn_atualiza"], relief=FLAT)

        fr_atualizaca.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(2, weight=1)
        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_versao_dev.grid(row=1, column=1)
        lb_versao_tex.grid(row=2, column=1, sticky=NSEW)
        fr_botoes.grid(row=3, column=1, sticky=NSEW)
        
        j_width = self.__tp_atualizacao.winfo_reqwidth()
        j_height = self.__tp_atualizacao.winfo_reqheight()
        t_width = self.master.winfo_screenwidth()
        t_heigth = self.master.winfo_screenheight()

        self.__tp_atualizacao.geometry("+{}+{}".format(int(t_width/2)-int(j_width/2), int(t_heigth/2)-int(j_height/2)))
        self.__tp_atualizacao.deiconify()
        self.__tp_atualizacao.update()

        th = Thread(target=lambda ver=recente, lb = lb_versao_tex, bt_at=bt_atualiza, lb_2=lb_versao_dev: self.__aplica_versao(ver, lb, bt_at, lb_2))
        th.start()

    def __log(self, label, texto):
        label['text'] = label['text'] + '\n{}'.format(texto)

    def __aplica_versao(self, versao, lb_versao_tex, bt_atualiza, lb_versao_dev):
        """Baixa, faz o download e atualiza a Safira"""

        self.__log(lb_versao_tex, "Baixando Versão {}".format(versao))

        atualizar = self.__up.baixar_versao(versao)
        sucesso, msg, arquivo = atualizar

        # Baixou com sucesso
        if sucesso:
            self.__log(lb_versao_tex, msg)
            self.__log(lb_versao_tex, "Extraindo: {}".format(self.__up.dest_download))

            # Extraiu com sucesso
            sucesso, msg = self.__up.extrair_versao(arquivo)
            if sucesso:
                self.__log(lb_versao_tex, msg)
                self.__log(lb_versao_tex, "Fazendo Backup")

                # Backup da versão atual
                sucesso_bkup, msg_bpk = self.__up.fazer_backup_versao()
                if sucesso_bkup:
                    self.__log(lb_versao_tex, msg_bpk)
                    self.__log(lb_versao_tex, "Atualizando Versão")

                    # Atualizar a versão
                    sucesso_atualizar, msg_atualizar = self.up.atualizar_arquivos(versao)
                    if sucesso_atualizar:
                        self.__log(lb_versao_tex, msg_atualizar)
                        self.__log(lb_versao_tex, "Sucesso!")

                        lb_versao_dev.configure(text='{:^30}'.format('Atualizado com sucesso!'), fg='green')
                        self.__tp_atualizacao.title('Safira Atualizada!')

                    else:
                        self.__log(lb_versao_tex, msg_atualizar)
                        self.__log(lb_versao_tex, "\nRestaurando")

                        sucesso_restaurar, msg_restaurar = self.up.restaurar_versao()

                        self.__log(lb_versao_tex, sucesso_restaurar[1])
                        lb_versao_dev.configure(text='{:^30}'.format(sucesso_restaurar[1]), fg='orange')
                        self.__tp_atualizacao.title('Safira Não Atualizada!')

                else:
                    self.__log(lb_versao_tex, msg_bpk)

                    lb_versao_dev.configure(text='{:^30}'.format('Erro ao fazer Backup'), fg='orange')
                    self.__tp_atualizacao.title('Safira Não Atualizada!')

            else:
                self.__log(lb_versao_tex, msg)

                lb_versao_dev.configure(text='{:^30}'.format('Erro ao Extrair os arquivos'), fg='orange')
                self.__tp_atualizacao.title('Safira Não Atualizada!')

        else:
            self.__log(lb_versao_tex, msg)

            lb_versao_dev.configure(text='{:^30}'.format('Erro ao fazer Baixar Safira'), fg='orange')
            self.__tp_atualizacao.title('Safira Não Atualizada!')

        bt_atualiza.configure(command=lambda event=None: self.__fechar_tudo())
        
        bt_atualiza['text'] = 'Reinicie a Safira!'
        bt_atualiza.grid(row=1, column=2)

    def __fechar_tudo(self):
        self.master.destroy()

    def __abrir_site(self, url):
        self.__tp_atualizacao.destroy()

        th = Thread(target=lambda url=url: webbrowser_open(url))
        th.start()

    def __aviso_versao_atualizada(self, baixada):
        self.__tp_atualizacao = Toplevel(self.master, self.design.dic["aviso_versao_tp_atualizada"])
        self.__tp_atualizacao.withdraw()
        self.__tp_atualizacao.focus_force()
        self.__tp_atualizacao.resizable(False, False)
        self.__tp_atualizacao.tk.call('wm', 'iconphoto', self.__tp_atualizacao._w, self.icon)
        self.__tp_atualizacao.grid_columnconfigure(1, weight=1)

        j_width = self.__tp_atualizacao.winfo_reqwidth()
        j_height = self.__tp_atualizacao.winfo_reqheight()
        t_width = self.master.winfo_screenwidth()
        t_heigth = self.master.winfo_screenheight()

        self.__tp_atualizacao.title(self.interface_idioma["titulo_aviso_atualizado"][self.idioma])

        fr_atualizaca = Frame(self.__tp_atualizacao)
        lb_versao_dev = Label(fr_atualizaca, text=self.interface_idioma["atualizado_versao_ultima"][self.idioma])
        lb_versao_tex = Message(fr_atualizaca, text='{}'.format(self.interface_idioma["texto_atualizado"][self.idioma]).format(baixada["versao"]), relief=FLAT)
        fr_botoes = Frame(fr_atualizaca)
        bt_cancela = Button(fr_botoes, text=self.interface_idioma["texto_nao_quero"][self.idioma], relief=FLAT)
        bt_facebook = Button(fr_botoes, self.design.dic["aviso_versao_bt_facebook_atualizada"], text=self.interface_idioma["atualizado_facebook"][self.idioma], relief=FLAT)
        bt_blogger_ = Button(fr_botoes, self.design.dic["aviso_versao_bt_blog_atualizada"], text=self.interface_idioma["atualizado_blog"][self.idioma], relief=FLAT)
        
        # Configurações de desingn
        fr_atualizaca.configure(self.design.dic["aviso_versao_fr_atualizacao"])
        lb_versao_dev.configure(self.design.dic["aviso_versao_lb_dev"])
        lb_versao_tex.configure(self.design.dic["aviso_versao_ms"])
        fr_botoes.configure(self.design.dic["aviso_versao_btn"])
        bt_cancela.configure(self.design.dic["aviso_versao_btn_cancela"], relief=FLAT)

        bt_cancela.configure(command=lambda event=None: self.__tp_atualizacao.destroy())
        bt_facebook.configure(command=lambda event=None: self.__abrir_site("https://www.facebook.com/safiralang/"))
        bt_blogger_.configure(command=lambda event=None: self.__abrir_site("https://safiralang.blogspot.com/"))

        fr_atualizaca.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(2, weight=1)
        fr_botoes.grid_columnconfigure(3, weight=1)

        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_versao_dev.grid(row=1, column=1)
        lb_versao_tex.grid(row=2, column=1, sticky=NSEW)
        fr_botoes.grid(row=3, column=1, sticky=NSEW)
        bt_cancela.grid(row=1, column=1)
        bt_facebook.grid(row=1, column=2)
        bt_blogger_.grid(row=1, column=3)

        x, y = int(t_width/2)-int(j_width/2), int(t_heigth/2)-int(j_height/2)

        self.__tp_atualizacao.geometry("+{}+{}".format(x, y))
        self.__tp_atualizacao.update()
        self.__tp_atualizacao.deiconify()
