import sqlite3
from faker import Faker
import random

# Configura o gerador de dados falsos para Português do Brasil
fake = Faker('pt_BR')

def popular_tudo():
    print("Iniciando geração de dados... Aguarde.")
    
    con = sqlite3.connect('dados.db')
    cursor = con.cursor()

    # --- 1. GERAR 300 USUÁRIOS ---
    print("Gerando 300 usuários...")
    lista_turmas = ['Sexto ano', 'Sétimo ano', 'Oitavo ano', 'Nono ano']
    
    usuarios_para_inserir = []
    
    for _ in range(300):
        nome = fake.name()
        turma = random.choice(lista_turmas)
        endereco = fake.address().replace('\n', ', ') # Remove quebra de linha do endereço
        email = fake.email()
        telefone = fake.cellphone_number()
        
        usuarios_para_inserir.append((nome, turma, endereco, email, telefone))

    # Inserção em massa (muito mais rápido que inserir um por um)
    cursor.executemany("""
        INSERT INTO usuarios (nome, turma, endereco, email, telefone) 
        VALUES (?, ?, ?, ?, ?)
    """, usuarios_para_inserir)

    # --- 2. GERAR 2000 LIVROS ---
    print("Gerando 2000 livros...")
    lista_origem = ['Doação', 'Governo']
    
    livros_para_inserir = []
    
    for _ in range(2000):
        # Cria um título fictício (ex: "A Arte da Programação")
        titulo = fake.catch_phrase().title() 
        autor = fake.name()
        editora = fake.company()
        ano = random.randint(1990, 2024)
        isbn = fake.isbn13()
        origem = random.choice(lista_origem)
        
        livros_para_inserir.append((titulo, autor, editora, ano, isbn, origem))

    # Inserção em massa
    cursor.executemany("""
        INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn, origem) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, livros_para_inserir)

    # Salvar alterações e fechar
    con.commit()
    con.close()
    
    print("-" * 30)
    print("SUCESSO! Foram inseridos:")
    print(f"✅ {len(usuarios_para_inserir)} Usuários")
    print(f"✅ {len(livros_para_inserir)} Livros")
    print("-" * 30)

if __name__ == "__main__":
    popular_tudo()