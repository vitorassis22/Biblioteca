# Importar Bibliotecas
import sys
import os
import customtkinter as ctk 
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime 
from PIL import Image

# --- Configuração do CustomTkinter ---
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("green") 

# Importar as funcoes da view (Banco de dados)
from view import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CORES ---
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

# --- Criando janela (TAMANHO REDUZIDO) ---
janela = ctk.CTk() 
janela.title("") 
janela.geometry('800x600') # <--- REDUZIDO PARA 800x600
janela.configure(fg_color=co1) 
janela.resizable(width=False, height=False) 

# ----- CONFIGURANDO O GRID DA JANELA -----
janela.grid_columnconfigure(1, weight=1) 
janela.grid_rowconfigure(1, weight=1)

# ----- FRAMES -----
frameCima = ctk.CTkFrame(janela, height=50, fg_color=co11, corner_radius=0)
frameCima.grid(row=0, column=0, columnspan=2, sticky="ew")

frameEsquerda = ctk.CTkFrame(janela, fg_color=co8, corner_radius=0)
frameEsquerda.grid(row=1, column=0, sticky="nsew") 

frameDireita = ctk.CTkFrame(janela, fg_color=co12, corner_radius=0)
frameDireita.grid(row=1, column=1, sticky="nsew") 

# -------- LOGO & IMAGENS --------
def get_ctk_image(filename, size=(20, 20)):
    try:
        img_path = resource_path(f"assets/{filename}")
        return ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=size)
    except:
        return None

logo_img = get_ctk_image("icons8-book-100.png", size=(40, 40))
app_logo = ctk.CTkLabel(
    frameCima,
    text=" Sistema de Gerenciamento para Biblioteca", 
    image=logo_img,
    compound="left",
    font=('Verdana', 18, 'bold'), 
    text_color=co0,
    fg_color="transparent"
)
app_logo.pack(side="left", padx=10, pady=5)

app_linha = ctk.CTkFrame(frameCima, width=800, height=2, fg_color=co3)
app_linha.place(x=0, y=48)

# ===================================================================
# FUNÇÕES AUXILIARES
# ===================================================================

def limpar_frame_direita():
    for widget in frameDireita.winfo_children():
        widget.destroy()
    for i in range(15): frameDireita.grid_rowconfigure(i, weight=0)
    for i in range(5): frameDireita.grid_columnconfigure(i, weight=0)

# ===================================================================
# FUNÇÕES DAS TELAS
# ===================================================================

# --- Inserir novo cadastro ---
def Novo_cadastro(): 
    limpar_frame_direita()
    
    def add():
        nome = ENome.get(); turma = ETurma.get(); telefone = ETel.get()
        endereco = EEndereco.get(); email = EEmail.get()
        lista_obrigatoria = [nome, turma]
        for i in lista_obrigatoria:
            if i=='' or i=='Selecione a turma':
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
        insert_user(nome, turma, endereco, email, telefone) 
        messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso!')
        ENome.delete(0, 'end'); ETel.delete(0, 'end'); EEndereco.delete(0, 'end'); EEmail.delete(0, 'end')
        ETurma.set('Selecione a turma')

    # Layout Centralizado
    frameDireita.grid_columnconfigure(0, weight=1)
    frameDireita.grid_columnconfigure(3, weight=1)

    ctk.CTkLabel(frameDireita, text="Inserir novo cadastro", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=15)
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, columnspan=4, sticky="ew", padx=20)

    ctk.CTkLabel(frameDireita, text="Nome *", font=('Verdana', 14), text_color=co0).grid(row=2, column=1, padx=10, pady=10, sticky="e")
    ENome = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black")
    ENome.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    
    ctk.CTkLabel(frameDireita, text="Turma *", font=('Verdana', 14), text_color=co0).grid(row=3, column=1, padx=10, pady=10, sticky="e")
    ETurma = ctk.CTkOptionMenu(frameDireita, width=250, values=['Sexto ano', 'Sétimo ano', 'Oitavo ano', 'Nono ano'], fg_color="white", text_color="black", state="readonly")
    ETurma.grid(row=3, column=2, padx=10, pady=10, sticky="w"); ETurma.set('Selecione a turma') 
    
    ctk.CTkLabel(frameDireita, text="Telefone", font=('Verdana', 14), text_color=co0).grid(row=4, column=1, padx=10, pady=10, sticky="e")
    ETel = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black")
    ETel.grid(row=4, column=2, padx=10, pady=10, sticky="w") 
    
    ctk.CTkLabel(frameDireita, text="Endereço", font=('Verdana', 14), text_color=co0).grid(row=5, column=1, padx=10, pady=10, sticky="e")
    EEndereco = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black")
    EEndereco.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(frameDireita, text="Email", font=('Verdana', 14), text_color=co0).grid(row=6, column=1, padx=10, pady=10, sticky="e")
    EEmail = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black")
    EEmail.grid(row=6, column=2, padx=10, pady=10, sticky="w")
    
    img_save = get_ctk_image("save.png")
    b_salvar = ctk.CTkButton(frameDireita, command=add, image=img_save, text='SALVAR', font=('Ivy', 14), 
                             fg_color=co1, text_color=co0, hover_color=co1, border_width=1, border_color=co0)
    b_salvar.grid(row=7, column=2, sticky="w", padx=10, pady=20)

# --- Inserir novo LIVRO ---
def Novo_livro():
    limpar_frame_direita()
    
    def add_livro():
        titulo = ETitulo.get(); autor = EAutor.get(); editora = EEditora.get()
        ano = EAno.get(); isbn = EIsbn.get(); origem = Eorigem.get()
        lista_obrigatoria = [titulo, autor, editora, ano, isbn, origem]
        for i in lista_obrigatoria:
            if i=='' or i=='Selecione a origem':
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios (*)')
                return
        insert_book(titulo, autor, editora, ano, isbn, origem) 
        messagebox.showinfo('Sucesso', 'Livro cadastrado com sucesso!')
        ETitulo.delete(0,'end'); EAutor.delete(0,'end'); EEditora.delete(0,'end'); EAno.delete(0,'end'); EIsbn.delete(0,'end')
        Eorigem.set('Selecione a origem')

    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_columnconfigure(3, weight=1)

    ctk.CTkLabel(frameDireita, text="Inserir novo livro", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=15)
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, columnspan=4, sticky="ew", padx=20)
    
    campos = [("Título *", 2), ("Autor *", 3), ("Editora *", 4), ("Ano *", 5), ("ISBN *", 6)]
    entries = {}

    for texto, linha in campos:
        ctk.CTkLabel(frameDireita, text=texto, font=('Verdana', 14), text_color=co0).grid(row=linha, column=1, padx=10, pady=10, sticky="e")
        entry = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black")
        entry.grid(row=linha, column=2, padx=10, pady=10, sticky="w")
        entries[texto] = entry
    
    ETitulo = entries["Título *"]; EAutor = entries["Autor *"]; EEditora = entries["Editora *"]; EAno = entries["Ano *"]; EIsbn = entries["ISBN *"]
    
    ctk.CTkLabel(frameDireita, text="Origem *", font=('Verdana', 14), text_color=co0).grid(row=7, column=1, padx=10, pady=10, sticky="e")
    Eorigem = ctk.CTkOptionMenu(frameDireita, width=250, values=['Doação', 'Governo'], fg_color="white", text_color="black", state="readonly")
    Eorigem.grid(row=7, column=2, padx=10, pady=10, sticky="w"); Eorigem.set('Selecione a origem') 
    
    img_save = get_ctk_image("save.png")
    b_salvar = ctk.CTkButton(frameDireita, command=add_livro, image=img_save, text='SALVAR', font=('Ivy', 14), 
                             fg_color=co1, text_color=co0, hover_color=co1, border_width=1, border_color=co0)
    b_salvar.grid(row=8, column=2, sticky="w", padx=10, pady=20)

# --- Tabela ---
def criar_tabela(headers, columns_width):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=co11, fieldbackground=co11, foreground="black", rowheight=25, font=('Arial', 10))
    style.configure("Treeview.Heading", background=co2, foreground="white", font=('Arial', 10, 'bold'))
    style.map("Treeview", background=[('selected', co6)])

    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=headers, show="headings")
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
    vsb.grid(column=1, row=2, sticky='ns', pady=10)
    hsb.grid(column=0, row=3, sticky='ew', padx=10)

    for col, width in zip(headers, columns_width):
        tree.heading(col, text=col.title(), anchor='nw')
        tree.column(col, width=width, anchor='nw')
    return tree

# --- Ver usuarios ---
def ver_usuarios():
    limpar_frame_direita()
    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_rowconfigure(2, weight=1)

    ctk.CTkLabel(frameDireita, text="Todos os usuários cadastrados", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, pady=10, sticky="ew")
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, sticky="ew", padx=10)

    headers = ['id','nome','turma','endereço','email','telefone']
    widths = [40, 150, 80, 150, 150, 100]
    tree = criar_tabela(headers, widths)
    dados = listar_usuarios()
    if dados:
        for item in dados: tree.insert('', 'end', values=item)

# --- Ver LIVROS ---
def ver_livros():
    limpar_frame_direita()
    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_rowconfigure(2, weight=1)

    ctk.CTkLabel(frameDireita, text="Todos os livros cadastrados", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, pady=10, sticky="ew")
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, sticky="ew", padx=10)

    headers = ['id', 'titulo', 'autor', 'editora', 'ano', 'isbn', 'origem']
    widths = [30, 150, 120, 100, 50, 100, 100]
    tree = criar_tabela(headers, widths)
    dados = listar_livros()
    if dados:
        for item in dados: tree.insert('', 'end', values=item)

# --- Ver EMPRÉSTIMOS ---
def ver_emprestimos():
    limpar_frame_direita()
    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_rowconfigure(2, weight=1)

    ctk.CTkLabel(frameDireita, text="Todos os empréstimos", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, pady=10, sticky="ew")
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, sticky="ew", padx=10)

    headers = ['id', 'livro', 'usuario', 'data_emp', 'data_prev', 'data_dev']
    widths = [30, 150, 150, 90, 90, 90]
    tree = criar_tabela(headers, widths)
    dados = listar_emprestimos()
    if dados:
        for item in dados: tree.insert('', 'end', values=item)

# --- Realizar EMPRÉSTIMO ---
def realizar_emprestimo():
    limpar_frame_direita()

    def add_emprestimo():
        try:
            livro_str = ELivro.get(); usuario_str = EUsuario.get(); data_emp = EData.get()
            if not livro_str or not usuario_str or not data_emp or \
               livro_str == 'Selecione o livro' or usuario_str == 'Selecione o usuário':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
            insert_loan(int(livro_str.split(':')[0]), int(usuario_str.split(':')[0]), data_emp)
            messagebox.showinfo('Sucesso', 'Empréstimo realizado!')
            ELivro.set('Selecione o livro'); EUsuario.set('Selecione o usuário')
            EData.delete(0, 'end'); EData.insert(0, datetime.now().strftime("%d-%m-%Y"))
        except Exception as e: messagebox.showerror('Erro', f'Erro: {e}')
            
    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_columnconfigure(3, weight=1)
    
    ctk.CTkLabel(frameDireita, text="Realizar Empréstimo", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=15)
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, columnspan=4, sticky="ew", padx=20)

    ctk.CTkLabel(frameDireita, text="Livro *", font=('Verdana', 14), text_color=co0).grid(row=2, column=1, padx=10, pady=15, sticky="e")
    ELivro = ctk.CTkOptionMenu(frameDireita, width=250, values=get_all_livros(), fg_color="white", text_color="black", state="readonly")
    ELivro.grid(row=2, column=2, padx=10, pady=15, sticky="w"); ELivro.set('Selecione o livro')

    ctk.CTkLabel(frameDireita, text="Usuário *", font=('Verdana', 14), text_color=co0).grid(row=3, column=1, padx=10, pady=15, sticky="e")
    EUsuario = ctk.CTkOptionMenu(frameDireita, width=250, values=get_all_usuarios(), fg_color="white", text_color="black", state="readonly")
    EUsuario.grid(row=3, column=2, padx=10, pady=15, sticky="w"); EUsuario.set('Selecione o usuário')

    ctk.CTkLabel(frameDireita, text="Data *", font=('Verdana', 14), text_color=co0).grid(row=4, column=1, padx=10, pady=15, sticky="e")
    EData = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black")
    EData.grid(row=4, column=2, padx=10, pady=15, sticky="w"); EData.insert(0, datetime.now().strftime("%d-%m-%Y"))

    img_save = get_ctk_image("save.png")
    b_salvar = ctk.CTkButton(frameDireita, command=add_emprestimo, image=img_save, text='SALVAR', font=('Ivy', 14), 
                             fg_color=co1, text_color=co0, hover_color=co1, border_width=1, border_color=co0)
    b_salvar.grid(row=5, column=2, sticky="w", padx=10, pady=20)

# --- Alterar Cadastro (USUÁRIO) ---
def Alterar_cadastro():
    limpar_frame_direita()
    
    def carregar_dados():
        try:
            usuario_str = EUsuario.get()
            if not usuario_str or usuario_str == 'Selecione o usuário': return
            dados = get_user_by_id(int(usuario_str.split(':')[0])) 
            ENome.delete(0, 'end'); ENome.insert(0, dados[1])
            ETurma.set(dados[2])
            ETel.delete(0, 'end'); ETel.insert(0, dados[5])
            EEndereco.delete(0, 'end'); EEndereco.insert(0, dados[3])
            EEmail.delete(0, 'end'); EEmail.insert(0, dados[4])
            b_salvar.configure(state='normal')
        except Exception as e: messagebox.showerror('Erro', f'Erro: {e}')

    def salvar_alteracoes():
        try:
            id_user = int(EUsuario.get().split(':')[0])
            update_user(id_user, ENome.get(), ETurma.get(), EEndereco.get(), EEmail.get(), ETel.get())
            messagebox.showinfo('Sucesso', 'Atualizado!')
            control('Alterar cadastro')
        except Exception as e: messagebox.showerror('Erro', f'Erro: {e}')

    # Layout
    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_columnconfigure(3, weight=1)

    ctk.CTkLabel(frameDireita, text="Alterar Cadastro de Usuário", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=10)
    
    ctk.CTkLabel(frameDireita, text="Selecione:", font=('Verdana', 12), text_color=co0).grid(row=1, column=1, padx=10, pady=5, sticky="e")
    
    EUsuario = ctk.CTkOptionMenu(frameDireita, width=250, values=get_all_usuarios(), 
                                 fg_color=co1, text_color=co0)
    EUsuario.grid(row=1, column=2, padx=10, pady=5, sticky="w"); EUsuario.set('Selecione o usuário')
    
    # --- BOTÃO CARREGAR COM BORDA ---
    # Adicionado border_width e border_color
    ctk.CTkButton(frameDireita, command=carregar_dados, text='Carregar Dados', width=150, 
                  fg_color=co1, text_color=co0, hover_color=co1, 
                  border_width=1, border_color=co0).grid(row=2, column=2, padx=10, pady=5, sticky="w")

    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=3, column=0, columnspan=4, sticky="ew", padx=20, pady=10)

    # Campos
    ctk.CTkLabel(frameDireita, text="Nome *", font=('Verdana', 14), text_color=co0).grid(row=4, column=1, padx=10, sticky="e")
    ENome = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black"); ENome.grid(row=4, column=2, padx=10, pady=5, sticky="w")
    
    ctk.CTkLabel(frameDireita, text="Turma *", font=('Verdana', 14), text_color=co0).grid(row=5, column=1, padx=10, sticky="e")
    ETurma = ctk.CTkOptionMenu(frameDireita, width=250, values=['Sexto ano', 'Sétimo ano', 'Oitavo ano', 'Nono ano'], fg_color="white", text_color="black")
    ETurma.grid(row=5, column=2, padx=10, pady=5, sticky="w")
    
    ctk.CTkLabel(frameDireita, text="Telefone", font=('Verdana', 14), text_color=co0).grid(row=6, column=1, padx=10, sticky="e")
    ETel = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black"); ETel.grid(row=6, column=2, padx=10, pady=5, sticky="w")
    
    ctk.CTkLabel(frameDireita, text="Endereço", font=('Verdana', 14), text_color=co0).grid(row=7, column=1, padx=10, sticky="e")
    EEndereco = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black"); EEndereco.grid(row=7, column=2, padx=10, pady=5, sticky="w")

    ctk.CTkLabel(frameDireita, text="Email", font=('Verdana', 14), text_color=co0).grid(row=8, column=1, padx=10, sticky="e")
    EEmail = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black"); EEmail.grid(row=8, column=2, padx=10, pady=5, sticky="w")
    
    b_salvar = ctk.CTkButton(frameDireita, command=salvar_alteracoes, text='SALVAR ALTERAÇÕES', fg_color=co1, text_color=co0, hover_color=co1)
    b_salvar.grid(row=9, column=2, sticky="w", padx=10, pady=20)
# --- Excluir Cadastro ---
def Excluir_cadastro():
    limpar_frame_direita()
    def deletar():
        try:
            user = EUsuario.get()
            if not user or user == 'Selecione o usuário': return
            if messagebox.askyesno("Confirmar", f"Excluir {user}?"):
                delete_user(int(user.split(':')[0]))
                messagebox.showinfo('Sucesso', 'Excluído!')
                control('Excluir cadastro')
        except: messagebox.showerror('Erro', 'Erro ao excluir')

    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_columnconfigure(3, weight=1)

    ctk.CTkLabel(frameDireita, text="Excluir Usuário", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=20)
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, columnspan=4, sticky="ew", padx=20)
    
    ctk.CTkLabel(frameDireita, text="Selecione:", font=('Verdana', 14), text_color=co0).grid(row=2, column=1, padx=10, pady=20, sticky="e")
    EUsuario = ctk.CTkOptionMenu(frameDireita, width=250, values=get_all_usuarios(), fg_color="white", text_color="black", state="readonly")
    EUsuario.grid(row=2, column=2, padx=10, pady=20, sticky="w"); EUsuario.set('Selecione o usuário')
    
    img_del = get_ctk_image("delete.png")
    ctk.CTkButton(frameDireita, command=deletar, image=img_del, text='EXCLUIR USUÁRIO', fg_color=co1, text_color=co0, hover_color=co1).grid(row=3, column=2, padx=10, sticky="w")

# --- Alterar LIVRO ---
def Alterar_livro():
    limpar_frame_direita()
    
    def carregar():
        try:
            livro = ELivro.get()
            if not livro or livro == 'Selecione o livro': return
            dados = get_book_by_id(int(livro.split(':')[0])) 
            ETitulo.delete(0,'end'); ETitulo.insert(0, dados[1])
            EAutor.delete(0,'end'); EAutor.insert(0, dados[2])
            EEditora.delete(0,'end'); EEditora.insert(0, dados[3])
            EAno.delete(0,'end'); EAno.insert(0, str(dados[4]))
            EIsbn.delete(0,'end'); EIsbn.insert(0, dados[5])
            val_origem = dados[6] if len(dados) > 6 else "Doação"
            EOrigem.set(val_origem)
            b_salvar.configure(state='normal')
        except: pass

    def salvar():
        try:
            update_book(int(ELivro.get().split(':')[0]), ETitulo.get(), EAutor.get(), EEditora.get(), EAno.get(), EIsbn.get(), EOrigem.get())
            messagebox.showinfo('Sucesso', 'Atualizado!')
            control('Alterar livro') 
        except: messagebox.showerror('Erro', 'Erro ao salvar')

    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_columnconfigure(3, weight=1)

    ctk.CTkLabel(frameDireita, text="Alterar Livro", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=10)
    
    ctk.CTkLabel(frameDireita, text="Selecione:", font=('Verdana', 12), text_color=co0).grid(row=1, column=1, padx=10, sticky="e")
    
    ELivro = ctk.CTkOptionMenu(frameDireita, width=200, values=get_all_livros(), 
                               fg_color=co1, text_color=co0)
    ELivro.grid(row=1, column=2, padx=10, sticky="w"); ELivro.set('Selecione o livro')
    
    # --- BOTÃO CARREGAR COM BORDA ---
    ctk.CTkButton(frameDireita, command=carregar, text='Carregar', width=80, 
                  fg_color=co1, text_color=co0, hover_color=co1,
                  border_width=1, border_color=co0).grid(row=2, column=2, padx=10, pady=5, sticky="w")

    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=3, column=0, columnspan=4, sticky="ew", padx=20, pady=10)

    campos = [("Título *", 4), ("Autor *", 5), ("Editora", 6), ("Ano", 7), ("ISBN", 8)]
    entries = {}
    for txt, ln in campos:
        ctk.CTkLabel(frameDireita, text=txt, font=('Verdana', 14), text_color=co0).grid(row=ln, column=1, padx=10, sticky="e")
        e = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black"); e.grid(row=ln, column=2, padx=10, pady=5, sticky="w")
        entries[txt] = e
    ETitulo=entries["Título *"]; EAutor=entries["Autor *"]; EEditora=entries["Editora"]; EAno=entries["Ano"]; EIsbn=entries["ISBN"]
    
    ctk.CTkLabel(frameDireita, text="Origem *", font=('Verdana', 14), text_color=co0).grid(row=9, column=1, padx=10, sticky="e")
    EOrigem = ctk.CTkOptionMenu(frameDireita, width=250, values=['Doação', 'Governo'], fg_color="white", text_color="black")
    EOrigem.grid(row=9, column=2, padx=10, pady=5, sticky="w"); EOrigem.set('Selecione a origem')

    b_salvar = ctk.CTkButton(frameDireita, command=salvar, text='SALVAR ALTERAÇÕES', fg_color=co1, text_color=co0, hover_color=co1)
    b_salvar.grid(row=10, column=2, sticky="w", padx=10, pady=20)
# --- Excluir Livro ---
def Excluir_livro():
    limpar_frame_direita()
    def deletar():
        try:
            item = ELivro.get()
            if not item or item == 'Selecione o livro': return
            if messagebox.askyesno("Confirmar", f"Excluir {item}?"):
                delete_book(int(item.split(':')[0]))
                messagebox.showinfo('Sucesso', 'Excluído!')
                control('Excluir livro')
        except: messagebox.showerror('Erro', 'Erro')

    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_columnconfigure(3, weight=1)
    ctk.CTkLabel(frameDireita, text="Excluir Livro", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=20)
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, columnspan=4, sticky="ew", padx=20)
    ctk.CTkLabel(frameDireita, text="Selecione:", font=('Verdana', 14), text_color=co0).grid(row=2, column=1, padx=10, pady=20, sticky="e")
    ELivro = ctk.CTkOptionMenu(frameDireita, width=250, values=get_all_livros(), fg_color="white", text_color="black", state="readonly")
    ELivro.grid(row=2, column=2, padx=10, pady=20, sticky="w"); ELivro.set('Selecione o livro')
    
    img_del = get_ctk_image("delete.png")
    ctk.CTkButton(frameDireita, command=deletar, image=img_del, text='EXCLUIR LIVRO', fg_color=co1, text_color=co0, hover_color=co1).grid(row=3, column=2, padx=10, sticky="w")

# --- Realizar DEVOLUÇÃO ---
def realizar_devolucao():
    limpar_frame_direita()
    def add_devolucao():
        try:
            emp_str = EEmprestimo.get(); data_dev = EData.get()
            if not emp_str or not data_dev or emp_str == 'Selecione o empréstimo':
                messagebox.showerror('Erro', 'Preencha tudo')
                return
            devolver_livro(int(emp_str.split(':')[0]), data_dev)
            messagebox.showinfo('Sucesso', 'Devolvido!')
            EEmprestimo.configure(values=get_active_loans()); EEmprestimo.set('Selecione o empréstimo')
            EData.delete(0, 'end'); EData.insert(0, datetime.now().strftime("%d-%m-%Y"))
        except Exception as e: messagebox.showerror('Erro', f'Erro: {e}')
            
    frameDireita.grid_columnconfigure(0, weight=1); frameDireita.grid_columnconfigure(3, weight=1)
    ctk.CTkLabel(frameDireita, text="Realizar Devolução", font=('Verdana', 20, 'bold'), text_color=co0).grid(row=0, column=0, columnspan=4, pady=15)
    ctk.CTkFrame(frameDireita, height=2, fg_color=co3).grid(row=1, column=0, columnspan=4, sticky="ew", padx=20)

    ctk.CTkLabel(frameDireita, text="Empréstimo *", font=('Verdana', 14), text_color=co0).grid(row=2, column=1, padx=10, pady=15, sticky="e")
    EEmprestimo = ctk.CTkOptionMenu(frameDireita, width=250, values=get_active_loans(), fg_color="white", text_color="black", state="readonly")
    EEmprestimo.grid(row=2, column=2, padx=10, pady=15, sticky="w"); EEmprestimo.set('Selecione o empréstimo')

    ctk.CTkLabel(frameDireita, text="Data Devolução *", font=('Verdana', 14), text_color=co0).grid(row=3, column=1, padx=10, pady=15, sticky="e")
    EData = ctk.CTkEntry(frameDireita, width=250, fg_color="white", text_color="black")
    EData.grid(row=3, column=2, padx=10, pady=15, sticky="w"); EData.insert(0, datetime.now().strftime("%d-%m-%Y")) 

    img_save = get_ctk_image("save.png")
    b_salvar = ctk.CTkButton(frameDireita, command=add_devolucao, image=img_save, text='SALVAR DEVOLUÇÃO', font=('Ivy', 14), fg_color=co1, text_color=co0, hover_color=co1)
    b_salvar.grid(row=4, column=2, sticky="w", padx=10, pady=20) 

# --- TELA INICIAL ---
def mostrar_tela_inicial():
    limpar_frame_direita()
    
    canvas = ctk.CTkCanvas(frameDireita, bg=co12, highlightthickness=0) 
    canvas.pack(expand=True, padx=20, pady=20) 

    quad_size = 40; spacing = 10; red_circle_radius = quad_size / 2 
    color_green = "#2bb937"; color_red = "#e06636"

    def draw_square(x, y, color):
        canvas.create_rectangle(x, y, x + quad_size, y + quad_size, fill=color, outline=color)

    start_x = 120; start_y = 0 
    canvas.create_oval(start_x, start_y, start_x + red_circle_radius * 2, start_y + red_circle_radius * 2, fill=color_red, outline=color_red)
    draw_square(start_x + quad_size + spacing, start_y, color_green)
    draw_square(start_x + 2*(quad_size + spacing), start_y, color_green)
    draw_square(start_x, start_y + quad_size + spacing, color_green)
    draw_square(start_x + quad_size + spacing, start_y + quad_size + spacing, color_green)
    draw_square(start_x + 2*(quad_size + spacing), start_y + quad_size + spacing, co12)
    draw_square(start_x, start_y + 2*(quad_size + spacing), color_green)
    draw_square(start_x + quad_size + spacing, start_y + 2*(quad_size + spacing), color_green)
    draw_square(start_x + 2*(quad_size + spacing), start_y + 2*(quad_size + spacing), color_green)
    draw_square(start_x, start_y + 3*(quad_size + spacing), color_green)
    draw_square(start_x + quad_size + spacing, start_y + 3*(quad_size + spacing), color_green)
    
# --- MENU CONTROL ---
def control(i):
    limpar_frame_direita()
    if i == 'Novo cadastro': Novo_cadastro()
    elif i == 'Novo Livro': Novo_livro()
    elif i == 'Consultar Livros': ver_livros()
    elif i == 'Consultar pessoas cadastradas': ver_usuarios()
    elif i == 'Consultar empréstimos': ver_emprestimos()
    elif i == 'Realizar empréstimo': realizar_emprestimo()
    elif i == 'Devolução': realizar_devolucao()
    elif i == 'Alterar cadastro': Alterar_cadastro()
    elif i == 'Excluir cadastro': Excluir_cadastro()
    elif i == 'Alterar livro': Alterar_livro()
    elif i == 'Excluir livro': Excluir_livro()

# ===================================================================
# MENU LATERAL (BOTÕES)
# ===================================================================
def criar_botao_menu(texto, imagem_nome, comando, linha):
    img = get_ctk_image(imagem_nome)
    btn = ctk.CTkButton(frameEsquerda, command=comando, image=img, text=texto, anchor="w",
                        fg_color=co8, text_color=co0, hover_color=co1, 
                        font=('Ivy', 11), corner_radius=0, height=40)
    btn.grid(row=linha, column=0, sticky="ew", padx=2, pady=2)

botoes = [
    ('Novo cadastro', 'plus.png', lambda: control('Novo cadastro')),
    ('Novo Livro', 'plus.png', lambda: control('Novo Livro')),
    ('Consultar Livros', 'icons8-book-100.png', lambda: control('Consultar Livros')),
    ('Ver Usuários', 'pessoa.png', lambda: control('Consultar pessoas cadastradas')),
    ('Ver Empréstimos', 'consulta.png', lambda: control('Consultar empréstimos')),
    ('Empréstimo', 'emprestar.png', lambda: control('Realizar empréstimo')),
    ('Devolução', 'icons8-reload-100.png', lambda: control('Devolução')),
    ('Alterar usuário', 'edit.png', lambda: control('Alterar cadastro')),
    ('Excluir usuário', 'delete.png', lambda: control('Excluir cadastro')),
    ('Alterar livro', 'edit.png', lambda: control('Alterar livro')),
    ('Excluir livro', 'delete.png', lambda: control('Excluir livro')),
]

for i, (txt, img, cmd) in enumerate(botoes):
    criar_botao_menu(txt, img, cmd, i)

# --- Inicia a aplicação ---
mostrar_tela_inicial()
janela.mainloop()