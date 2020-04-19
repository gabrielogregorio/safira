sudo apt-get install python3-pip --fix-missing
sudo pip3.7 install pyinstaller --no-cache

rm -rf feynman
cp script.py feynman.pyw
python3.7 -m pyinstaller --onefile -windowed --icon=app.ico feynman.pyw

mv dist/feynman .
sudo chmod +x feynman

rm feynman.pyw
rm -rf dist/
rm -rf build/
rm -rf feynman.spec
rm -rf typescript