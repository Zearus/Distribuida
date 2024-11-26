import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL_AUTH = "http://localhost:5001"
BASE_URL_SALDO = "http://localhost:5002"
BASE_URL_TRANSACOES = "http://localhost:5003"

usuario_atual = None  # Variável para armazenar o ID do usuário logado
Nome = None 

# Funções para interagir com os microserviços
def login():
    global usuario_atual
    global Nome
    login = login_entry.get()
    senha = senha_entry.get()

    response = requests.post(f"{BASE_URL_AUTH}/login", json={"login": login, "senha": senha})
    if response.status_code == 200:
        usuario_atual = response.json().get("user_id")
        Nome = login
        messagebox.showinfo("Login", f"Bem-vindo, {login}!")
        abrir_menu_principal()
    else:
        messagebox.showerror("Erro", "Login ou senha incorretos.")

def registrar_usuario():
    login = login_entry.get()
    senha = senha_entry.get()

    response = requests.post(f"{BASE_URL_AUTH}/registrar", json={"login": login, "senha": senha})
    if response.status_code == 201:
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
    else:
        messagebox.showerror("Erro", response.json().get("error", "Erro desconhecido."))

def verificar_saldo():
    response = requests.get(f"{BASE_URL_SALDO}/saldo/{usuario_atual}")
    if response.status_code == 200:
        saldo = response.json().get("saldo")
        messagebox.showinfo("Saldo", f"Seu saldo é: R${saldo:.2f}")
    else:
        messagebox.showerror("Erro", "Erro ao consultar saldo.")

def depositar():
    valor = float(valor_entry.get())
    response = requests.post(f"{BASE_URL_TRANSACOES}/depositar", json={"user_id": usuario_atual, "valor": valor})
    if response.status_code == 200:
        messagebox.showinfo("Depósito", response.json().get("message"))
    else:
        messagebox.showerror("Erro", response.json().get("error", "Erro desconhecido."))

def sacar():
    valor = float(valor_entry.get())
    response = requests.post(f"{BASE_URL_TRANSACOES}/sacar", json={"user_id": usuario_atual, "valor": valor})
    if response.status_code == 200:
        messagebox.showinfo("Saque", response.json().get("message"))
    else:
        messagebox.showerror("Erro", response.json().get("error", "Erro desconhecido."))

# Interfaces gráficas
def abrir_menu_principal():
    login_janela.destroy()
    menu_principal = tk.Tk()
    menu_principal.title("Banco - Menu Principal")
    menu_principal.geometry("600x400")
    menu_principal.configure(bg="#f0f0f5")

    tk.Label(menu_principal, text=f"Bem-vindo, usuário {Nome}!", font=("Arial", 18), bg="#f0f0f5").pack(pady=10)

    tk.Button(menu_principal, text="Verificar Saldo", command=verificar_saldo, font=("Arial", 12), width=20).pack(pady=10)

    global valor_entry
    tk.Label(menu_principal, text="Valor:", font=("Arial", 12), bg="#f0f0f5").pack(pady=5)
    valor_entry = tk.Entry(menu_principal, font=("Arial", 12), width=15)
    valor_entry.pack(pady=5)

    tk.Button(menu_principal, text="Depositar", command=depositar, font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(menu_principal, text="Sacar", command=sacar, font=("Arial", 12), width=20).pack(pady=10)

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

# Inicializar a interface
abrir_tela_login()
