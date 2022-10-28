from app import db

class Gatos(db.Model): #conexão campos do cadastro
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.String(2), nullable=False)
    castracao = db.Column(db.String(5), nullable=False)
    
    def __repr__(self) -> str:
        return '<Name %r>' % self.name

class Usuarios(db.Model): #conexão usuarios
    nickname = db.Column(db.String(8), primary_key= True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self) -> str:
        return '<Name %r>' % self.name