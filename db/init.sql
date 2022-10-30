DROP DATABASE IF EXISTS catgang;
CREATE DATABASE catgang;
USE catgang;
CREATE TABLE gatos (
    id int(11) NOT NULL AUTO_INCREMENT,
    nome varchar(50) NOT NULL,
    idade varchar(2) NOT NULL,
    castracao varchar(5) NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE usuarios (
    nome varchar(20) NOT NULL,
    nickname varchar(8) NOT NULL,
    senha varchar(100) NOT NULL,
    PRIMARY KEY (nickname)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
INSERT INTO usuarios (nome, nickname, senha) VALUES ('admin', 'admin', 'admin');
INSERT INTO usuarios (nome, nickname, senha) VALUES ('user', 'user', 'user');
INSERT INTO gatos (nome, idade, castracao) VALUES ('chicoria', '1', 'True');
INSERT INTO gatos (nome, idade, castracao) VALUES ('Feijoada', '3', 'False');
INSERT INTO gatos (nome, idade, castracao) VALUES ('Lentilha', '4', 'True');
INSERT INTO gatos (nome, idade, castracao) VALUES ('Maria FiFi', '6', 'False');
INSERT INTO gatos (nome, idade, castracao) VALUES ('Nininho', '10', 'True');
