from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def configurar_banco():
    conexao = sqlite3.connect("saldo.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saldos (
            user_id INTEGER PRIMARY KEY,
            saldo REAL DEFAULT 0
        )
    ''')
    conexao.commit()
    conexao.close()

@app.route('/saldo/<int:user_id>', methods=['GET'])
def consultar_saldo(user_id):
    conexao = sqlite3.connect("saldo.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT saldo FROM saldos WHERE user_id = ?", (user_id,))
    saldo = cursor.fetchone()
    conexao.close()

    if saldo:
        return jsonify({"saldo": saldo[0]}), 200
    else:
        return jsonify({"error": "Usuário não encontrado."}), 404

@app.route('/criar_saldo', methods=['POST'])
def criar_saldo():
    data = request.json
    user_id = data.get('user_id')

    conexao = sqlite3.connect("saldo.db")
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO saldos (user_id, saldo) VALUES (?, 0)", (user_id,))
        conexao.commit()
        return jsonify({"message": "Saldo inicial criado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Saldo já existe para este usuário."}), 400
    finally:
        conexao.close()

if __name__ == '__main__':
    configurar_banco()
    app.run(port=5002)
