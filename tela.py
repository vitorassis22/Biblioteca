import sys
import os
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image
from view import *

# --- CONFIGURAÇÃO INICIAL ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

# --- CORES ---
co_bg = "#ffffff"
co_menu = "#e5c29f" # burlywood2
co_accent = "#4fa882"
co_text = "black"
co_light_green = "#98fb98"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- JANELA PRINCIPAL ---
janela = ctk.CTk()
janela.title("Sistema de Biblioteca Completo")
janela.geometry("1000x720")
janela.configure(fg_color=co_bg)
janela.resizable(True, True)

# Grid Principal
janela.grid_columnconfigure(1, weight=1)
janela.grid_rowconfigure(0, weight=1)

# Menu Lateral
frame_menu = ctk.CTkFrame(janela, width=200, fg_color=co_menu, corner_radius=0)
frame_menu.grid(row=0, column=0, sticky="nsew")

# Área de Conteúdo
frame_main = ctk.CTkFrame(janela, fg_color=co_light_green, corner_radius=0)
frame_main.grid(row=0, column=1, sticky="nsew")

# Variável global para armazenar ID selecionado na edição
selected_id = None

# --- FUNÇÕES AUXILIARES DE UI ---
def clear_main_frame():
    global selected_id
    selected_id = None
    for widget in frame_main.winfo_children():
        widget.destroy()

def get_icon(name):
    try:
        return ctk.CTkImage(Image.open(resource_path(f"assets/{name}")), size=(20, 20))
    except: return None

def create_table(headers, columns_width):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=('Arial', 10))
    style.configure("Treeview.Heading", background=co_accent, foreground="white", font=('Arial', 10, 'bold'))
    
    tree = ttk.Treeview(frame_main, selectmode="browse", columns=headers, show="headings")
    vsb = ttk.Scrollbar(frame_main, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_main, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    for col, width in zip(headers, columns_width):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='w')
        
    return tree, vsb, hsb

# =============================================================================
# 1. GERENCIAR LIVROS (Consolidado)
# =============================================================================
# --- view_gerenciar_livros (ATUALIZADO com Quantidade) ---
def view_gerenciar_livros():
    clear_main_frame()
    
    # Frame Formulário (TOPO)
    frame_form = ctk.CTkFrame(frame_main, fg_color="transparent")
    frame_form.pack(fill="x", padx=10, pady=10)
    
    ctk.CTkLabel(frame_form, text="Gerenciar Livros", font=("Arial", 20, "bold")).pack(pady=5)
    
    inputs_frame = ctk.CTkFrame(frame_form, fg_color="transparent")
    inputs_frame.pack()
    
    # Linha 1
    ctk.CTkLabel(inputs_frame, text="Título:").grid(row=0, column=0, padx=(10,2), sticky='e')
    e_titulo = ctk.CTkEntry(inputs_frame, width=300)
    e_titulo.grid(row=0, column=1, padx=(2,10), pady=2)
    
    ctk.CTkLabel(inputs_frame, text="Autor:").grid(row=0, column=2, padx=(10,2), sticky='e')
    e_autor = ctk.CTkEntry(inputs_frame, width=200)
    e_autor.grid(row=0, column=3, padx=(2,10), pady=2)
    
    # Linha 2
    ctk.CTkLabel(inputs_frame, text="Editora:").grid(row=1, column=0, padx=(10,2), sticky='e')
    e_editora = ctk.CTkEntry(inputs_frame, width=300)
    e_editora.grid(row=1, column=1, padx=(2,10), pady=2)
    
    # --- NOVO CAMPO: Quantidade (no lugar do Ano) ---
    ctk.CTkLabel(inputs_frame, text="Qtd:").grid(row=1, column=2, padx=(10,2), sticky='e')
    e_quantidade = ctk.CTkEntry(inputs_frame, width=50) # Novo campo
    e_quantidade.grid(row=1, column=3, padx=(2,10), sticky='w')

    ctk.CTkLabel(inputs_frame, text="Ano:").grid(row=1, column=3, padx=(10,2), sticky='e')
    e_ano = ctk.CTkEntry(inputs_frame, width=80)
    e_ano.grid(row=1, column=4, padx=(2,10), sticky='w')

    ctk.CTkLabel(inputs_frame, text="Código:").grid(row=2, column=0, padx=(10,2), sticky='e')
    e_isbn = ctk.CTkEntry(inputs_frame, width=200)
    e_isbn.grid(row=2, column=1, padx=(2,10), sticky='w')

    # Linha 3 (Cidade e Estado)
    list_ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    
    ctk.CTkLabel(inputs_frame, text="Cidade:").grid(row=3, column=0, padx=(10,2), pady=5, sticky='e')
    e_cidade = ctk.CTkEntry(inputs_frame, width=200)
    e_cidade.grid(row=3, column=1, padx=(2,10), pady=5, sticky='w')
    
    ctk.CTkLabel(inputs_frame, text="UF:").grid(row=3, column=1, padx=(10,2), pady=6, sticky='e')
    e_estado = ctk.CTkOptionMenu(inputs_frame, values=list_ufs, width=70)
    e_estado.grid(row=3, column=2, padx=(2,10), sticky='w')
    
    ctk.CTkLabel(inputs_frame, text="Origem:").grid(row=3, column=3, padx=(10,2), sticky='e')
    e_origem = ctk.CTkOptionMenu(inputs_frame, values=["Doação", "Governo", "Indefinido"], width=120)
    e_origem.grid(row=3, column=4, padx=(2,10), sticky='w')

    # Linha 4 (Gênero e Prateleira)
    ctk.CTkLabel(inputs_frame, text="Gênero:").grid(row=4, column=0, padx=(10,2), sticky='e')
    e_genero = ctk.CTkOptionMenu(inputs_frame, values=get_generos_list() or ["Geral"], width=150)
    e_genero.grid(row=4, column=1, padx=(2,10), sticky='w')
    
    ctk.CTkLabel(inputs_frame, text="Prateleira:").grid(row=4, column=3, padx=(10,2), sticky='e')
    e_prat = ctk.CTkOptionMenu(inputs_frame, values=get_prateleiras_list() or ["A1"], width=100)
    e_prat.grid(row=4, column=4, padx=(2,10), sticky='w')

    # Tabela
    # Adicionada 'Qtd' ao cabeçalho e ajustada a largura
    headers = ["ID", "Título", "Autor", "Editora", "Ano", "ISBN", "Qtd", "Origem", "Gênero", "Cidade", "UF", "Prat"]
    widths = [30, 150, 100, 80, 40, 80, 40, 70, 80, 80, 40, 50]
    tree, vsb, hsb = create_table(headers, widths)
    tree.pack(expand=True, fill="both", padx=10)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    def carregar_tabela():
        for i in tree.get_children(): tree.delete(i)
        for row in get_books(): tree.insert("", "end", values=row)

    def limpar_campos():
        global selected_id
        selected_id = None
        e_titulo.delete(0, 'end'); e_autor.delete(0, 'end'); e_editora.delete(0, 'end')
        e_ano.delete(0, 'end'); e_isbn.delete(0, 'end'); e_cidade.delete(0, 'end')
        e_quantidade.delete(0, 'end') # Limpar o novo campo
        btn_action.configure(text="SALVAR NOVO", fg_color=co_accent)

    def on_select(event):
        global selected_id
        try:
            item = tree.selection()[0]
            vals = tree.item(item, "values")
            # Índices: 0:ID, 1:Titulo, 2:Autor, 3:Editora, 4:Ano, 5:ISBN, 6:Origem, 7:Genero, 8:Cidade, 9:UF, 10:Prat, 11:Qtd
            selected_id = vals[0]
            
            e_titulo.delete(0, 'end'); e_titulo.insert(0, vals[1])
            e_autor.delete(0, 'end'); e_autor.insert(0, vals[2])
            e_editora.delete(0, 'end'); e_editora.insert(0, vals[3])
            e_ano.delete(0, 'end'); e_ano.insert(0, vals[4])
            e_isbn.delete(0, 'end'); e_isbn.insert(0, vals[5])
            e_quantidade.delete(0, 'end'); e_quantidade.insert(0, vals[6]) # <--- Índice 6
            e_origem.set(vals[7])
            e_genero.set(vals[8])
            e_cidade.delete(0, 'end'); e_cidade.insert(0, vals[9])
            e_estado.set(vals[10])
            e_prat.set(vals[11])

            btn_action.configure(text="ATUALIZAR", fg_color="#e0a96d")
        except Exception as e: 
            print(f"Erro ao selecionar: {e}")

    tree.bind("<<TreeviewSelect>>", on_select)

    def salvar():
        if not e_titulo.get() or not e_autor.get():
            messagebox.showerror("Erro", "Título e Autor são obrigatórios")
            return
        
        # Coleta todos os campos, incluindo o novo (quantidade)
        args = [e_titulo.get(), e_autor.get(), e_editora.get(), e_ano.get(), 
                e_isbn.get(), e_origem.get(), e_genero.get(), e_cidade.get(), 
                e_estado.get(), e_prat.get(), e_quantidade.get() or 1] # Pega 1 se vazio
        
        if selected_id: # Update
            update_book(selected_id, *args)
            messagebox.showinfo("Sucesso", "Livro atualizado!")
        else: # Insert
            insert_book(*args)
            messagebox.showinfo("Sucesso", "Livro cadastrado!")
        
        limpar_campos()
        carregar_tabela()

    def excluir():
        if not selected_id: return
        if messagebox.askyesno("Confirmar", "Excluir livro selecionado?"):
            delete_book(selected_id)
            limpar_campos()
            carregar_tabela()

    # Botões
    btn_frame = ctk.CTkFrame(frame_form, fg_color="transparent")
    btn_frame.pack(pady=10)
    
    btn_action = ctk.CTkButton(btn_frame, text="SALVAR NOVO", command=salvar, fg_color=co_accent)
    btn_action.pack(side="left", padx=5)
    
    ctk.CTkButton(btn_frame, text="LIMPAR", command=limpar_campos, fg_color="gray").pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="EXCLUIR", command=excluir, fg_color="#e06636").pack(side="left", padx=5)

    carregar_tabela()
    
# =============================================================================
# 2. GERENCIAR USUÁRIOS (Consolidado)
# =============================================================================
def view_gerenciar_usuarios():
    clear_main_frame()
    
    frame_form = ctk.CTkFrame(frame_main, fg_color="transparent")
    frame_form.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(frame_form, text="Gerenciar Usuários", font=("Arial", 20, "bold")).pack(pady=5)
    
    inputs_frame = ctk.CTkFrame(frame_form, fg_color="transparent")
    inputs_frame.pack()
    
    ctk.CTkLabel(inputs_frame, text="Nome:").grid(row=0, column=0, padx=5, sticky='e')
    e_nome = ctk.CTkEntry(inputs_frame, width=250)
    e_nome.grid(row=0, column=1, padx=5, pady=2)
    
    ctk.CTkLabel(inputs_frame, text="Turma:").grid(row=0, column=2, padx=5, sticky='e')
    e_turma = ctk.CTkOptionMenu(inputs_frame, values=['Sexto Ano', 'Sétimo Ano', 'Oitavo Ano', 'Nono Ano'])
    e_turma.grid(row=0, column=3, padx=5, pady=2)
    
    ctk.CTkLabel(inputs_frame, text="Endereço:").grid(row=1, column=0, padx=5, sticky='e')
    e_end = ctk.CTkEntry(inputs_frame, width=250)
    e_end.grid(row=1, column=1, padx=5, pady=2)
    
    ctk.CTkLabel(inputs_frame, text="Email:").grid(row=1, column=2, padx=5, sticky='e')
    e_email = ctk.CTkEntry(inputs_frame, width=200)
    e_email.grid(row=1, column=3, padx=5, pady=2)
    
    ctk.CTkLabel(inputs_frame, text="Telefone:").grid(row=2, column=0, padx=5, sticky='e')
    e_tel = ctk.CTkEntry(inputs_frame, width=150)
    e_tel.grid(row=2, column=1, padx=5, pady=2, sticky='w')

    headers = ["ID", "Nome", "Turma", "Endereço", "Email", "Telefone"]
    widths = [30, 150, 80, 150, 150, 100]
    tree, vsb, hsb = create_table(headers, widths)
    tree.pack(expand=True, fill="both", padx=10)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    def carregar_tabela():
        for i in tree.get_children(): tree.delete(i)
        for row in get_users(): tree.insert("", "end", values=row)

    def limpar_campos():
        global selected_id
        selected_id = None
        e_nome.delete(0, 'end'); e_end.delete(0, 'end'); e_email.delete(0, 'end'); e_tel.delete(0, 'end')
        btn_action.configure(text="SALVAR NOVO", fg_color=co_accent)

    def on_select(event):
        global selected_id
        try:
            vals = tree.item(tree.selection()[0], "values")
            selected_id = vals[0]
            e_nome.delete(0, 'end'); e_nome.insert(0, vals[1])
            e_turma.set(vals[2])
            e_end.delete(0, 'end'); e_end.insert(0, vals[3])
            e_email.delete(0, 'end'); e_email.insert(0, vals[4])
            e_tel.delete(0, 'end'); e_tel.insert(0, vals[5])
            btn_action.configure(text="ATUALIZAR", fg_color="#e0a96d")
        except: pass

    tree.bind("<<TreeviewSelect>>", on_select)

    def salvar():
        if not e_nome.get(): return
        if selected_id:
            update_user(selected_id, e_nome.get(), e_turma.get(), e_end.get(), e_email.get(), e_tel.get())
            messagebox.showinfo("Sucesso", "Atualizado!")
        else:
            insert_user(e_nome.get(), e_turma.get(), e_end.get(), e_email.get(), e_tel.get())
            messagebox.showinfo("Sucesso", "Cadastrado!")
        limpar_campos(); carregar_tabela()

    def excluir():
        if selected_id and messagebox.askyesno("Confirmar", "Excluir?"):
            delete_user(selected_id); limpar_campos(); carregar_tabela()

    btn_frame = ctk.CTkFrame(frame_form, fg_color="transparent")
    btn_frame.pack(pady=10)
    btn_action = ctk.CTkButton(btn_frame, text="SALVAR NOVO", command=salvar, fg_color=co_accent)
    btn_action.pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="LIMPAR", command=limpar_campos, fg_color="gray").pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="EXCLUIR", command=excluir, fg_color="#e06636").pack(side="left", padx=5)

    carregar_tabela()

# =============================================================================
# 3. CADASTROS AUXILIARES (Gêneros e Prateleiras)
# =============================================================================
def view_auxiliar(tipo):
    # tipo = 'genero' ou 'prateleira'
    clear_main_frame()
    titulo = "Gerenciar Gêneros" if tipo == 'genero' else "Gerenciar Prateleiras"
    
    frame_form = ctk.CTkFrame(frame_main, fg_color="transparent")
    frame_form.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(frame_form, text=titulo, font=("Arial", 20, "bold")).pack(pady=5)
    
    ctk.CTkLabel(frame_form, text="Nome:").pack()
    e_nome = ctk.CTkEntry(frame_form, width=200)
    e_nome.pack(pady=5)

    tree, vsb, hsb = create_table(["ID", "Nome"], [50, 300])
    tree.pack(expand=True, fill="both", padx=10)

    def carregar():
        for i in tree.get_children(): tree.delete(i)
        rows = get_generos() if tipo == 'genero' else get_prateleiras()
        for r in rows: tree.insert("", "end", values=r)

    def salvar():
        if not e_nome.get(): return
        try:
            if tipo == 'genero': insert_genero(e_nome.get())
            else: insert_prateleira(e_nome.get())
            e_nome.delete(0, 'end')
            carregar()
        except: messagebox.showerror("Erro", "Item já existe ou erro no banco")

    def excluir():
        try:
            id_sel = tree.item(tree.selection()[0], "values")[0]
            if tipo == 'genero': delete_genero(id_sel)
            else: delete_prateleira(id_sel)
            carregar()
        except: pass

    btn_frame = ctk.CTkFrame(frame_form, fg_color="transparent")
    btn_frame.pack(pady=10)
    ctk.CTkButton(btn_frame, text="ADICIONAR", command=salvar, fg_color=co_accent).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="EXCLUIR SELECIONADO", command=excluir, fg_color="#e06636").pack(side="left", padx=5)

    carregar()

# =============================================================================
# 4. EMPRÉSTIMOS (Fluxo Simplificado)
# =============================================================================
def view_emprestimos():
    clear_main_frame()
    
    # Tabs para alternar entre Novo e Devolução
    tabview = ctk.CTkTabview(frame_main, width=800, height=600)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)
    
    tab_novo = tabview.add("Novo Empréstimo")
    tab_dev = tabview.add("Devolução")
    
    # --- NOVO ---
    ctk.CTkLabel(tab_novo, text="Selecione o Livro:").pack(pady=5)
    cb_livro = ctk.CTkOptionMenu(tab_novo, values=get_books_list(), width=400)
    cb_livro.pack()
    
    ctk.CTkLabel(tab_novo, text="Selecione o Aluno:").pack(pady=5)
    cb_user = ctk.CTkOptionMenu(tab_novo, values=get_users_list(), width=400)
    cb_user.pack()
    
    ctk.CTkLabel(tab_novo, text="Data Empréstimo:").pack(pady=5)
    e_data = ctk.CTkEntry(tab_novo, width=150)
    e_data.pack(); e_data.insert(0, datetime.now().strftime("%d-%m-%Y"))
    
    def realizar_emp():
        try:
            lid = int(cb_livro.get().split(':')[0])
            uid = int(cb_user.get().split(':')[0])
            insert_loan(lid, uid, e_data.get())
            messagebox.showinfo("Sucesso", "Empréstimo realizado!")
            # Atualiza lista de devoluções
            atualizar_lista_dev()
        except: messagebox.showerror("Erro", "Selecione livro e aluno")
        
    ctk.CTkButton(tab_novo, text="CONFIRMAR EMPRÉSTIMO", command=realizar_emp, fg_color=co_accent).pack(pady=20)

    # --- DEVOLUÇÃO ---
    ctk.CTkLabel(tab_dev, text="Empréstimos Ativos (Selecione para devolver):").pack(pady=5)
    cb_loan = ctk.CTkOptionMenu(tab_dev, values=[], width=500)
    cb_loan.pack()
    
    ctk.CTkLabel(tab_dev, text="Data Devolução:").pack(pady=5)
    e_data_dev = ctk.CTkEntry(tab_dev, width=150)
    e_data_dev.pack(); e_data_dev.insert(0, datetime.now().strftime("%d-%m-%Y"))

    def atualizar_lista_dev():
        loans = get_loans_list()
        if loans:
            cb_loan.configure(values=loans)
            cb_loan.set(loans[0])
        else:
            cb_loan.configure(values=["Nenhum empréstimo ativo"])
            cb_loan.set("Nenhum empréstimo ativo")

    def realizar_dev():
        try:
            val = cb_loan.get()
            if "Nenhum" in val: return
            lid = int(val.split(':')[0])
            return_loan(lid, e_data_dev.get())
            messagebox.showinfo("Sucesso", "Devolvido!")
            atualizar_lista_dev()
        except: pass

    ctk.CTkButton(tab_dev, text="CONFIRMAR DEVOLUÇÃO", command=realizar_dev, fg_color="#e06636").pack(pady=20)
    
    atualizar_lista_dev()

# =============================================================================
# MENU LATERAL
# =============================================================================
def criar_botao_menu(texto, img_name, cmd):
    icon = get_icon(img_name)
    btn = ctk.CTkButton(frame_menu, text=texto, image=icon, command=cmd, 
                        fg_color="transparent", hover_color=co_accent, text_color="black", anchor="w", height=40)
    btn.pack(fill="x", padx=5, pady=2)

# Tela inicial (Logo)
# --- TELA INICIAL (Logo do IF Corrigida) ---
def view_home():
    clear_main_frame()
    
    # O Canvas preenche o frame_main (fundo verde claro)
    canvas = ctk.CTkCanvas(frame_main, bg=co_light_green, highlightthickness=0) 
    canvas.pack(expand=True, fill="both") 

    quad_size = 40
    spacing = 7
    red_circle_radius = quad_size / 2 
    
    color_green = "#2bb937" # Seu co9 
    color_red = "#e06636"   # Seu co5 

    def draw_square(x, y, color):
        # O Corner Radius do Canvas ajuda a dar um visual mais suave ao logo
        canvas.create_rectangle(x, y, x + quad_size, y + quad_size, fill=color, outline=color, tags=("logo_part"))

    # Ponto de partida centralizado (ajustado para a nova largura/altura)
    start_x = 350 
    start_y = 200

    # --- Primeira Linha (y=0) ---
    # Círculo Vermelho
    canvas.create_oval(
        start_x, start_y, 
        start_x + red_circle_radius * 2, start_y + red_circle_radius * 2, 
        fill=color_red, outline=color_red
    )
    # Quadrados Verdes
    draw_square(start_x + quad_size + spacing, start_y, color_green)
    draw_square(start_x + 2*(quad_size + spacing), start_y, color_green)

    # --- Segunda Linha (y=1) ---
    draw_square(start_x, start_y + quad_size + spacing, color_green)
    draw_square(start_x + quad_size + spacing, start_y + quad_size + spacing, color_green)
    # O quadrado final é da cor do fundo (invisível)
    draw_square(start_x + 2*(quad_size + spacing), start_y + quad_size + spacing, co_light_green)

    # --- Terceira Linha (y=2) ---
    draw_square(start_x, start_y + 2*(quad_size + spacing), color_green)
    draw_square(start_x + quad_size + spacing, start_y + 2*(quad_size + spacing), color_green)
    # CORREÇÃO 1: Este era o quadrado que estava verde na sua versão anterior
    draw_square(start_x + 2*(quad_size + spacing), start_y + 2*(quad_size + spacing), color_green)

    # --- Quarta Linha (y=3) ---
    draw_square(start_x, start_y + 3*(quad_size + spacing), color_green)
    draw_square(start_x + quad_size + spacing, start_y + 3*(quad_size + spacing), color_green)
    # CORREÇÃO 2: Adiciona o quadrado final na cor do fundo para completar a forma 'F'
    draw_square(start_x + 2*(quad_size + spacing), start_y + 3*(quad_size + spacing), co_light_green)
    
def view_table(type_data):
    clear_main_frame()
    
    # Configurações baseadas no tipo
    if type_data == "users":
        title_text = "Consultar Usuários"
        headers = ['ID', 'Nome', 'Turma', 'Endereço', 'Email', 'Telefone']
        widths = [30, 150, 80, 150, 150, 100]
        get_data_func = get_users # Chama a função direto, sem 'db.'
        
    elif type_data == "books":
        title_text = "Consultar Livros"
        headers = ['ID', 'Título', 'Autor', 'Editora', 'Ano', 'ISBN', 'Origem', 'Gênero']
        widths = [30, 200, 150, 100, 50, 80, 80, 80]
        get_data_func = get_books # Chama a função direto
        
    elif type_data == "loans":
        title_text = "Consultar Empréstimos"
        headers = ['ID', 'Livro', 'Usuário', 'Data Emp', 'Data Prev', 'Status']
        widths = [30, 300, 150, 90, 90, 100]
        get_data_func = get_loans # Chama a função direto

    # Frame de Título e Busca
    frame_top = ctk.CTkFrame(frame_main, fg_color="transparent")
    frame_top.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(frame_top, text=title_text, font=("Arial", 20, "bold")).pack(side="top", pady=5)

    # Barra de Pesquisa
    entry_busca = ctk.CTkEntry(frame_top, placeholder_text="Pesquisar...", width=300)
    entry_busca.pack(side="left", padx=5)

    def filtrar():
        termo = entry_busca.get()
        # Limpa a tabela
        for i in tree.get_children(): tree.delete(i)
        # Busca novos dados passando o termo
        novos_dados = get_data_func(search_term=termo)
        
        for r in novos_dados:
            display_row = r[:len(headers)]
            tree.insert("", "end", values=display_row)

    btn_buscar = ctk.CTkButton(frame_top, text="Buscar", width=80, command=filtrar, fg_color=co_accent)
    btn_buscar.pack(side="left", padx=5)

    # Tabela
    tree, vsb, hsb = create_table(headers, widths)
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    # Carga Inicial (sem filtro)
    filtrar()
# Botoes
criar_botao_menu("Início", "icons8-book-100.png", view_home)
criar_botao_menu("Gerenciar Livros", "icons8-book-100.png", view_gerenciar_livros)
criar_botao_menu("Gerenciar Usuários", "pessoa.png", view_gerenciar_usuarios)
criar_botao_menu("Empréstimos", "emprestar.png", view_emprestimos)
criar_botao_menu("Gêneros", "plus.png", lambda: view_auxiliar('genero'))
criar_botao_menu("Prateleiras", "plus.png", lambda: view_auxiliar('prateleira'))
# ... (Seu código de criação de botões) ...

# VER LIVROS (Consultar Livros)
#criar_botao_menu("Consultar Livros", "icons8-book-100.png", lambda: view_table('books')) 

# VER USUARIOS (Consultar pessoas cadastradas)
#criar_botao_menu("Consultar pessoas cadastradas", "pessoa.png", lambda: view_table('users')) 

# VER EMPRESTIMOS (Consultar empréstimos)
criar_botao_menu("Consultar empréstimos", "emprestar.png", lambda: view_table('loans'))

view_home()
janela.mainloop()