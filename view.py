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

    # calcula data_prevista
    data_prevista_str = None
    if isinstance(data_emprestimo, str):
        try:
            data_emp_clean = data_emprestimo.strip()
            data_emp_dt = datetime.strptime(data_emp_clean, "%d-%m-%Y")
            data_prevista_dt = data_emp_dt + timedelta(days=30)
            data_prevista_str = data_prevista_dt.strftime("%d-%m-%Y")
        except Exception as e:
            # se falhar, mantém data_prevista_str = None e avisa (ou remova o print em produção)
            print(f"Não foi possível calcular data_prevista a partir de '{data_emprestimo}': {e}")

    # insere no banco
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

    print("\n=== LIVROS CADASTRADOS ===")
    if livros:
        for livro in livros:
            print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | Editora: {livro[3]} | Ano: {livro[4]} | ISBN: {livro[5]}")
    else:
        print("Nenhum livro cadastrado ainda.")

# Listar usuários
def listar_usuarios():
    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT id, nome, turma, endereco, email, telefone FROM usuarios")
    usuarios = cursor.fetchall()
    con.close()

    print("\n=== USUÁRIOS CADASTRADOS ===")
    if usuarios:
        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Nome: {usuario[1]} | Turma: {usuario[2]} | Endereço: {usuario[3]} | Email: {usuario[4]} | Telefone: {usuario[5]}")
    else:
        print("Nenhum usuário cadastrado ainda.")
    return usuarios
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
    print("\n=== EMPRÉSTIMOS ===")
    for r in rows:
        id_emp, titulo, usuario, data_emp, data_prev, data_dev = r
        data_prev_clean = data_prev.strip() if isinstance(data_prev, str) else None
        status = "Data inválida"
        dias_atraso = None

        if data_dev:  # já devolvido
            status = "Devolvido"
        elif data_prev_clean:
            try:
                data_prev_dt = datetime.strptime(data_prev_clean, "%d-%m-%Y")
                hoje = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                if hoje > data_prev_dt:
                    dias_atraso = (hoje - data_prev_dt).days
                    status = f"Atrasado há {dias_atraso} dia(s)"
                else:
                    dias_restantes = (data_prev_dt - hoje).days
                    status = f"Dentro do prazo ({dias_restantes} dia(s) restantes)"
            except ValueError:
                status = "Formato da data_prevista inválido"
        else:
            status = "Data prevista não calculada"
        print(f"ID:{id_emp} | Livro:{titulo} | Usuário:{usuario} | Empréstimo:{data_emp} | Previsto:{data_prev} | Devolução:{data_dev} | Status:{status}")

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
from datetime import datetime

# Testando as funções
if __name__ == '__main__':
  #  insert_book("Dom Quixote", "Miguel de Cervantes", "Editora X", 1605, "123456")
  #  insert_user("Vitor", "3º Ano", "Rua Aaaa Aaa Aaa", "vitorassis@gmail.com", "18989899")
  #  insert_loan(1, 1, "14-10-2025", None)
  #  insert_book("B", "Miguel", "Editora Y", 1600, "123345")
  #  insert_user("Joao", "2º Ano", "Rua bb bbb, 105", "joao@exemplo.br", "189919999")
  #  insert_loan(2, 2, "15-10-2025", "25-10-2025")

    # Exibir dados cadastrados
    listar_livros()
    listar_usuarios()
    listar_emprestimos()
    devolver_livro(1, "20-10-2025")
    listar_emprestimos()