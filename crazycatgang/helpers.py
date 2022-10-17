import os
from app import app

def recupera_img(id):
    caminho = app.config['UPLOAD_PATH']
    for nome_arquivo in os.listdir(caminho):
        if f'Foto_{id}.jpg' == nome_arquivo:
            return nome_arquivo

    return 'preview_cat.jpg'