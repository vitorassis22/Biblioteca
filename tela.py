# Importar Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.constants import FALSE 
# Importar pillow
from PIL import Image, ImageTk

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
janela.geometry('1080x720') # Tamanho
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
frameEsquerda = tk.Frame(janela, width=1000, bg=co8, relief="flat")
frameEsquerda.grid(row=1, column=0, sticky="nsew") # "ns" = esticar Norte-Sul (vertical)

# ---- FRAME DA DIREITA PARA CONTEÚDO ----
#frameDireita = tk.Frame(janela, bg=co2, relief="flat")
#frameDireita.grid(row=1, column=1, sticky="nsew") # "nsew" = esticar em todas as direções

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

# ------------ MENU ------------
# NOVO USUARIO
img_usuario = Image.open("plus.png")
img_usuario = img_usuario.resize((18, 18))
img_usuario = ImageTk.PhotoImage(img_usuario)
b_usuario = tk.Button(frameEsquerda, image=img_usuario, compound=tk.LEFT, anchor=tk.NW, text='Novo cadastro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_usuario.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=6)
# NOVO LIVRO
img_livro = Image.open("plus.png")
img_livro = img_livro.resize((18, 18))
img_livro = ImageTk.PhotoImage(img_livro)
b_livro = tk.Button(frameEsquerda, image=img_livro, compound=tk.LEFT, anchor=tk.NW, text='Novo Livro', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_livro.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER LIVROS
img_ver = Image.open("icons8-book-100.png")
img_ver = img_ver.resize((18, 18))
img_ver = ImageTk.PhotoImage(img_ver)
b_ver = tk.Button(frameEsquerda, image=img_ver, compound=tk.LEFT, anchor=tk.NW, text='Consultar Livros', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
b_ver.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=6)
# VER USUARIOS
img_verUser = Image.open("pessoa.png")
img_verUser = img_verUser.resize((18, 18))
img_verUser = ImageTk.PhotoImage(img_verUser)
b_verUser = tk.Button(frameEsquerda, image=img_verUser, compound=tk.LEFT, anchor=tk.NW, text='Consultar pessoas cadastradas', bg=co8, fg=co0, font=('Ivy 11'), overrelief="ridge", relief="groove")
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