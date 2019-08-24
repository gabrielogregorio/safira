from tkinter import filedialog
from tkinter import *
tela = Tk()
tela.title('Linguagem ec beta 0.1')

from PIL import ImageTk, Image
tela.call('wm', 'iconphoto', tela._w, ImageTk.PhotoImage(Image.open('icone.gif')))

tela.configure(bg='#343434')

global btn_ativado # Botão compilar clicado
global aconteceu   # Caso o print(' para colocar ')
global filename    # Arquivo
global programa    # Novo código
global text        # Texto do arquivo
global st          # Text orincipal
global p

aconteceu = [False,'']
btn_ativado = True
filename = ''
programa = ''
st = ''
p = 0


def log(texto):
    global st
    st.insert(END,str(texto)+"\n")
    st.see("end")
    st.update()

def IniciarCompilador():
    global s
    log('compilador iniciado')
    log('abrindo programa em altissimo nível')
    try:
        a = open('programa.ec','r',encoding="utf8")
        s = a.read() + ' '
        a.close()
    except:
        log('[--] Erro ao abrir programa')
    return s


def substitui(valor,por):
    global aconteceu
    global p
    global programa
    if valor == s[p:p+len(valor)]:
        programa += por
        p += len(valor)
        aconteceu = [True,por]

def troca(p,s):
    substitui('vale','=')
    substitui('recebe','=')

    substitui('enquanto','while')

    substitui(' e ',' and ')
    substitui(' ou ',' or ')
    substitui('for diferente de','!=')

    substitui('for diferente de','!=')
    substitui('for menor que','<')
    substitui('for maior que','>')
    substitui('for igual a','==')

    substitui('exiba nessa linha','print( ')
    substitui('exiba','print(')
    substitui('mostre nessa linha ','print( ')
    substitui('mostre','print(')

    substitui('senao','else: ')
    substitui('se ','if ')
    substitui('digitado','input()')

def Iniciar():
    log('Convertendo para linguagem de alto nível')
    global aconteceu
    global programa
    global s
    global p

    while p < len(s):
        # troca valores
        troca(p , len(s))

        # se não aconteceu nada
        if aconteceu[0] == False:
            programa += s[p]
            p += 1

        elif aconteceu[1] == 'print(':
           inicio = s[ p : p+s[p:].find('\n')+1]
           inicio = inicio.replace('\n',')\n')
           s = s[:p] + inicio + s[p+s[p:].find('\n')+1:]

        elif aconteceu[1] == 'print( ':
           inicio = s[ p : p+s[p:].find('\n')+1]
           inicio = inicio.replace('\n',',end=" ")\n')
           s = s[:p] + inicio + s[p+s[p:].find('\n')+1:]

        elif aconteceu[1] == 'if ' or aconteceu[1] == 'while':
           inicio = s[ p : p+s[p:].find('\n')+1]
           inicio = inicio.replace('\n',':\n')
           s = s[:p] + inicio + s[p+s[p:].find('\n')+1:]

        aconteceu[0] = False

    log('programa em python concluido')
    f = open('programa.py','w',encoding="utf8")
    f.write(programa)
    f.close()

def GerarProgramaExecutavel():
    import os
    log('gerando executável para Windows')
    os.system('pyinstaller --onefile programa.py')
    log('Executável gerado para Windows')

def GerarProgramaLinux():
    import os
    log('gerando executável para Linux')
    os.system('cxfreeze programa.py --target-dir Linux')
    log('Executável gerado para Linux')
    
def Compilar():
    global btn_ativado
    btn_ativado = False
    IniciarCompilador()
    Iniciar()
    GerarProgramaExecutavel()
    GerarProgramaLinux()
    log('**Compilação Finalizada**')
    btn_ativado = True

def executar():
    IniciarCompilador()
    global btn_ativado
    if btn_ativado == True:
        import threading
        t = threading.Thread(target=Compilar)
        t.start()


def abrirArquivo():
    global filename
    global text
    ftypes = [('Arquivos ec', '*.ec'), ('Todos os arquivos', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    filename = dlg.show()

    if filename != ():
        text = lerArquivo(filename)
        pr.delete(1.0, END)
        pr.insert(END, text)
        atualizar_sintaxe()

def lerArquivo(filename):
    with open(filename, "r") as f:
        text = f.read()
    return text

def salvarArquivo():
    global text
    global filename
    if filename != () and filename != '':
        a = open(filename, "w")
        a.write(pr.get(1.0,END))
        a.close()

# COR SINTAXE
def sintaxe_linha(palavra,cor,frase,linha):
    conteudo = frase
    if palavra in frase:
        pr.tag_add(palavra, linha+str('.')+str(conteudo.find(palavra)), linha+str('.')+str(conteudo.find(palavra)+len(palavra)))
        pr.tag_config(palavra, foreground=cor)

def sintaxe(palavra,cor,pr):
    lista = pr.get(1.0,END).split('\n')
    for linha in range(len(lista)):
        sintaxe_linha(palavra,cor,lista[linha],str(linha+1))

def atualizar_sintaxe():
    sintaxe('vale','orange',pr)
    sintaxe('recebe','orange',pr)

    sintaxe('enquanto','#fe468a',pr)
    sintaxe(' e ','#f9264a',pr)
    sintaxe(' ou ','#f9264a',pr)
  
    sintaxe('for diferente de','#66d9ef',pr)
    sintaxe('for menor que','#66d9ef',pr)
    sintaxe('for maior que','#66d9ef',pr)
    sintaxe('for igual a','#66d9ef',pr)

    sintaxe('exiba nessa linha','#22ee22',pr)
    sintaxe('exiba','#22ee22',pr)
    sintaxe('mostre nessa linha ','#22ee22',pr)
    sintaxe('mostre','#22ee22',pr)

    sintaxe('senao','#e2d872',pr)
    sintaxe('se ','#e2d872',pr)
    sintaxe('digitado','#e2d872',pr)

# INTERFACE
tela.grid_columnconfigure(1,weight=1)
tela.rowconfigure(1,weight=1)

fr = Frame(tela)
menubar = Menu(tela,bg='#343434',fg='white')
tela.config(menu=menubar)

menu_arquivo  = Menu(menubar)
menu_compilar = Menu(menubar)
menu_paleta   = Menu(menubar)
menu_ajuda    = Menu(menubar)

menubar.add_cascade(label='Arquivo', menu=menu_arquivo)
menubar.add_cascade(label='Compilar',menu=menu_compilar)
menubar.add_cascade(label='Cores', menu=menu_paleta)
menubar.add_cascade(label='Ajuda', menu=menu_ajuda)

#menu_arquivo.add_separator()
menu_arquivo.add_command(label='Abrir...',command=abrirArquivo)
menu_arquivo.add_command(label='Salvar',command=salvarArquivo)
menu_arquivo.add_command(label='Sair')
menu_compilar.add_command(label='Compilar',command=executar)
menu_paleta.add_command(label='Azul')
menu_paleta.add_command(label='Vermelho')
menu_paleta.add_command(label='Preto')
menu_ajuda.add_command(label='Ajuda')

fr.grid_columnconfigure((0,1),weight=2)
fr.rowconfigure(1,weight=1)

st = Text(fr,width=40,bg='#343434',fg='#ffffff',font=('',15))
st.grid(row=1,column=0,sticky=NSEW)

pr = Text(fr,bg='#343434',fg='#ffffff',font=('',15))
pr.grid(row=1,column=1,sticky=NSEW)
pr.bind("<Key>",lambda pr:atualizar_sintaxe())
pr.delete(1.0, END)
fr.grid(row=1,column=1,sticky=NSEW)

tela.mainloop()
