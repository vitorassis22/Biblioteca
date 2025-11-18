# Importar Tkinter
import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter.constants import FALSE 
from tkinter import messagebox
from datetime import datetime # <--- IMPORTADO

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para o PyInstaller """
    try:
        # PyInstaller cria um caminho temp e o armazena em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # _MEIPASS não existe, então estamos rodando no modo de dev
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Importar pillow
from PIL import Image, ImageTk
# Importar as funcoes da view
from view import *
# --- cores ---
co0 = "black" 
co1 = "white"  
co2 = "#4fa882" 
co3 = "#000000" 
co4 = "tan3" 
co5 = "#e06636"
co6 = "seagreen4"
co7 = "green1"  
co8 = "burlywood2"
co9 = "#2bb937"
co10 = "#0f7be7"
co11 = "white"
co12 = "#98fb98"
# --- Criando janela ---
janela = tk.Tk() # Usando tk.Tk()
janela.title("") # Titulo
janela.geometry('720x500') # Tamanho
janela.configure(background=co1) # Cor de fundo
janela.resizable(width=FALSE, height=FALSE) # Nao ajustavel
style = ttk.Style(janela) # Usando ttk.Style()
style.theme_use("clam")
# ----- CONFIGURANDO O GRID DA JANELA -----
janela.grid_columnconfigure(1, weight=1) 
janela.grid_rowconfigure(1, weight=1)
# ----- FRAMES -----
frameCima = tk.Frame(janela, height=50, bg=co11, relief="flat")
frameCima.grid(row=0, column=0, columnspan=2, sticky="ew")
frameEsquerda = tk.Frame(janela, bg=co8, relief="flat")
frameEsquerda.grid(row=1, column=0, sticky="nsew") # "ns" = esticar Norte-Sul (vertical)
frameDireita = tk.Frame(janela, bg=co12, relief="flat")
frameDireita.grid(row=1, column=1, sticky="nsew") # "nsew" = esticar em todas as direções
# -------- LOGO --------
img = Image.open(resource_path("assets/icons8-book-100.png"))
img = img.resize((40, 40))
app_img = ImageTk.PhotoImage(img)
app_logo = tk.Label(
    frameCima,
    text="Sistema de Gerenciamento para Biblioteca", 
    image=app_img,
    bg=co11,       
    compound=tk.LEFT,             
    padx=10,                      
    anchor=tk.W,                  
    font=('Verdana', 16, 'bold'), 
    fg=co0                        
)
app_logo.image = app_img
app_logo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
app_linha = tk.Label(frameCima, width=1080, height=1, padx=5, anchor=tk.NW, font=('Verdana 1'), bg=co3, fg=co1)
app_linha.place(x=0, y=50)

# ===================================================================
# FUNÇÕES DAS TELAS
# ===================================================================

# --- Inserir novo cadastro (USUÁRIO) ---
def Novo_cadastro(): 
    
    def add():
        nome = ENome.get()
        turma = ETurma.get()
        telefone = ETel.get()
        endereco = EEndereco.get()
        email = EEmail.get()

        lista_obrigatoria = [nome, turma]
        
        for i in lista_obrigatoria:
            if i=='' or i=='Selecione a turma':
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
        
        insert_user(nome, turma, endereco, email, telefone) 
        messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso!')

        ENome.delete(0,tk.END)
        ETurma.set('Selecione a turma')
        ETel.delete(0,tk.END)
        EEndereco.delete(0,tk.END)
        EEmail.delete(0,tk.END)
        
    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    frameDireita.grid_columnconfigure(2, weight=0)
    frameDireita.grid_columnconfigure(3, weight=1)
    
    # Reinicia os pesos das linhas para 0
    frameDireita.grid_rowconfigure(0, weight=0) # Título
    frameDireita.grid_rowconfigure(1, weight=0) # Linha
    frameDireita.grid_rowconfigure(2, weight=0) # Nome
    frameDireita.grid_rowconfigure(3, weight=0) # Turma
    frameDireita.grid_rowconfigure(4, weight=0) # Telefone
    frameDireita.grid_rowconfigure(5, weight=0) # Endereço
    frameDireita.grid_rowconfigure(6, weight=0) # Email
    frameDireita.grid_rowconfigure(7, weight=0) # Botão
    
    app_ = tk.Label(frameDireita, text="Inserir novo cadastro", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=4, sticky="ew")
    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
    
    LNome = tk.Label(frameDireita, text="Nome *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LNome.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
    ENome = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    ENome.grid(row=2, column=1, padx=5, pady=10, sticky=tk.NSEW)
    
    LTurma = tk.Label(frameDireita, text="Turma *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LTurma.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
    lista_turmas = ['Primeiro ano', 'Segundo ano', 'Terceiro ano']
    ETurma = ttk.Combobox(frameDireita, width=23, values=lista_turmas, font=('Ivy 10'), state='readonly')
    ETurma.grid(row=3, column=1, padx=5, pady=10, sticky=tk.NSEW)
    ETurma.set('Selecione a turma') 
    
    LTel = tk.Label(frameDireita, text="Telefone", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LTel.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
    ETel = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    ETel.grid(row=4, column=1, padx=5, pady=10, sticky=tk.NSEW) 
    
    LEndereco = tk.Label(frameDireita, text="Endereço", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LEndereco.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")
    EEndereco = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EEndereco.grid(row=5, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)

    LEmail = tk.Label(frameDireita, text="Email", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LEmail.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")
    EEmail = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EEmail.grid(row=6, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)
    
    try:
        img_salvar = Image.open(resource_path("assets/save.png"))
        img_salvar = img_salvar.resize((18, 18))
        img_salvar = ImageTk.PhotoImage(img_salvar)
    except FileNotFoundError:
        img_salvar = None

    b_salvar = tk.Button(frameDireita, command=add, image=img_salvar, compound=tk.LEFT, anchor=tk.CENTER,
                         text=' Salvar', bg=co1, fg=co0, font=('Ivy 11 bold'), overrelief="ridge", relief="groove")
    b_salvar.grid(row=7, column=1, sticky="ew", padx=5, pady=20) 
    
    if img_salvar:
        b_salvar.image = img_salvar

# --- (NOVO) Inserir novo LIVRO ---
def Novo_livro():
    
    def add_livro():
        titulo = ETitulo.get()
        autor = EAutor.get()
        editora = EEditora.get()
        ano = EAno.get()
        isbn = EIsbn.get()

        lista_obrigatoria = [titulo, autor, editora, ano, isbn]
        
        for i in lista_obrigatoria:
            if i=='':
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
        
        insert_book(titulo, autor, editora, ano, isbn) 
        messagebox.showinfo('Sucesso', 'Livro cadastrado com sucesso!')

        ETitulo.delete(0,tk.END)
        EAutor.delete(0,tk.END)
        EEditora.delete(0,tk.END)
        EAno.delete(0,tk.END)
        EIsbn.delete(0,tk.END)

    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    frameDireita.grid_columnconfigure(2, weight=0)
    frameDireita.grid_columnconfigure(3, weight=1)
    
    frameDireita.grid_rowconfigure(0, weight=0) # Título
    frameDireita.grid_rowconfigure(1, weight=0) # Linha
    frameDireita.grid_rowconfigure(2, weight=0) # Nome
    frameDireita.grid_rowconfigure(3, weight=0) # Turma
    frameDireita.grid_rowconfigure(4, weight=0) # Telefone
    frameDireita.grid_rowconfigure(5, weight=0) # Endereço
    frameDireita.grid_rowconfigure(6, weight=0) # Email
    frameDireita.grid_rowconfigure(7, weight=0) # Botão
    
    app_ = tk.Label(frameDireita, text="Inserir novo livro", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=4, sticky="ew")
    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
    
    LTitulo = tk.Label(frameDireita, text="Título *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LTitulo.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
    ETitulo = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    ETitulo.grid(row=2, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)
    
    LAutor = tk.Label(frameDireita, text="Autor *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LAutor.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
    EAutor = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EAutor.grid(row=3, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)
    
    LEditora = tk.Label(frameDireita, text="Editora *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LEditora.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
    EEditora = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EEditora.grid(row=4, column=1, padx=5, pady=10, sticky=tk.NSEW) 
    
    LAno = tk.Label(frameDireita, text="Ano *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LAno.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")
    EAno = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EAno.grid(row=5, column=1, padx=5, pady=10, sticky=tk.NSEW)

    LIsbn = tk.Label(frameDireita, text="ISBN *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LIsbn.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")
    EIsbn = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EIsbn.grid(row=6, column=1, padx=5, pady=10, sticky=tk.NSEW)
    
    try:
        img_salvar = Image.open(resource_path("assets/save.png"))
        img_salvar = img_salvar.resize((18, 18))
        img_salvar = ImageTk.PhotoImage(img_salvar)
    except FileNotFoundError:
        img_salvar = None

    b_salvar = tk.Button(frameDireita, command=add_livro, image=img_salvar, compound=tk.LEFT, anchor=tk.CENTER,
                         text=' Salvar', bg=co1, fg=co0, font=('Ivy 11 bold'), overrelief="ridge", relief="groove")
    b_salvar.grid(row=7, column=1, sticky="ew", padx=5, pady=20) 
    if img_salvar:
        b_salvar.image = img_salvar

# --- Ver usuarios (CONSULTAR PESSOAS) ---
def ver_usuarios():
    
    frameDireita.grid_columnconfigure(0, weight=1) 
    frameDireita.grid_columnconfigure(1, weight=0) 
    frameDireita.grid_rowconfigure(2, weight=1) 

    app_ = tk.Label(frameDireita, text="Todos os usuários cadastrados", 
                    padx=5, pady=10, 
                    font=('Verdana 14'), 
                    bg=co12,               
                    fg=co0, 
                    anchor=tk.CENTER)    
    app_.grid(row=0, column=0, columnspan=2, sticky="ew") 

    l_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Verdana 1 '), bg=co3, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW) 

    dados = listar_usuarios()
    
    list_header = ['id','nome','turma','endereço','email','telefone']
    
    global tree
    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=list_header, show="headings")
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew', padx=5, pady=5)
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, columnspan=2, sticky='ew', padx=5)

    h=[20, 80, 80, 120, 120, 100] # Larguras das colunas
    n=0
    for col in list_header:
        tree.heading(col, text=col.title(), anchor='nw') 
        tree.column(col, width=h[n],anchor='nw')
        n+=1

    if dados: 
        for item in dados:
            tree.insert('', 'end', values=item)

# --- (NOVO) Ver LIVROS ---
def ver_livros():
    frameDireita.grid_columnconfigure(0, weight=1) 
    frameDireita.grid_columnconfigure(1, weight=0) 
    frameDireita.grid_rowconfigure(2, weight=1) 

    app_ = tk.Label(frameDireita, text="Todos os livros cadastrados", padx=5, pady=10, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)    
    app_.grid(row=0, column=0, columnspan=2, sticky="ew") 
    l_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Verdana 1 '), bg=co3, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW) 

    dados = listar_livros() # <--- Chama a função de livros
    
    list_header = ['id', 'titulo', 'autor', 'editora', 'ano', 'isbn'] # <--- Cabeçalhos de livros
    
    global tree
    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=list_header, show="headings")
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew', padx=5, pady=5)
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, columnspan=2, sticky='ew', padx=5)

    h=[20, 100, 100, 80, 40, 80] # Larguras das colunas
    n=0
    for col in list_header:
        tree.heading(col, text=col.title(), anchor='nw') 
        tree.column(col, width=h[n],anchor='nw')
        n+=1

    if dados: 
        for item in dados:
            tree.insert('', 'end', values=item)

# --- (NOVO) Ver EMPRÉSTIMOS ---
def ver_emprestimos():
    frameDireita.grid_columnconfigure(0, weight=1) 
    frameDireita.grid_columnconfigure(1, weight=0) 
    frameDireita.grid_rowconfigure(2, weight=1) 

    app_ = tk.Label(frameDireita, text="Todos os empréstimos", padx=5, pady=10, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)    
    app_.grid(row=0, column=0, columnspan=2, sticky="ew") 
    l_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Verdana 1 '), bg=co3, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW) 

    dados = listar_emprestimos() # <--- Chama a função de empréstimos
    
    list_header = ['id', 'livro', 'usuario', 'data_emp', 'data_prev', 'data_dev'] # <--- Cabeçalhos
    
    global tree
    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=list_header, show="headings")
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew', padx=5, pady=5)
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, columnspan=2, sticky='ew', padx=5)

    h=[20, 100, 100, 80, 80, 80] # Larguras das colunas
    n=0
    for col in list_header:
        tree.heading(col, text=col.title(), anchor='nw') 
        tree.column(col, width=h[n],anchor='nw')
        n+=1

    if dados: 
        for item in dados:
            tree.insert('', 'end', values=item)

# --- (NOVO) Realizar EMPRÉSTIMO ---
def realizar_emprestimo():

    def add_emprestimo():
        try:
            livro_str = ELivro.get()
            usuario_str = EUsuario.get()
            data_emp = EData.get()

            if not livro_str or not usuario_str or not data_emp or \
               livro_str == 'Selecione o livro' or usuario_str == 'Selecione o usuário':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return

            id_livro = int(livro_str.split(':')[0])
            id_usuario = int(usuario_str.split(':')[0])

            insert_loan(id_livro, id_usuario, data_emp)
            messagebox.showinfo('Sucesso', 'Empréstimo realizado com sucesso!')
            
            # Recarregar a lista de livros (opcional, se quiser controlar estoque)
            # e limpar os campos
            ELivro.set('Selecione o livro')
            EUsuario.set('Selecione o usuário')
            EData.delete(0, tk.END)
            EData.insert(0, datetime.now().strftime("%d-%m-%Y"))

        except Exception as e:
            messagebox.showerror('Erro', f'Ocorreu um erro: {e}')
            
    for i in range(5):
        frameDireita.grid_columnconfigure(i, weight=0)

    for i in range(7):
        frameDireita.grid_rowconfigure(i, weight=0)
        
    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    
    app_ = tk.Label(frameDireita, text="Realizar Empréstimo", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=3, sticky="ew")
    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

    # Livro
    LLivro = tk.Label(frameDireita, text="Livro *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LLivro.grid(row=2, column=0, padx=5, pady=10, sticky="w")
    livros_disponiveis = get_all_livros() # <--- Chama a nova função
    ELivro = ttk.Combobox(frameDireita, width=40, values=livros_disponiveis, font=('Ivy 10'), state='readonly')
    ELivro.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
    ELivro.set('Selecione o livro')

    # Usuário
    LUsuario = tk.Label(frameDireita, text="Usuário *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LUsuario.grid(row=3, column=0, padx=5, pady=10, sticky="w")
    usuarios_disponiveis = get_all_usuarios() # <--- Chama a nova função
    EUsuario = ttk.Combobox(frameDireita, width=40, values=usuarios_disponiveis, font=('Ivy 10'), state='readonly')
    EUsuario.grid(row=3, column=1, padx=5, pady=10, sticky="ew")
    EUsuario.set('Selecione o usuário')

    # Data Empréstimo
    LData = tk.Label(frameDireita, text="Data *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LData.grid(row=4, column=0, padx=5, pady=10, sticky="w")
    EData = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EData.grid(row=4, column=1, padx=5, pady=10, sticky="w")
    EData.insert(0, datetime.now().strftime("%d-%m-%Y")) # <--- Preenche data de hoje

    try:
        img_salvar = Image.open(resource_path("D:/biblioteca/assets/save.png"))
        img_salvar = img_salvar.resize((18, 18))
        img_salvar = ImageTk.PhotoImage(img_salvar)
    except FileNotFoundError:
        img_salvar = None

    b_salvar = tk.Button(frameDireita, command=add_emprestimo, image=img_salvar, compound=tk.LEFT, anchor=tk.CENTER,
                         text=' Salvar', bg=co1, fg=co0, font=('Ivy 11 bold'), overrelief="ridge", relief="groove")
    b_salvar.grid(row=5, column=1, sticky="w", padx=5, pady=20) 
    if img_salvar:
        b_salvar.image = img_salvar

# ===================================================================
# NOVA FEAT
# ===================================================================

# --- (NOVO) Alterar Cadastro (USUÁRIO) ---
def Alterar_cadastro():
    
    # --- Funções Internas ---
    def carregar_dados():
        try:
            usuario_str = EUsuario.get()
            if not usuario_str or usuario_str == 'Selecione o usuário':
                messagebox.showerror('Erro', 'Selecione um usuário para carregar')
                return

            id_usuario = int(usuario_str.split(':')[0])
            
            # Busca os dados no banco
            dados = get_user_by_id(id_usuario) # dados[0]=id, [1]=nome, [2]=turma, etc.

            # Habilita e preenche os campos
            ENome.config(state='normal')
            ETurma.config(state='normal')
            ETel.config(state='normal')
            EEndereco.config(state='normal')
            EEmail.config(state='normal')
            b_salvar.config(state='normal')

            ENome.delete(0, tk.END)
            ENome.insert(0, dados[1])
            
            ETurma.set(dados[2]) # Combobox usa .set()
            
            ETel.delete(0, tk.END)
            ETel.insert(0, dados[5]) # dados[5] é telefone
            
            EEndereco.delete(0, tk.END)
            EEndereco.insert(0, dados[3]) # dados[3] é endereco
            
            EEmail.delete(0, tk.END)
            EEmail.insert(0, dados[4]) # dados[4] é email

        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar os dados: {e}')

    def salvar_alteracoes():
        try:
            id_usuario = int(EUsuario.get().split(':')[0])
            nome = ENome.get()
            turma = ETurma.get()
            telefone = ETel.get()
            endereco = EEndereco.get()
            email = EEmail.get()

            lista_obrigatoria = [nome, turma]
            for i in lista_obrigatoria:
                if i=='' or i=='Selecione a turma':
                    messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                    return
            
            update_user(id_usuario, nome, turma, endereco, email, telefone)
            messagebox.showinfo('Sucesso', 'Usuário atualizado com sucesso!')

            # Limpa tudo e recarrega a lista
            control('Alterar cadastro')

        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível salvar: {e}')

    # --- Configuração do Grid ---
    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    # ... (Reiniciar pesos das linhas) ...
    for i in range(10): frameDireita.grid_rowconfigure(i, weight=0)

    # --- Título ---
    app_ = tk.Label(frameDireita, text="Alterar Cadastro de Usuário", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=2, sticky="ew")

    # --- Seletor de Usuário ---
    LUsuario = tk.Label(frameDireita, text="Selecione o Usuário:", font=('Verdana 12'), bg=co12, fg=co0)
    LUsuario.grid(row=1, column=0, padx=5, pady=10, sticky="w")
    
    lista_usuarios = get_all_usuarios()
    EUsuario = ttk.Combobox(frameDireita, width=40, values=lista_usuarios, font=('Ivy 10'), state='readonly')
    EUsuario.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
    EUsuario.set('Selecione o usuário')

    b_carregar = tk.Button(frameDireita, command=carregar_dados, text='Carregar Dados', bg=co1, fg=co0, font=('Ivy 10 bold'))
    b_carregar.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)

    # --- Campos do Formulário (copiado de Novo_cadastro) ---
    LNome = tk.Label(frameDireita, text="Nome *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LNome.grid(row=4, column=0, padx=5, pady=10, sticky="w")
    ENome = tk.Entry(frameDireita, width=25, justify='left', relief="solid", state='disabled')
    ENome.grid(row=4, column=1, padx=5, pady=10, sticky="ew")
    
    LTurma = tk.Label(frameDireita, text="Turma *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LTurma.grid(row=5, column=0, padx=5, pady=10, sticky="w")
    lista_turmas = ['Primeiro ano', 'Segundo ano', 'Terceiro ano']
    ETurma = ttk.Combobox(frameDireita, width=23, values=lista_turmas, font=('Ivy 10'), state='disabled')
    ETurma.grid(row=5, column=1, padx=5, pady=10, sticky="ew")
    
    LTel = tk.Label(frameDireita, text="Telefone", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LTel.grid(row=6, column=0, padx=5, pady=10, sticky="w")
    ETel = tk.Entry(frameDireita, width=25, justify='left', relief="solid", state='disabled')
    ETel.grid(row=6, column=1, padx=5, pady=10, sticky="ew") 
    
    LEndereco = tk.Label(frameDireita, text="Endereço", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LEndereco.grid(row=7, column=0, padx=5, pady=10, sticky="w")
    EEndereco = tk.Entry(frameDireita, width=25, justify='left', relief="solid", state='disabled')
    EEndereco.grid(row=7, column=1, padx=5, pady=10, sticky="ew")

    LEmail = tk.Label(frameDireita, text="Email", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LEmail.grid(row=8, column=0, padx=5, pady=10, sticky="w")
    EEmail = tk.Entry(frameDireita, width=25, justify='left', relief="solid", state='disabled')
    EEmail.grid(row=8, column=1, padx=5, pady=10, sticky="ew")
    
    b_salvar = tk.Button(frameDireita, command=salvar_alteracoes, text=' Salvar Alterações', bg=co1, fg=co0, font=('Ivy 11 bold'))
    b_salvar.grid(row=9, column=1, sticky="w", padx=5, pady=20) 

# --- (NOVO) Excluir Cadastro (USUÁRIO) ---
def Excluir_cadastro():

    def deletar_usuario_agora():
        try:
            usuario_str = EUsuario.get()
            if not usuario_str or usuario_str == 'Selecione o usuário':
                messagebox.showerror('Erro', 'Selecione um usuário para excluir')
                return
            
            id_usuario = int(usuario_str.split(':')[0])
            nome_usuario = usuario_str.split(':')[1]

            if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o usuário:\n\n{nome_usuario}\n\nEsta ação não pode ser desfeita."):
                delete_user(id_usuario)
                messagebox.showinfo('Sucesso', 'Usuário excluído com sucesso!')
                # Recarregar a tela
                control('Excluir cadastro')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível excluir: {e}')

    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    for i in range(4): frameDireita.grid_rowconfigure(i, weight=0)

    app_ = tk.Label(frameDireita, text="Excluir Usuário", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=2, sticky="ew")
    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
    
    LUsuario = tk.Label(frameDireita, text="Selecione o Usuário:", font=('Verdana 12'), bg=co12, fg=co0)
    LUsuario.grid(row=2, column=0, padx=5, pady=10, sticky="w")
    
    lista_usuarios = get_all_usuarios()
    EUsuario = ttk.Combobox(frameDireita, width=40, values=lista_usuarios, font=('Ivy 10'), state='readonly')
    EUsuario.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
    EUsuario.set('Selecione o usuário')
    
    b_excluir = tk.Button(frameDireita, command=deletar_usuario_agora, text='Excluir Usuário', bg=co1, fg=co0, font=('Ivy 11 bold'))
    b_excluir.grid(row=3, column=1, padx=5, pady=20, sticky="w")

# --- (NOVO) Alterar LIVRO ---
def Alterar_livro():
    
    # (Funções internas 'carregar_livro' e 'salvar_livro' - similar ao Alterar_cadastro)
    # ... (Para economizar espaço, esta é uma cópia de Alterar_cadastro, mas para livros) ...
    
    def carregar_livro():
        try:
            livro_str = ELivro.get()
            if not livro_str or livro_str == 'Selecione o livro': return
            id_livro = int(livro_str.split(':')[0])
            dados = get_book_by_id(id_livro) # [1]=titulo, [2]=autor, [3]=editora, [4]=ano, [5]=isbn

            ETitulo.config(state='normal'); ETitulo.delete(0, tk.END); ETitulo.insert(0, dados[1])
            EAutor.config(state='normal'); EAutor.delete(0, tk.END); EAutor.insert(0, dados[2])
            EEditora.config(state='normal'); EEditora.delete(0, tk.END); EEditora.insert(0, dados[3])
            EAno.config(state='normal'); EAno.delete(0, tk.END); EAno.insert(0, str(dados[4]))
            EIsbn.config(state='normal'); EIsbn.delete(0, tk.END); EIsbn.insert(0, dados[5])
            b_salvar.config(state='normal')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar: {e}')

    def salvar_livro():
        try:
            id_livro = int(ELivro.get().split(':')[0])
            titulo = ETitulo.get()
            autor = EAutor.get()
            editora = EEditora.get()
            ano = EAno.get()
            isbn = EIsbn.get()

            if not titulo or not autor:
                messagebox.showerror('Erro', 'Título e Autor são obrigatórios')
                return

            update_book(id_livro, titulo, autor, editora, ano, isbn)
            messagebox.showinfo('Sucesso', 'Livro atualizado com sucesso!')
            control('Alterar livro')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível salvar: {e}')

    frameDireita.grid_columnconfigure(0, weight=0); frameDireita.grid_columnconfigure(1, weight=1)
    for i in range(10): frameDireita.grid_rowconfigure(i, weight=0)

    app_ = tk.Label(frameDireita, text="Alterar Cadastro de Livro", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=2, sticky="ew")

    # Seletor
    LLivro = tk.Label(frameDireita, text="Selecione o Livro:", font=('Verdana 12'), bg=co12, fg=co0)
    LLivro.grid(row=1, column=0, padx=5, pady=10, sticky="w")
    lista_livros = get_all_livros()
    ELivro = ttk.Combobox(frameDireita, width=40, values=lista_livros, font=('Ivy 10'), state='readonly')
    ELivro.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
    ELivro.set('Selecione o livro')
    b_carregar = tk.Button(frameDireita, command=carregar_livro, text='Carregar Dados', bg=co1, fg=co0, font=('Ivy 10 bold'))
    b_carregar.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    app_linha = tk.Label(frameDireita, height=1, font=('Ivy 1'), bg=co3)
    app_linha.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)

    # Campos
    LTitulo = tk.Label(frameDireita, text="Título *", font=('Verdana 12'), bg=co12, fg=co0)
    LTitulo.grid(row=4, column=0, padx=5, pady=10, sticky="w")
    ETitulo = tk.Entry(frameDireita, width=25, relief="solid", state='disabled')
    ETitulo.grid(row=4, column=1, padx=5, pady=10, sticky="ew")
    
    LAutor = tk.Label(frameDireita, text="Autor *", font=('Verdana 12'), bg=co12, fg=co0)
    LAutor.grid(row=5, column=0, padx=5, pady=10, sticky="w")
    EAutor = tk.Entry(frameDireita, width=25, relief="solid", state='disabled')
    EAutor.grid(row=5, column=1, padx=5, pady=10, sticky="ew")
    
    LEditora = tk.Label(frameDireita, text="Editora", font=('Verdana 12'), bg=co12, fg=co0)
    LEditora.grid(row=6, column=0, padx=5, pady=10, sticky="w")
    EEditora = tk.Entry(frameDireita, width=25, relief="solid", state='disabled')
    EEditora.grid(row=6, column=1, padx=5, pady=10, sticky="ew") 
    
    LAno = tk.Label(frameDireita, text="Ano", font=('Verdana 12'), bg=co12, fg=co0)
    LAno.grid(row=7, column=0, padx=5, pady=10, sticky="w")
    EAno = tk.Entry(frameDireita, width=25, relief="solid", state='disabled')
    EAno.grid(row=7, column=1, padx=5, pady=10, sticky="w")

    LIsbn = tk.Label(frameDireita, text="ISBN", font=('Verdana 12'), bg=co12, fg=co0)
    LIsbn.grid(row=8, column=0, padx=5, pady=10, sticky="w")
    EIsbn = tk.Entry(frameDireita, width=25, relief="solid", state='disabled')
    EIsbn.grid(row=8, column=1, padx=5, pady=10, sticky="w")
    
    b_salvar = tk.Button(frameDireita, command=salvar_livro, text=' Salvar Alterações', bg=co1, fg=co0, font=('Ivy 11 bold'))
    b_salvar.grid(row=9, column=1, sticky="w", padx=5, pady=20) 

# --- (NOVO) Excluir Livro ---
def Excluir_livro():

    def deletar_livro_agora():
        try:
            livro_str = ELivro.get()
            if not livro_str or livro_str == 'Selecione o livro':
                messagebox.showerror('Erro', 'Selecione um livro para excluir')
                return
            
            id_livro = int(livro_str.split(':')[0])
            nome_livro = livro_str.split(':')[1]

            if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o livro:\n\n{nome_livro}\n\nEsta ação não pode ser desfeita."):
                delete_book(id_livro)
                messagebox.showinfo('Sucesso', 'Livro excluído com sucesso!')
                control('Excluir livro')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível excluir: {e}')

    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    for i in range(4): frameDireita.grid_rowconfigure(i, weight=0)

    app_ = tk.Label(frameDireita, text="Excluir Livro", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=2, sticky="ew")
    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
    
    LLivro = tk.Label(frameDireita, text="Selecione o Livro:", font=('Verdana 12'), bg=co12, fg=co0)
    LLivro.grid(row=2, column=0, padx=5, pady=10, sticky="w")
    
    lista_livros = get_all_livros()
    ELivro = ttk.Combobox(frameDireita, width=40, values=lista_livros, font=('Ivy 10'), state='readonly')
    ELivro.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
    ELivro.set('Selecione o livro')
    
    b_excluir = tk.Button(frameDireita, command=deletar_livro_agora, text='Excluir Livro', bg=co1, fg=co0, font=('Ivy 11 bold'))
    b_excluir.grid(row=3, column=1, padx=5, pady=20, sticky="w")
    
    # Livro
    LLivro = tk.Label(frameDireita, text="Livro *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LLivro.grid(row=2, column=0, padx=5, pady=10, sticky="w")
    livros_disponiveis = get_all_livros() # <--- Chama a nova função
    ELivro = ttk.Combobox(frameDireita, width=40, values=livros_disponiveis, font=('Ivy 10'), state='readonly')
    ELivro.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
    ELivro.set('Selecione o livro')
# --- (NOVO) Realizar DEVOLUÇÃO ---
def realizar_devolucao():

    def add_devolucao():
        try:
            emprestimo_str = EEmprestimo.get()
            data_dev = EData.get()

            if not emprestimo_str or not data_dev or emprestimo_str == 'Selecione o empréstimo':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return

            id_emprestimo = int(emprestimo_str.split(':')[0])

            devolver_livro(id_emprestimo, data_dev)
            messagebox.showinfo('Sucesso', 'Devolução registrada com sucesso!')
            
            # Recarregar a lista de empréstimos ativos
            EEmprestimo['values'] = get_active_loans()
            EEmprestimo.set('Selecione o empréstimo')
            EData.delete(0, tk.END)
            EData.insert(0, datetime.now().strftime("%d-%m-%Y"))

        except Exception as e:
            messagebox.showerror('Erro', f'Ocorreu um erro: {e}')
            
    for i in range(5):
        frameDireita.grid_columnconfigure(i, weight=0)
    for i in range(7):
        frameDireita.grid_rowconfigure(i, weight=0)
        
    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    
    app_ = tk.Label(frameDireita, text="Realizar Devolução", padx=5, pady=5, font=('Verdana 14'), bg=co12, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=2, sticky="ew")
    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

    # Empréstimo Ativo
    LEmprestimo = tk.Label(frameDireita, text="Empréstimo *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LEmprestimo.grid(row=2, column=0, padx=5, pady=10, sticky="w")
    emprestimos_ativos = get_active_loans() # <--- Chama a nova função
    EEmprestimo = ttk.Combobox(frameDireita, width=40, values=emprestimos_ativos, font=('Ivy 10'), state='readonly')
    EEmprestimo.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
    EEmprestimo.set('Selecione o empréstimo')

    # Data Devolução
    LData = tk.Label(frameDireita, text="Data Devolução *", font=('Verdana 12'), bg=co12, fg=co0, anchor=tk.NW)
    LData.grid(row=3, column=0, padx=5, pady=10, sticky="w")
    EData = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EData.grid(row=3, column=1, padx=5, pady=10, sticky="w")
    EData.insert(0, datetime.now().strftime("%d-%m-%Y")) # <--- Preenche data de hoje

    try:
        img_salvar = Image.open(resource_path("assets/save.png"))
        img_salvar = img_salvar.resize((18, 18))
        img_salvar = ImageTk.PhotoImage(img_salvar)
    except FileNotFoundError:
        img_salvar = None

    b_salvar = tk.Button(frameDireita, command=add_devolucao, image=img_salvar, compound=tk.LEFT, anchor=tk.CENTER,
                         text=' Salvar Devolução', bg=co1, fg=co0, font=('Ivy 11 bold'), overrelief="ridge", relief="groove")
    b_salvar.grid(row=4, column=1, sticky="w", padx=5, pady=20) 
    if img_salvar:
        b_salvar.image = img_salvar
# ============== TELA INICIAL =====================

# ===================================================================
# (COLE ESTA FUNÇÃO JUNTO COM AS OUTRAS)
# ===================================================================
# ===================================================================
# (FUNÇÃOmostrar_tela_inicial MODIFICADA)
# ===================================================================

def mostrar_tela_inicial():
    # --- Limpa o frameDireita ---
    for widget in frameDireita.winfo_children():
        widget.destroy()

    # --- REINICIA A CONFIGURAÇÃO DO GRID ---
    for i in range(10): 
        frameDireita.grid_columnconfigure(i, weight=0)
        frameDireita.grid_rowconfigure(i, weight=0)

    # --- Configura o fundo do frameDireita para a tela inicial ---
    # Usaremos um verde mais claro para o fundo da logo, se você definiu co12
    frameDireita.config(bg=co12) # Use co12 ou a cor que preferir

    # --- Cria um Canvas para desenhar a logo ---
    canvas = tk.Canvas(frameDireita, bg=co12, highlightthickness=0) # Sem borda
    canvas.pack(expand=True, padx=20, pady=20) # Centraliza o canvas e dá um respiro

    # --- Desenha a logo do Instituto Federal ---
    # Define o tamanho dos quadrados e o espaçamento
    quad_size = 40
    spacing = 10
    red_circle_radius = quad_size / 2 # Raio do círculo
    
    # Cores
    color_green = "#2bb937" # Seu co9 (verde mais forte)
    color_red = "#e06636"   # Seu co5 (vermelho)
    color_transparent = "#ff0000ff"

    # Função auxiliar para desenhar um quadrado
    def draw_square(x, y, color):
        canvas.create_rectangle(x, y, x + quad_size, y + quad_size, fill=color, outline=color)

    # Define a posição inicial para o desenho (para centralizar o conjunto da logo)
    # A logo tem 3 colunas de quadrados (mais o círculo) e 4 linhas
    # Largura total = 3*quad_size + 2*spacing
    # Altura total = 4*quad_size + 3*spacing
    
    # Ajuste para centralizar:
    total_width = 3 * quad_size + 2 * spacing
    total_height = 4 * quad_size + 3 * spacing
    
    # Posiciona o desenho no centro do canvas
    # (canvas.winfo_width() e canvas.winfo_height() podem não estar disponíveis
    #  imediatamente, então ajustamos o posicionamento depois ou centralizamos no pack)
    # Vamos usar um ponto de partida fixo e o pack/expand irá centralizar o canvas.
    start_x = 120 # Relativo ao canvas
    start_y = 0 # Relativo ao canvas

    # --- Primeira Linha ---
    # Círculo Vermelho
    canvas.create_oval(
        start_x, start_y, 
        start_x + red_circle_radius * 2, start_y + red_circle_radius * 2, 
        fill=color_red, outline=color_red
    )
    
    # Quadrados Verdes
    draw_square(start_x + quad_size + spacing, start_y, color_green)
    draw_square(start_x + 2*(quad_size + spacing), start_y, color_green)

    # --- Segunda Linha ---
    draw_square(start_x, start_y + quad_size + spacing, color_green)
    draw_square(start_x + quad_size + spacing, start_y + quad_size + spacing, color_green)
    draw_square(start_x + 2*(quad_size + spacing), start_y + quad_size + spacing, co12)

    # --- Terceira Linha ---
    draw_square(start_x, start_y + 2*(quad_size + spacing), color_green)
    draw_square(start_x + quad_size + spacing, start_y + 2*(quad_size + spacing), color_green)
    draw_square(start_x + 2*(quad_size + spacing), start_y + 2*(quad_size + spacing), color_green)

    # --- Quarta Linha ---
    draw_square(start_x, start_y + 3*(quad_size + spacing), color_green)
    draw_square(start_x + quad_size + spacing, start_y + 3*(quad_size + spacing), color_green)
    
    # --- IMPORTANTE: Certifique-se de que a imagem da logo anterior não está sendo carregada aqui ---
    # Se você tinha um Label com image no mostrar_tela_inicial, remova-o.
    # Apenas o canvas deve estar no pack.
# ===================================================================
# FUNÇÃO DE CONTROLE PRINCIPAL
# ===================================================================
      
def control(i):
    # Limpa o frameDireita antes de carregar a nova tela
    for widget in frameDireita.winfo_children():
        widget.destroy()

    if i == 'Novo cadastro':
        Novo_cadastro()
    elif i == 'Novo Livro':
        Novo_livro()
    elif i == 'Consultar Livros':
        ver_livros()
    elif i == 'Consultar pessoas cadastradas':
        ver_usuarios()
    elif i == 'Consultar empréstimos':
        ver_emprestimos()
    elif i == 'Realizar empréstimo':
        realizar_emprestimo()
    elif i == 'Devolução':
        realizar_devolucao()
    
    # --- NOVOS COMANDOS ADICIONADOS ---
    elif i == 'Alterar cadastro':
        Alterar_cadastro()
    elif i == 'Excluir cadastro':
        Excluir_cadastro()
    elif i == 'Alterar livro':
        Alterar_livro()
    elif i == 'Excluir livro':
        Excluir_livro()
# ===================================================================
# MENU (Botões da Esquerda) - AGORA COM COMANDOS
# ===================================================================

# NOVO USUARIO
img_usuario = Image.open(resource_path("assets/plus.png"))
img_usuario = img_usuario.resize((18, 18))
img_usuario = ImageTk.PhotoImage(img_usuario)
b_usuario = tk.Button(frameEsquerda, command=lambda:control('Novo cadastro'),image=img_usuario, compound=tk.LEFT, anchor=tk.NW, text='Novo cadastro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_usuario.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=6)
# NOVO LIVRO
img_livro = Image.open(resource_path("assets/plus.png"))
img_livro = img_livro.resize((18, 18))
img_livro = ImageTk.PhotoImage(img_livro)
b_livro = tk.Button(frameEsquerda, command=lambda:control('Novo Livro'), image=img_livro, compound=tk.LEFT, anchor=tk.NW, text='Novo Livro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_livro.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER LIVROS
img_ver = Image.open(resource_path("assets/icons8-book-100.png"))
img_ver = img_ver.resize((18, 18))
img_ver = ImageTk.PhotoImage(img_ver)
b_ver = tk.Button(frameEsquerda, command=lambda:control('Consultar Livros'), image=img_ver, compound=tk.LEFT, anchor=tk.NW, text='Consultar Livros', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_ver.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER USUARIOS
img_verUser = Image.open(resource_path("assets/pessoa.png"))
img_verUser = img_verUser.resize((18, 18))
img_verUser = ImageTk.PhotoImage(img_verUser)
b_verUser = tk.Button(frameEsquerda, command=lambda:control('Consultar pessoas cadastradas'), image=img_verUser, compound=tk.LEFT, anchor=tk.NW, text='Consultar pessoas cadastradas', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_verUser.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER EMPRESTIMOS
img_verempresta = Image.open(resource_path("assets/consulta.png"))
img_verempresta = img_verempresta.resize((18, 18))
img_verempresta = ImageTk.PhotoImage(img_verempresta)
b_verempresta = tk.Button(frameEsquerda, command=lambda:control('Consultar empréstimos'), image=img_verempresta, compound=tk.LEFT, anchor=tk.NW, text='Consultar empréstimos', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_verempresta.grid(row=4, column=0, sticky=tk.NSEW, padx=5, pady=6)
# EMPRESTIMO
img_empresta = Image.open(resource_path("assets/emprestar.png"))
img_empresta = img_empresta.resize((18, 18))
img_empresta = ImageTk.PhotoImage(img_empresta)
b_empresta = tk.Button(frameEsquerda, command=lambda:control('Realizar empréstimo'), image=img_empresta, compound=tk.LEFT, anchor=tk.NW, text='Realizar empréstimo', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_empresta.grid(row=6, column=0, sticky=tk.NSEW, padx=5, pady=6)
# DEVOLUCAO
img_devolve = Image.open(resource_path("assets/icons8-reload-100.png"))
img_devolve = img_devolve.resize((18, 18))
img_devolve = ImageTk.PhotoImage(img_devolve)
b_devolve = tk.Button(frameEsquerda, command=lambda:control('Devolução'), image=img_devolve, compound=tk.LEFT, anchor=tk.NW, text='Devolução', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_devolve.grid(row=7, column=0, sticky=tk.NSEW, padx=5, pady=6)
# ------- novo --------
# ===================================================================
# MENU (Botões da Esquerda) - (COLE NO FINAL)
# ===================================================================

# (Botão de Devolução ... )
b_devolve.grid(row=7, column=0, sticky=tk.NSEW, padx=5, pady=6)

# --- (NOVOS BOTÕES) ---

# ALTERAR USUARIO
# (Vou usar 'edit.png' e 'delete.png', troque se o nome for diferente)
try:
    img_edit = Image.open(resource_path("assets/edit.png")) # Assumindo que você tem 'edit.png'
    img_edit = img_edit.resize((18, 18))
    img_edit = ImageTk.PhotoImage(img_edit)
except:
    img_edit = img_usuario # Reutiliza a imagem 'plus' se não achar

b_alterar_usuario = tk.Button(frameEsquerda, command=lambda:control('Alterar cadastro'),image=img_edit, compound=tk.LEFT, anchor=tk.NW, text='Alterar cadastro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_alterar_usuario.grid(row=8, column=0, sticky=tk.NSEW, padx=5, pady=6)

# EXCLUIR USUARIO
try:
    img_delete = Image.open(resource_path("assets/delete.png")) # Assumindo que você tem 'delete.png'
    img_delete = img_delete.resize((18, 18))
    img_delete = ImageTk.PhotoImage(img_delete)
except:
    img_delete = img_usuario # Reutiliza a imagem 'plus' se não achar

b_excluir_usuario = tk.Button(frameEsquerda, command=lambda:control('Excluir cadastro'),image=img_delete, compound=tk.LEFT, anchor=tk.NW, text='Excluir cadastro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_excluir_usuario.grid(row=9, column=0, sticky=tk.NSEW, padx=5, pady=6)

# ALTERAR LIVRO
b_alterar_livro = tk.Button(frameEsquerda, command=lambda:control('Alterar livro'),image=img_edit, compound=tk.LEFT, anchor=tk.NW, text='Alterar livro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_alterar_livro.grid(row=10, column=0, sticky=tk.NSEW, padx=5, pady=6)

# EXCLUIR LIVRO
b_excluir_livro = tk.Button(frameEsquerda, command=lambda:control('Excluir livro'),image=img_delete, compound=tk.LEFT, anchor=tk.NW, text='Excluir livro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_excluir_livro.grid(row=11, column=0, sticky=tk.NSEW, padx=5, pady=6)
# --- Inicia a aplicação ---
mostrar_tela_inicial()
janela.mainloop()