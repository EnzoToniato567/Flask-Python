const API_URL = "http://localhost:5000";
const lista = document.querySelector("#lista");
const mensagem = document.querySelector("#mensagem");
const formLivro = document.querySelector("#form-livro");
const tituloInput = document.querySelector("#titulo");
const autorInput = document.querySelector("#autor");
let idEmEdicao = null;

async function api(caminho, opcoes = {}) {
    const resposta = await fetch(API_URL + caminho, opcoes).catch(() => {
        throw new Error("Não foi possível conectar à API em localhost:5000");
    });
    const dados = await resposta.json().catch(() => ({}));
    if (!resposta.ok) throw new Error(dados.error || `Erro na API (${resposta.status})`);
    return dados;
}

function avisar(texto, erro = false) {
    mensagem.textContent = texto;
    mensagem.className = erro ? "erro" : "";
}

function mostrarLivros(livros) {
    lista.replaceChildren();

    for (const livro of livros) {
        const linha = document.createElement("tr");
        for (const valor of [livro.id, livro.titulo, livro.autor]) {
            const celula = document.createElement("td");
            celula.textContent = valor;
            linha.append(celula);
        }

        const acoes = document.createElement("td");
        const editar = document.createElement("button");
        editar.textContent = "Editar";
        editar.onclick = () => {
            idEmEdicao = livro.id;
            tituloInput.value = livro.titulo;
            autorInput.value = livro.autor;
            document.querySelector("#salvar").textContent = "Salvar edição";
            document.querySelector("#cancelar").hidden = false;
            tituloInput.focus();
        };

        const excluir = document.createElement("button");
        excluir.textContent = "Excluir";
        excluir.onclick = () => excluirLivro(livro.id);
        acoes.append(editar, excluir);
        linha.append(acoes);
        lista.append(linha);
    }

    if (livros.length === 0) {
        const linha = document.createElement("tr");
        const celula = document.createElement("td");
        celula.colSpan = 4;
        celula.textContent = "Nenhum livro encontrado.";
        linha.append(celula);
        lista.append(linha);
    }
}

async function listarLivros() {
    mostrarLivros(await api("/livros/listar"));
}

function cancelarEdicao() {
    idEmEdicao = null;
    formLivro.reset();
    document.querySelector("#salvar").textContent = "Cadastrar";
    document.querySelector("#cancelar").hidden = true;
}

formLivro.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const atualizando = idEmEdicao !== null;
    const caminho = atualizando ? `/livros/atualizar/${idEmEdicao}` : "/livros/cadastrar";

    try {
        await api(caminho, {
            method: atualizando ? "PUT" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                titulo: tituloInput.value.trim(),
                autor: autorInput.value.trim()
            })
        });
        cancelarEdicao();
        await listarLivros();
        avisar(atualizando ? "Livro atualizado." : "Livro cadastrado.");
    } catch (erro) {
        avisar(erro.message, true);
    }
});

document.querySelector("#cancelar").onclick = cancelarEdicao;

document.querySelector("#form-busca").addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const id = document.querySelector("#id-busca").value;
    try {
        mostrarLivros([await api(`/livros/buscar/${id}`)]);
        avisar("Livro encontrado.");
    } catch (erro) {
        mostrarLivros([]);
        avisar(erro.message, true);
    }
});

document.querySelector("#mostrar-todos").onclick = () => {
    document.querySelector("#form-busca").reset();
    avisar("");
    listarLivros().catch((erro) => avisar(erro.message, true));
};

async function excluirLivro(id) {
    if (!confirm("Excluir este livro?")) return;
    try {
        await api(`/livros/excluir/${id}`, { method: "DELETE" });
        await listarLivros();
        avisar("Livro excluído.");
    } catch (erro) {
        avisar(erro.message, true);
    }
}

listarLivros().catch((erro) => avisar(erro.message, true));
