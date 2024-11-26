import tkinter as tk
from tkinter import messagebox
import sqlite3

# Configurando o banco de dados SQLite
def configurar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            saldo REAL DEFAULT 0
        )
    ''')
    conexao.commit()
    conexao.close()

# Funções do sistema
def login():
    login = login_entry.get()
    senha = senha_entry.get()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE login = ? AND senha = ?", (login, senha))
    usuario = cursor.fetchone()
    conexao.close()

    if usuario:
        messagebox.showinfo("Login", f"Bem-vindo, {login}!")
        abrir_menu_principal(usuario)
    else:
        messagebox.showerror("Erro", "Login ou senha incorretos.")

def registrar_usuario():
    login = login_entry.get()
    senha = senha_entry.get()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (login, senha))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Usuário já existe.")
    finally:
        conexao.close()

def verificar_saldo(usuario):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario[0],))
    saldo = cursor.fetchone()[0]
    conexao.close()
    messagebox.showinfo("Saldo", f"Seu saldo é: R${saldo:.2f}")

def depositar(usuario):
    valor = float(valor_entry.get())
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios SET saldo = saldo + ? WHERE id = ?", (valor, usuario[0]))
    conexao.commit()
    conexao.close()
    messagebox.showinfo("Depósito", f"R${valor:.2f} depositados com sucesso!")

def sacar(usuario):
    valor = float(valor_entry.get())
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario[0],))
    saldo = cursor.fetchone()[0]

    if valor > saldo:
        messagebox.showerror("Erro", "Saldo insuficiente.")
    else:
        cursor.execute("UPDATE usuarios SET saldo = saldo - ? WHERE id = ?", (valor, usuario[0]))
        conexao.commit()
        messagebox.showinfo("Saque", f"R${valor:.2f} sacados com sucesso!")
    conexao.close()

# Interfaces gráficas
def abrir_menu_principal(usuario):
    login_janela.destroy()
    menu_principal = tk.Tk()
    menu_principal.title("Banco - Menu Principal")
    menu_principal.geometry("600x400")
    menu_principal.configure(bg="#f0f0f5")

    tk.Label(menu_principal, text=f"Bem-vindo, {usuario[1]}!", font=("Arial", 18), bg="#f0f0f5").pack(pady=10)

    tk.Button(menu_principal, text="Verificar Saldo", command=lambda: verificar_saldo(usuario), font=("Arial", 12), width=20).pack(pady=10)

    global valor_entry
    tk.Label(menu_principal, text="Valor:", font=("Arial", 12), bg="#f0f0f5").pack(pady=5)
    valor_entry = tk.Entry(menu_principal, font=("Arial", 12), width=15)
    valor_entry.pack(pady=5)

    tk.Button(menu_principal, text="Depositar", command=lambda: depositar(usuario), font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(menu_principal, text="Sacar", command=lambda: sacar(usuario), font=("Arial", 12), width=20).pack(pady=10)

    menu_principal.mainloop()

def abrir_tela_login():
    global login_janela, login_entry, senha_entry
    login_janela = tk.Tk()
    login_janela.title("Banco - Login")
    login_janela.geometry("400x300")
    login_janela.configure(bg="#d6eaf8")

    tk.Label(login_janela, text="Sistema Bancário", font=("Arial", 20), bg="#d6eaf8").pack(pady=15)
    tk.Label(login_janela, text="Login:", font=("Arial", 12), bg="#d6eaf8").pack(pady=5)
    login_entry = tk.Entry(login_janela, font=("Arial", 12), width=25)
    login_entry.pack(pady=5)

    tk.Label(login_janela, text="Senha:", font=("Arial", 12), bg="#d6eaf8").pack(pady=5)
    senha_entry = tk.Entry(login_janela, font=("Arial", 12), width=25, show="*")
    senha_entry.pack(pady=5)

    tk.Button(login_janela, text="Entrar", command=login, font=("Arial", 12), width=15).pack(pady=10)
    tk.Button(login_janela, text="Registrar", command=registrar_usuario, font=("Arial", 12), width=15).pack()

    login_janela.mainloop()

# Configuração inicial
configurar_banco()
abrir_tela_login()
