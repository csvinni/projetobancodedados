CREATE DATABASE IF NOT EXISTS `db_banco`;
USE `db_banco`;

CREATE TABLE IF NOT EXISTS admin (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    ong TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS doadores (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    senha TEXT NOT NULL  -- Certifique-se de que a coluna 'senha' existe
);

CREATE TABLE IF NOT EXISTS campanhas (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    titulo TEXT NOT NULL, 
    descricao TEXT NOT NULL, 
    meta_financeira TEXT NOT NULL, 
    meta_itens TEXT NOT NULL, 
    data_inicio DATE,
    data_fim DATE,
    status TEXT NOT NULL,
    admin_id INT NOT NULL,
    doador_id INT,  -- Pode ser NULL, pois pode haver campanhas sem doador associado diretamente
    FOREIGN KEY (admin_id) REFERENCES admin(id) ON DELETE CASCADE,
    FOREIGN KEY (doador_id) REFERENCES doadores(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS categorias (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS doacoes (
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
);

CREATE TABLE IF NOT EXISTS relatorios (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_campanha INT,
    data_referencia DATE,
    total FLOAT,
    total_itens_doados INT NOT NULL,
    meta_comparativo TEXT NOT NULL,
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id)
);

CREATE TABLE IF NOT EXISTS logs_doacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_doador INT NOT NULL,
    id_campanha INT NOT NULL,
    total_arrecadado DECIMAL(10, 2),
    meta_financeira DECIMAL(10, 2),
    status_atual VARCHAR(50),
    momento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_doador) REFERENCES doadores(id),
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id)
);