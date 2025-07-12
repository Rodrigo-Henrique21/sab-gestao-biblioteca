CREATE TABLE IF NOT EXISTS livros (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo       STRING NOT NULL,
    autor        STRING NOT NULL,
    isbn         STRING UNIQUE NOT NULL,
    preco        DECIMAL(10,2) NOT NULL,
    estoque      INT NOT NULL CHECK (estoque >= 0),
    created_at   TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS clientes (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome         STRING NOT NULL,
    telefone     STRING,
    created_at   TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS vendas (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id   UUID NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    livro_id     UUID NOT NULL REFERENCES livros(id)   ON DELETE RESTRICT,
    quantidade   INT   NOT NULL CHECK (quantidade > 0),
    valor_total  DECIMAL(10,2) NOT NULL,
    created_at   TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_livro   ON vendas(livro_id);
