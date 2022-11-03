import mysql.connector
from mysql.connector import errorcode

try:
    conn = mysql.connector.connect(
        host="mysql-flask-app-container",
        # host="127.0.0.1",
        user="root",
        password="root",
        port="3306",
        database="catcang"
)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
        print(err.errno)
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `catgang`;")

cursor.execute("CREATE DATABASE `catgang`;")

cursor.execute("USE `catgang`;")

# criando tabelas
TABLES = {}
TABLES['gatos'] = ('''
    CREATE TABLE `gatos` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(50) NOT NULL,
    `idade` varchar(2) NOT NULL,
    `castracao` varchar(5) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `usuarios` (
    `nome` varchar(20) NOT NULL,
    `nickname` varchar(8) NOT NULL,
    `senha` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}', end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("admin", "admin", "admin"),
    ("user", "user", "user")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from catgang.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo gatos
gatos_sql = 'INSERT INTO gatos (nome, idade, castracao) VALUES (%s, %s, %s)'
gatos = [
    ('chicoria', '1', 'True'),
    ('Feijoada', '3', 'False'),
    ('Lentilha', '4', 'True'),
    ('Maria FiFi', '6', 'False'),
    ('Nininho', '10', 'True'),
]
cursor.executemany(gatos_sql, gatos)

cursor.execute('select * from catgang.gatos')
print(' -------------  gatos:  -------------')
for gato in cursor.fetchall():
    print(gato[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()