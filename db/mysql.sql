CREATE DATABASE IF NOT EXISTS `db_banco`;
USE `db_banco`;

CREATE TABLE doadores (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome TEXT NOT NULL, 
    email TEXT NOT NULL,
    telefone TEXT NOT NULL
);

CREATE TABLE campanhas (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    titulo TEXT NOT NULL, 
    descricao TEXT NOT NULL, 
    meta_financeira TEXT NOT NULL, 
    meta_itens TEXT NOT NULL, 
    data_inicio DATE,
    data_fim DATE
);

CREATE TABLE itens (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome TEXT NOT NULL, 
    descricao TEXT NOT NULL, 
    categoria TEXT NOT NULL
);

CREATE TABLE doacoes (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_doador INT NOT NULL,
    id_campanha INT NOT NULL,
    id_item INT NOT NULL,
    quant INT NOT NULL, 
    data_doacao DATE,
    FOREIGN KEY (id_doador) REFERENCES doadores(id),
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id),
    FOREIGN KEY (id_item) REFERENCES itens(id)
);

CREATE TABLE relatorios (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_campanha INT,
    data_referencia DATE,
    total FLOAT,
    total_itens_doados INT NOT NULL,
    meta_comparativo TEXT NOT NULL,
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id)
);