create database studio;
use studio;

CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    numero VARCHAR(11) NOT NULL,
    email VARCHAR(100) NOT NULL,
    atividades VARCHAR(255)  -- Coluna para armazenar atividades selecionadas
);