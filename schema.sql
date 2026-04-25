-- Usuários para autenticação e RBAC
CREATE TABLE IF NOT EXISTS usuarios (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username     VARCHAR(50) UNIQUE NOT NULL,
    email        VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role         VARCHAR(20) NOT NULL CHECK (role IN ('user', 'admin')),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS livros (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo       VARCHAR(255) NOT NULL,
    autor        VARCHAR(255) NOT NULL,
    isbn         VARCHAR(20) UNIQUE NOT NULL,
    ano          INTEGER,
    preco        DECIMAL(10,2) NOT NULL,
    estoque      INTEGER NOT NULL CHECK (estoque >= 0),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clientes (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome         VARCHAR(255) NOT NULL,
    telefone     VARCHAR(20),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vendas (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id   UUID NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    livro_id     UUID NOT NULL REFERENCES livros(id) ON DELETE RESTRICT,
    quantidade   INTEGER NOT NULL CHECK (quantidade > 0),
    valor_total  DECIMAL(10,2) NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_livro ON vendas(livro_id);
