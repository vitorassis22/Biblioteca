import sqlite3
from datetime import datetime, timedelta

# =============================================================================
# CONEXÃO E CRIAÇÃO DE TABELAS
# =============================================================================
def connect():
    con = sqlite3.connect("dados.db")
    create_tables_if_missing(con)
    check_and_update_columns(con)
    return con

def create_tables_if_missing(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS generos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE)")
    cur.execute("CREATE TABLE IF NOT EXISTS prateleiras (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE)")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT, autor TEXT, editora TEXT, ano_publicacao TEXT, isbn TEXT, 
        origem TEXT, genero TEXT, cidade TEXT, estado TEXT, prateleira TEXT,
        quantidade INTEGER DEFAULT 1
    )""")
    
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, turma TEXT, endereco TEXT, email TEXT, telefone TEXT)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS emprestimos (id INTEGER PRIMARY KEY AUTOINCREMENT, id_livro INTEGER, id_usuario INTEGER, data_emprestimo TEXT, data_prazo TEXT, data_devolucao TEXT, status TEXT)")
    con.commit()

def check_and_update_columns(con):
    """Garante que colunas novas existam em bancos antigos"""
    cur = con.cursor()
    try:
        cur.execute("SELECT data_prazo FROM emprestimos LIMIT 1")
    except:
        cur.execute("ALTER TABLE emprestimos ADD COLUMN data_prazo TEXT")
        cur.execute("ALTER TABLE emprestimos ADD COLUMN status TEXT DEFAULT 'Ativo'")
        con.commit()

# =============================================================================
# DASHBOARD
# =============================================================================
def get_total_books():
    with connect() as con: return con.execute("SELECT COALESCE(SUM(quantidade), 0) FROM livros").fetchone()[0]

def get_total_users():
    with connect() as con: return con.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]

def get_total_loans():
    with connect() as con: 
        # Tenta contar pela coluna status, se falhar usa data_devolucao
        try: return con.execute("SELECT COUNT(*) FROM emprestimos WHERE status = 'Ativo'").fetchone()[0]
        except: return con.execute("SELECT COUNT(*) FROM emprestimos WHERE data_devolucao IS NULL OR data_devolucao = ''").fetchone()[0]

# =============================================================================
# EMPRÉSTIMOS
# =============================================================================
def insert_loan(id_livro, id_usuario, data_emp, data_prazo):
    with connect() as con:
        con.execute("INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_prazo, data_devolucao, status) VALUES (?, ?, ?, ?, '', 'Ativo')", 
                    (id_livro, id_usuario, data_emp, data_prazo))

def return_loan(id, data_dev):
    with connect() as con: 
        con.execute("UPDATE emprestimos SET data_devolucao=?, status='Devolvido' WHERE id=?", (data_dev, id))

def get_loans(search_term="", somente_ativos=False):
    """Busca histórico. Parâmetro 'somente_ativos' corrigido para combinar com a Tela."""
    with connect() as con:
        sql = """SELECT e.id, l.titulo, u.nome, e.data_emprestimo, e.data_prazo, e.data_devolucao, e.status 
                 FROM emprestimos e JOIN livros l ON e.id_livro = l.id JOIN usuarios u ON e.id_usuario = u.id WHERE 1=1"""
        
        if somente_ativos:
            sql += " AND (e.status='Ativo' OR e.data_devolucao IS NULL OR e.data_devolucao = '')"
        
        if search_term:
            sql += f" AND (l.titulo LIKE '%{search_term}%' OR u.nome LIKE '%{search_term}%')"
        
        return con.execute(sql + " ORDER BY e.id DESC").fetchall()

def get_loans_list():
    """Retorna lista formatada de empréstimos ativos para o Combobox de devolução"""
    with connect() as con:
        return [f"{r[0]} - {r[1]} ({r[2]})" for r in con.execute("""
            SELECT e.id, l.titulo, u.nome 
            FROM emprestimos e 
            JOIN livros l ON e.id_livro = l.id 
            JOIN usuarios u ON e.id_usuario = u.id 
            WHERE e.status = 'Ativo' OR e.data_devolucao IS NULL OR e.data_devolucao = ''
        """).fetchall()]

def get_active_loans():
    """Retorna lista pura de ativos para tabelas"""
    with connect() as con:
        return con.execute("""
            SELECT e.id, l.titulo, u.nome, e.data_emprestimo 
            FROM emprestimos e 
            JOIN livros l ON e.id_livro = l.id 
            JOIN usuarios u ON e.id_usuario = u.id 
            WHERE e.status = 'Ativo' OR e.data_devolucao IS NULL OR e.data_devolucao = ''
            ORDER BY e.id DESC
        """).fetchall()

def get_detailed_loan_history():
    with connect() as con: 
        return con.execute("SELECT e.data_emprestimo, l.titulo FROM emprestimos e JOIN livros l ON l.id=e.id_livro ORDER BY e.id DESC").fetchall()

# =============================================================================
# LIVROS
# =============================================================================
def insert_book(titulo, autor, editora, ano, isbn, origem, genero, cid, uf, prat, qtd):
    with connect() as con:
        con.execute("""INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn, origem, genero, cidade, estado, prateleira, quantidade) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (titulo, autor, editora, ano, isbn, origem, genero, cid, uf, prat, qtd))

def update_book(id, titulo, autor, editora, ano, isbn, origem, genero, cid, uf, prat, qtd):
    with connect() as con:
        con.execute("""UPDATE livros SET titulo=?, autor=?, editora=?, ano_publicacao=?, isbn=?, origem=?, genero=?, cidade=?, estado=?, prateleira=?, quantidade=?
                       WHERE id=?""", (titulo, autor, editora, ano, isbn, origem, genero, cid, uf, prat, qtd, id))

def delete_book(id):
    with connect() as con: con.execute("DELETE FROM livros WHERE id=?", (id,))

def get_books(search_term=""):
    with connect() as con:
        if search_term:
            return con.execute("SELECT * FROM livros WHERE titulo LIKE ? OR autor LIKE ? OR isbn LIKE ?", 
                               (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')).fetchall()
        return con.execute("SELECT * FROM livros ORDER BY id DESC").fetchall()

def get_book_by_id(id):
    with connect() as con: return con.execute("SELECT * FROM livros WHERE id=?", (id,)).fetchone()

def get_books_list(): 
    with connect() as con: return [f"{r[0]}: {r[1]}" for r in con.execute("SELECT id, titulo FROM livros").fetchall()]

def get_books_ranking():
    with connect() as con: return con.execute("SELECT l.titulo, l.autor, l.isbn, COUNT(e.id) as t FROM livros l JOIN emprestimos e ON l.id=e.id_livro GROUP BY l.id ORDER BY t DESC").fetchall()

# =============================================================================
# USUÁRIOS
# =============================================================================
def insert_user(nome, turma, endereco, email, telefone):
    with connect() as con: con.execute("INSERT INTO usuarios (nome, turma, endereco, email, telefone) VALUES (?, ?, ?, ?, ?)", (nome, turma, endereco, email, telefone))

def update_user(id, nome, turma, endereco, email, telefone):
    with connect() as con: con.execute("UPDATE usuarios SET nome=?, turma=?, endereco=?, email=?, telefone=? WHERE id=?", (nome, turma, endereco, email, telefone, id))

def delete_user(id):
    with connect() as con: con.execute("DELETE FROM usuarios WHERE id=?", (id,))

def get_users(search_term=""):
    with connect() as con:
        if search_term: return con.execute("SELECT * FROM usuarios WHERE nome LIKE ? OR turma LIKE ?", (f'%{search_term}%', f'%{search_term}%')).fetchall()
        return con.execute("SELECT * FROM usuarios ORDER BY id DESC").fetchall()

def get_users_list(): 
    with connect() as con: return [f"{r[0]}: {r[1]}" for r in con.execute("SELECT id, nome FROM usuarios").fetchall()]

# =============================================================================
# AUXILIARES
# =============================================================================
def insert_genero(nome):
    with connect() as con: con.execute("INSERT INTO generos (nome) VALUES (?)", (nome,))
def delete_genero(id):
    with connect() as con: con.execute("DELETE FROM generos WHERE id=?", (id,))
def get_generos():
    with connect() as con: return con.execute("SELECT * FROM generos").fetchall()
def get_generos_list():
    with connect() as con: return [r[0] for r in con.execute("SELECT nome FROM generos").fetchall()]

def insert_prateleira(nome):
    with connect() as con: con.execute("INSERT INTO prateleiras (nome) VALUES (?)", (nome,))
def delete_prateleira(id):
    with connect() as con: con.execute("DELETE FROM prateleiras WHERE id=?", (id,))
def get_prateleiras():
    with connect() as con: return con.execute("SELECT * FROM prateleiras").fetchall()
def get_prateleiras_list():
    with connect() as con: return [r[0] for r in con.execute("SELECT nome FROM prateleiras").fetchall()]