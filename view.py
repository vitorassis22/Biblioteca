import sqlite3

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
def insert_loan(id_livro, id_usuario, data_emprestimo, data_devolucao):
    con = connect()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)",
        (id_livro, id_usuario, data_emprestimo, data_devolucao)
    )
    con.commit()
    con.close()
    print("Empréstimo inserido com sucesso.")

# Listar todos os livros
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

# Listar todos os usuários
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

# Listar todos os empréstimos
def listar_emprestimos():
    con = connect()
    cursor = con.cursor()
    cursor.execute('''
        SELECT emprestimos.id, livros.titulo, usuarios.nome, emprestimos.data_emprestimo, emprestimos.data_devolucao
        FROM emprestimos
        INNER JOIN livros ON livros.id = emprestimos.id_livro
        INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario
    ''')
    emprestimos = cursor.fetchall()
    con.close()

    print("\n=== EMPRÉSTIMOS ===")
    if emprestimos:
        for emp in emprestimos:
            devolucao = emp[4] if emp[4] else "Ainda não devolvido"
            print(f"ID: {emp[0]} | Livro: {emp[1]} | Usuário: {emp[2]} | Empréstimo: {emp[3]} | Devolução: {devolucao}")
    else:
        print("Nenhum empréstimo registrado.")
        
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
    
# Testando as funções
if __name__ == '__main__':
   # insert_book("Dom Quixote", "Miguel de Cervantes", "Editora X", 1605, "123456")
   # insert_user("Vitor", "3º Ano", "Rua Aaaa Aaa Aaa", "vitorassis@gmail.com", "18989899")
   # insert_loan(1, 1, "14-10-2025", None)
   # insert_book("B", "Miguel", "Editora Y", 1600, "123345")
   #  insert_user("Joao", "2º Ano", "Rua bb bbb, 105", "joao@exemplo.br", "189919999")
   # insert_loan(2, 2, "15-10-2025", "25-10-2025")
    # Exibir dados cadastrados
    
    listar_livros()
    listar_usuarios()
    listar_emprestimos()
    devolver_livro(2, "20-10-2025")
    listar_emprestimos()