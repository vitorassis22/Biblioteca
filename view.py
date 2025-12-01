import sqlite3


# =============================================================================
# CONEXÃO COM AUTO-CORREÇÃO (CRIA TABELAS E COLUNAS NOVAS)
# =============================================================================
def connect():
    """
    Establishes a connection to the SQLite database and ensures the database schema is up-to-date.

    This function performs the following steps:
    1. Connects to the SQLite database file named 'dados.db'.
    2. Creates any missing tables in the database.
    3. Checks and updates the database columns to ensure they are consistent with the expected schema.

    Returns:
        sqlite3.Connection: A connection object to interact with the SQLite database.
    """
    con = sqlite3.connect("dados.db")
    create_tables_if_missing(con)
    check_and_update_columns(con)  # <--- AQUI ESTÁ A PROTEÇÃO EXTRA
    return con


def create_tables_if_missing(con):
    cur = con.cursor()

    # Cria a estrutura BASE (caso o banco não exista)
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT, autor TEXT, editora TEXT, ano_publicacao TEXT, isbn TEXT, 
        origem TEXT, genero TEXT, cidade TEXT, estado TEXT, prateleira TEXT,
        quantidade INTEGER DEFAULT 1
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT, turma TEXT, endereco TEXT, email TEXT, telefone TEXT
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_livro INTEGER, id_usuario INTEGER, 
        data_emprestimo TEXT, data_devolucao TEXT, status TEXT, data_prazo TEXT,
        FOREIGN KEY(id_livro) REFERENCES livros(id),
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
    )
    """
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS generos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS prateleiras (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)"
    )

    con.commit()


def check_and_update_columns(con):
    """
    Verifica se colunas adicionadas depois (quantidade, data_prazo) existem.
    Se não existirem (banco antigo), adiciona elas sem perder dados.
    """
    cur = con.cursor()

    # --- VERIFICAÇÃO 1: Coluna 'quantidade' em LIVROS ---
    try:
        cur.execute("SELECT quantidade FROM livros LIMIT 1")
    except sqlite3.OperationalError:
        # Se der erro, é porque a coluna não existe. Vamos criar.
        print("Atualizando banco: Adicionando coluna 'quantidade'...")
        cur.execute("ALTER TABLE livros ADD COLUMN quantidade INTEGER DEFAULT 1")
        con.commit()

    # --- VERIFICAÇÃO 2: Coluna 'data_prazo' em EMPRÉSTIMOS ---
    try:
        cur.execute("SELECT data_prazo FROM emprestimos LIMIT 1")
    except sqlite3.OperationalError:
        print("Atualizando banco: Adicionando coluna 'data_prazo'...")
        cur.execute("ALTER TABLE emprestimos ADD COLUMN data_prazo TEXT")
        con.commit()


# =============================================================================
# FUNÇÕES DE CRUD
# =============================================================================


# --- LIVROS ---
def insert_book(
    titulo,
    autor,
    editora,
    ano,
    isbn,
    origem,
    genero,
    cidade,
    estado,
    prateleira,
    quantidade,
):
    con = connect()
    con.execute(
        """INSERT INTO livros 
                (titulo, autor, editora, ano_publicacao, isbn, origem, genero, cidade, estado, prateleira, quantidade) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            titulo,
            autor,
            editora,
            ano,
            isbn,
            origem,
            genero,
            cidade,
            estado,
            prateleira,
            quantidade,
        ),
    )
    con.commit()
    con.close()


def get_books(search_term=""):
    con = connect()
    cur = con.cursor()
    if search_term:
        cur.execute(
            "SELECT * FROM livros WHERE titulo LIKE ? OR autor LIKE ?",
            ("%" + search_term + "%", "%" + search_term + "%"),
        )
    else:
        cur.execute("SELECT * FROM livros")
    rows = cur.fetchall()
    con.close()
    return rows


def get_books_list():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT id, titulo FROM livros")
    rows = cur.fetchall()
    con.close()
    return [f"{r[0]}: {r[1]}" for r in rows]


def update_book(
    i,
    titulo,
    autor,
    editora,
    ano,
    isbn,
    origem,
    genero,
    cidade,
    estado,
    prateleira,
    quantidade,
):
    con = connect()
    con.execute(
        """UPDATE livros SET 
                titulo=?, autor=?, editora=?, ano_publicacao=?, isbn=?, origem=?, 
                genero=?, cidade=?, estado=?, prateleira=?, quantidade=? 
                WHERE id=?""",
        (
            titulo,
            autor,
            editora,
            ano,
            isbn,
            origem,
            genero,
            cidade,
            estado,
            prateleira,
            quantidade,
            i,
        ),
    )
    con.commit()
    con.close()


def delete_book(i):
    con = connect()
    con.execute("DELETE FROM livros WHERE id=?", (i,))
    con.commit()
    con.close()


# --- USUÁRIOS ---
def insert_user(nome, turma, endereco, email, telefone):
    con = connect()
    con.execute(
        "INSERT INTO usuarios (nome, turma, endereco, email, telefone) VALUES (?, ?, ?, ?, ?)",
        (nome, turma, endereco, email, telefone),
    )
    con.commit()
    con.close()


def get_users(search_term=""):
    con = connect()
    cur = con.cursor()
    if search_term:
        cur.execute(
            "SELECT * FROM usuarios WHERE nome LIKE ?", ("%" + search_term + "%",)
        )
    else:
        cur.execute("SELECT * FROM usuarios")
    rows = cur.fetchall()
    con.close()
    return rows


def get_users_list():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT id, nome FROM usuarios")
    rows = cur.fetchall()
    con.close()
    return [f"{r[0]}: {r[1]}" for r in rows]


def update_user(i, nome, turma, endereco, email, telefone):
    con = connect()
    con.execute(
        "UPDATE usuarios SET nome=?, turma=?, endereco=?, email=?, telefone=? WHERE id=?",
        (nome, turma, endereco, email, telefone, i),
    )
    con.commit()
    con.close()


def delete_user(i):
    con = connect()
    con.execute("DELETE FROM usuarios WHERE id=?", (i,))
    con.commit()
    con.close()


# --- AUXILIARES ---
def insert_genero(nome):
    con = connect()
    con.execute("INSERT INTO generos (nome) VALUES (?)", (nome,))
    con.commit()
    con.close()


def get_generos():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM generos")
    rows = cur.fetchall()
    con.close()
    return rows


def get_generos_list():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT nome FROM generos")
    rows = cur.fetchall()
    con.close()
    return [r[0] for r in rows]


def delete_genero(i):
    con = connect()
    con.execute("DELETE FROM generos WHERE id=?", (i,))
    con.commit()
    con.close()


def insert_prateleira(nome):
    con = connect()
    con.execute("INSERT INTO prateleiras (nome) VALUES (?)", (nome,))
    con.commit()
    con.close()


def get_prateleiras():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM prateleiras")
    rows = cur.fetchall()
    con.close()
    return rows


def get_prateleiras_list():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT nome FROM prateleiras")
    rows = cur.fetchall()
    con.close()
    return [r[0] for r in rows]


def delete_prateleira(i):
    con = connect()
    con.execute("DELETE FROM prateleiras WHERE id=?", (i,))
    con.commit()
    con.close()


# --- EMPRÉSTIMOS ---
def insert_loan(id_livro, id_usuario, data_emp, data_prazo):
    con = connect()
    con.execute(
        "INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_prazo, status) VALUES (?, ?, ?, ?, 'Ativo')",
        (id_livro, id_usuario, data_emp, data_prazo),
    )
    con.commit()
    con.close()


def get_loans(search_term="", somente_ativos=False):
    con = connect()
    cur = con.cursor()

    sql = """
    SELECT e.id, l.titulo, u.nome, e.data_emprestimo, e.data_prazo, e.data_devolucao, e.status
    FROM emprestimos e
    JOIN livros l ON e.id_livro = l.id
    JOIN usuarios u ON e.id_usuario = u.id
    WHERE 1=1 
    """

    params = []
    if somente_ativos:
        sql += " AND e.status = 'Ativo'"

    if search_term:
        sql += " AND (l.titulo LIKE ? OR u.nome LIKE ?)"
        params.append(f"%{search_term}%")
        params.append(f"%{search_term}%")

    cur.execute(sql, params)
    rows = cur.fetchall()
    con.close()
    return rows


def get_loans_list():
    con = connect()
    cur = con.cursor()
    sql = """
    SELECT e.id, l.titulo, u.nome 
    FROM emprestimos e
    JOIN livros l ON e.id_livro = l.id
    JOIN usuarios u ON e.id_usuario = u.id
    WHERE e.status = 'Ativo'
    """
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    return [f"{r[0]}: {r[1]} - {r[2]}" for r in rows]


def return_loan(id_emp, data_dev):
    con = connect()
    con.execute(
        "UPDATE emprestimos SET status='Devolvido', data_devolucao=? WHERE id=?",
        (data_dev, id_emp),
    )
    con.commit()
    con.close()
