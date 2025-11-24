import sqlite3

def inicializar_banco():
    with sqlite3.connect('dados.db', timeout=10) as con:
        cursor = con.cursor()

        # Tabela de livros (Atualizada com genero)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT,
            ano_publicacao INTEGER,
            isbn TEXT UNIQUE,
            origem TEXT,
            genero TEXT
        )
        ''')

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

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT,
            data_prevista TEXT,
            FOREIGN KEY (id_livro) REFERENCES livros(id),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
        ''')
        con.commit()
        print("Banco atualizado com campo Gênero.")

if __name__ == '__main__':
    inicializar_banco()