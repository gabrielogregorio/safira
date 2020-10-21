dics = {}

def add(chave):
    try:
        dics[str(chave)] += 1
    except:
        dics[str(chave)] = 1


def gerar_pontos(maximo, espaco):
    pontos = []
    for x in range(0, maximo, espaco):
        for y in range(0, maximo, espaco):
            pontos.append([x, y])
    return pontos

def obter_posicao(pontos, alvo, espaco):
    for ponto in pontos:
        if ponto[0] >= alvo[0] and ponto[0] < alvo[0]+espaco:
            if ponto[1] >= alvo[1] and ponto[1] < alvo[1]+espaco:
                return (ponto[0], ponto[1])
    return (0, 0)

        

espaco = 100

pontos = gerar_pontos(2000, espaco)

def teste(event):
    posicao = obter_posicao(pontos, [event.x, event.y], espaco)
    add(posicao)
    atualiza_cor_botao(posicao)



from tkinter import *
tela = Tk()
tela.bind('<Motion>', teste)

fr = Frame(tela, bg='red', width=100, height=100)
fr.grid()



espaco = int(espaco)

dict_btn = {}
def cria_cor_botao(chave, btn):
    dict_btn[str(chave)] = btn


def atualiza_cor_botao(chave):

    dict_btn[str(list(chave))].configure(bg='red')


espaco2= 20
for ponto in pontos:
    print(ponto)
    bt = Button(tela, text='te')
    cria_cor_botao(ponto, bt)

    bt.place(x=ponto[0],
        y=ponto[1],
        width=ponto[0]+espaco2,
        height=ponto[1]+espaco2)

tela.mainloop()

print(dics)

{'(200, 200)': 101}