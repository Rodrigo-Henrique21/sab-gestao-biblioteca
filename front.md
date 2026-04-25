# Frontend — Gestão de Biblioteca

Este documento descreve a parte de frontend do projeto.

## Visão geral

O frontend é uma aplicação estática que consome a API do backend.
Ele é composto por HTML, CSS e JavaScript e pode ser servido diretamente como site estático.

## Arquivos principais

- `templates/index.html` — página principal do sistema
- `static/css/style.css` — estilos visuais e responsividade
- `static/js/script.js` — lógica de interação com a API e atualização da interface

## Funcionalidades do frontend

- Exibe lista de livros e clientes
- Permite cadastro de livros e clientes
- Registra vendas e atualiza estoque
- Faz chamadas AJAX para o backend
- Renderiza dados retornados pela API na página

## Conexão com o backend

O frontend usa uma URL base para todas as chamadas à API.
No arquivo `static/js/script.js`, essa URL é configurada em uma constante semelhante a:

```js
const API_BASE = 'http://localhost:8000';
```

### Configuração para deploy

- Para desenvolvimento local, mantenha `API_BASE` apontando para `http://localhost:8000`.
- Para deploy no GitHub Pages, ajuste `API_BASE` para a URL pública do backend hospedado no Render ou em outro serviço.

## Executando localmente

Este frontend é estático e pode ser servido com qualquer servidor HTTP simples.
Exemplo com Python:

```bash
cd c:\Users\FIC\Desktop\projetoSAP\sab-gestao-biblioteca-1
python -m http.server 8001
```

Acesse `http://localhost:8001` para abrir o frontend.

> Se o backend também estiver rodando localmente em `http://localhost:8000`, o frontend conseguirá chamar a API normalmente.

## Observações

- O GitHub Pages serve somente arquivos estáticos.
- Se o frontend for hospedado no GitHub Pages, toda a lógica de dados depende do backend remoto.
- Mantenha o diretório `static/` e o arquivo `index.html` na mesma raiz do site final do Pages.
