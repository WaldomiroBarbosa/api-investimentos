-- Criação da tabela 'client'
CREATE TABLE client (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number INT NOT NULL,
    user_profile TEXT
);

-- Criação da tabela 'stock'
CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    stock_profile TEXT
);

-- Criação da tabela 'client_stock'
CREATE TABLE client_stock (
    id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    stock_id INT NOT NULL,
    interest INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES stock(id) ON DELETE CASCADE
);
