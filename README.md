# Gestão de Biblioteca

Documentação principal do projeto com links para os detalhes de cada parte.

## Documentação separada

- [Frontend](front.md)
- [Backend](back.md)
- [Deploy](deploy.md)

## Sobre o projeto

Sistema web para gestão de biblioteca com frontend estático e backend em FastAPI.

- O **frontend** é responsivo e construído com HTML, CSS e JavaScript.
- O **backend** é uma API REST desenvolvida em Python com FastAPI.
- O **banco de dados** é compatível com PostgreSQL/CockroachDB usando `DATABASE_URL`.

## Como usar

1. Leia `front.md` para entender a parte de frontend.
2. Leia `back.md` para configurar e rodar o backend.
3. Leia `deploy.md` para publicar backend e frontend.

## Estrutura do repositório

```
.
├── src/
│   ├── app.py
│   ├── db.py
│   ├── livros.py
│   ├── clientes.py
│   ├── vendas.py
│   ├── errors.py
│   └── main.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── tests/
│   ├── test_clientes.py
│   ├── test_livros.py
│   └── test_vendas.py
├── requirements.txt
├── schema.sql
├── seed.sql
├── render.yaml
├── front.md
├── back.md
├── deploy.md
└── README.md
```

## Testes

```bash
pytest
```

> Este `README.md` é o índice do projeto. As instruções detalhadas estão em `front.md`, `back.md` e `deploy.md`.
