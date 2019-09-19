from tkinter import filedialog
from tkinter import *          
from PIL import ImageTk, Image # Icone
import os

tela = Tk()
tela.title('Linguagem ec beta 0.1')
tela.call('wm', 'iconphoto', tela._w, ImageTk.PhotoImage(Image.open('icone.gif'))) # Icone
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

def abrir_arquivo(filename):
    try:
        a = open(filename,'r',encoding="utf8")
        s = a.read() + ' '
        a.close()
        return s
    except:
        a = open(filename,'r')
        s = a.read() + ' '
        a.close()
        return s

def salvarArquivo():
    global text
    global filename
    if filename != () and filename != '':
        a = open(filename, "w")
        a.write(pr.get(1.0,END))
        a.close()

def dialog_salvar_arquivo():
    global filename
    f = filedialog.asksaveasfile(mode='w', defaultextension=".ec",title = "Selecione o arquivo",filetypes = (("Meus projetos","*.ec"),("all files","*.*")))

    if f is None:
        return

    text2save = str(pr.get(1.0, END))
    f.write(text2save)
    f.close()
    filename = f.name
    abrir_arquivo(filename)

def dialog_abrir_arquivo():
    global filename
    global text

    ftypes = [('Arquivos ec', '*.ec'), ('Todos os arquivos', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    filename = dlg.show()

    if filename != ():
        text = abrir_arquivo(filename)
        pr.delete(1.0, END)
        pr.insert(END, text)
        atualizar_sintaxe()

def escrever_codigo():
    f = open('programa.py','w',encoding='utf8')
    f.write("# encoding: utf-8\nimport time\n"+programa)
    f.close()

def log(texto):
    global st
    st.insert(END,str(texto)+"\n")
    st.see("end")
    st.update()

def IniciarCompilador():
    global s
    global filename
    log('abrindo programa em altissimo nível')
    s = abrir_arquivo(filename)
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
    substitui('é igual a','=')

    substitui('enquanto','while')

    substitui(' e ',' and ')
    substitui(' ou ',' or ')
    substitui('for diferente de','!=')

    substitui('for diferente de','!=')
    substitui('for menor que','<')
    substitui('for maior que','>')
    substitui('for igual a','==')

    substitui('exiba nessa linha','print(')
    substitui('exiba','print(')
    substitui('mostre nessa linha ','print(')
    substitui('mostre','print(')

    substitui('senao','else:')
    substitui('se ','if ')
    substitui('digitado','input()')

    substitui('espere ','time.sleep(')

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

        elif aconteceu[1] == 'time.sleep(':
           inicio = s[ p : p+s[p:].find('segundos')+1]
           inicio = inicio.replace('segundos',')\n')
           s = s[:p] + inicio + s[p+s[p:].find('segundos')+1:]

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
    escrever_codigo()

def GerarProgramaExecutavel():
    import os
    os.system('pyinstaller --onefile programa.py')

def GerarProgramaLinux():
    import os
    os.system('cxfreeze programa.py --target-dir Linux')
    
def Compilar():
    global btn_ativado
    btn_ativado = False
    IniciarCompilador()
    Iniciar()
    btn_ativado = True

def executar_script():
    global btn_ativado
    btn_ativado = False
    IniciarCompilador()
    Iniciar()
    btn_ativado = True
    os.system('python3.6 programa.py')
    #os.system('python3 programa.py')
    
def executar():
    IniciarCompilador()
    global btn_ativado
    if btn_ativado == True:
        import threading
        t = threading.Thread(target=Compilar)
        t.start()

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
    sintaxe('é igual a','orange',pr)

    sintaxe('enquanto','#fe468a',pr)
    sintaxe(' e ',     '#f9264a',pr)
    sintaxe(' ou ',    '#f9264a',pr)
  
    sintaxe('for diferente de','#66d9ef',pr)
    sintaxe('for menor que',   '#66d9ef',pr)
    sintaxe('for maior que',   '#66d9ef',pr)
    sintaxe('for igual a',     '#66d9ef',pr)

    sintaxe('exiba nessa linha',  '#22ee22',pr)
    sintaxe('exiba',              '#22ee22',pr)
    sintaxe('mostre nessa linha ','#22ee22',pr)
    sintaxe('mostre',             '#22ee22',pr)

    sintaxe('senao','#e2d872',pr)
    sintaxe('se','#e2d872',pr)
    sintaxe('digitado','#e2d872',pr)

    sintaxe('espere','#fc00ff',pr)
    sintaxe('segundos','#fc00ff',pr)

from design import design

tela.grid_columnconfigure(1,weight=1)
tela.rowconfigure(1,weight=1)

menubar = Menu(tela,design.cor_menu())
tela.config(menu=menubar)

menu_arquivo  = Menu(menubar,design.cor_menu())
menu_compilar = Menu(menubar,design.cor_menu())
menu_executar = Menu(menubar,design.cor_menu())
menu_paleta   = Menu(menubar,design.cor_menu())
menu_ajuda    = Menu(menubar,design.cor_menu())
menu_sobre    = Menu(menubar,design.cor_menu())

menubar.add_cascade(label='Arquivo' , menu=menu_arquivo)
menubar.add_cascade(label='Compilar', menu=menu_compilar)
menubar.add_cascade(label='Executar', menu=menu_executar)
menubar.add_cascade(label='Cores'   , menu=menu_paleta)
menubar.add_cascade(label='Ajuda'   , menu=menu_ajuda)
menubar.add_cascade(label='sobre'   , menu=menu_sobre)

menu_arquivo.add_command(label='Abrir...',command=dialog_abrir_arquivo)
menu_arquivo.add_command(label='Salvar',command=salvarArquivo)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Salvar Como',command=dialog_salvar_arquivo)
menu_arquivo.add_command(label='Sair')
menu_compilar.add_command(label='Compilar',command=executar)
menu_executar.add_command(label='Executar',command=executar_script)
menu_paleta.add_command(label='Azul')
menu_paleta.add_command(label='Vermelho')
menu_paleta.add_command(label='Preto')
menu_ajuda.add_command(label='Ajuda')
menu_sobre.add_command(label='Projeto')
menu_sobre.add_command(label='Desenvolvedores',command=lambda:trocar_de_tela(fr,frConfig))

def trocar_de_tela(fechar,carregar):
    fechar.grid_forget()
    carregar.grid(row=1,column=1,sticky=NSEW)

#|--------
fr = Frame(tela)
fr.grid_columnconfigure((0,1),weight=2)
fr.rowconfigure(1,weight=1)
st = Text(fr,width=40,bg='#343434',fg='#ffffff',font=('',15))
st.grid(row=1,column=0,sticky=NSEW)

pr = Text(fr,bg='#343434',fg='#ffffff',font=('',15))
pr.grid(row=1,column=1,sticky=NSEW)
pr.bind("<Key>",lambda pr:atualizar_sintaxe())
pr.delete(1.0, END)
fr.grid(row=1,column=1,sticky=NSEW)

#|--------
frConfig = Frame(tela)
frConfig.rowconfigure(1,weight=15)
frConfig.rowconfigure(2,weight=1)
frConfig.rowconfigure(3,weight=1)
frConfig.grid_columnconfigure(1,weight=2)
titulo = Label(frConfig,text=" combratec ",font=("Arial",70,"bold"),height=5,bg='#343434',fg='#ffffff')

autor  = Label(frConfig,text="Gabriel Gregório da Silva",font=("Arial",15),bg='#343434',fg='#ffffff')
ano    = Label(frConfig,text="2019",font=("Arial",10),bg='#343434',fg='#ffffff')
titulo.grid(row=1,column=1,sticky=NSEW)
autor.grid(row=2,column=1,sticky=NSEW)
ano.grid(row=3,column=1,sticky=NSEW)

tela.mainloop()
