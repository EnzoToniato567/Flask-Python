import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__, static_folder="../web", static_url_path="/web") # Patch da pasta web


@app.after_request
def permitir_frontend(resposta):
    resposta.headers["Access-Control-Allow-Origin"] = "*"
    resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resposta.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return resposta # Libera o acesso da API para o frontend


@app.get("/")
def pagina_inicial():
    return app.send_static_file("index.html") # Rota do index.html, no frontend


def executar(comando, valores=()):
    with pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="flask_api",
        cursorclass=pymysql.cursors.DictCursor,
    ) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(comando, valores)

            if cursor.description:  # SELECT
                return cursor.fetchall()

            conexao.commit()  # INSERT, UPDATE ou DELETE

            if comando.startswith("INSERT"):
                return cursor.lastrowid

            return cursor.rowcount


@app.get("/livros/listar")
def listar_livros():
    livros = executar("SELECT * FROM livros ORDER BY id")
    return jsonify(livros)


@app.get("/livros/buscar/<int:id>")
def buscar_livro(id):
    livros = executar("SELECT * FROM livros WHERE id = %s", (id,))

    if not livros:
        return jsonify({"error": "Livro não encontrado"}), 404

    return jsonify(livros[0]) # O [0] retorna apenas o índice que foi afetado/buscado


@app.post("/livros/cadastrar")
def cadastrar_livro():
    dados = request.get_json() or {}

    titulo = dados.get("titulo")
    autor = dados.get("autor")

    if not titulo or not autor:
        return jsonify({"error": "Informe titulo e autor"}), 400

    id = executar(
        "INSERT INTO livros (titulo, autor) VALUES (%s, %s)",
        (titulo, autor),
    )

    livro = executar("SELECT * FROM livros WHERE id = %s", (id,))

    return jsonify(livro[0]), 201


@app.put("/livros/atualizar/<int:id>")
def atualizar_livro(id):
    dados = request.get_json() or {}

    titulo = dados.get("titulo")
    autor = dados.get("autor")

    if not titulo or not autor:
        return jsonify({"error": "Informe titulo e autor"}), 400

    livro = executar("SELECT id FROM livros WHERE id = %s", (id,))

    if not livro:
        return jsonify({"error": "Livro não encontrado"}), 404

    executar(
        "UPDATE livros SET titulo = %s, autor = %s WHERE id = %s",
        (titulo, autor, id),
    )

    return jsonify({"titulo": titulo, "autor": autor})


@app.delete("/livros/excluir/<int:id>")
def excluir_livro(id):
    livro = executar("SELECT * FROM livros WHERE id = %s", (id,))

    if not livro:
        return jsonify({"error": "Livro não encontrado"}), 404

    executar("DELETE FROM livros WHERE id = %s", (id,))

    return jsonify(livro[0])


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
