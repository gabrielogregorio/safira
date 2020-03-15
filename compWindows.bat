@echo off
color a

echo Certifique-se que a versão do Python é a 3.7.2
echo Execute os comandos abaixo caso tenha erro:
python -m pip install --upgrade pip
python -m pip install pyinstaller

echo Deletando arquivo feynman.exe
del feynman.exe

echo Criando uma cópia temporária
copy script.py feynman.pyw

echo Gerando o Executável
pyinstaller --onefile -windowed --icon=app.ico feynman.pyw

echo Tornando o executável acessivel
move dist\feynman.exe .

echo Deleteando o arquivo temporário
del feynman.pyw

echo deletando o residuo feynman.spec
del feynman.spec

echo deletando pasta build/
rd /s  /q build

echo deletando pasta dist/
rd /s  /q dist

color e
pause