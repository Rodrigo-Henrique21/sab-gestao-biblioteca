-- População de usuários (senhas: admin123, user123)
INSERT INTO usuarios (username, email, hashed_password, role) VALUES
  ('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPjYLC7hZwUe', 'admin'),
  ('user', 'user@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPjYLC7hZwUe', 'user');

-- População de livros
INSERT INTO livros (titulo, autor, isbn, preco, estoque) VALUES
  ('Python para Iniciantes',     'Maria Andrade',  '9788501400011', 89.90, 15),
  ('Aprenda SQL',                'João Paulo',     '9788501400028', 69.50, 10),
  ('Flask Web Development',      'Miguel Grinberg','9780134398628', 110.00, 7),
  ('Algoritmos em Python',       'Carlos Silva',   '9788534609950', 99.90, 20),
  ('Testes Automatizados',       'Lívia Rocha',    '9788534611168', 85.00, 8);

-- População de clientes
INSERT INTO clientes (nome, telefone) VALUES
  ('André Ramos',      '11999990001'),
  ('Beatriz Souza',    '11988880002'),
  ('Carlos Silva',     '11977770003');
