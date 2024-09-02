from flask import Flask, request, jsonify, abort
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DATABASE = os.getenv("DATABASE_URL", "pessoas.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/pessoas', methods=['POST'])
def create_person():
    data = request.get_json()

    if not data.get('apelido') or not data.get('nome') or not data.get('nascimento'):
        return jsonify({"error": "Dados invalidos"}), 422

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pessoas (apelido, nome, nascimento, stack) VALUES (?, ?, ?, ?)",
                (data['apelido'], data['nome'], data['nascimento'], ",".join(data.get('stack', [])))
            )
            conn.commit()
            return jsonify({"id": cursor.lastrowid}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Apelido já utilizado"}), 422


@app.route('/pessoas/<int:id>', methods=['GET'])
def get_person(id):
    conn = get_db()
    person = conn.execute("SELECT * FROM pessoas WHERE id = ?", (id,)).fetchone()
    conn.close()

    if person is None:
        return jsonify({"error": "Não econtrado"}), 404

    return jsonify(dict(person)), 200


@app.route('/pessoas', methods=['GET'])
def search_people():
    term = request.args.get('t')
    if not term:
        return jsonify({"error": "Necessario preencher"}), 400

    conn = get_db()
    term = f"%{term}%"
    people = conn.execute(
        "SELECT * FROM pessoas WHERE apelido LIKE ? OR nome LIKE ? OR stack LIKE ?",
        (term, term, term)
    ).fetchall()
    conn.close()

    return jsonify([dict(person) for person in people]), 200


@app.route('/pessoas/<int:id>', methods=['PUT'])
def update_person(id):
    data = request.get_json()
    if not data.get('apelido') or not data.get('nome') or not data.get('nascimento'):
        return jsonify({"error": "Dados invalidos"}), 422

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pessoas SET apelido = ?, nome = ?, nascimento = ?, stack = ? WHERE id = ?",
        (data['apelido'], data['nome'], data['nascimento'], ",".join(data.get('stack', [])), id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Não econtrado"}), 404

    return jsonify({"message": "Person updated"}), 200


@app.route('/pessoas/<int:id>', methods=['DELETE'])
def delete_person(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pessoas WHERE id = ?", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Não econtrado"}), 404

    return '', 204


if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 5000)))
