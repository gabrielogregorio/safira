#!/usr/bin/python3.8
from libs.funcoes import carregar_json
from atualizar import Atualizar
from tkinter import Tk
from design import Design

tela_update = Tk()
design_update = Design()
design_update.update_design_dic()

atualizar = Atualizar(tela_update, design_update)

def test_versao():
    assert atualizar.verificar_versao()

def test_primeira():
    assert atualizar.verificar_versao(primeira_vez=True)

