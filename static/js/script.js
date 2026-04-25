const API_BASE = 'https://SEU_BACKEND_AQUI';
let token = localStorage.getItem('token');
let currentUser = null;

document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        showDashboard();
    } else {
        showLogin();
    }

    // Login
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                token = data.access_token;
                localStorage.setItem('token', token);
                decodeToken();
                showDashboard();
                showNotification('Login realizado com sucesso!');
            } else {
                showNotification(data.detail, 'error');
            }
        } catch (error) {
            showNotification('Erro no login', 'error');
        }
    });

    // Register
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;
        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
            if (response.ok) {
                showNotification('Cadastro realizado! Faça login.');
                toggleToLogin();
            } else {
                const data = await response.json();
                showNotification(data.detail, 'error');
            }
        } catch (error) {
            showNotification('Erro no cadastro', 'error');
        }
    });

    // Toggle forms
    document.getElementById('toggleRegister').addEventListener('click', toggleToRegister);
    document.getElementById('toggleLogin').addEventListener('click', toggleToLogin);

    // Logout
    document.getElementById('logout').addEventListener('click', () => {
        token = null;
        localStorage.removeItem('token');
        showLogin();
    });

    // Modal
    document.querySelector('.close').addEventListener('click', () => {
        document.getElementById('modal').classList.add('hidden');
    });

    // Add Livro
    document.getElementById('addLivro').addEventListener('click', () => {
        document.getElementById('livroForm').reset();
        document.getElementById('modal').classList.remove('hidden');
    });

    // Livro Form
    document.getElementById('livroForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const titulo = document.getElementById('titulo').value;
        const autor = document.getElementById('autor').value;
        const isbn = document.getElementById('isbn').value;
        const ano = document.getElementById('ano').value;
        const preco = document.getElementById('preco').value;
        const estoque = document.getElementById('estoque').value;
        try {
            const response = await fetch(`${API_BASE}/livros`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ titulo, autor, isbn, ano: ano ? parseInt(ano) : null, preco: parseFloat(preco), estoque: parseInt(estoque) })
            });
            if (response.ok) {
                document.getElementById('modal').classList.add('hidden');
                loadLivros();
                showNotification('Livro adicionado!');
            } else {
                const data = await response.json();
                showNotification(data.detail, 'error');
            }
        } catch (error) {
            showNotification('Erro ao adicionar livro', 'error');
        }
    });

    // Venda Form
    document.getElementById('vendaForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const cliente_id = document.getElementById('clienteSelect').value;
        const livro_id = document.getElementById('livroSelect').value;
        const quantidade = document.getElementById('quantidade').value;
        try {
            const response = await fetch(`${API_BASE}/vendas`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ cliente_id, livro_id, quantidade: parseInt(quantidade) })
            });
            if (response.ok) {
                loadLivros();
                showNotification('Venda registrada!');
            } else {
                const data = await response.json();
                showNotification(data.detail, 'error');
            }
        } catch (error) {
            showNotification('Erro ao registrar venda', 'error');
        }
    });
});

function decodeToken() {
    const payload = JSON.parse(atob(token.split('.')[1]));
    currentUser = payload;
    document.getElementById('userRole').textContent = `Role: ${payload.role}`;
}

function showLogin() {
    document.getElementById('login').classList.remove('hidden');
    document.getElementById('register').classList.add('hidden');
    document.getElementById('dashboard').classList.add('hidden');
}

function showDashboard() {
    document.getElementById('login').classList.add('hidden');
    document.getElementById('register').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    if (currentUser.role === 'admin') {
        document.getElementById('adminDashboard').classList.remove('hidden');
        loadAdminData();
    } else {
        document.getElementById('userDashboard').classList.remove('hidden');
        loadUserData();
    }
}

function toggleToRegister() {
    document.getElementById('login').classList.add('hidden');
    document.getElementById('register').classList.remove('hidden');
}

function toggleToLogin() {
    document.getElementById('register').classList.add('hidden');
    document.getElementById('login').classList.remove('hidden');
}

async function loadLivros() {
    try {
        const response = await fetch(`${API_BASE}/livros`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const livros = await response.json();
        const tbody = document.querySelector('#livrosTable tbody');
        tbody.innerHTML = '';
        livros.forEach(livro => {
            const row = `<tr>
                <td>${livro.titulo}</td>
                <td>${livro.autor}</td>
                <td>${livro.isbn}</td>
                <td>${livro.preco}</td>
                <td>${livro.estoque}</td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Erro ao carregar livros:', error);
    }
}

async function loadUserData() {
    loadLivros();
    loadClientes();
}

async function loadClientes() {
    try {
        const response = await fetch(`${API_BASE}/clientes`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const clientes = await response.json();
        const select = document.getElementById('clienteSelect');
        select.innerHTML = '<option value="">Selecione Cliente</option>';
        clientes.forEach(cliente => {
            select.innerHTML += `<option value="${cliente.id}">${cliente.nome}</option>`;
        });
        const livroSelect = document.getElementById('livroSelect');
        livroSelect.innerHTML = '<option value="">Selecione Livro</option>';
        const livrosResponse = await fetch(`${API_BASE}/livros`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const livros = await livrosResponse.json();
        livros.forEach(livro => {
            livroSelect.innerHTML += `<option value="${livro.id}">${livro.titulo}</option>`;
        });
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
}

async function loadAdminData() {
    loadLivros();
    loadClientes();
    loadVendas();
}

async function loadVendas() {
    try {
        const response = await fetch(`${API_BASE}/vendas`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const vendas = await response.json();
        const tbody = document.querySelector('#vendasTable tbody');
        tbody.innerHTML = '';
        vendas.forEach(venda => {
            const row = `<tr>
                <td>${venda.cliente}</td>
                <td>${venda.livro}</td>
                <td>${venda.quantidade}</td>
                <td>${venda.valor_total}</td>
                <td>${new Date(venda.created_at).toLocaleDateString()}</td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Erro ao carregar vendas:', error);
    }
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.remove('hidden');
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}