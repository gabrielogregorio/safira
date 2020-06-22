from tkinter import filedialog
from tkinter import messagebox
from tkinter import END

import libs.funcoes as funcoes


class Arquivo():
    def __init__(self, dic_abas, aba_focada, tx_codfc):
        self.dic_abas = dic_abas
        self.aba_focada = aba_focada
        self.tx_codfc = tx_codfc

    def atualiza_infos(self, dic_abas, aba_focada, tx_codfc):
        self.dic_abas = dic_abas
        self.aba_focada = aba_focada
        self.tx_codfc = tx_codfc

    def salvar_arquivo_como_dialog(self, event=None):
        arq = filedialog.asksaveasfile(
            mode='w',
            defaultextension=".safira",
            title="Selecione o script",
            filetypes=(("Meus scripts", "*.safira"), ("all files", "*.*")))

        if arq is None:
            return None

        lnk_arquivo_salvar = str(arq.name)

        arq.close()

        text2save = str(self.tx_codfc.get(1.0, END))
        try:
            arq = open(lnk_arquivo_salvar, 'w', encoding='utf8')
            arq.write(text2save)
            arq.close()

        except Exception as erro:
            messagebox.showinfo(
                'Erro', 'Erro ao salvar programa, erro: {}'.format(erro))

        else:
            self.dic_abas[self.aba_focada]["arquivoSalvo"]['link'] = arq.name
            self.dic_abas[self.aba_focada]["arquivoSalvo"]['texto'] = text2save
            self.dic_abas[self.aba_focada]["arquivoAtual"]['texto'] = text2save

            return arq.name

    def salvar_arquivo(self, event=None):
        if self.dic_abas[self.aba_focada]["arquivoSalvo"]['link'] == "":
            Arquivo.salvar_arquivo_como_dialog(self)
            return "salvar_arquivo_como_dialog"

        else:
            programaCodigo = self.tx_codfc.get(1.0, END)

            if self.dic_abas[self.aba_focada]["arquivoSalvo"]['texto'] == programaCodigo:
                print("Não sofreu modificações")

            else:
                try:
                    funcoes.salvar_arquivo(
                        arquivo=self.dic_abas[self.aba_focada]["arquivoSalvo"]['link'],
                        texto=programaCodigo)

                except Exception as erro:
                    messagebox.showinfo(
                        'Erro',
                        'Impossivel salvar essa verso, erro: {}'.format(erro))

                else:
                    self.dic_abas[self.aba_focada]["arquivoSalvo"]['texto'] = programaCodigo
                    self.dic_abas[self.aba_focada]["arquivoAtual"]['texto'] = programaCodigo
        return None  

    def salvar_arquivo_dialog(self, event=None):

        arq_tips = [('Scripts Safira', '*.safira'), ('Todos os arquivos', '*')]
        arq_dial = filedialog.Open(filetypes=arq_tips)
        arq_nome = arq_dial.show()

        if arq_nome == () :
            print(' Nenhum arquivo escolhido')
            return 0

        else:
            print(' Arquivo "{}" escolhido'.format(arq_nome))
            arq_txts = funcoes.abrir_arquivo(arq_nome)

            if arq_txts[0] is not None:
                self.tx_codfc.delete(1.0, END)
                self.tx_codfc.insert(END, arq_txts[0][0:-1])

            else:
                messagebox.showinfo(
                    "ops",
                    "Aconteceu um erro ao abrir o arquivo" + arq_txts[1])

            self.dic_abas[self.aba_focada]["arquivoSalvo"]['link'] = arq_nome
            self.dic_abas[self.aba_focada]["arquivoSalvo"]['texto'] = arq_txts[0]
            self.dic_abas[self.aba_focada]["arquivoAtual"]['texto'] = arq_txts[0]

    def abrirArquivo(self, link):
        print(' Abrindo arquivo "{}" escolhido'.format(link))

        arq = funcoes.abrir_arquivo(link)

        if arq[0] is not None:
            self.tx_codfc.delete(1.0, END)
            self.tx_codfc.insert(END, arq[0][0:-1])

            self.dic_abas[self.aba_focada]["arquivoSalvo"]['link'] = link
            self.dic_abas[self.aba_focada]["arquivoSalvo"]['texto'] = arq[0]
            self.dic_abas[self.aba_focada]["arquivoAtual"]['texto'] = arq[0]

        else:
            if "\'utf-8' codec can\'t decode byte" in arq[1]:
                messagebox.showinfo(
                    "Erro de codificação",
                    'Converta  para UTF-8. arquivo: "{}", erro: "{}"'.format(
                        link,
                        arq[1]))
            else:
                messagebox.showinfo(
                    'Erro',
                    'Error ao abrir o script: {}, erro: {}'.format(
                        link,
                        arq[1]))

            print('Arquivo não selecionado')
