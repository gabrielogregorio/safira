sudo apt-get install python3-distutils
python3.8 -m pip install setuptools --upgrade
python3.8 -m pip install wheel --upgrade

sudo apt-get install python3-pip --fix-missing
sudo python3.8 -m pip install pyinstaller --no-cache

rm -rf safira
cp safira.py safira.pyw
python3.8 -m pyinstaller --onefile -windowed --icon="imagens/icone.png" safira.pyw -w

mv dist/safira .
sudo chmod +x safira

rm safira.pyw
rm -rf dist/
rm -rf build/
rm -rf safira.spec
rm -rf typescript
