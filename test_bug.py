#!/usr/bin/python3.8
from libs.funcoes import carregar_json
from bug import Bug
from tkinter import Tk
from design import Design

tela_bug = Tk()
design = Design()
design.update_design_dic()

bug = Bug(tela_bug, design)

#def test_interface():
#    assert bug.interface() == None

