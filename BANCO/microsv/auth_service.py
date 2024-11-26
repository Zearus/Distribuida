from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

SALDO_SERVICE_URL = "http://localhost:5002"

def configurar_banco():
    conexao = sqlite3.connect("auth.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    data = request.json
    login = data.get('login')
    senha = data.get('senha')

    conexao = sqlite3.connect("auth.db")
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (login, senha))
        conexao.commit()
        user_id = cursor.lastrowid
        requests.post(f"{SALDO_SERVICE_URL}/criar_saldo", json={"user_id": user_id})

        return jsonify({"message": "Usuário registrado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Usuário já existe."}), 400
    finally:
        conexao.close()

@app.route('/login', methods=['POST'])
def login_usuario():
    data = request.json
    login = data.get('login')
    senha = data.get('senha')

    conexao = sqlite3.connect("auth.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE login = ? AND senha = ?", (login, senha))
    usuario = cursor.fetchone()
    conexao.close()

    if usuario:
        return jsonify({"message": "Login bem-sucedido!", "user_id": usuario[0]}), 200
    else:
        return jsonify({"error": "Login ou senha incorretos."}), 401

if __name__ == '__main__':
    configurar_banco()
    app.run(port=5001)
