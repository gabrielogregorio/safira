@echo off
color a

pip install --upgrade pip
pip install pyinstaller --upgrade
pip install setuptools --upgrade

del safira.exe
copy safira.py safira.pyw

pyinstaller --onefile --icon="imagens\icone.ico" safira.pyw

move dist\safira.exe .
del safira.pyw
del safira.spec
rd /s  /q build
rd /s  /q dist

color e
pause
