from tkinter import Canvas
from tkinter import Text


class ContadorLinhas(Canvas):
    def __init__(self, frame, design, bool_tem_linha):
        Canvas.__init__(self, frame)

        self.textwidget = None
        self.linha_analise = 0
        self.design = design
        self.bool_tem_linha = bool_tem_linha

    def atribuir(self, tx_editor_codigo):
        self.textwidget = tx_editor_codigo

    def desenhar_linhas(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break

            y = dline[1]
            num_linha = str(i).split(".")[0].strip()
            cor_padrao = "#777777"

            if int(num_linha) == self.linha_analise and not int(num_linha) in self.dic_abas2[self.aba_focada2]["lst_breakpoints"]:
                if not self.bool_tem_linha:
                    num_linha = ">   "
                    cor_padrao = "#7dff63"
                else:
                    num_linha = " " + num_linha + " "

            elif int(num_linha) == self.linha_analise and int(num_linha) in self.dic_abas2[self.aba_focada2]["lst_breakpoints"]:
                if not self.bool_tem_linha:
                    num_linha = " *> "
                    cor_padrao = "#7aff95"
                else:
                    num_linha = " " + num_linha + " "

            elif int(num_linha) in self.dic_abas2[self.aba_focada2]["lst_breakpoints"]:
                if not self.bool_tem_linha:
                    num_linha = " * "
                    cor_padrao = "#ff7a95"
                else:
                    num_linha = " " + num_linha + "  "
            else:
                if not self.bool_tem_linha:
                    num_linha = "  "
                else:
                    num_linha = " " + num_linha + "  "

            self.create_text(2, y, anchor="nw", text=num_linha, font=self.design.dic["fonte_ct_linha"]["font"],  fill=cor_padrao)
            i = self.textwidget.index("{}+1line".format(i))



class EditorDeCodigo(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)

            if (args[0] in ("insert", "replace", "delete") or args[0:3] == ("mark", "set", "insert") or args[0:2] == ("xview", "moveto") or args[0:2] == ("xview", "scroll") or args[0:2] == ("yview", "moveto") or args[0:2] == ("yview", "scroll")):
                self.event_generate("<<Change>>", when="tail")

            return result
        except Exception as erro:
            return str(erro)
