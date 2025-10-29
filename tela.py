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
co3 = "#38576b" # Valor
co4 = "#403d3d" # Letra
co5 = "#e06636" # - profit
co6 = "#E9A178"
co7 = "green1"  # Verde
co8 = "#0DA12D" # + Verde
co9 = "#2bb937" # + Verde
co10 = "#6e8faf"
co11 = "#f2f4f2"

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
frameCima = tk.Frame(janela, height=50, bg=co6, relief="flat")
frameCima.grid(row=0, column=0, columnspan=2, sticky="ew")

# Frame da Esquerda (Sidebar)
# 1. Colocado na column=0
frameEsquerda = tk.Frame(janela, width=400, bg=co4, relief="raised")
frameEsquerda.grid(row=1, column=0, sticky="ns") # "ns" = esticar Norte-Sul (vertical)

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
    bg=co6,                           # Cor de fundo do label (mesma do frame)
    compound=tk.LEFT,                 # Coloca a imagem à esquerda do texto
    padx=10,                          # Espaço extra nas laterais
    anchor=tk.W,                      # Alinha o conteúdo à esquerda (W = West)
    font=('Verdana', 16, 'bold'),     # Define a fonte do texto
    fg=co0                            # Define a cor do texto (usei sua cor 'Letra')
)
# 4. "Ancora" a imagem para evitar o bug do garbage collector
app_logo.image = app_img
# 5. Coloca o label na tela (dentro do frameCima)
# fill=tk.Y para o label preencher a altura do frame
app_logo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

janela.mainloop()