import os
from app import app

def recupera_img(id):
    caminho = app.config['UPLOAD_PATH']
    for nome_arquivo in os.listdir(caminho):
        if f'Foto_{id}' in nome_arquivo:
            return nome_arquivo

    return 'preview_cat.jpg'

def deleta_arquivo(id):
    arquivo = recupera_img(id)
    caminho = app.config['UPLOAD_PATH']
    if arquivo != 'preview_cat.jpg':
        os.remove(os.path.join(caminho, arquivo))