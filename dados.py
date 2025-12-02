import sqlite3

def inicializar_banco():
    with sqlite3.connect('dados.db') as con:
        cursor = con.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS generos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE)')
        cursor.execute('CREATE TABLE IF NOT EXISTS prateleiras (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            editora TEXT,
            ano_publicacao INTEGER,
            isbn TEXT,
            origem TEXT,
            genero TEXT,
            cidade TEXT,
            estado TEXT,
            prateleira TEXT,
            quantidade INTEGER DEFAULT 1
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            turma TEXT,
            endereco TEXT,
            email TEXT,
            telefone TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER,
            id_usuario INTEGER,
            data_emprestimo TEXT,
            data_devolucao TEXT,
            data_prevista TEXT,
            FOREIGN KEY (id_livro) REFERENCES livros(id),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
        ''')
        
        # Dados padrão
        try:
            cursor.execute("INSERT INTO generos (nome) VALUES ('Geral'), ('Ficção'), ('Didático')")
            cursor.execute("INSERT INTO prateleiras (nome) VALUES ('A1'), ('B1'), ('C1')")
        except: pass

        print("Banco de dados atualizado!")

if __name__ == '__main__':
    inicializar_banco()