# 📚 Sistema de Gerenciamento para Biblioteca (CustomTkinter + SQLite)

## Resumo

O sistema apresentado é derivado da matéria Projeto de Extensão I de Tecnologia em Análise e Desenvolvimento de Sistemas - IFMS - Três Lagoas - MS

## Visão Geral do Projeto

Este é um sistema completo e moderno para gerenciar o acervo, usuários e o fluxo de empréstimos e devoluções em uma biblioteca. Construído em Python, ele utiliza a biblioteca CustomTkinter para oferecer uma interface de usuário agradável e responsiva.

---

## ✨ Funcionalidades Principais

| Módulo | Funcionalidades | Detalhes |
| :--- | :--- | :--- |
| **Geração de Dados** | Relatórios Avançados | Exibe rankings dos livros mais emprestados, além de estatísticas de movimentação por Dia, Mês e Ano. |
| **Exportação** | Exportar Dados | Permite exportar todos os relatórios gerados para **Excel (.xlsx)** e **PDF**. |
| **Livros** | CRUD Consolidado | Cadastro, visualização, edição e exclusão de livros em uma única aba. Inclui campos essenciais como **Gênero, Quantidade, Prateleira e Localização (Cidade/UF)**. |
| **Usuários** | CRUD Consolidado | Cadastro, visualização, edição e exclusão de usuários (alunos/pessoas). |
| **Empréstimos** | Fluxo Completo | Registro de novos empréstimos e devoluções de itens pendentes. |
| **Auxiliares** | Cadastros Dinâmicos | Gerenciamento de listas de seleção (Ex: Gêneros e Prateleiras). |
| **Segurança** | Backup Automático | Cria um backup do arquivo `dados.db` toda vez que o aplicativo é fechado, garantindo a permanência dos dados. |

---

## 💻 Tecnologias Utilizadas

* **Linguagem:** Python 3.8+ (Recomendado 3.8.10 para compatibilidade com Windows 7).
* **Interface Gráfica (GUI):** **CustomTkinter** (para estética moderna).
* **Banco de Dados:** SQLite3 (Serverless e leve, armazenado no arquivo `dados.db`).
* **Gerenciamento de Dados:** Pandas (usado internamente para otimização e exportação de relatórios).
* **Imagens:** Pillow (PIL).

---

## ⚙️ Instalação e Execução (Modo Desenvolvedor)

### Pré-requisitos

Certifique-se de que o Python esteja instalado e que você tenha as bibliotecas necessárias:

```bash
pip install customtkinter pillow pandas openpyxl reportlab
```

--- 


## ⬆️ Melhorias

Automatizar o sistema de importar dados

### Processo de import atual

#### Pré-Requisitos

- O arquivo a ser inserido deve estar em .csv e as colunas devem estar coerentes ao banco de dados
 ---

- Utilizar o importador_livros.py
- Alterar o nome do arquivo .csv em ` ARQUIVO_ENTRADA = "nomeArquivo" `. Ele irá gerar outro arquivo chamado insert_completo.sql
- Copiar este arquivo todo e colar no inserirdados.py abaixo de `sql_script= """` e acima de 
```python
""" 
cursor.executescript(sql_script)
con.close()
```

### Processo de backup atual

- O app salva uma nova cópia do banco com data e hora no nome automaticamente após fechado. Porém caso um rollback seja necessário é preciso mudar o nome do arquivo de backup para dados.db