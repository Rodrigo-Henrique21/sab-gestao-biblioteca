# Deploy — Gestão de Biblioteca

Este documento descreve como publicar o backend e o frontend do projeto.

## Backend no Render

### Passos

1. Crie conta no [Render](https://render.com).
2. Crie um novo serviço do tipo **Web Service**.
3. Conecte o repositório Git.
4. Configure as variáveis de ambiente:
   - `DATABASE_URL`
   - `SECRET_KEY`
5. Build Command:

```bash
pip install -r requirements.txt
```

6. Start Command:

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

7. Desative o deploy manual, se desejar, e mantenha o `render.yaml` na raiz do projeto para controle de configuração.

### Observações

- O Render fornece uma URL pública para o backend.
- Use essa URL como `API_BASE` no frontend.
- Caso use banco de dados hospedado, assegure que o serviço do Render tem acesso à instância.

## Frontend no GitHub Pages

### Passos

1. Garanta que `templates/index.html` e a pasta `static/` estejam versionados no repositório.
2. No GitHub, abra as configurações do repositório.
3. Na seção **Pages**, escolha a branch `main` ou `gh-pages`.
4. Configure a pasta como `/ (root)` se estiver usando a raiz do repositório.
5. Ajuste o arquivo `static/js/script.js` para apontar ao backend:

```js
const API_BASE = 'https://seu-backend.onrender.com';
```

6. Salve e publique.

### Observações

- GitHub Pages serve apenas conteúdo estático.
- Todas as chamadas de API devem apontar para o backend público.
- Se usar `gh-pages`, mantenha a estrutura de arquivos estáticos intacta.

## Combinação Render + GitHub Pages

- Backend: hospedado no Render
- Frontend: hospedado no GitHub Pages
- `API_BASE`: URL pública do Render

### Exemplo

```js
const API_BASE = 'https://meu-backend-render.onrender.com';
```

## Alternativa: frontend hospedado junto com o backend

- Isso é possível se o backend servir o `index.html` e `static/` diretamente.
- No entanto, a forma mais simples para este projeto é manter o backend no Render e o frontend no GitHub Pages.
