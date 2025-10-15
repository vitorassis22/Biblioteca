import sqlite3

# Função para criar o banco e as tabelas
def inicializar_banco():
    # Conecta ao banco (ou cria, se não existir), com timeout para evitar erro de "database is locked"
    with sqlite3.connect('dados.db', timeout=10) as con:
        cursor = con.cursor()

        # Criar tabela de livros
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT,
            ano_publicacao INTEGER,
            isbn TEXT UNIQUE
        )
        ''')

        # Criar tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT,
            endereco TEXT,
            email TEXT UNIQUE,
            telefone TEXT
        )
        ''')

        # Criar tabela de empréstimos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT,
            FOREIGN KEY (id_livro) REFERENCES livros(id),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
        ''')

        con.commit()
        print("Banco e tabelas criados com sucesso.")

# Executa a função
if __name__ == '__main__':
    inicializar_banco()
