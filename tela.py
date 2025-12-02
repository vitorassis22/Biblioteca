import sys
import os
import shutil  # Necessário para o Backup
import customtkinter as ctk
from tkinter import ttk, messagebox
from CTkMessagebox import CTkMessagebox
from datetime import datetime, timedelta
from PIL import Image
import pandas as pd  # Necessário para Relatórios
from reportlab.lib.pagesizes import letter # Necessário para PDF
from reportlab.pdfgen import canvas # Necessário para PDF

# Importa todas as funções do view
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

        self.title("Sistema Sala de Leitura")
        self.geometry("1100x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected_id = None

        # Configura o fechamento da janela para realizar BACKUP
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ===================================================
        # 1. MENU LATERAL (FIXO)
        # ===================================================
        self.frame_menu = ctk.CTkFrame(
            self, width=220, corner_radius=0, fg_color=COLOR_MENU_BG
        )
        self.frame_menu.grid(row=0, column=0, sticky="nsew")

        # Título do Menu
        self.label_titulo = ctk.CTkLabel(
            self.frame_menu,
            text="Sala\nde\nLeitura",
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
            text_color="white",
        )
        self.label_titulo.grid(
            row=0, column=0, padx=20, pady=(40, 20)
        )

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
            ("Relatórios e Dados", self.view_relatorios), # <--- NOVO BOTÃO AQUI
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
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.switch_tema.configure(text="Tema Escuro")
            bg_color = "#2b2b2b"
            text_color = "white"
            header_bg = "#1B5E20"
            header_text = "white"
            selected_bg = "#2E7D32"
            novo_texto_home = "#FFFFFF"
        else:
            ctk.set_appearance_mode("Light")
            self.switch_tema.configure(text="Tema Claro")
            bg_color = "#FFFFFF"
            text_color = "#333333"
            header_bg = "#2E7D32"
            header_text = "white"
            selected_bg = "#C8E6C9"
            novo_texto_home = "#333333"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=bg_color,
            foreground=text_color,
            fieldbackground=bg_color,
            borderwidth=0,
            rowheight=40,
            font=("Roboto", 11),
        )
        style.map(
            "Treeview",
            background=[("selected", selected_bg)],
            foreground=[("selected", "black" if self.switch_tema.get() == 0 else "white")],
        )
        style.configure(
            "Treeview.Heading",
            background=header_bg,
            foreground=header_text,
            relief="flat",
            borderwidth=0,
            font=("Roboto", 12, "bold"),
        )
        style.map(
            "Treeview.Heading",
            background=[("active", header_bg)],
            relief=[("pressed", "flat"), ("!pressed", "flat")],
        )

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
        frame_container = ctk.CTkFrame(parent, fg_color="transparent")
        frame_container.pack(fill="both", expand=True)

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

        for col, width in zip(headers, columns_width):
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=width, anchor="center")

        return tree, vsb, hsb

    # =========================================================================
    # FUNÇÃO DE BACKUP (NOVA)
    # =========================================================================
    def on_closing(self):
        """Executa backup e fecha o app"""
        try:
            if not os.path.exists("backups"):
                os.makedirs("backups")
            
            # Gera nome do arquivo com data/hora
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            backup_name = f"backups/dados_{timestamp}.db"
            
            # Copia o banco
            shutil.copy("dados.db", backup_name)
            
            # Limpeza: Mantém apenas os 5 backups mais recentes
            backups = sorted(
                [os.path.join("backups", f) for f in os.listdir("backups")], 
                key=os.path.getmtime
            )
            while len(backups) > 5:
                os.remove(backups[0])
                backups.pop(0)
                
        except Exception as e:
            print(f"Erro no backup: {e}")
        
        self.destroy()

    # =========================================================================
    # TELA DE RELATÓRIOS (NOVA)
    # =========================================================================
    def view_relatorios(self):
        self.clear_main_frame()

        # Título
        ctk.CTkLabel(
            self.frame_main,
            text="Relatórios e Estatísticas",
            font=("Roboto", 24, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(pady=20)

        # Processamento dos Dados
        dados_rank = get_books_ranking()
        raw_data = get_detailed_loan_history()
        
        # Agrupamento por data
        dict_dia, dict_mes, dict_ano = {}, {}, {}
        for row in raw_data:
            try:
                dt = datetime.strptime(row[0], "%d-%m-%Y")
                dict_dia.setdefault(dt.strftime("%d/%m/%Y"), []).append(row[1])
                dict_mes.setdefault(dt.strftime("%m/%Y"), []).append(row[1])
                dict_ano.setdefault(dt.strftime("%Y"), []).append(row[1])
            except: pass

        def prep_data(d):
            return [(k, len(v), ", ".join(v)) for k, v in sorted(d.items(), reverse=True)]

        l_dia = prep_data(dict_dia)
        l_mes = prep_data(dict_mes)
        l_ano = prep_data(dict_ano)

        # Abas
        tabview = ctk.CTkTabview(self.frame_main, text_color=COLOR_TEXT_PRIMARY)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        t_rank = tabview.add("Ranking")
        t_dia = tabview.add("Por Dia")
        t_mes = tabview.add("Por Mês")
        t_ano = tabview.add("Por Ano")
        t_export = tabview.add("Exportar")

        # Helper para criar tabelas internas
        def create_inner_tree(parent, headers, widths, data):
            frame_t = ctk.CTkFrame(parent, fg_color="transparent")
            frame_t.pack(fill="both", expand=True, padx=10, pady=10)
            tr, v, h = self.create_table(frame_t, headers, widths)
            for item in data:
                tr.insert("", "end", values=item)

        # Tabelas
        create_inner_tree(t_rank, ["Título", "Autor", "Código", "Total"], [250, 200, 100, 80], [(r[0], r[1], r[2], r[3]) for r in dados_rank])
        create_inner_tree(t_dia, ["Data", "Qtd", "Livros"], [100, 50, 400], l_dia)
        create_inner_tree(t_mes, ["Mês", "Qtd", "Livros"], [100, 50, 400], l_mes)
        create_inner_tree(t_ano, ["Ano", "Qtd", "Livros"], [100, 50, 400], l_ano)

        # Botões de Exportação
        f_exp = ctk.CTkFrame(t_export, fg_color="transparent")
        f_exp.pack(fill="both", expand=True, padx=50, pady=50)
        
        def exportar_excel():
            try:
                with pd.ExcelWriter('Relatorio_Completo.xlsx') as writer:
                    pd.DataFrame(dados_rank, columns=["Titulo","Autor","Código","Total"]).to_excel(writer, sheet_name="Ranking", index=False)
                    pd.DataFrame(l_mes, columns=["Mes","Qtd","Livros"]).to_excel(writer, sheet_name="Mensal", index=False)
                    pd.DataFrame(l_dia, columns=["Dia","Qtd","Livros"]).to_excel(writer, sheet_name="Diario", index=False)
                CTkMessagebox(title="Sucesso", message="Arquivo Excel gerado com sucesso!", icon="check")
            except Exception as e:
                CTkMessagebox(title="Erro", message=f"Erro ao exportar: {e}", icon="cancel")

        def exportar_pdf():
            try:
                c = canvas.Canvas("Relatorio_Resumo.pdf", pagesize=letter)
                y = 750
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, y, "Relatório da Biblioteca"); y -= 30
                
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, "Top 20 Livros Mais Emprestados:"); y -= 20
                c.setFont("Helvetica", 10)
                
                for i, r in enumerate(dados_rank[:20]):
                    if y < 50: c.showPage(); y = 750
                    c.drawString(50, y, f"{i+1}. {r[0]} - {r[3]} empréstimos")
                    y -= 15
                
                c.save()
                CTkMessagebox(title="Sucesso", message="PDF gerado com sucesso!", icon="check")
            except Exception as e:
                CTkMessagebox(title="Erro", message=f"Erro ao exportar: {e}", icon="cancel")

        ctk.CTkButton(f_exp, text="Exportar Excel Completo (.xlsx)", command=exportar_excel, 
                      fg_color="#217346", height=50, font=("Roboto", 16)).pack(pady=10, fill="x")
        
        ctk.CTkButton(f_exp, text="Exportar Resumo em PDF (.pdf)", command=exportar_pdf, 
                      fg_color="#B30B00", height=50, font=("Roboto", 16)).pack(pady=10, fill="x")

    # =========================================================================
    # TELAS (VIEWS ORIGINAIS - MANTIDAS)
    # =========================================================================

    def view_home(self):
        self.clear_main_frame()
        self.container_center = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        self.container_center.place(relx=0.5, rely=0.5, anchor="center")

        # LOGO
        block_size = 35; gap = 6; rad = block_size; color_green = "#2E7D32"; color_red = "#D32F2F"
        frame_logo = ctk.CTkFrame(self.container_center, fg_color="transparent")
        frame_logo.pack(pady=(0, 20))

        def create_block(row, col, color, is_circle=False):
            if is_circle:
                ctk.CTkButton(frame_logo, text="", width=block_size, height=block_size, corner_radius=rad, fg_color=color, hover=False, state="disabled").grid(row=row, column=col, padx=gap/2, pady=gap/2)
            else:
                ctk.CTkFrame(frame_logo, width=block_size, height=block_size, corner_radius=0, fg_color=color).grid(row=row, column=col, padx=gap/2, pady=gap/2)

        create_block(0,0,color_red,True); create_block(0,1,color_green); create_block(0,2,color_green)
        create_block(1,0,color_green); create_block(1,1,color_green); create_block(2,0,color_green)
        create_block(2,1,color_green); create_block(2,2,color_green); create_block(3,0,color_green); create_block(3,1,color_green)

        self.lbl_home_title = ctk.CTkLabel(self.container_center, text="Sistema Bibliotecário", font=("Roboto", 28, "bold"), text_color=("black", "white"))
        self.lbl_home_title.pack(pady=(10, 30))

        # CARDS
        frame_cards = ctk.CTkFrame(self.container_center, fg_color="transparent")
        frame_cards.pack()

        def create_kpi_card(parent, title, value, color_bar):
            card = ctk.CTkFrame(parent, width=220, height=100, corner_radius=10, fg_color=("white", "#2b2b2b"))
            card.pack_propagate(False)
            ctk.CTkFrame(card, width=10, height=100, corner_radius=0, fg_color=color_bar).pack(side="left", fill="y")
            content = ctk.CTkFrame(card, fg_color="transparent"); content.pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(content, text=title, font=("Roboto", 14), text_color=("gray40", "gray80")).pack(anchor="w")
            ctk.CTkLabel(content, text=str(value), font=("Roboto", 30, "bold"), text_color=("#333333", "white")).pack(anchor="w")
            return card

        try: q_liv = get_total_books()
        except: q_liv = 0
        try: q_use = len(get_users())
        except: q_use = 0
        try: q_emp = len(get_loans(somente_ativos=True))
        except: q_emp = 0

        create_kpi_card(frame_cards, "Total de Livros", q_liv, "#2196F3").grid(row=0, column=0, padx=10)
        create_kpi_card(frame_cards, "Empréstimos Ativos", q_emp, "#FF9800").grid(row=0, column=1, padx=10)
        create_kpi_card(frame_cards, "Usuários Cadastrados", q_use, "#4CAF50").grid(row=0, column=2, padx=10)

    def view_gerenciar_livros(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.frame_main, text="Gerenciar Livros", font=("Roboto", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(pady=20)
        
        frame_form = ctk.CTkFrame(self.frame_main, fg_color="transparent", width=900); frame_form.pack(pady=10)
        def ci(r, c, l, w=200):
            ctk.CTkLabel(frame_form, text=l, text_color=COLOR_TEXT_PRIMARY).grid(row=r, column=c, padx=10, sticky="e")
            e = ctk.CTkEntry(frame_form, width=w); e.grid(row=r, column=c+1, padx=10, pady=5); return e
        def cc(r, c, l, v, w=200):
            ctk.CTkLabel(frame_form, text=l, text_color=COLOR_TEXT_PRIMARY).grid(row=r, column=c, padx=10, sticky="e")
            cb = ctk.CTkComboBox(frame_form, values=v, width=w); cb.grid(row=r, column=c+1, padx=10, pady=5); return cb

        self.e_titulo = ci(0,0,"Título:", 300); self.e_autor = ci(0,2,"Autor:", 200)
        self.e_editora = ci(1,0,"Editora:", 300)
        
        f_aq = ctk.CTkFrame(frame_form, fg_color="transparent"); f_aq.grid(row=1, column=3, sticky="w", padx=10)
        ctk.CTkLabel(f_aq, text="Ano:", text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=5)
        self.e_ano = ctk.CTkEntry(f_aq, width=60); self.e_ano.pack(side="left")
        ctk.CTkLabel(f_aq, text="Qtd:", text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=(15,5))
        self.e_qtd = ctk.CTkEntry(f_aq, width=40); self.e_qtd.pack(side="left")

        self.e_isbn = ci(2,0,"Código:", 200); self.e_cidade = ci(2,2,"Cidade:", 200)
        self.e_uf = cc(3,0,"UF:", ["SP", "RJ", "MG", "Outro"], 80)
        self.e_origem = cc(3,2,"Origem:", ["Doação", "Governo", "Compra"], 150)
        self.e_genero = cc(4,0,"Gênero:", get_generos_list() or ["Geral"], 200)
        self.e_prat = cc(4,2,"Prateleira:", get_prateleiras_list() or ["A1"], 100)

        frame_btns = ctk.CTkFrame(self.frame_main, fg_color="transparent"); frame_btns.pack(pady=10)
        self.btn_salvar = ctk.CTkButton(frame_btns, text="Salvar", command=self.salvar_livro, fg_color=COLOR_ACCENT, width=150)
        self.btn_salvar.pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text="Limpar", command=self.limpar_campos_livro, fg_color="gray", width=100).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text="Excluir", command=self.excluir_livro, fg_color=COLOR_DANGER, width=100).pack(side="left", padx=10)

        frame_search = ctk.CTkFrame(self.frame_main, fg_color="transparent"); frame_search.pack(fill="x", padx=50, pady=(20, 5))
        ctk.CTkLabel(frame_search, text="Pesquisar Livro:", text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=10)
        entry_search = ctk.CTkEntry(frame_search, placeholder_text="Título/Autor...", width=300); entry_search.pack(side="left", padx=10)
        
        def filtrar(e):
            t = entry_search.get()
            for i in self.tree_livros.get_children(): self.tree_livros.delete(i)
            for r in get_books(t):
                # Ordena colunas para visual
                # row: [0:ID, 1:Tit, 2:Aut, 3:Edi, 4:Ano, 5:ISBN, 6:Ori, 7:Gen, 8:Cid, 9:UF, 10:Prat, 11:Qtd]
                # visual: ID, Tit, Aut, Edi, Ano, ISBN, Qtd, Ori, Gen, Cid, UF, Prat
                self.tree_livros.insert("", "end", values=[r[0], r[1], r[2], r[3], r[4], r[5], r[11], r[6], r[7], r[8], r[9], r[10]])
        entry_search.bind("<KeyRelease>", filtrar)

        h = ["ID", "Título", "Autor", "Editora", "Ano", "Código", "Qtd", "Origem", "Gênero", "Cidade", "UF", "Prat"]
        w = [30, 150, 100, 80, 50, 80, 40, 70, 80, 80, 40, 50]
        ft = ctk.CTkFrame(self.frame_main, fg_color="transparent"); ft.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.tree_livros, v, hs = self.create_table(ft, h, w)
        self.tree_livros.pack(fill="both", expand=True, side="left"); v.pack(side="right", fill="y"); hs.pack(side="bottom", fill="x")
        self.tree_livros.bind("<<TreeviewSelect>>", self.selecionar_livro)
        self.carregar_tabela_livros()

    def carregar_tabela_livros(self):
        for i in self.tree_livros.get_children(): self.tree_livros.delete(i)
        for row in get_books():
            self.tree_livros.insert("", "end", values=[row[0], row[1], row[2], row[3], row[4], row[5], row[11], row[6], row[7], row[8], row[9], row[10]])

    def limpar_campos_livro(self):
        self.selected_id = None
        for e in [self.e_titulo, self.e_autor, self.e_editora, self.e_ano, self.e_isbn, self.e_cidade, self.e_qtd]: e.delete(0, "end")
        self.btn_salvar.configure(text="Salvar Novo")

    def selecionar_livro(self, event):
        try:
            item = self.tree_livros.selection()[0]
            vals = self.tree_livros.item(item, "values")
            self.selected_id = vals[0]
            self.e_titulo.delete(0,"end"); self.e_titulo.insert(0, vals[1])
            self.e_autor.delete(0,"end"); self.e_autor.insert(0, vals[2])
            self.e_editora.delete(0,"end"); self.e_editora.insert(0, vals[3])
            self.e_ano.delete(0,"end"); self.e_ano.insert(0, vals[4])
            self.e_isbn.delete(0,"end"); self.e_isbn.insert(0, vals[5])
            self.e_qtd.delete(0,"end"); self.e_qtd.insert(0, vals[6])
            self.e_origem.set(vals[7]); self.e_genero.set(vals[8])
            self.e_cidade.delete(0,"end"); self.e_cidade.insert(0, vals[9])
            self.e_uf.set(vals[10]); self.e_prat.set(vals[11])
            self.btn_salvar.configure(text="Atualizar")
        except: pass

    def salvar_livro(self):
        if not self.e_titulo.get(): return
        args = [self.e_titulo.get(), self.e_autor.get(), self.e_editora.get(), self.e_ano.get(), self.e_isbn.get(), self.e_origem.get(), self.e_genero.get(), self.e_cidade.get(), self.e_uf.get(), self.e_prat.get(), self.e_qtd.get() or 1]
        try:
            if self.selected_id: update_book(self.selected_id, *args); msg="Atualizado!"
            else: insert_book(*args); msg="Cadastrado!"
            CTkMessagebox(title="Sucesso", message=msg, icon="check")
            self.limpar_campos_livro(); self.carregar_tabela_livros()
        except Exception as e: CTkMessagebox(title="Erro", message=str(e), icon="cancel")

    def excluir_livro(self):
        if self.selected_id and CTkMessagebox(title="Confirmar", message="Excluir?", icon="question", option_1="Não", option_2="Sim").get() == "Sim":
            delete_book(self.selected_id); self.limpar_campos_livro(); self.carregar_tabela_livros()

    def view_gerenciar_usuarios(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.frame_main, text="Gerenciar Usuários", font=("Roboto", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(pady=20)
        ff = ctk.CTkFrame(self.frame_main, fg_color="transparent", width=850); ff.pack(pady=10)
        
        def ci(r,c,l,w=200): ctk.CTkLabel(ff, text=l, text_color=COLOR_TEXT_PRIMARY).grid(row=r,column=c,padx=10,sticky="e"); e=ctk.CTkEntry(ff, width=w); e.grid(row=r,column=c+1,padx=10,pady=5); return e
        self.e_u_nome=ci(0,0,"Nome:",300); ctk.CTkLabel(ff, text="Turma:", text_color=COLOR_TEXT_PRIMARY).grid(row=0,column=2); self.e_u_turma=ctk.CTkComboBox(ff, values=["6º","7º","8º","9º","EM"]); self.e_u_turma.grid(row=0,column=3,padx=10)
        self.e_u_tel=ci(1,0,"Tel:",200); self.e_u_email=ci(1,2,"Email:",300)
        ctk.CTkLabel(ff, text="End:", text_color=COLOR_TEXT_PRIMARY).grid(row=2,column=0,sticky="e",padx=10); self.e_u_end=ctk.CTkEntry(ff, width=600); self.e_u_end.grid(row=2,column=1,columnspan=3,sticky="w",padx=10,pady=5)

        fb = ctk.CTkFrame(self.frame_main, fg_color="transparent"); fb.pack(pady=15)
        self.btn_salvar_user=ctk.CTkButton(fb, text="Salvar", command=self.salvar_user, fg_color=COLOR_ACCENT, width=150); self.btn_salvar_user.pack(side="left", padx=10)
        ctk.CTkButton(fb, text="Limpar", command=self.limpar_campos_user, fg_color="gray", width=100).pack(side="left", padx=10)
        ctk.CTkButton(fb, text="Excluir", command=self.excluir_user, fg_color=COLOR_DANGER, width=100).pack(side="left", padx=10)

        fs = ctk.CTkFrame(self.frame_main, fg_color="transparent"); fs.pack(fill="x", padx=50, pady=10)
        ctk.CTkLabel(fs, text="Pesquisar:", text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=10)
        es = ctk.CTkEntry(fs, placeholder_text="Nome...", width=300); es.pack(side="left", padx=10)
        def fu(e):
            for i in self.tree_users.get_children(): self.tree_users.delete(i)
            for r in get_users(es.get()): self.tree_users.insert("", "end", values=r)
        es.bind("<KeyRelease>", fu)

        ft = ctk.CTkFrame(self.frame_main, fg_color="transparent"); ft.pack(fill="both", expand=True, padx=20, pady=(0,20))
        self.tree_users, v, h = self.create_table(ft, ["ID", "Nome", "Turma", "Endereço", "Email", "Tel"], [30, 200, 100, 200, 150, 100])
        self.tree_users.pack(fill="both", expand=True, side="left"); v.pack(side="right", fill="y"); h.pack(side="bottom", fill="x")
        self.tree_users.bind("<<TreeviewSelect>>", self.selecionar_user)
        self.carregar_tabela_users()

    def carregar_tabela_users(self):
        for i in self.tree_users.get_children(): self.tree_users.delete(i)
        for row in get_users(): self.tree_users.insert("", "end", values=row)

    def limpar_campos_user(self):
        self.selected_id=None; self.e_u_nome.delete(0,"end"); self.e_u_tel.delete(0,"end"); self.e_u_email.delete(0,"end"); self.e_u_end.delete(0,"end"); self.btn_salvar_user.configure(text="Salvar Novo")

    def selecionar_user(self, e):
        try:
            vals=self.tree_users.item(self.tree_users.selection()[0], "values"); self.selected_id=vals[0]
            self.e_u_nome.delete(0,"end"); self.e_u_nome.insert(0,vals[1]); self.e_u_turma.set(vals[2]); self.e_u_end.delete(0,"end"); self.e_u_end.insert(0,vals[3])
            self.e_u_email.delete(0,"end"); self.e_u_email.insert(0,vals[4]); self.e_u_tel.delete(0,"end"); self.e_u_tel.insert(0,vals[5]); self.btn_salvar_user.configure(text="Atualizar")
        except: pass

    def salvar_user(self):
        if not self.e_u_nome.get(): return
        args=[self.e_u_nome.get(), self.e_u_turma.get(), self.e_u_end.get(), self.e_u_email.get(), self.e_u_tel.get()]
        try:
            if self.selected_id: update_user(self.selected_id, *args); msg="Atualizado"
            else: insert_user(*args); msg="Cadastrado"
            CTkMessagebox(title="Sucesso", message=msg, icon="check"); self.limpar_campos_user(); self.carregar_tabela_users()
        except Exception as e: CTkMessagebox(title="Erro", message=str(e), icon="cancel")

    def excluir_user(self):
        if self.selected_id and CTkMessagebox(title="Confirmar", message="Excluir?", icon="question", option_1="Não", option_2="Sim").get()=="Sim":
            delete_user(self.selected_id); self.limpar_campos_user(); self.carregar_tabela_users(); CTkMessagebox(title="Info", message="Excluído", icon="check")

    def view_auxiliar(self, tipo):
        self.clear_main_frame()
        t = "Gêneros" if tipo == "genero" else "Prateleiras"
        ctk.CTkLabel(self.frame_main, text=f"Gerenciar {t}", font=("Arial", 20, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(pady=20)
        e = ctk.CTkEntry(self.frame_main, width=300, placeholder_text="Novo item..."); e.pack(pady=10)
        
        def carregar():
            for i in tr.get_children(): tr.delete(i)
            r = get_generos() if tipo=="genero" else get_prateleiras()
            for x in r: tr.insert("", "end", values=x)

        def add():
            if not e.get(): return
            if tipo=="genero": insert_genero(e.get())
            else: insert_prateleira(e.get())
            carregar(); e.delete(0,"end")

        ctk.CTkButton(self.frame_main, text="Adicionar", command=add, fg_color=COLOR_ACCENT).pack(pady=10)
        
        ft=ctk.CTkFrame(self.frame_main, fg_color="transparent"); ft.pack(fill="both", expand=True, padx=20, pady=20)
        tr,_,_ = self.create_table(ft, ["ID", "Nome"], [50, 400]); tr.pack(fill="both", expand=True, side="left")
        
        def dele():
            try: 
                iid=tr.item(tr.selection()[0], "values")[0]
                if tipo=="genero": delete_genero(iid)
                else: delete_prateleira(iid)
                carregar()
            except: pass
        
        ctk.CTkButton(self.frame_main, text="Excluir Sel.", command=dele, fg_color=COLOR_DANGER).pack(pady=10)
        carregar()

    def view_emprestimos(self):
        self.clear_main_frame()
        
        # Abas
        tab = ctk.CTkTabview(self.frame_main, text_color=COLOR_TEXT_PRIMARY)
        tab.pack(fill="both", expand=True, padx=20, pady=20)
        t_novo = tab.add("Novo Empréstimo")
        t_dev = tab.add("Devolução")
        
        # --- ABA 1: NOVO EMPRÉSTIMO ---
        fc = ctk.CTkFrame(t_novo, fg_color="transparent")
        fc.place(relx=0.5, rely=0.05, anchor="n")
        
        l_all = get_books_list()
        u_all = get_users_list()
        
        # 1. Livro
        ctk.CTkLabel(fc, text="1. Livro:", text_color=COLOR_TEXT_PRIMARY).pack(pady=5)
        el = ctk.CTkEntry(fc, width=500, placeholder_text="Pesquisar...")
        el.pack(pady=5)
        cbl = ctk.CTkComboBox(fc, values=l_all, width=500)
        cbl.pack(pady=5)
        
        def ul(e): 
            d = el.get().lower()
            v = [x for x in l_all if d in x.lower()]
            cbl.configure(values=v or ["Nenhum"])
            cbl.set(v[0] if v else "")
        el.bind("<KeyRelease>", ul)

        # 2. Aluno
        ctk.CTkLabel(fc, text="2. Aluno:", text_color=COLOR_TEXT_PRIMARY).pack(pady=5)
        eu = ctk.CTkEntry(fc, width=500, placeholder_text="Pesquisar...")
        eu.pack(pady=5)
        cbu = ctk.CTkComboBox(fc, values=u_all, width=500)
        cbu.pack(pady=5)
        
        def uu(e): 
            d = eu.get().lower()
            v = [x for x in u_all if d in x.lower()]
            cbu.configure(values=v or ["Nenhum"])
            cbu.set(v[0] if v else "")
        eu.bind("<KeyRelease>", uu)

        # 3. Prazo
        ctk.CTkLabel(fc, text="3. Prazo:", text_color=COLOR_TEXT_PRIMARY).pack(pady=5)
        ep = ctk.CTkEntry(fc, width=500)
        ep.pack(pady=10)
        ep.insert(0, (datetime.now() + timedelta(days=15)).strftime("%d-%m-%Y"))

        def ce():
            try:
                # Aqui o separador é ':' pois get_books_list usa ':'
                lid = int(cbl.get().split(":")[0])
                uid = int(cbu.get().split(":")[0])
                insert_loan(lid, uid, datetime.now().strftime("%d-%m-%Y"), ep.get())
                CTkMessagebox(title="Sucesso", message="Emprestado!", icon="check")
                # Atualiza a lista de devolução na outra aba
                atualizar_lista_dev()
            except Exception as e: 
                CTkMessagebox(title="Erro", message=f"Erro ao emprestar: {e}", icon="cancel")
                
        ctk.CTkButton(fc, text="CONFIRMAR", command=ce, fg_color=COLOR_ACCENT, width=500).pack(pady=20)

        # --- ABA 2: DEVOLUÇÃO (CORRIGIDA) ---
        fd = ctk.CTkFrame(t_dev, fg_color="transparent")
        fd.place(relx=0.5, rely=0.1, anchor="n")
        
        ctk.CTkLabel(fd, text="Selecione Empréstimo Ativo:", text_color=COLOR_TEXT_PRIMARY).pack()
        
        # Variável para o combobox de devolução
        cbd = ctk.CTkComboBox(fd, width=500)
        cbd.pack(pady=10)

        def atualizar_lista_dev():
            lista = get_loans_list()
            if not lista:
                cbd.configure(values=["Nenhum ativo"])
                cbd.set("Nenhum ativo")
            else:
                cbd.configure(values=lista)
                cbd.set(lista[0])

        # Chama uma vez para carregar
        atualizar_lista_dev()
        
        def cd():
            try:
                val = cbd.get()
                if "Nenhum" in val: return
                
                # --- CORREÇÃO AQUI ---
                # O formato do get_loans_list() é "ID - Livro (Usuario)"
                # Então usamos split(" - ") e pegamos a parte 0
                lid = int(val.split(" - ")[0])
                
                return_loan(lid, datetime.now().strftime("%d-%m-%Y"))
                CTkMessagebox(title="Sucesso", message="Devolvido!", icon="check")
                
                # Atualiza a lista para remover o que acabou de ser devolvido
                atualizar_lista_dev()
                
            except Exception as e:
                # Mostra o erro real em vez de ignorar
                CTkMessagebox(title="Erro", message=f"Falha ao devolver: {e}", icon="cancel")
                print(e)

        ctk.CTkButton(fd, text="DEVOLVER", command=cd, fg_color=COLOR_DANGER, width=500).pack(pady=20)
        
    def view_table(self, type_data):
        self.clear_main_frame()
        if type_data == "loans":
            h=["ID", "Livro", "Usuário", "Emp", "Prazo", "Dev", "St"]; w=[30,200,150,80,80,80,60]; f=get_loans
            t="Empréstimos"
        
        ft = ctk.CTkFrame(self.frame_main, fg_color="transparent"); ft.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(ft, text=t, font=("Roboto", 24, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left")
        e = ctk.CTkEntry(ft, placeholder_text="Filtrar...", width=200); e.pack(side="right", padx=10)
        sw = ctk.CTkSwitch(ft, text="Histórico", progress_color=COLOR_ACCENT); sw.pack(side="right")

        f_tb = ctk.CTkFrame(self.frame_main, fg_color="transparent"); f_tb.pack(fill="both", expand=True, padx=20, pady=(0,20))
        tr, v, hs = self.create_table(f_tb, h, w)
        tr.pack(fill="both", expand=True, side="left"); v.pack(side="right", fill="y"); hs.pack(side="bottom", fill="x")

        def filt(ev=None):
            for i in tr.get_children(): tr.delete(i)
            # Switch 'on' = mostrar tudo (somente_ativos=False), 'off' = somente_ativos=True
            d = f(search_term=e.get(), somente_ativos=not sw.get())
            for r in d: tr.insert("", "end", values=r[:len(h)])
        
        e.bind("<KeyRelease>", filt); sw.configure(command=filt); filt()

if __name__ == "__main__":
    app = AppBiblioteca()
    app.mainloop()