# -*- coding: utf-8 -*-

from tkinter import PhotoImage
from tkinter import Tk
from telas.ide import *
from telas.atualizar import Atualizar
from telas.design import Design
from telas.bug import Bug
from telas.splash import Splash
from time import sleep
from time import time as time_time
import util.funcoes as funcoes
from tkinter import *
import tkinter.font as tkFont
from os import makedirs as os_makedirs
from re import search as re_search
from os import walk as os_walk
from zipfile import ZipFile
from io import BytesIO
from os import path as os_path
from requests import get as requests_get
from shutil import copy as shutil_copy
from threading import Thread
from tkinter import END
from copy import deepcopy
from re import finditer
from re import search
from time import time
from util.funcoes import carregar_json
from platform import system as platform_system
from tkinter import Frame
from tkinter import Label
from tkinter import NSEW
from tkinter import Toplevel
from tkinter import Button
from tkinter import GROOVE, GROOVE, NSEW
from tkinter import GROOVE
from tkinter import Canvas
from tkinter import Text
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import CURRENT
from tkinter import Message
from tkinter import INSERT
from tkinter import RAISED
from tkinter import Entry
from tkinter import Menu
from tkinter import FLAT
from tkinter import SEL
from tkinter import N
from tkinter import W
from tkinter.ttk import Treeview
from tkinter.ttk import Style
from os.path import abspath
from os.path import join
from os import getcwd
from os import listdir
from re import compile
from sys import version
from webbrowser import open as webbrowser_open
from util.arquivo import Arquivo
from telas.escolher_idioma import Idioma
from telas.visualizacao import ContadorLinhas
from telas.visualizacao import EditorDeCodigo
from telas.colorir import Colorir
from logs.log import Log
from re import sub as re_sub
from datetime import datetime
from os import getcwd as os_getcwd
from upgrade import Upgrade
from pyglet import resource
from pyglet import font
from tkinter import filedialog
from os import path, walk
from re import findall, MULTILINE, sub
from json import load, loads, dumps
from json import loads as json_loads
from datetime import datetime as datetime_datetime
from random import randint
from re import findall
from os import system
from os import remove as os_remove
from interpretador.mensagens import Mensagens
from interpretador.interpretador import Interpretador


# Instância de tela principal
tela = Tk()
tela.withdraw()
tela.rowconfigure(1, weight=1)
tela.overrideredirect(1)
tela.grid_columnconfigure(1, weight=1)

# Traz barra de titulo
tela.overrideredirect(0)

# Ocultar tkinter
tela.withdraw()
tela.title('Safira')
icon = PhotoImage(file='imagens/icone.png')
tela.call('wm', 'iconphoto', tela._w, icon)

instancia = Interface(tela, icon)
func_fechar_tela = lambda inst=tela: instancia.fechar_janela(inst)
tela.protocol("WM_DELETE_WINDOW", func_fechar_tela)

tela.mainloop()
