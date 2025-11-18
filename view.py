import sqlite3
from datetime import datetime, timedelta

# Conectar ao banco
def connect():
    return sqlite3.connect('dados.db')

# Inserir novo livro
def insert_book(titulo, autor, editora, ano, isbn):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn) VALUES (?, ?, ?, ?, ?)",
        (titulo, autor, editora, ano, isbn)
    )
    con.commit()
    con.close()
    print(f"Livro '{titulo}' inserido com sucesso.")

# Inserir novo usuário
def insert_user(nome, turma, endereco, email, telefone):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, turma, endereco, email, telefone) VALUES (?, ?, ?, ?, ?)",
        (nome, turma, endereco, email, telefone)
    )
    con.commit()
    con.close()
    print(f"Usuário '{nome}' inserido com sucesso.")

# Inserir novo empréstimo
def insert_loan(id_livro, id_usuario, data_emprestimo, data_devolucao=None):
    con = connect()
    cursor = con.cursor()

    data_prevista_str = None
    if isinstance(data_emprestimo, str):
        try:
            data_emp_clean = data_emprestimo.strip()
            data_emp_dt = datetime.strptime(data_emp_clean, "%d-%m-%Y")
            data_prevista_dt = data_emp_dt + timedelta(days=30)
            data_prevista_str = data_prevista_dt.strftime("%d-%m-%Y")
        except Exception as e:
            print(f"Não foi possível calcular data_prevista a partir de '{data_emprestimo}': {e}")

    cursor.execute('''
        INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_devolucao, data_prevista)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_livro, id_usuario, data_emprestimo, data_devolucao, data_prevista_str))

    con.commit()
    con.close()
    print(f"Empréstimo inserido com sucesso. Prevista: {data_prevista_str}")

# Listar livros
def listar_livros():
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT id, titulo, autor, editora, ano_publicacao, isbn FROM livros")
    livros = cursor.fetchall()
    con.close()
    
    print("\n=== LIVROS CADASTRADOS (via print) ===")
    if not livros:
        print("Nenhum livro cadastrado ainda.")
    else:
        for livro in livros:
            print(f"ID: {livro[0]} | Título: {livro[1]}")
            
    return livros # <--- CORRIGIDO: Adicionado return

# Listar usuários
def listar_usuarios():
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT id, nome, turma, endereco, email, telefone FROM usuarios")
    usuarios = cursor.fetchall()
    con.close()
    
    print("\n=== USUÁRIOS CADASTRADOS (via print) ===")
    if not usuarios:
        print("Nenhum usuário cadastrado ainda.")
    else:
        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Nome: {usuario[1]}")

    return usuarios # <--- CORRETO (Já tinha)

#Listar emprestimos
def listar_emprestimos():
    con = connect()
    cur = con.cursor()
    cur.execute('''
        SELECT emprestimos.id, livros.titulo, usuarios.nome,
               emprestimos.data_emprestimo, emprestimos.data_prevista, emprestimos.data_devolucao
        FROM emprestimos
        INNER JOIN livros ON livros.id = emprestimos.id_livro
        INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario
    ''')
    rows = cur.fetchall()
    con.close()
    
    print("\n=== EMPRÉSTIMOS (via print) ===")
    if not rows:
        print("Nenhum empréstimo cadastrado.")
    else:
        for r in rows:
            print(f"ID:{r[0]} | Livro:{r[1]} | Usuário:{r[2]}")
            
    return rows # <--- CORRIGIDO: Adicionado return

# Atualizar data de devolucao
def devolver_livro(id_emprestimo, data_devolucao):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        "UPDATE emprestimos SET data_devolucao = ? WHERE id = ?",
        (data_devolucao, id_emprestimo))
    
    if cursor.rowcount == 0:
         print(f"Nenhum empréstimo encontrado com ID {id_emprestimo}.")
    else:
         print(f"Empréstimo {id_emprestimo} atualizado com data de devolução {data_devolucao}.")

    con.commit()
    con.close()

# --- NOVAS FUNÇÕES 'GET' PARA FORMULÁRIOS ---

# Retorna livros no formato "ID: Titulo"
def get_all_livros():
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT id, titulo FROM livros ORDER BY titulo")
    livros = cursor.fetchall()
    con.close()
    return [f"{id}: {titulo}" for id, titulo in livros]

# Retorna usuários no formato "ID: Nome"
def get_all_usuarios():
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT id, nome FROM usuarios ORDER BY nome")
    usuarios = cursor.fetchall()
    con.close()
    return [f"{id}: {nome}" for id, nome in usuarios]

# Retorna empréstimos ativos (não devolvidos)
def get_active_loans():
    con = connect()
    cur = con.cursor()
    cur.execute('''
        SELECT emprestimos.id, livros.titulo, usuarios.nome
        FROM emprestimos
        INNER JOIN livros ON livros.id = emprestimos.id_livro
        INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario
        WHERE emprestimos.data_devolucao IS NULL OR emprestimos.data_devolucao = ''
        ORDER BY emprestimos.id
    ''')
    rows = cur.fetchall()
    con.close()
    return [f"{id}: {titulo} (com {usuario})" for id, titulo, usuario in rows]
#----- novo ------------

# --- NOVAS FUNÇÕES DE ALTERAÇÃO E EXCLUSÃO ---

# --- FUNÇÕES 'GET' PARA PREENCHER FORMULÁRIOS ---

def get_user_by_id(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    data = cursor.fetchone() # fetchone() pega apenas um resultado
    con.close()
    return data

def get_book_by_id(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    data = cursor.fetchone()
    con.close()
    return data

# -- novo --

# --- NOVAS FUNÇÕES DE ALTERAÇÃO E EXCLUSÃO ---

# --- FUNÇÕES 'GET' PARA PREENCHER FORMULÁRIOS ---

def get_user_by_id(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    data = cursor.fetchone() # fetchone() pega apenas um resultado
    con.close()
    return data

def get_book_by_id(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
    data = cursor.fetchone()
    con.close()
    return data

# --- FUNÇÕES 'UPDATE' (ALTERAR) ---

def update_user(id, nome, turma, endereco, email, telefone):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        """UPDATE usuarios SET nome=?, turma=?, endereco=?, email=?, telefone=?
           WHERE id = ?""",
        (nome, turma, endereco, email, telefone, id)
    )
    con.commit()
    con.close()
    print(f"Usuário ID {id} atualizado.")

def update_book(id, titulo, autor, editora, ano, isbn):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        """UPDATE livros SET titulo=?, autor=?, editora=?, ano_publicacao=?, isbn=?
           WHERE id = ?""",
        (titulo, autor, editora, ano, isbn, id)
    )
    con.commit()
    con.close()
    print(f"Livro ID {id} atualizado.")

# --- FUNÇÕES 'DELETE' (EXCLUIR) ---

def delete_user(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    con.commit()
    con.close()
    print(f"Usuário ID {id} deletado.")

def delete_book(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
    con.commit()
    con.close()
    print(f"Livro ID {id} deletado.")
    
    #-- fim novo --

# --- FUNÇÕES 'UPDATE' (ALTERAR) ---

def update_user(id, nome, turma, endereco, email, telefone):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        """UPDATE usuarios SET nome=?, turma=?, endereco=?, email=?, telefone=?
           WHERE id = ?""",
        (nome, turma, endereco, email, telefone, id)
    )
    con.commit()
    con.close()
    print(f"Usuário ID {id} atualizado.")

def update_book(id, titulo, autor, editora, ano, isbn):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        """UPDATE livros SET titulo=?, autor=?, editora=?, ano_publicacao=?, isbn=?
           WHERE id = ?""",
        (titulo, autor, editora, ano, isbn, id)
    )
    con.commit()
    con.close()
    print(f"Livro ID {id} atualizado.")

# --- FUNÇÕES 'DELETE' (EXCLUIR) ---

def delete_user(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    con.commit()
    con.close()
    print(f"Usuário ID {id} deletado.")

def delete_book(id):
    con = connect()
    cursor = con.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
    con.commit()
    con.close()
    print(f"Livro ID {id} deletado.")
# (O resto do seu código de teste __main__ pode ficar aqui)