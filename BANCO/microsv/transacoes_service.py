from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def configurar_banco():
    conexao = sqlite3.connect("saldo.db")  # Compartilha o mesmo banco com o serviço de saldo
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saldos (
            user_id INTEGER PRIMARY KEY,
            saldo REAL DEFAULT 0
        )
    ''')
    conexao.commit()
    conexao.close()

@app.route('/depositar', methods=['POST'])
def depositar():
    data = request.json
    user_id = data.get('user_id')
    valor = data.get('valor')

    if valor <= 0:
        return jsonify({"error": "Valor inválido."}), 400

    conexao = sqlite3.connect("saldo.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE saldos SET saldo = saldo + ? WHERE user_id = ?", (valor, user_id))
    conexao.commit()
    conexao.close()
    return jsonify({"message": f"Depósito de R${valor:.2f} realizado com sucesso!"}), 200

@app.route('/sacar', methods=['POST'])
def sacar():
    data = request.json
    user_id = data.get('user_id')
    valor = data.get('valor')

    conexao = sqlite3.connect("saldo.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT saldo FROM saldos WHERE user_id = ?", (user_id,))
    saldo = cursor.fetchone()

    if not saldo or saldo[0] < valor:
        return jsonify({"error": "Saldo insuficiente."}), 400

    cursor.execute("UPDATE saldos SET saldo = saldo - ? WHERE user_id = ?", (valor, user_id))
    conexao.commit()
    conexao.close()
    return jsonify({"message": f"Saque de R${valor:.2f} realizado com sucesso!"}), 200

if __name__ == '__main__':
    configurar_banco()
    app.run(port=5003)
