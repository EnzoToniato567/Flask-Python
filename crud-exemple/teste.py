from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
    {
        "id": 1,
        "titulo": "Livro 1",
        "autor": "Autor 1"
    },
    {
        "id": 2,
        "titulo": "Livro 2",
        "autor": "Autor 2"
    },
    {
        "id": 3,
        "titulo": "Livro 3",
        "autor": "Autor 3"
    }
]

@app.route('/livros/listar', methods = ['GET'])
def listar_livros():
    return jsonify(livros)


@app.route('/livros/buscar/<int:id>', methods = ['GET'])
def buscar_livro(id):
    for livro in livros:
        if livro.get("id") == id:
            return jsonify(livro)
    return jsonify({"error": "Livro não encontrado"}), 404


@app.route("/livros/atualizar/<int:id>", methods = ["PUT"])
def atualizar_livro(id):
    livro_alterado = request.get_json()
    for indice, livro in enumerate(livros):
        if livro.get("id") == id:
            livros[indice].update(livro_alterado)
            return jsonify(livros[indice])
    return jsonify({"error": "Livro não encontrado"}), 404


@app.route("/livros/cadastrar", methods = ["POST"])
def cadastrar_livro():
    novo_livro = request.get_json()
    livros.append(novo_livro)
    return jsonify(livros)


@app.route("/livros/excluir/<int:id>", methods = ["DELETE"])
def excluir_livro(id):
    for indice, livro in enumerate(livros):
        if livro.get("id") == id:
            del livros[indice]
            return jsonify(livros)
    return jsonify({"error": "Livro não encontrado"}), 404
    

app.run(port = 5000, host = "localhost", debug = True)