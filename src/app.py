from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from db import get_cursor
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Gestão de Biblioteca API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class LivroCreate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    ano: Optional[int] = None
    preco: float
    estoque: int

class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    ano: Optional[int] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None

class ClienteCreate(BaseModel):
    nome: str
    telefone: Optional[str] = None

class VendaCreate(BaseModel):
    cliente_id: str
    livro_id: str
    quantidade: int

# Auth functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

# Routes
@app.post("/auth/register")
def register(user: UserCreate):
    with get_cursor(commit=True) as cur:
        hashed_password = get_password_hash(user.password)
        cur.execute(
            "INSERT INTO usuarios (username, email, hashed_password, role) VALUES (%s, %s, %s, %s)",
            (user.username, user.email, hashed_password, "user")
        )
    return {"message": "User created"}

@app.post("/auth/login")
def login(user: UserLogin):
    with get_cursor() as cur:
        cur.execute("SELECT id, hashed_password, role FROM usuarios WHERE username = %s", (user.username,))
        result = cur.fetchone()
        if not result or not verify_password(user.password, result[1]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user.username, "role": result[2]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/livros", response_model=List[dict])
def listar_livros(current_user: dict = Depends(get_current_user)):
    with get_cursor() as cur:
        cur.execute("SELECT id, titulo, autor, isbn, ano, preco, estoque FROM livros")
        livros = cur.fetchall()
    return [{"id": str(l[0]), "titulo": l[1], "autor": l[2], "isbn": l[3], "ano": l[4], "preco": l[5], "estoque": l[6]} for l in livros]

@app.post("/livros")
def criar_livro(livro: LivroCreate, current_user: dict = Depends(get_current_user)):
    with get_cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO livros (titulo, autor, isbn, ano, preco, estoque) VALUES (%s, %s, %s, %s, %s, %s)",
            (livro.titulo, livro.autor, livro.isbn, livro.ano, livro.preco, livro.estoque)
        )
    return {"message": "Livro criado"}

@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: str, livro: LivroUpdate, current_user: dict = Depends(get_current_user)):
    update_fields = {k: v for k, v in livro.dict().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = %s" for k in update_fields.keys())
    values = list(update_fields.values()) + [livro_id]
    with get_cursor(commit=True) as cur:
        cur.execute(f"UPDATE livros SET {set_clause} WHERE id = %s", values)
    return {"message": "Livro atualizado"}

@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: str, current_user: dict = Depends(get_current_admin)):
    with get_cursor(commit=True) as cur:
        cur.execute("DELETE FROM livros WHERE id = %s", (livro_id,))
    return {"message": "Livro deletado"}

@app.get("/clientes", response_model=List[dict])
def listar_clientes(current_user: dict = Depends(get_current_user)):
    with get_cursor() as cur:
        cur.execute("SELECT id, nome, telefone FROM clientes")
        clientes = cur.fetchall()
    return [{"id": str(c[0]), "nome": c[1], "telefone": c[2]} for c in clientes]

@app.post("/clientes")
def criar_cliente(cliente: ClienteCreate, current_user: dict = Depends(get_current_user)):
    with get_cursor(commit=True) as cur:
        cur.execute("INSERT INTO clientes (nome, telefone) VALUES (%s, %s)", (cliente.nome, cliente.telefone))
    return {"message": "Cliente criado"}

@app.get("/vendas", response_model=List[dict])
def listar_vendas(current_user: dict = Depends(get_current_user)):
    with get_cursor() as cur:
        cur.execute("""
            SELECT v.id, c.nome, l.titulo, v.quantidade, v.valor_total, v.created_at
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN livros l ON v.livro_id = l.id
        """)
        vendas = cur.fetchall()
    return [{"id": str(v[0]), "cliente": v[1], "livro": v[2], "quantidade": v[3], "valor_total": v[4], "created_at": v[5]} for v in vendas]

@app.post("/vendas")
def registrar_venda(venda: VendaCreate, current_user: dict = Depends(get_current_user)):
    with get_cursor(commit=True) as cur:
        # Check stock
        cur.execute("SELECT preco, estoque FROM livros WHERE id = %s", (venda.livro_id,))
        livro = cur.fetchone()
        if not livro or livro[1] < venda.quantidade:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        valor_total = livro[0] * venda.quantidade
        cur.execute(
            "INSERT INTO vendas (cliente_id, livro_id, quantidade, valor_total) VALUES (%s, %s, %s, %s)",
            (venda.cliente_id, venda.livro_id, venda.quantidade, valor_total)
        )
        cur.execute("UPDATE livros SET estoque = estoque - %s WHERE id = %s", (venda.quantidade, venda.livro_id))
    return {"message": "Venda registrada"}

@app.get("/", response_class=HTMLResponse)
def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)