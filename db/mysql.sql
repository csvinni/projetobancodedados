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
    status TEXT NOT NULL,
    data_fim DATE
);

CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome TEXT NOT NULL
);

CREATE TABLE doacoes (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_doador INT NOT NULL,
    id_campanha INT NOT NULL,
    tipo_doacao TEXT NOT NULL,
    tipo_item TEXT,  
    quantidade INT,  
    valor DECIMAL(10, 2), 
    data_doacao DATE NOT NULL,
    FOREIGN KEY (id_doador) REFERENCES doadores(id),
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id)
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id)

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