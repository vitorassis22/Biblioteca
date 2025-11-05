# Importar Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.constants import FALSE 
from tkinter import messagebox
# Importar pillow
from PIL import Image, ImageTk
# Importar as funcoes da view
from view import *
# --- cores ---
co0 = "black" # Preto
co1 = "white"   # Branco
co2 = "#4fa882" # Verde
co3 = "#000000" # Valor
co4 = "tan3" # Letra
co5 = "#e06636" # - profit
co6 = "seagreen4"
co7 = "green1"  # Verde
co8 = "burlywood2" # + Verde
co9 = "#2bb937" # + Verde
co10 = "#0f7be7"
co11 = "white"
# --- Criando janela ---
janela = tk.Tk() # Usando tk.Tk()
janela.title("") # Titulo
janela.geometry('720x480') # Tamanho
janela.configure(background=co1) # Cor de fundo
janela.resizable(width=FALSE, height=FALSE) # Nao ajustavel
style = ttk.Style(janela) # Usando ttk.Style()
style.theme_use("clam")
# ----- CONFIGURANDO O GRID DA JANELA -----
# Diz à janela que a COLUNA 1 (a da direita/conteúdo) deve se expandir
janela.grid_columnconfigure(1, weight=1) 
# Diz à janela que a LINHA 1 (abaixo do header) deve se expandir
janela.grid_rowconfigure(1, weight=1)
# ----- FRAMES -----
# Frame de Cima (Header)
# Está na linha 0 e ocupa as colunas 0 e 1 (columnspan=2)
frameCima = tk.Frame(janela, height=50, bg=co11, relief="flat")
frameCima.grid(row=0, column=0, columnspan=2, sticky="ew")
# Frame da Esquerda (Sidebar)
# 1. Colocado na column=0
frameEsquerda = tk.Frame(janela, bg=co8, relief="flat")
frameEsquerda.grid(row=1, column=0, sticky="nsew") # "ns" = esticar Norte-Sul (vertical)
# ---- FRAME DA DIREITA PARA CONTEÚDO ----
frameDireita = tk.Frame(janela, bg=co2, relief="flat")
frameDireita.grid(row=1, column=1, sticky="nsew") # "nsew" = esticar em todas as direções
# -------- LOGO --------
# 1. Carrega com Pillow (Image.open)
img = Image.open("icons8-book-100.png")
img = img.resize((40, 40))
# 2. Converte para o Tkinter (ImageTk.PhotoImage)
app_img = ImageTk.PhotoImage(img)
# 3. Cria o Label COM IMAGEM E TEXTO
app_logo = tk.Label(
    frameCima,
    text="Sistema de Gerenciamento para Biblioteca", # <--- ADICIONE SEU TEXTO AQUI
    image=app_img,
    bg=co11,                           # Cor de fundo do label (mesma do frame)
    compound=tk.LEFT,                 # Coloca a imagem à esquerda do texto
    padx=10,                          # Espaço extra nas laterais
    anchor=tk.W,                      # Alinha o conteúdo à esquerda (W = West)
    font=('Verdana', 16, 'bold'),     # Define a fonte do texto
    fg=co0                           # Define a cor do texto (usei sua cor 'Letra')
)
# 4. "Ancora" a imagem para evitar o bug do garbage collector
app_logo.image = app_img
# 5. Coloca o label na tela (dentro do frameCima)
# fill=tk.Y para o label preencher a altura do frame
app_logo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
app_linha = tk.Label(frameCima, width=1080, height=1, padx=5, anchor=tk.NW, font=('Verdana 1'), bg=co3, fg=co1) # linha abaixo do texto
app_linha.place(x=0, y=50)
# Inserir novo cadastro
def Novo_cadastro(): 
    
    # --- FUNÇÃO INTERNA 'add' ---
    def add():
        nome = ENome.get()
        turma = ETurma.get()
        telefone = ETel.get()
        endereco = EEndereco.get()
        email = EEmail.get()

        # --- CORREÇÃO AQUI ---
        # A lista de verificação agora só contém os campos obrigatórios
        lista_obrigatoria = [nome, turma]
        
        # Verificando caso algum campo OBRIGATÓRIO esteja vazio
        for i in lista_obrigatoria:
            if i=='' or i=='Selecione a turma': # Adiciona verificação do Combobox
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
        
        # Inserir os dados no banco (a função insert_user ainda recebe todos)
        insert_user(nome, turma, endereco, email, telefone) 
        
        messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso!')

        # Limpando as entradas
        ENome.delete(0,tk.END)
        ETurma.set('Selecione a turma') # Limpa o combobox
        ETel.delete(0,tk.END)
        EEndereco.delete(0,tk.END)
        EEmail.delete(0,tk.END)
        
    # --- CONFIGURAÇÃO DO GRID ---
    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    frameDireita.grid_columnconfigure(2, weight=0)
    frameDireita.grid_columnconfigure(3, weight=1)
    
    # --- TÍTULO ---
    app_ = tk.Label(frameDireita, text="Inserir novo cadastro", padx=5, pady=5, font=('Verdana 14'), bg=co2, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=4, sticky="ew")

    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
    
    # --- NOME (Obrigatório) ---
    # Adicionado '*' ao texto
    LNome = tk.Label(frameDireita, text="Nome *", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    LNome.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

    ENome = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    ENome.grid(row=2, column=1, padx=5, pady=10, sticky=tk.NSEW)
    
    # --- TURMA (Obrigatório) ---
    # Adicionado '*' ao texto
    LTurma = tk.Label(frameDireita, text="Turma *", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    LTurma.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

    lista_turmas = ['Primeiro ano', 'Segundo ano', 'Terceiro ano']
    ETurma = ttk.Combobox(frameDireita, width=23, values=lista_turmas, font=('Ivy 10'), state='readonly')
    ETurma.grid(row=3, column=1, padx=5, pady=10, sticky=tk.NSEW)
    ETurma.set('Selecione a turma') 
    
    # --- Telefone (Opcional) ---
    LTel = tk.Label(frameDireita, text="Telefone", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    LTel.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

    ETel = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    ETel.grid(row=4, column=1, padx=5, pady=10, sticky=tk.NSEW) 
    
    # --- Endereço (Opcional) ---
    LEndereco = tk.Label(frameDireita, text="Endereço", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    LEndereco.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

    EEndereco = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EEndereco.grid(row=5, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)

    # --- Email (Opcional) ---
    LEmail = tk.Label(frameDireita, text="Email", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    LEmail.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

    EEmail = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    EEmail.grid(row=6, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)
    
    # --- Botao salvar ---
    try:
        img_salvar = Image.open("save.png")
        img_salvar = img_salvar.resize((18, 18))
        img_salvar = ImageTk.PhotoImage(img_salvar)
    except FileNotFoundError:
        print("Aviso: 'save.png' não encontrado. Botão salvará sem imagem.")
        img_salvar = None

    b_salvar = tk.Button(frameDireita,
                         command=add,      # Salvar no banco
                         image=img_salvar,
                         compound=tk.LEFT,
                         anchor=tk.CENTER,
                         text=' Salvar', 
                         bg=co1,
                         fg=co0,
                         font=('Ivy 11'),
                         overrelief="ridge",
                         relief="groove")

    b_salvar.grid(row=7, column=1, sticky="ew", padx=5, pady=20) 
    
    if img_salvar:
        b_salvar.image = img_salvar

# ------- Cadastrar livro ---------
def Novo_livro(): 
    
    # --- FUNÇÃO INTERNA 'add' ---
    def add():
        titulo = Etitulo.get()
        autor = Eautor.get()
        editora = Eeditora.get()
        ano_publicacao = Eano_publicacao.get()
        isbn = Eisbn.get()

        # --- CORREÇÃO AQUI ---
        # A lista de verificação agora só contém os campos obrigatórios
        lista_obrigatoria = [titulo, autor, editora, ano_publicacao, ibsn]
        
        # Verificando caso algum campo OBRIGATÓRIO esteja vazio
        for i in lista_obrigatoria:
            if i=='': # Adiciona verificação do Combobox
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
        
        # Inserir os dados no banco (a função insert_user ainda recebe todos)
        insert_book(titulo, autor, editora, ano_publicacao, ibsn) 
        
        messagebox.showinfo('Sucesso', 'Livro cadastrado com sucesso!')

        # Limpando as entradas
        Etitulo.delete(0,tk.END)
        Eautor.delete(0,tk.END)
        Eeditora.delete(0,tk.END)
        Eano_publicacao.delete(0,tk.END)
        Eisbn.delete(0,tk.END)
        
    # --- CONFIGURAÇÃO DO GRID ---
    frameDireita.grid_columnconfigure(0, weight=0) 
    frameDireita.grid_columnconfigure(1, weight=1)
    frameDireita.grid_columnconfigure(2, weight=0)
    frameDireita.grid_columnconfigure(3, weight=1)
    
    # --- TÍTULO ---
    app_ = tk.Label(frameDireita, text="Inserir novo livro", padx=5, pady=5, font=('Verdana 14'), bg=co2, fg=co0, anchor=tk.CENTER)
    app_.grid(row=0, column=0, columnspan=4, sticky="ew")

    app_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Ivy 1'), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
    
    # --- TITULO (Obrigatório) ---
    Ltitulo = tk.Label(frameDireita, text="Título *", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    Ltitulo.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

    Etitulo = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    Etitulo.grid(row=2, column=1, padx=5, pady=10, sticky=tk.NSEW)
    
    # --- Autor (Obrigatório) ---
    Lautor = tk.Label(frameDireita, text="Autor *", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    Lautor.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

    Eautor = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    Eautor.grid(row=3, column=1, padx=5, pady=10, sticky=tk.NSEW)

    # --- Editora (Obrigatório) ---
    Leditora = tk.Label(frameDireita, text="Editora *", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    Leditora.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

    Eeditora = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    Eeditora.grid(row=4, column=1, padx=5, pady=10, sticky=tk.NSEW) 
    
   # --- Ano de publicação (Obrigatório) ---
    Lano_publicacao = tk.Label(frameDireita, text="Ano de publicação *", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    Lano_publicacao.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

    Eano_publicacao = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    Eano_publicacao.grid(row=5, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)

    # --- isbn (Obrigatório) ---
    Lisbn = tk.Label(frameDireita, text="ISBN *", font=('Verdana 12'), bg=co2, fg=co0, anchor=tk.NW)
    Lisbn.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

    Eisbn = tk.Entry(frameDireita, width=25, justify='left', relief="solid")
    Eisbn.grid(row=6, column=1, columnspan=3, padx=5, pady=10, sticky=tk.NSEW)
    
    # --- Botao salvar ---
    try:
        img_salvar = Image.open("save.png")
        img_salvar = img_salvar.resize((18, 18))
        img_salvar = ImageTk.PhotoImage(img_salvar)
    except FileNotFoundError:
        print("Aviso: 'save.png' não encontrado. Botão salvará sem imagem.")
        img_salvar = None

    b_salvar = tk.Button(frameDireita,
                         command=add,      # Salvar no banco
                         image=img_salvar,
                         compound=tk.LEFT,
                         anchor=tk.CENTER,
                         text=' Salvar', 
                         bg=co1,
                         fg=co0,
                         font=('Ivy 11'),
                         overrelief="ridge",
                         relief="groove")

    b_salvar.grid(row=7, column=1, sticky="ew", padx=5, pady=20) 
    
    if img_salvar:
        b_salvar.image = img_salvar
    # --- Botao salvar ---
    try:
        img_salvar = Image.open("save.png")
        img_salvar = img_salvar.resize((18, 18))
        img_salvar = ImageTk.PhotoImage(img_salvar)
    except FileNotFoundError:
        print("Aviso: 'save.png' não encontrado. Botão salvará sem imagem.")
        img_salvar = None # Define como None se não encontrar

    b_salvar = tk.Button(frameDireita,
                         command=add,      # Salvar no banco
                         image=img_salvar,
                         compound=tk.LEFT,
                         anchor=tk.CENTER,
                         text=' Salvar', # Adicionei um espaço
                         bg=co1,
                         fg=co0,
                         font=('Ivy 11'),
                         overrelief="ridge",
                         relief="groove")

    # Mudei a linha do botão de 6 para 7
    b_salvar.grid(row=7, column=1, sticky="ew", padx=5, pady=20) # Aumentei pady
    
    if img_salvar:
        b_salvar.image = img_salvar

# Ver usuarios
def ver_usuarios():
    
    app_ = tk.Label(frameDireita,text="Todos os usuários cadastrados",compound=tk.N, padx=5, pady=5, relief=tk.FLAT, anchor=tk.CENTER, font=('Verdana 12'),bg=co1, fg=co0)
    app_.grid(row=0, column=0, columnspan=3, sticky=tk.EW)
    l_linha = tk.Label(frameDireita, anchor=tk.NW, font=('Verdana 1 '), bg=co6, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
    dados = listar_usuarios()
    # creating a treeview with dual scrollbars
    list_header = ['id','nome','turma','endereço','email','telefone']
    
    global tree

    tree = ttk.Treeview(frameDireita, selectmode="extended",
                        columns=list_header, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew')
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, sticky='ew')
    frameDireita.grid_rowconfigure(0, weight=12)

    hd=["nw","nw","nw","nw","nw","nw"]
    h=[20,80,80,120,120,76,100]
    n=0

    for col in list_header:
        tree.heading(col, text=col, anchor='nw')
        #adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in dados:
        tree.insert('', 'end', values=item)

def ver_usuarios():
    
    # --- Configuração das colunas do frameDireita para o Treeview ---
    # É importante redefinir o grid_columnconfigure aqui para o layout do Treeview
    # Coluna 0 (Treeview) deve expandir
    frameDireita.grid_columnconfigure(0, weight=1) 
    # Coluna 1 (Scrollbar vertical) não expande
    frameDireita.grid_columnconfigure(1, weight=0) 
    # Linha 2 (Treeview) deve expandir
    frameDireita.grid_rowconfigure(2, weight=1) 

    # --- TÍTULO (ajustado para ter o mesmo estilo) ---
    app_ = tk.Label(frameDireita, text="Todos os usuários cadastrados", 
                    padx=5, pady=10, 
                    font=('Verdana 14'), # Usei o mesmo font size do "Inserir novo cadastro"
                    bg=co2,              # <--- CORREÇÃO: Fundo verde para combinar com o frameDireita
                    fg=co0, 
                    anchor=tk.CENTER)    # <--- CORREÇÃO: Centraliza o texto
    app_.grid(row=0, column=0, columnspan=2, sticky="ew") # columnspan 2 para ocupar a coluna do Treeview e da Scrollbar

    # --- LINHA DIVISÓRIA ---
    l_linha = tk.Label(frameDireita, height=1, anchor=tk.NW, font=('Verdana 1 '), bg=co3, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW) # columnspan 2

    # --- DADOS (agora com 'return') ---
    dados = listar_usuarios()
    
    list_header = ['id','nome','turma','endereço','email','telefone']
    
    global tree

    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=list_header, show="headings")
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # --- POSICIONAMENTO DA TABELA E SCROLLBARS ---
    tree.grid(column=0, row=2, sticky='nsew', padx=5, pady=5) # Adicionado padx/pady
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, columnspan=2, sticky='ew', padx=5) # Adicionado padx

    # --- CONFIGURAÇÃO DAS COLUNAS DA TABELA ---
    hd=["nw","nw","nw","nw","nw","nw"]
    h=[20, 80, 80, 120, 120, 100] # Larguras das colunas
    n=0

    for col in list_header:
        tree.heading(col, text=col.title(), anchor='nw') 
        tree.column(col, width=h[n],anchor=hd[n])
        n+=1

    # --- POPULANDO A TABELA ---
    if dados: 
        for item in dados:
            tree.insert('', 'end', values=item)
            
def control(i):
    # novo usuario
    if i == 'Novo cadastro':
        for widget in frameDireita.winfo_children():
            widget.destroy()
        Novo_cadastro()
     # novo usuario
    if i == 'Consultar pessoas cadastradas':
        for widget in frameDireita.winfo_children():
            widget.destroy()
        ver_usuarios()
    if i == 'Novo livro':
        for widget in frameDireita.winfo_children():
            widget.destroy()
        Novo_livro() 
            
# ------------ MENU ------------
# NOVO USUARIO
img_usuario = Image.open("plus.png")
img_usuario = img_usuario.resize((18, 18))
img_usuario = ImageTk.PhotoImage(img_usuario)
b_usuario = tk.Button(frameEsquerda, command=lambda:control('Novo cadastro'),image=img_usuario, compound=tk.LEFT, anchor=tk.NW, text='Novo cadastro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_usuario.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=6)
# NOVO LIVRO
img_livro = Image.open("plus.png")
img_livro = img_livro.resize((18, 18))
img_livro = ImageTk.PhotoImage(img_livro)
b_livro = tk.Button(frameEsquerda, command=lambda:control('Novo livro'), image=img_livro, compound=tk.LEFT, anchor=tk.NW, text='Novo livro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_livro.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER LIVROS
img_ver = Image.open("icons8-book-100.png")
img_ver = img_ver.resize((18, 18))
img_ver = ImageTk.PhotoImage(img_ver)
b_ver = tk.Button(frameEsquerda, image=img_ver, compound=tk.LEFT, anchor=tk.NW, text='Consultar livros', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_ver.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER USUARIOS
img_verUser = Image.open("pessoa.png")
img_verUser = img_verUser.resize((18, 18))
img_verUser = ImageTk.PhotoImage(img_verUser)
b_verUser = tk.Button(frameEsquerda, command=lambda:control('Consultar pessoas cadastradas'), image=img_verUser, compound=tk.LEFT, anchor=tk.NW, text='Consultar pessoas cadastradas', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_verUser.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER EMPRESTIMOS
img_verempresta = Image.open("consulta.png")
img_verempresta = img_verempresta.resize((18, 18))
img_verempresta = ImageTk.PhotoImage(img_verempresta)
b_verempresta = tk.Button(frameEsquerda, image=img_verempresta, compound=tk.LEFT, anchor=tk.NW, text='Consultar empréstimos', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_verempresta.grid(row=4, column=0, sticky=tk.NSEW, padx=5, pady=6)
# EMPRESTIMO
img_empresta = Image.open("emprestar.png")
img_empresta = img_empresta.resize((18, 18))
img_empresta = ImageTk.PhotoImage(img_empresta)
b_empresta = tk.Button(frameEsquerda, image=img_empresta, compound=tk.LEFT, anchor=tk.NW, text='Realizar empréstimo', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_empresta.grid(row=6, column=0, sticky=tk.NSEW, padx=5, pady=6)
# DEVOLUCAO
img_devolve = Image.open("icons8-reload-100.png")
img_devolve = img_devolve.resize((18, 18))
img_devolve = ImageTk.PhotoImage(img_devolve)
b_devolve = tk.Button(frameEsquerda, image=img_devolve, compound=tk.LEFT, anchor=tk.NW, text='Devolução', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_devolve.grid(row=7, column=0, sticky=tk.NSEW, padx=5, pady=6)
janela.mainloop()