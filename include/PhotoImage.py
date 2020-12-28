#####
#    Inclusa biblioteca PIL (pillow) para utilização de imagens do Tkinter no mac ou em um ambiente posix,
#
#    Exemplo de instalação através do pip:
#    $ python -m pip install pillow
#####

from os import name

def PhotoImagePIL(file):
    """Cria um objeto do tipo PhotoImage automáticamente, e incluí nele a função subsample, que pode ser encontrada no padrão do Tkinter
    Args:
    file = diretório do arquivo de imagem
    Returns:
        PhotoImage<>
    """
    from PIL import Image, ImageTk

    image = Image.open(file)
    imageTk = ImageTk.PhotoImage(image)

    imageTk.subsample = lambda x, y: ImageTk.PhotoImage(image.resize((x*4, y*4)))

    return imageTk

if (name == 'posix' or name == 'darwin'):
    PhotoImage = lambda file: PhotoImagePIL(file)

else:
    from tkinter import PhotoImage as PhotoImage