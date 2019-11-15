# fontes: https://pyautogui.readthedocs.io/

import pyautogui
import os

# PYAUTOGUI
def clique_em(x,y,clicks=1,interval=0.5,button="left"):
    pyautogui.click(x,y,clicks,interval,button)

def clique(clicks=1,interval=0.5,button="left"):
    pyautogui.click(clicks,interval,button)

def localize_a_imagem(imagem, confianca = 0.7, grayscale=True):
    posicoes = pyautogui.locateOnScreen(imagem, confidence = confianca)
    return posicoes

def localize_a_imagem_e_retorne_o_centro(imagem, confianca = 0.7, grayscale=True):
    posicoes = pyautogui.locateCenterOnScreen(imagem, confidence = confianca)
    return posicoes

def localize_todas_as_imagens(imagem, confianca = 0.7, grayscale=True):
    retorno = []
    for pos in pyautogui.locateAllOnScreen(imagem):
        retorno.append(pos)
    return retorno

def localize_mouse():
    posicao = pyautogui.position()
    return {'x':int(posicao[0]),'y':int(posicao[1])}

def obter_tamanho_da_tela():
    posicao = pyautogui.size()
    return {'width':int(posicao[0]),'height':int(posicao[1])}

def esta_dentro_da_tela(x=None,y=None):
    return pyautogui.onScreen(X, Y)

def move_para(x=None,y=None,duracao = 0.05):
    pyautogui.moveTo(x, y, duracao)

def move_relativamente_para(x=None,y=None,duracao = 0.05):
    pyautogui.moveRel(x, y, duracao)

def arrasta_mouse(x=None,y=None,tempo=0.2,botao='left'):
    pyautogui.dragTo(x, y, tempo, button=botao)

def arrasta_mouse_relativamente(x=None,y=None,tempo=0.2,botao='left'):
    # left, right
    pyautogui.dragRel(x, y, tempo, button=botao)

def click_e_segure():
    pyautogui.mouseDown()

def solte_o_click():
    pyautogui.mouseUp()

def rode_scroll(ciclos):
    pyautogui.scroll(ciclos)

def digite(string, intervalo = 0.01):
    pyautogui.typewrite(string, interval=intervalo)

def pressione(tecla):
    pyautogui.press(tecla)

def pressione_segure(tecla):
    pyautogui.keyDown(tecla)

def pressione_e_solte(tecla):
    pyautogui.keyUp(tecla)

def capturar_tela(link='img.png'):
    pyautogui.screenshot(link)

def capturar_regiao_da_tela(link ,x ,y ,w ,h):
    pyautogui.screenshot(link, region = (x, y, w, h) )

