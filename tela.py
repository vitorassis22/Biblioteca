import sys
import os
import customtkinter as ctk
from tkinter import ttk, messagebox
from CTkMessagebox import CTkMessagebox
from datetime import datetime, timedelta
from PIL import Image
from view import *

# =============================================================================
# CONFIGURAÇÃO INICIAL DO TEMA
# =============================================================================
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

COLOR_MENU_BG = "#1B5E20"  # Verde IF Escuro (Fixo)
COLOR_MENU_BTN_HOVER = "#2E7D32"
COLOR_CONTENT_BG = ("#F5F7F9", "#242424")  # Claro / Escuro
COLOR_TEXT_PRIMARY = ("#333333", "white")  # Preto / Branco
COLOR_ACCENT = "#2E7D32"
COLOR_DANGER = "#D32F2F"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AppBiblioteca(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Biblioteca - IF")
        self.geometry("1100x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected_id = None

        # ===================================================
        # 1. MENU LATERAL (FIXO)
        # ===================================================
        self.frame_menu = ctk.CTkFrame(
            self, width=220, corner_radius=0, fg_color=COLOR_MENU_BG
        )
        self.frame_menu.grid(row=0, column=0, sticky="nsew")

        # Título do Menu (Visual Novo)
        self.label_titulo = ctk.CTkLabel(
            self.frame_menu,
            text="BIBLIOTECA\nDIGITAL",  # Nome mais moderno com quebra de linha
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),  # Fonte Roboto
            text_color="white",
        )
        self.label_titulo.grid(
            row=0, column=0, padx=20, pady=(40, 20)
        )  # Aumentei um pouco o padding do topo

        # ===================================================
        # 2. ÁREA DE CONTEÚDO (DINÂMICA)
        # ===================================================
        self.frame_main = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_CONTENT_BG)
        self.frame_main.grid(row=0, column=1, sticky="nsew")

        # Inicia com a tela Home
        self.view_home()
        self.setup_menu_buttons()
        self.setup_theme_switch()
        self.mudar_tema()

    def setup_menu_buttons(self):
        buttons = [
            ("Início", self.view_home),
            ("Gerenciar Livros", self.view_gerenciar_livros),
            ("Gerenciar Usuários", self.view_gerenciar_usuarios),
            ("Empréstimos", self.view_emprestimos),
            ("Gêneros", lambda: self.view_auxiliar("genero")),
            ("Prateleiras", lambda: self.view_auxiliar("prateleira")),
            ("Consultar Empréstimos", lambda: self.view_table("loans")),
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                self.frame_menu,
                text=text,
                command=command,
                corner_radius=8,
                height=45,
                fg_color="transparent",
                text_color="white",
                hover_color=COLOR_MENU_BTN_HOVER,
                anchor="w",
                font=ctk.CTkFont(size=14),
            )
            btn.grid(row=i + 1, column=0, padx=15, pady=5, sticky="ew")

    def setup_theme_switch(self):
        self.frame_menu.grid_rowconfigure(20, weight=1)
        self.switch_tema = ctk.CTkSwitch(
            self.frame_menu,
            text="Tema Claro",
            command=self.mudar_tema,
            text_color="white",
            progress_color="#4CAF50",
        )
        self.switch_tema.grid(row=21, column=0, padx=20, pady=20, sticky="s")

    def mudar_tema(self):
        # 1. Definição das Cores baseadas no Tema
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.switch_tema.configure(text="Tema Escuro")

            # Cores para Tabela Dark
            bg_color = "#2b2b2b"  # Fundo da tabela
            text_color = "white"  # Texto da tabela
            header_bg = "#1B5E20"  # Cabeçalho (Verde Escuro)
            header_text = "white"  # Texto do Cabeçalho
            selected_bg = "#2E7D32"  # Cor de seleção

            # Cores para o Home
            novo_texto_home = "#FFFFFF"
            novo_bg_home = "#242424"
        else:
            ctk.set_appearance_mode("Light")
            self.switch_tema.configure(text="Tema Claro")

            # Cores para Tabela Light
            bg_color = "#FFFFFF"  # Fundo Branco
            text_color = "#333333"  # Texto Cinza Escuro
            header_bg = "#2E7D32"  # Cabeçalho (Verde Padrão)
            header_text = "white"  # Texto do Cabeçalho
            selected_bg = "#C8E6C9"  # Seleção (Verde Claro)

            # Cores para o Home
            novo_texto_home = "#333333"
            novo_bg_home = "#F5F7F9"

        # 2. Atualização do Estilo da Tabela (O "Hack" Visual)
        style = ttk.Style()
        style.theme_use("clam")  # 'clam' é o melhor tema base para personalizar

        # Configura o visual geral da Treeview (Corpo da tabela)
        style.configure(
            "Treeview",
            background=bg_color,
            foreground=text_color,
            fieldbackground=bg_color,
            borderwidth=0,  # Remove borda 3D
            rowheight=40,  # Aumenta altura da linha (Visual Moderno)
            font=("Roboto", 11),
        )  # Fonte mais bonita

        # Remove a borda ativa chata
        style.map(
            "Treeview",
            background=[("selected", selected_bg)],
            foreground=[
                ("selected", "black" if self.switch_tema.get() == 0 else "white")
            ],
        )

        # Configura o Cabeçalho (Header)
        style.configure(
            "Treeview.Heading",
            background=header_bg,
            foreground=header_text,
            relief="flat",  # Remove relevo do botão de título
            borderwidth=0,
            font=("Roboto", 12, "bold"),
        )

        # Hack para remover a borda branca/cinza que sobra no cabeçalho
        style.map(
            "Treeview.Heading",
            background=[("active", header_bg)],
            relief=[("pressed", "flat"), ("!pressed", "flat")],
        )

        # 3. Atualiza elementos da Home (Logo e Texto)
        if hasattr(self, "lbl_home_title") and self.lbl_home_title.winfo_exists():
            self.lbl_home_title.configure(text_color=novo_texto_home)

    def clear_main_frame(self):
        self.selected_id = None
        for widget in self.frame_main.winfo_children():
            widget.destroy()

    def get_icon(self, name):
        try:
            return ctk.CTkImage(
                Image.open(resource_path(f"assets/{name}")), size=(20, 20)
            )
        except:
            return None

    def create_table(self, parent, headers, columns_width):
        # Frame Container
        frame_container = ctk.CTkFrame(parent, fg_color="transparent")
        frame_container.pack(fill="both", expand=True)

        # Scrollbars Modernas
        vsb = ctk.CTkScrollbar(frame_container, orientation="vertical")
        hsb = ctk.CTkScrollbar(frame_container, orientation="horizontal")

        tree = ttk.Treeview(
            frame_container,
            selectmode="browse",
            columns=headers,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
        )

        vsb.configure(command=tree.yview)
        hsb.configure(command=tree.xview)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)

        # Configuração das colunas (CENTRALIZANDO TUDO)
        for col, width in zip(headers, columns_width):
            tree.heading(
                col, text=col, anchor="center"
            )  # Centraliza o Título da coluna
            tree.column(
                col, width=width, anchor="center"
            )  # Centraliza o Conteúdo da coluna

        return tree, vsb, hsb

    # =========================================================================
    # TELAS (VIEWS)
    # =========================================================================

    # --- HOME (Logo com Círculo Corrigido) ---
    # --- HOME (Logo "Montado" - Qualidade Máxima) ---
    # --- HOME (Logo + Dashboard de Cards) ---
    # --- HOME (Logo em Blocos + Dashboard Automático) ---
    # --- HOME (Centralização Perfeita) ---
    def view_home(self):
        self.clear_main_frame()

        # Container Mestre (Fica flutuando exatamente no meio da tela)
        self.container_center = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        self.container_center.place(relx=0.5, rely=0.5, anchor="center")

        # --- 1. LOGO ---
        # (Código dos blocos igual ao anterior, mas empacotado no container_center)
        block_size = 35
        gap = 6
        rad = block_size
        color_green = "#2E7D32"
        color_red = "#D32F2F"

        frame_logo = ctk.CTkFrame(self.container_center, fg_color="transparent")
        frame_logo.pack(pady=(0, 20))  # Espaço embaixo do logo

        def create_block(row, col, color, is_circle=False):
            if is_circle:
                btn = ctk.CTkButton(
                    frame_logo,
                    text="",
                    width=block_size,
                    height=block_size,
                    corner_radius=rad,
                    fg_color=color,
                    hover=False,
                    state="disabled",
                )
                btn.grid(row=row, column=col, padx=gap / 2, pady=gap / 2)
            else:
                frm = ctk.CTkFrame(
                    frame_logo,
                    width=block_size,
                    height=block_size,
                    corner_radius=0,
                    fg_color=color,
                )
                frm.grid(row=row, column=col, padx=gap / 2, pady=gap / 2)

        # Desenho
        create_block(0, 0, color_red, True)
        create_block(0, 1, color_green)
        create_block(0, 2, color_green)
        create_block(1, 0, color_green)
        create_block(1, 1, color_green)
        create_block(2, 0, color_green)
        create_block(2, 1, color_green)
        create_block(2, 2, color_green)
        create_block(3, 0, color_green)
        create_block(3, 1, color_green)

        # Título
        self.lbl_home_title = ctk.CTkLabel(
            self.container_center,
            text="Sistema Bibliotecário",
            font=("Roboto", 28, "bold"),
            text_color=("black", "white"),
        )
        self.lbl_home_title.pack(pady=(10, 30))  # Espaço entre Título e Cards

        # --- 2. CARDS (Lado a Lado) ---
        frame_cards = ctk.CTkFrame(self.container_center, fg_color="transparent")
        frame_cards.pack()

        def create_kpi_card(parent, title, value, color_bar):
            card = ctk.CTkFrame(
                parent,
                width=220,
                height=100,
                corner_radius=10,
                fg_color=("white", "#2b2b2b"),
            )
            card.pack_propagate(False)

            bar = ctk.CTkFrame(
                card, width=10, height=100, corner_radius=0, fg_color=color_bar
            )
            bar.pack(side="left", fill="y")

            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(side="left", padx=15, pady=10)

            ctk.CTkLabel(
                content,
                text=title,
                font=("Roboto", 14),
                text_color=("gray40", "gray80"),
            ).pack(anchor="w")
            ctk.CTkLabel(
                content,
                text=str(value),
                font=("Roboto", 30, "bold"),
                text_color=("#333333", "white"),
            ).pack(anchor="w")
            return card

        # --- DADOS DO DASHBOARD ---
        try:
            qtd_livros = len(get_books())
        except:
            qtd_livros = 0

        try:
            qtd_users = len(get_users())
        except:
            qtd_users = 0

        try:
            qtd_loans = len(get_loans(somente_ativos=True))
        except:
            qtd_loans = 0

        # Posicionamento dos Cards
        card1 = create_kpi_card(
            frame_cards, "Total de Livros", qtd_livros, "#2196F3"
        )  # Azul
        card1.grid(row=0, column=0, padx=10)

        # MUDANÇA AQUI: Título atualizado para refletir a realidade
        card2 = create_kpi_card(
            frame_cards, "Empréstimos Ativos", qtd_loans, "#FF9800"
        )  # Laranja (Atenção)
        card2.grid(row=0, column=1, padx=10)

        card3 = create_kpi_card(
            frame_cards, "Usuários Cadastrados", qtd_users, "#4CAF50"
        )  # Verde
        card3.grid(row=0, column=2, padx=10)

    # --- GERENCIAR LIVROS ---
    # --- GERENCIAR LIVROS (CENTRALIZADO E COM PESQUISA) ---
    # --- GERENCIAR LIVROS (SEM SCROLL NO FORMULÁRIO) ---
    def view_gerenciar_livros(self):
        self.clear_main_frame()

        # 1. Título
        ctk.CTkLabel(
            self.frame_main,
            text="Gerenciar Livros",
            font=("Roboto", 24, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(pady=20)

        # 2. Formulário (Frame Normal, sem Scrollbar)
        # Removi o ScrollableFrame e voltei para Frame simples
        frame_form = ctk.CTkFrame(self.frame_main, fg_color="transparent", width=900)
        frame_form.pack(pady=10)

        # Helpers
        def create_input(row, col, label, width=200):
            ctk.CTkLabel(frame_form, text=label, text_color=COLOR_TEXT_PRIMARY).grid(
                row=row, column=col, padx=10, sticky="e"
            )
            entry = ctk.CTkEntry(frame_form, width=width)
            entry.grid(row=row, column=col + 1, padx=10, pady=5)
            return entry

        def create_combo(row, col, label, values, width=200):
            ctk.CTkLabel(frame_form, text=label, text_color=COLOR_TEXT_PRIMARY).grid(
                row=row, column=col, padx=10, sticky="e"
            )
            combo = ctk.CTkComboBox(frame_form, values=values, width=width)
            combo.grid(row=row, column=col + 1, padx=10, pady=5)
            return combo

        # --- CAMPOS DO FORMULÁRIO ---
        self.e_titulo = create_input(0, 0, "Título:", 300)
        self.e_autor = create_input(0, 2, "Autor:", 200)

        # Linha 2
        self.e_editora = create_input(1, 0, "Editora:", 300)

        # Agrupando Ano e Qtd
        f_ano_qtd = ctk.CTkFrame(frame_form, fg_color="transparent")
        f_ano_qtd.grid(row=1, column=3, sticky="w", padx=10)

        ctk.CTkLabel(f_ano_qtd, text="Ano:", text_color=COLOR_TEXT_PRIMARY).pack(
            side="left", padx=5
        )
        self.e_ano = ctk.CTkEntry(f_ano_qtd, width=60)
        self.e_ano.pack(side="left")

        ctk.CTkLabel(f_ano_qtd, text="Qtd:", text_color=COLOR_TEXT_PRIMARY).pack(
            side="left", padx=(15, 5)
        )
        self.e_qtd = ctk.CTkEntry(f_ano_qtd, width=40)
        self.e_qtd.pack(side="left")

        # Linha 3
        self.e_isbn = create_input(2, 0, "ISBN:", 200)
        self.e_cidade = create_input(2, 2, "Cidade:", 200)

        # Linha 4
        list_ufs = [
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        ]
        self.e_uf = create_combo(3, 0, "UF:", list_ufs, 80)
        self.e_origem = create_combo(
            3, 2, "Origem:", ["Doação", "Governo", "Compra"], 150
        )

        # Linha 5
        self.e_genero = create_combo(
            4, 0, "Gênero:", get_generos_list() or ["Geral"], 200
        )
        self.e_prat = create_combo(
            4, 2, "Prateleira:", get_prateleiras_list() or ["A1"], 100
        )

        # --- BOTÕES ---
        frame_btns = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_btns.pack(pady=10)

        self.btn_salvar = ctk.CTkButton(
            frame_btns,
            text="Salvar",
            command=self.salvar_livro,
            fg_color=COLOR_ACCENT,
            width=150,
        )
        self.btn_salvar.pack(side="left", padx=10)

        ctk.CTkButton(
            frame_btns,
            text="Limpar",
            command=self.limpar_campos_livro,
            fg_color="gray",
            width=100,
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            frame_btns,
            text="Excluir",
            command=self.excluir_livro,
            fg_color=COLOR_DANGER,
            width=100,
        ).pack(side="left", padx=10)

        # --- BARRA DE PESQUISA ---
        frame_search = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_search.pack(fill="x", padx=50, pady=(20, 5))

        ctk.CTkLabel(
            frame_search, text="Pesquisar Livro:", text_color=COLOR_TEXT_PRIMARY
        ).pack(side="left", padx=10)
        entry_search = ctk.CTkEntry(
            frame_search, placeholder_text="Digite título ou autor...", width=300
        )
        entry_search.pack(side="left", padx=10)

        def filtrar_tabela(event):
            termo = entry_search.get()
            for i in self.tree_livros.get_children():
                self.tree_livros.delete(i)
            livros = get_books(termo)
            for row in livros:
                # Mantendo a ordenação correta da Qtd
                dados_ordenados = [
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[11],
                    row[6],
                    row[7],
                    row[8],
                    row[9],
                    row[10],
                ]
                self.tree_livros.insert("", "end", values=dados_ordenados)

        entry_search.bind("<KeyRelease>", filtrar_tabela)

        # --- TABELA ---
        headers = [
            "ID",
            "Título",
            "Autor",
            "Editora",
            "Ano",
            "ISBN",
            "Qtd",
            "Origem",
            "Gênero",
            "Cidade",
            "UF",
            "Prat",
        ]
        widths = [30, 150, 100, 80, 50, 80, 40, 70, 80, 80, 40, 50]

        frame_table = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree_livros, vsb, hsb = self.create_table(frame_table, headers, widths)
        self.tree_livros.pack(fill="both", expand=True, side="left")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.tree_livros.bind("<<TreeviewSelect>>", self.selecionar_livro)
        self.carregar_tabela_livros()

    def carregar_tabela_livros(self):
        for i in self.tree_livros.get_children():
            self.tree_livros.delete(i)

        for row in get_books():
            # row original do Banco:
            # [0:ID, 1:Titulo, 2:Autor, 3:Editora, 4:Ano, 5:ISBN, 6:Origem, 7:Genero, 8:Cidade, 9:Estado, 10:Prat, 11:Qtd]

            # Vamos criar uma nova lista na ordem que a Tabela Visual pede:
            # ["ID", "Título", "Autor", "Editora", "Ano", "ISBN", "Qtd", "Origem", "Gênero", "Cidade", "UF", "Prat"]

            dados_ordenados = [
                row[0],  # ID
                row[1],  # Título
                row[2],  # Autor
                row[3],  # Editora
                row[4],  # Ano
                row[5],  # ISBN
                row[11],  # <--- QUANTIDADE (Puxamos do fim (índice 11) para o meio)
                row[6],  # Origem
                row[7],  # Gênero
                row[8],  # Cidade
                row[9],  # UF
                row[10],  # Prateleira
            ]
            self.tree_livros.insert("", "end", values=dados_ordenados)

    def limpar_campos_livro(self):
        self.selected_id = None
        entries = [
            self.e_titulo,
            self.e_autor,
            self.e_editora,
            self.e_ano,
            self.e_isbn,
            self.e_cidade,
            self.e_qtd,
        ]
        for e in entries:
            e.delete(0, "end")
        self.btn_salvar.configure(text="Salvar Novo")

    def selecionar_livro(self, event):
        try:
            item = self.tree_livros.selection()[0]
            vals = self.tree_livros.item(item, "values")
            # Agora 'vals' está na ordem visual:
            # 0:ID, 1:Titulo, 2:Autor, 3:Editora, 4:Ano, 5:ISBN, 6:Qtd, 7:Origem, 8:Genero, 9:Cidade, 10:UF, 11:Prat

            self.selected_id = vals[0]

            self.e_titulo.delete(0, "end")
            self.e_titulo.insert(0, vals[1])
            self.e_autor.delete(0, "end")
            self.e_autor.insert(0, vals[2])
            self.e_editora.delete(0, "end")
            self.e_editora.insert(0, vals[3])
            self.e_ano.delete(0, "end")
            self.e_ano.insert(0, vals[4])
            self.e_isbn.delete(0, "end")
            self.e_isbn.insert(0, vals[5])

            # Quantidade agora está no índice 6 da lista visual
            self.e_qtd.delete(0, "end")
            self.e_qtd.insert(0, vals[6])

            self.e_origem.set(vals[7])
            self.e_genero.set(vals[8])
            self.e_cidade.delete(0, "end")
            self.e_cidade.insert(0, vals[9])
            self.e_uf.set(vals[10])
            self.e_prat.set(vals[11])

            self.btn_salvar.configure(text="Atualizar")
        except IndexError:
            pass
        except Exception as e:
            print(f"Erro ao selecionar: {e}")

    def salvar_livro(self):
        if not self.e_titulo.get():
            CTkMessagebox(
                title="Atenção", message="Título é obrigatório.", icon="warning"
            )
            return

        args = [
            self.e_titulo.get(),
            self.e_autor.get(),
            self.e_editora.get(),
            self.e_ano.get(),
            self.e_isbn.get(),
            self.e_origem.get(),
            self.e_genero.get(),
            self.e_cidade.get(),
            self.e_uf.get(),
            self.e_prat.get(),
            self.e_qtd.get() or 1,
        ]

        try:
            if self.selected_id:
                update_book(self.selected_id, *args)
                CTkMessagebox(
                    title="Sucesso",
                    message="Livro Atualizado com Sucesso!",
                    icon="check",
                )
            else:
                insert_book(*args)
                CTkMessagebox(
                    title="Sucesso",
                    message="Livro Cadastrado com Sucesso!",
                    icon="check",
                )

            self.limpar_campos_livro()
            self.carregar_tabela_livros()
        except Exception as e:
            CTkMessagebox(
                title="Erro", message=f"Erro no banco de dados: {e}", icon="cancel"
            )

    def excluir_livro(self):
        if not self.selected_id:
            return
        # Pergunta de confirmação moderna
        msg = CTkMessagebox(
            title="Confirmar",
            message="Deseja excluir este livro permanentemente?",
            icon="question",
            option_1="Cancelar",
            option_2="Excluir",
        )

        if msg.get() == "Excluir":
            delete_book(self.selected_id)
            self.limpar_campos_livro()
            self.carregar_tabela_livros()
            CTkMessagebox(title="Apagado", message="Livro excluído.", icon="check")

    # --- GERENCIAR USUÁRIOS ---
    # --- GERENCIAR USUÁRIOS (COM PESQUISA E CAMPOS EXTRAS) ---
    def view_gerenciar_usuarios(self):
        self.clear_main_frame()

        # 1. Título
        ctk.CTkLabel(
            self.frame_main,
            text="Gerenciar Usuários",
            font=("Roboto", 24, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(pady=20)

        # 2. Formulário Centralizado
        frame_form = ctk.CTkFrame(self.frame_main, fg_color="transparent", width=850)
        frame_form.pack(pady=10)

        # Helpers
        def create_input(row, col, label, width=200):
            ctk.CTkLabel(frame_form, text=label, text_color=COLOR_TEXT_PRIMARY).grid(
                row=row, column=col, padx=10, sticky="e"
            )
            entry = ctk.CTkEntry(frame_form, width=width)
            entry.grid(row=row, column=col + 1, padx=10, pady=5)
            return entry

        # --- CAMPOS ---
        # Linha 0: Nome (Obrigatório) e Turma
        self.e_u_nome = create_input(0, 0, "Nome:", 300)

        ctk.CTkLabel(frame_form, text="Turma:", text_color=COLOR_TEXT_PRIMARY).grid(
            row=0, column=2, padx=10, sticky="e"
        )
        self.e_u_turma = ctk.CTkComboBox(
            frame_form,
            values=["6º Ano", "7º Ano", "8º Ano", "9º Ano", "Ensino Médio"],
            width=150,
        )
        self.e_u_turma.grid(row=0, column=3, padx=10, pady=5)

        # Linha 1: Telefone e Email (Opcional)
        self.e_u_tel = create_input(1, 0, "Telefone:", 200)
        self.e_u_email = create_input(1, 2, "Email (Opc.):", 300)

        # Linha 2: Endereço (Opcional) - Ocupando a largura toda para ficar bonito
        ctk.CTkLabel(
            frame_form, text="Endereço (Opc.):", text_color=COLOR_TEXT_PRIMARY
        ).grid(row=2, column=0, padx=10, sticky="e")
        self.e_u_end = ctk.CTkEntry(frame_form, width=600)  # Campo mais largo
        self.e_u_end.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="w")

        # --- BOTÕES ---
        frame_btns = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_btns.pack(pady=15)

        self.btn_salvar_user = ctk.CTkButton(
            frame_btns,
            text="Salvar",
            command=self.salvar_user,
            fg_color=COLOR_ACCENT,
            width=150,
        )
        self.btn_salvar_user.pack(side="left", padx=10)

        ctk.CTkButton(
            frame_btns,
            text="Limpar",
            command=self.limpar_campos_user,
            fg_color="gray",
            width=100,
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            frame_btns,
            text="Excluir",
            command=self.excluir_user,
            fg_color=COLOR_DANGER,
            width=100,
        ).pack(side="left", padx=10)

        # --- BARRA DE PESQUISA (Igual Livros) ---
        frame_search = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_search.pack(fill="x", padx=50, pady=(10, 5))

        ctk.CTkLabel(
            frame_search, text="Pesquisar Usuário:", text_color=COLOR_TEXT_PRIMARY
        ).pack(side="left", padx=10)
        entry_search = ctk.CTkEntry(
            frame_search, placeholder_text="Digite o nome...", width=300
        )
        entry_search.pack(side="left", padx=10)

        def filtrar_users(event):
            termo = entry_search.get()
            for i in self.tree_users.get_children():
                self.tree_users.delete(i)
            # Chama a função do view.py passando o termo
            for row in get_users(termo):
                self.tree_users.insert("", "end", values=row)

        entry_search.bind("<KeyRelease>", filtrar_users)

        # --- TABELA ---
        # Adicionei Endereço e Email na visualização da tabela também
        headers = ["ID", "Nome", "Turma", "Endereço", "Email", "Telefone"]
        widths = [30, 200, 100, 200, 150, 100]

        frame_table = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree_users, vsb, hsb = self.create_table(frame_table, headers, widths)
        self.tree_users.pack(fill="both", expand=True, side="left")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.tree_users.bind("<<TreeviewSelect>>", self.selecionar_user)
        self.carregar_tabela_users()

    # --- FUNÇÕES AUXILIARES DE USUÁRIO (ATUALIZADAS) ---
    def carregar_tabela_users(self):
        for i in self.tree_users.get_children():
            self.tree_users.delete(i)
        for row in get_users():
            self.tree_users.insert("", "end", values=row)

    def limpar_campos_user(self):
        self.selected_id = None
        self.e_u_nome.delete(0, "end")
        self.e_u_tel.delete(0, "end")
        self.e_u_email.delete(0, "end")
        self.e_u_end.delete(0, "end")
        self.btn_salvar_user.configure(text="Salvar Novo")

    def selecionar_user(self, event):
        try:
            vals = self.tree_users.item(self.tree_users.selection()[0], "values")
            # Ordem: 0:ID, 1:Nome, 2:Turma, 3:Endereço, 4:Email, 5:Telefone
            self.selected_id = vals[0]

            self.e_u_nome.delete(0, "end")
            self.e_u_nome.insert(0, vals[1])
            self.e_u_turma.set(vals[2])
            self.e_u_end.delete(0, "end")
            self.e_u_end.insert(0, vals[3])
            self.e_u_email.delete(0, "end")
            self.e_u_email.insert(0, vals[4])
            self.e_u_tel.delete(0, "end")
            self.e_u_tel.insert(0, vals[5])

            self.btn_salvar_user.configure(text="Atualizar")
        except:
            pass

    def salvar_user(self):
        if not self.e_u_nome.get():
            CTkMessagebox(
                title="Atenção", message="O nome é obrigatório.", icon="warning"
            )
            return

        nome = self.e_u_nome.get()
        turma = self.e_u_turma.get()
        tel = self.e_u_tel.get()
        email = self.e_u_email.get()
        end = self.e_u_end.get()

        try:
            if self.selected_id:
                update_user(self.selected_id, nome, turma, end, email, tel)
                CTkMessagebox(
                    title="Sucesso", message="Usuário atualizado!", icon="check"
                )
            else:
                insert_user(nome, turma, end, email, tel)
                CTkMessagebox(
                    title="Sucesso", message="Usuário cadastrado!", icon="check"
                )

            self.limpar_campos_user()
            self.carregar_tabela_users()
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao salvar: {e}", icon="cancel")

    def excluir_user(self):
        if not self.selected_id:
            return

        msg = CTkMessagebox(
            title="Confirmar",
            message="Excluir este usuário?",
            icon="question",
            option_1="Cancelar",
            option_2="Excluir",
        )

        if msg.get() == "Excluir":
            delete_user(self.selected_id)
            self.limpar_campos_user()
            self.carregar_tabela_users()
            CTkMessagebox(title="Apagado", message="Usuário excluído.", icon="check")

    # --- AUXILIARES ---
    def view_auxiliar(self, tipo):
        self.clear_main_frame()
        title = "Gêneros" if tipo == "genero" else "Prateleiras"
        ctk.CTkLabel(
            self.frame_main,
            text=f"Gerenciar {title}",
            font=("Arial", 20, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(pady=20)

        e_nome = ctk.CTkEntry(
            self.frame_main, width=300, placeholder_text=f"Nome do {title}"
        )
        e_nome.pack(pady=10)

        def add():
            if not e_nome.get():
                return
            if tipo == "genero":
                insert_genero(e_nome.get())
            else:
                insert_prateleira(e_nome.get())
            carregar()
            e_nome.delete(0, "end")

        ctk.CTkButton(
            self.frame_main, text="Adicionar", command=add, fg_color=COLOR_ACCENT
        ).pack(pady=10)

        tree, _, _ = self.create_table(self.frame_main, ["ID", "Nome"], [50, 400])
        tree.pack(fill="both", expand=True, padx=20, pady=20)

        def carregar():
            for i in tree.get_children():
                tree.delete(i)
            rows = get_generos() if tipo == "genero" else get_prateleiras()
            for r in rows:
                tree.insert("", "end", values=r)

        carregar()

    # --- EMPRÉSTIMOS ---
    # --- EMPRÉSTIMOS (COM PESQUISA INTELIGENTE) ---
    # --- EMPRÉSTIMOS (ALINHADO E ORGANIZADO) ---
    # --- EMPRÉSTIMOS (CENTRALIZADO) ---
    # --- EMPRÉSTIMOS (CENTRALIZADO) ---
    # --- EMPRÉSTIMOS (Centralização Forçada com Place) ---
    # Não esqueça de colocar lá em cima: from CTkMessagebox import CTkMessagebox

    # --- EMPRÉSTIMOS (COM DATA DE PRAZO) ---
    def view_emprestimos(self):
        self.clear_main_frame()

        tabview = ctk.CTkTabview(self.frame_main, text_color=COLOR_TEXT_PRIMARY)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)

        t_novo = tabview.add("Novo Empréstimo")
        t_dev = tabview.add("Devolução")

        # --- LÓGICA DE FILTRAGEM ---
        todos_livros = get_books_list()
        todos_usuarios = get_users_list()

        def atualizar_lista_livros(event):
            digitado = entry_search_livro.get().lower()
            if digitado == "":
                cb_livro.configure(values=todos_livros)
            else:
                lista_filtrada = [
                    livro for livro in todos_livros if digitado in livro.lower()
                ]
                if not lista_filtrada:
                    lista_filtrada = ["Nenhum livro encontrado"]
                cb_livro.configure(values=lista_filtrada)
                cb_livro.set(lista_filtrada[0])

        def atualizar_lista_usuarios(event):
            digitado = entry_search_user.get().lower()
            if digitado == "":
                cb_user.configure(values=todos_usuarios)
            else:
                lista_filtrada = [u for u in todos_usuarios if digitado in u.lower()]
                if not lista_filtrada:
                    lista_filtrada = ["Nenhum usuário encontrado"]
                cb_user.configure(values=lista_filtrada)
                cb_user.set(lista_filtrada[0])

        # ==================================================
        # ABA 1: NOVO EMPRÉSTIMO
        # ==================================================

        form_container = ctk.CTkFrame(t_novo, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.05, anchor="n")

        # 1. LIVRO
        ctk.CTkLabel(
            form_container,
            text="1. Pesquise o Livro:",
            text_color=COLOR_TEXT_PRIMARY,
            font=("Roboto", 16, "bold"),
        ).pack(pady=(10, 5))
        entry_search_livro = ctk.CTkEntry(
            form_container, width=500, placeholder_text="Digite o nome do livro..."
        )
        entry_search_livro.pack(pady=5)
        entry_search_livro.bind("<KeyRelease>", atualizar_lista_livros)
        cb_livro = ctk.CTkComboBox(form_container, values=todos_livros, width=500)
        cb_livro.pack(pady=(0, 20))

        # 2. ALUNO
        ctk.CTkLabel(
            form_container,
            text="2. Pesquise o Aluno:",
            text_color=COLOR_TEXT_PRIMARY,
            font=("Roboto", 16, "bold"),
        ).pack(pady=(10, 5))
        entry_search_user = ctk.CTkEntry(
            form_container, width=500, placeholder_text="Digite o nome do aluno..."
        )
        entry_search_user.pack(pady=5)
        entry_search_user.bind("<KeyRelease>", atualizar_lista_usuarios)
        cb_user = ctk.CTkComboBox(form_container, values=todos_usuarios, width=500)
        cb_user.pack(pady=(0, 20))

        # 3. PRAZO DE DEVOLUÇÃO (NOVO)
        ctk.CTkLabel(
            form_container,
            text="3. Data Limite para Devolução:",
            text_color=COLOR_TEXT_PRIMARY,
            font=("Roboto", 16, "bold"),
        ).pack(pady=(10, 5))

        entry_prazo = ctk.CTkEntry(form_container, width=500)
        entry_prazo.pack(pady=(0, 30))

        # Preenche automaticamente com a data de hoje + 15 dias
        data_hoje = datetime.now()
        data_15_dias = data_hoje + timedelta(days=15)
        entry_prazo.insert(0, data_15_dias.strftime("%d-%m-%Y"))

        # BOTÃO
        def confirmar_emp():
            try:
                val_livro = cb_livro.get()
                val_user = cb_user.get()
                prazo = entry_prazo.get()

                if "Nenhum" in val_livro or "Nenhum" in val_user:
                    CTkMessagebox(
                        title="Atenção",
                        message="Selecione dados válidos.",
                        icon="warning",
                    )
                    return

                lid = int(val_livro.split(":")[0])
                uid = int(val_user.split(":")[0])

                # Passamos o prazo para a função de insert
                insert_loan(lid, uid, datetime.now().strftime("%d-%m-%Y"), prazo)

                CTkMessagebox(
                    title="Sucesso",
                    message="Empréstimo realizado!",
                    icon="check",
                    option_1="OK",
                )

                entry_search_livro.delete(0, "end")
                entry_search_user.delete(0, "end")
                atualizar_lista_devolucao()

            except Exception as e:
                CTkMessagebox(title="Erro", message=str(e), icon="cancel")

        ctk.CTkButton(
            form_container,
            text="CONFIRMAR EMPRÉSTIMO",
            command=confirmar_emp,
            fg_color=COLOR_ACCENT,
            height=50,
            width=500,
            font=("Roboto", 15, "bold"),
        ).pack()

        # ==================================================
        # ABA 2: DEVOLUÇÃO
        # ==================================================
        dev_container = ctk.CTkFrame(t_dev, fg_color="transparent")
        dev_container.place(relx=0.5, rely=0.1, anchor="n")

        def atualizar_lista_devolucao():
            loans = get_loans_list()
            if not loans:
                cb_loans.configure(values=["Nenhum empréstimo ativo"])
                cb_loans.set("Nenhum empréstimo ativo")
            else:
                cb_loans.configure(values=loans)
                cb_loans.set(loans[0])

        ctk.CTkLabel(
            dev_container,
            text="Selecione o Empréstimo Ativo:",
            text_color=COLOR_TEXT_PRIMARY,
            font=("Roboto", 16, "bold"),
        ).pack(pady=(0, 5))

        loans_iniciais = get_loans_list() or ["Nenhum empréstimo ativo"]
        cb_loans = ctk.CTkComboBox(dev_container, values=loans_iniciais, width=500)
        cb_loans.pack(pady=10)

        def confirmar_dev():
            try:
                val = cb_loans.get()
                if "Nenhum" in val:
                    return
                lid = int(val.split(":")[0])
                return_loan(lid, datetime.now().strftime("%d-%m-%Y"))
                CTkMessagebox(
                    title="Devolvido", message="Livro Devolvido!", icon="check"
                )
                atualizar_lista_devolucao()
            except:
                pass

        ctk.CTkButton(
            dev_container,
            text="CONFIRMAR DEVOLUÇÃO",
            command=confirmar_dev,
            fg_color=COLOR_DANGER,
            height=50,
            width=500,
            font=("Roboto", 15, "bold"),
        ).pack(pady=20)

    # --- CONSULTAS GERAIS ---
    # --- CONSULTAS GERAIS (COM FILTRO DE ATIVOS) ---
    def view_table(self, type_data):
        self.clear_main_frame()

        # Configurações baseadas no tipo
        if type_data == "users":
            title_text = "Consultar Usuários"
            headers = ["ID", "Nome", "Turma", "Endereço", "Email", "Telefone"]
            widths = [30, 150, 80, 150, 150, 100]
            get_data_func = get_users

        elif type_data == "books":
            title_text = "Consultar Livros"
            headers = [
                "ID",
                "Título",
                "Autor",
                "Editora",
                "Ano",
                "ISBN",
                "Origem",
                "Gênero",
            ]
            widths = [30, 200, 150, 100, 50, 80, 80, 80]
            get_data_func = get_books

        elif type_data == "loans":
            title_text = "Empréstimos Ativos"  # Título padrão
            headers = ["ID", "Livro", "Usuário", "Data Emp", "Data Dev", "Status"]
            widths = [30, 300, 150, 90, 90, 100]
            get_data_func = get_loans

        # Frame de Título e Busca
        frame_top = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_top.pack(fill="x", padx=20, pady=20)

        # Título
        lbl_titulo = ctk.CTkLabel(
            frame_top,
            text=title_text,
            font=("Roboto", 24, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        )
        lbl_titulo.pack(side="left")

        # Barra de Pesquisa
        entry_busca = ctk.CTkEntry(
            frame_top, placeholder_text="Pesquisar...", width=250
        )
        entry_busca.pack(side="right", padx=10)

        # --- SWITCH DE HISTÓRICO (Só aparece se for Empréstimos) ---
        if type_data == "loans":
            switch_var = ctk.StringVar(value="off")

            def toggle_historico():
                # Se estiver ligado ("on"), mostra TODOS. Se desligado ("off"), só ATIVOS.
                mostrar_todos = switch_var.get() == "on"
                filtrar(mostrar_todos=mostrar_todos)

                # Muda o título pra dar feedback
                if mostrar_todos:
                    lbl_titulo.configure(text="Histórico Completo")
                else:
                    lbl_titulo.configure(text="Empréstimos Ativos")

            switch = ctk.CTkSwitch(
                frame_top,
                text="Ver Devolvidos",
                variable=switch_var,
                onvalue="on",
                offvalue="off",
                command=toggle_historico,
                progress_color=COLOR_ACCENT,
            )
            switch.pack(side="right", padx=20)

        def filtrar(event=None, mostrar_todos=False):
            termo = entry_busca.get()

            # Limpa a tabela
            for i in tree.get_children():
                tree.delete(i)

            # Lógica diferente para Empréstimos vs Outros
            if type_data == "loans":
                # Se mostrar_todos=True, então somente_ativos=False
                novos_dados = get_data_func(
                    search_term=termo, somente_ativos=not mostrar_todos
                )
            else:
                novos_dados = get_data_func(search_term=termo)

            for r in novos_dados:
                # Garante que não pegue colunas extras se houver
                display_row = r[: len(headers)]
                tree.insert("", "end", values=display_row)

        entry_busca.bind(
            "<KeyRelease>",
            lambda e: filtrar(
                e, mostrar_todos=(type_data == "loans" and switch_var.get() == "on")
            ),
        )

        # Tabela
        frame_table = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        frame_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tree, vsb, hsb = self.create_table(frame_table, headers, widths)
        tree.pack(fill="both", expand=True, side="left")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Carga Inicial (Para empréstimos, começa mostrando SÓ ATIVOS)
        if type_data == "loans":
            filtrar(mostrar_todos=False)
        elif type_data == "loans":
            title_text = "Empréstimos Ativos"
            # Adicionei "Prazo" nos cabeçalhos
            headers = [
                "ID",
                "Livro",
                "Usuário",
                "Data Emp",
                "Prazo",
                "Data Dev",
                "Status",
            ]
            widths = [30, 300, 150, 90, 90, 90, 100]
            get_data_func = get_loans
        else:
            filtrar()
