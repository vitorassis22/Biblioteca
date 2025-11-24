import sqlite3
from datetime import datetime, timedelta

def connect():
    return sqlite3.connect('dados.db')

# --- GÊNEROS ---
def insert_genero(nome):
    with connect() as con: con.execute("INSERT INTO generos (nome) VALUES (?)", (nome,))
def get_generos():
    with connect() as con: return con.execute("SELECT * FROM generos").fetchall()
def delete_genero(id):
    with connect() as con: con.execute("DELETE FROM generos WHERE id=?", (id,))
def get_generos_list(): 
    with connect() as con: return [r[0] for r in con.execute("SELECT nome FROM generos").fetchall()]

# --- PRATELEIRAS ---
def insert_prateleira(nome):
    with connect() as con: con.execute("INSERT INTO prateleiras (nome) VALUES (?)", (nome,))
def get_prateleiras():
    with connect() as con: return con.execute("SELECT * FROM prateleiras").fetchall()
def delete_prateleira(id):
    with connect() as con: con.execute("DELETE FROM prateleiras WHERE id=?", (id,))
def get_prateleiras_list():
    with connect() as con: return [r[0] for r in con.execute("SELECT nome FROM prateleiras").fetchall()]

# --- LIVROS ---
def insert_book(titulo, autor, editora, ano, isbn, origem, genero, cidade, estado, prateleira, quantidade):
    with connect() as con:
        con.execute("""INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn, origem, genero, cidade, estado, prateleira, quantidade) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (titulo, autor, editora, ano, isbn, origem, genero, cidade, estado, prateleira, quantidade))

def update_book(id, titulo, autor, editora, ano, isbn, origem, genero, cidade, estado, prateleira, quantidade):
    with connect() as con:
        con.execute("""UPDATE livros SET titulo=?, autor=?, editora=?, ano_publicacao=?, isbn=?, origem=?, genero=?, cidade=?, estado=?, prateleira=?, quantidade=?
                       WHERE id=?""",
                    (titulo, autor, editora, ano, isbn, origem, genero, cidade, estado, prateleira, quantidade, id))

def delete_book(id):
    with connect() as con: con.execute("DELETE FROM livros WHERE id=?", (id,))

# --- BUSCA INTELIGENTE DE LIVROS ---
def get_books(search_term=""):
    with connect() as con:
        if search_term:
            query = """
                SELECT id, titulo, autor, editora, ano_publicacao, isbn, origem, genero, cidade, estado, prateleira, quantidade 
                FROM livros 
                WHERE titulo LIKE ? OR autor LIKE ? OR isbn LIKE ?
            """
            return con.execute(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')).fetchall()
        else:
            return con.execute("""
                SELECT id, titulo, autor, editora, ano_publicacao, isbn, origem, genero, cidade, estado, prateleira, quantidade 
                FROM livros 
                ORDER BY id DESC LIMIT 50
            """).fetchall()

def get_book_by_id(id):
    with connect() as con: return con.execute("SELECT * FROM livros WHERE id=?", (id,)).fetchone()

# --- USUÁRIOS ---
def insert_user(nome, turma, endereco, email, telefone):
    with connect() as con:
        con.execute("INSERT INTO usuarios (nome, turma, endereco, email, telefone) VALUES (?, ?, ?, ?, ?)",
                    (nome, turma, endereco, email, telefone))

def update_user(id, nome, turma, endereco, email, telefone):
    with connect() as con:
        con.execute("UPDATE usuarios SET nome=?, turma=?, endereco=?, email=?, telefone=? WHERE id=?",
                    (nome, turma, endereco, email, telefone, id))

def delete_user(id):
    with connect() as con: con.execute("DELETE FROM usuarios WHERE id=?", (id,))

# --- BUSCA INTELIGENTE DE USUÁRIOS ---
def get_users(search_term=""):
    with connect() as con:
        if search_term:
            return con.execute("SELECT id, nome, turma, endereco, email, telefone FROM usuarios WHERE nome LIKE ? OR turma LIKE ?", 
                               (f'%{search_term}%', f'%{search_term}%')).fetchall()
        else:
            return con.execute("SELECT id, nome, turma, endereco, email, telefone FROM usuarios ORDER BY id DESC").fetchall()

def get_user_by_id(id):
    with connect() as con: return con.execute("SELECT * FROM usuarios WHERE id=?", (id,)).fetchone()

# --- EMPRÉSTIMOS ---
def insert_loan(id_livro, id_usuario, data_emp):
    try:
        dt = datetime.strptime(data_emp, "%d-%m-%Y")
        prevista = (dt + timedelta(days=15)).strftime("%d-%m-%Y")
    except: prevista = ""
    with connect() as con:
        con.execute("INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_prevista, data_devolucao) VALUES (?, ?, ?, ?, ?)",
                    (id_livro, id_usuario, data_emp, prevista, ""))

def get_active_loans():
    with connect() as con:
        return con.execute("""
            SELECT e.id, l.titulo, u.nome, e.data_emprestimo, e.data_prevista 
            FROM emprestimos e
            JOIN livros l ON l.id = e.id_livro
            JOIN usuarios u ON u.id = e.id_usuario
            WHERE e.data_devolucao IS NULL OR e.data_devolucao = ''
        """).fetchall()

# --- BUSCA INTELIGENTE DE EMPRÉSTIMOS ---
def get_loans(search_term=""):
    with connect() as con:
        base_query = '''
            SELECT e.id, l.titulo, u.nome, e.data_emprestimo, e.data_prevista, 
            CASE WHEN e.data_devolucao IS NULL OR e.data_devolucao = '' THEN 'Pendente' ELSE e.data_devolucao END
            FROM emprestimos e
            JOIN livros l ON l.id = e.id_livro
            JOIN usuarios u ON u.id = e.id_usuario
        '''
        
        if search_term:
            query = f"{base_query} WHERE l.titulo LIKE ? OR u.nome LIKE ? ORDER BY e.id DESC"
            return con.execute(query, (f'%{search_term}%', f'%{search_term}%')).fetchall()
        else:
            query = f"{base_query} ORDER BY e.id DESC LIMIT 50"
            return con.execute(query).fetchall()

def return_loan(id, data_dev):
    with connect() as con:
        con.execute("UPDATE emprestimos SET data_devolucao=? WHERE id=?", (data_dev, id))

# Helpers para Combobox
def get_books_list():
    with connect() as con: return [f"{r[0]}: {r[1]}" for r in con.execute("SELECT id, titulo FROM livros ORDER BY titulo").fetchall()]
def get_users_list():
    with connect() as con: return [f"{r[0]}: {r[1]}" for r in con.execute("SELECT id, nome FROM usuarios ORDER BY nome").fetchall()]
def get_loans_list():
    loans = get_active_loans()
    return [f"{r[0]}: {r[1]} - {r[2]}" for r in loans]