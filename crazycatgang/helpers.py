import os
from app import app

def recupera_img(id):
    caminho = app.config['UPLOAD_PATH'] #path da pasta uploads de imgs
    for nome_arquivo in os.listdir(caminho): #laço entre todas imgs buscando foto pelo id
        if f'Foto_{id}' in nome_arquivo:
            return nome_arquivo
    return 'preview_cat.jpg'

def deleta_arquivo(id):
    arquivo = recupera_img(id)
    caminho = app.config['UPLOAD_PATH'] #path da pasta uploads de imgs
    if arquivo != 'preview_cat.jpg': #remove a img anterior antes de inserir a nova
        os.remove(os.path.join(caminho, arquivo))