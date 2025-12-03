import pandas as pd
import os
import uuid

# --- CONFIGURAÇÃO ---
ARQUIVO_ENTRADA = "dadosAtt.csv"
ARQUIVO_SAIDA = "insert_completo.sql"

def escapar_sql(texto):
    """Previne erros de SQL e limpa espaços"""
    if pd.isna(texto): return ""
    return str(texto).strip().replace("'", "''")

def tratar_numero(valor):
    if pd.isna(valor) or valor == "": return "0"
    try:
        # Converte 1999.0 para 1999
        return str(int(float(str(valor).replace(',', '.'))))
    except: return "0"

def gerar_arquivo_sql():
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"❌ Erro: O arquivo '{ARQUIVO_ENTRADA}' não está na pasta.")
        return

    print("Lendo arquivo CSV...")
    
    # Tenta ler o arquivo
    try:
        # Tenta ler com UTF-8 primeiro (Corrige os acentos)
        df = pd.read_csv(ARQUIVO_ENTRADA, sep=';', encoding='utf-8', on_bad_lines='skip', dtype=str)
        
        # Se leu tudo numa coluna só, tenta com vírgula
        if len(df.columns) < 2:
             df = pd.read_csv(ARQUIVO_ENTRADA, sep=',', encoding='utf-8', on_bad_lines='skip', dtype=str)
             
    except UnicodeDecodeError:
        # Se der erro, tenta latin1 como fallback
        print("⚠️ Aviso: UTF-8 falhou, tentando Latin-1...")
        try:
            df = pd.read_csv(ARQUIVO_ENTRADA, sep=';', encoding='latin1', on_bad_lines='skip', dtype=str)
        except:
            print("❌ Erro fatal de codificação.")
            return
    except Exception as e:
        print(f"Erro ao ler: {e}")
        return

    # Normaliza colunas
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Localiza as colunas automaticamente
    col_map = {}
    for col in df.columns:
        if "TITULO" in col or "TÍTULO" in col: col_map['TITULO'] = col
        elif "AUTOR" in col: col_map['AUTOR'] = col
        elif "EDITORA" in col: col_map['EDITORA'] = col
        elif "ANO" in col or "EDIÇÃO" in col: col_map['ANO'] = col
        elif "ISBN" in col or "CÓDIGO" in col or "CODIGO" in col: col_map['ISBN'] = col 
        elif "GENERO" in col or "GÊNERO" in col or "ASSUNTO" in col: col_map['GENERO'] = col
        elif "QTD" in col or "QUANTIDADE" in col: col_map['QTD'] = col

    if 'TITULO' not in col_map:
        print("❌ Erro: Coluna de Título não encontrada.")
        print(f"Colunas lidas: {df.columns.tolist()}")
        return
    
    if 'ISBN' in col_map:
        print(f"✅ Coluna de ISBN/Código encontrada: {col_map['ISBN']}")
    else:
        print("⚠️ Aviso: Coluna de ISBN/Código NÃO encontrada. Serão gerados códigos aleatórios.")

    print(f"Gerando SQL para {len(df)} livros...")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write("-- Script gerado automaticamente\n")
        f.write("BEGIN TRANSACTION;\n")
        
        count = 0
        for index, row in df.iterrows():
            titulo = escapar_sql(row.get(col_map.get('TITULO')))
            if len(titulo) < 2: continue # Pula vazios

            autor = escapar_sql(row.get(col_map.get('AUTOR'), 'Desconhecido'))
            editora = escapar_sql(row.get(col_map.get('EDITORA'), ''))
            ano = tratar_numero(row.get(col_map.get('ANO'), 0))
            
            # --- LÓGICA DO ISBN ---
            isbn_raw = row.get(col_map.get('ISBN'), '')
            isbn = escapar_sql(isbn_raw)
            
            # Só gera código novo se o campo estiver realmente vazio ou muito curto
            if len(isbn) < 1: 
                isbn = f"GEN_{uuid.uuid4().hex[:8]}"
            else:
                isbn = isbn.replace('.0', '') # Remove decimal se houver

            genero = escapar_sql(row.get(col_map.get('GENERO'), 'Geral'))
            qtd = tratar_numero(row.get(col_map.get('QTD'), 1))
            if int(qtd) < 1: qtd = "1"

            # Valores fixos
            origem = "Governo"
            cidade = "Não Informada"
            estado = "SP"
            prateleira = "A1"

            # Monta a linha SQL
            sql = f"INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn, origem, genero, cidade, estado, prateleira, quantidade) VALUES ('{titulo}', '{autor}', '{editora}', {ano}, '{isbn}', '{origem}', '{genero}', '{cidade}', '{estado}', '{prateleira}', {qtd});\n"
            f.write(sql)
            count += 1

        f.write("COMMIT;\n")
    
    print(f"✅ SUCESSO! Arquivo '{ARQUIVO_SAIDA}' criado com {count} comandos INSERT.")
    print("Agora abra este arquivo no DB Browser (Execute SQL) e os acentos estarão corretos.")

if __name__ == "__main__":
    gerar_arquivo_sql()